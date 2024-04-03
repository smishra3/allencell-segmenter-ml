import asyncio

from allencell_ml_segmenter.core.subscriber import Subscriber
from allencell_ml_segmenter.core.event import Event

from cyto_dl.api.model import CytoDLModel
from allencell_ml_segmenter.main.experiments_model import ExperimentsModel
from allencell_ml_segmenter.training.training_model import (
    Hardware,
)
from allencell_ml_segmenter.training.training_model import TrainingModel
from typing import Dict, Union, Optional
from napari.utils.notifications import show_warning


class TrainingService(Subscriber):
    """
    Interface for training a model. Uses cyto-dl to train model according to spec
    """

    def __init__(
        self,
        training_model: TrainingModel,
        experiments_model: ExperimentsModel,
    ):
        super().__init__()
        self._training_model: TrainingModel = training_model
        self._experiments_model: ExperimentsModel = experiments_model
        self._training_model.subscribe(
            Event.PROCESS_TRAINING,
            self,
            self._train_model_handler,
        )

    def _train_model_handler(self, _: Event) -> None:
        """
        Trains the model according to the spec
        """
        # Only supporting segmentation config for now
        self._training_model.set_experiment_type("segmentation_plugin")
        # TODO make set_images_directory and get_images_directory less brittle.
        #  https://github.com/AllenCell/allencell-ml-segmenter/issues/156
        if self._able_to_continue_training():
            model = CytoDLModel()
            # model.download_example_data()
            model.load_default_experiment(
                self._training_model.get_experiment_type().value,
                output_dir=f"{self._experiments_model.get_user_experiments_path()}/{self._experiments_model.get_experiment_name()}",
            )
            model.override_config(self._build_overrides())
            model.print_config()
            asyncio.run(model._train_async())

    def _able_to_continue_training(self) -> bool:
        if self._experiments_model.get_experiment_name() is None:
            show_warning(
                "Please select an experiment before running prediction."
            )
            return False

        if self._training_model.get_spatial_dims() is None:
            show_warning(
                "Please select spatial dims for training dataset. 2-D or 3-D."
            )
            return False

        if self._training_model.get_images_directory() is None:
            show_warning("User has not selected input images for training")
            return False

        if self._training_model.get_patch_size() is None:
            show_warning("User has not selected a patch size for training")
            return False

        if self._training_model.get_max_epoch() is None:
            show_warning("Please define max epoch(s) to run for")
            return False

        if (
            self._training_model.get_max_channels() > 0
            and self._training_model.get_channel_index() is None
        ):
            show_warning(
                "Your raw images have multiple channels, please select a channel to train on."
            )
            return False
        return True

    def _hardware_override(self, overrides: Dict[str, Union[str, int, float, bool, Dict]]) -> None:
        """
        Get the hardware override for the CytoDLModel
        """
        # V1 defaults to CPU
        overrides["trainer.accelerator"] = "cpu"
        if self._training_model.get_hardware_type() == Hardware.GPU:
            overrides["trainer.accelerator"] = "gpu"

    def _spatial_dims_override(self, overrides: Dict[str, Union[str, int, float, bool, Dict]]) -> None:
        """
        Get the spatial_dims override for the CytoDlModel
        """
        overrides["spatial_dims"] = (
            self._training_model.get_spatial_dims()
        )

    def _experiment_name_override(self, overrides: Dict[str, Union[str, int, float, bool, Dict]]) -> None:
        """
        Get the experiment name override for the CytoDlModel
        """
        overrides["experiment_name"] = (
            self._experiments_model.get_experiment_name()
        )

    def _max_run_override(self, overrides: Dict[str, Union[str, int, float, bool, Dict]]) -> None:
        """
        Get the max epoch or time override for the CytoDlModel
        """
        # define max run (in epochs)
        overrides["trainer.max_epochs"] = (
            self._training_model.get_max_epoch()
        )
        # max run in time is also defined
        if self._training_model.use_max_time():
            # define max runtime (in hours)
            overrides["trainer.max_time"] = {
                "minutes": self._training_model.get_max_time()
            }

    def _images_directory_override(self, overrides: Dict[str, Union[str, int, float, bool, Dict]]) -> None:
        """
        Get the data path override for the CytoDlModel
        Cyto dl expects a train.csv, valid.csv, and a test.csv in this folder for training.
        """
        overrides["data.path"] = str(
            self._training_model.get_images_directory()
        )

    #
    def _patch_shape_override(self, overrides: Dict[str, Union[str, int, float, bool, Dict]]) -> None:
        """
        get the patch shape override for the CytoDLModel
        """
        overrides["data._aux.patch_shape"] = (
            self._training_model.get_patch_size().value
        )

    def _checkpoint_override(self, overrides: Dict[str, Union[str, int, float, bool, Dict]]) -> None:
        """
        Get the checkpoint path override for the CytoDLModel
        """
        if self._experiments_model.get_checkpoint() is not None:
            # We are going to continue training on an existing model
            overrides["ckpt_path"] = str(
                self._experiments_model.get_model_checkpoints_path(
                    self._experiments_model.get_experiment_name(),
                    self._experiments_model.get_checkpoint(),
                )
            )

    def _build_overrides(self) -> Dict[str, Union[str, int, float, bool, Dict]]:
        """
        Build a list of overrides for the CytoDLModel from plugin state.
        """
        overrides_dict: Dict[str, Union[str, int, float, bool, Dict]] = dict()
        # TODO: Add channel index selection from UI
        # TODO: Add max time from UI
        # do overrides based on user selections
        self._hardware_override(overrides_dict)
        self._spatial_dims_override(overrides_dict)
        self._max_run_override(overrides_dict)
        self._images_directory_override(overrides_dict)
        self._patch_shape_override(overrides_dict)
        self._checkpoint_override(overrides_dict)

        return overrides_dict
