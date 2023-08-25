import os
from allencell_ml_segmenter.core.publisher import Publisher
from allencell_ml_segmenter.core.event import Event
from enum import Enum
from typing import Union
from pathlib import Path

from allencell_ml_segmenter.main.main_model import MainModel


class TrainingType(Enum):
    """
    Different cyto-dl experiment types
    """

    SEGMENTATION = "segmentation"
    GAN = "gan"
    OMNIPOSE = "omnipose"
    SKOOTS = "skoots"


class Hardware(Enum):
    """
    Hardware, "cpu" or "gpu"
    """

    CPU = "cpu"
    GPU = "gpu"


class PatchSize(Enum):
    """
    Patch size for training, and their respective patch shapes.
    TODO: get from benji
    """

    SMALL = [1, 3, 3]
    MEDIUM = [16, 32, 32]
    LARGE = [20, 40, 40]


class TrainingModel(Publisher):
    """
    Stores state relevant to training processes.
    """

    def __init__(self, main_model: MainModel):
        super().__init__()
        self._main_model = main_model
        self._experiment_name: str = None
        self._checkpoint: str = None
        self._experiment_type: TrainingType = None
        self._hardware_type: Hardware = None
        self._images_directory: Path = None
        self._channel_index: Union[int, None] = None
        self._model_path: Union[
            Path, None
        ] = None  # if None, start a new model
        self._patch_size: PatchSize = None
        self._image_dims: int = None
        self._max_epoch: int = None
        self._current_epoch: int = None
        self._max_time: int = None  # in seconds
        self._config_dir: Path = None
        self._is_training_running: bool = False

    def get_experiment_name(self) -> str:
        """
        Gets experiment name
        """
        return self._experiment_name
    
    def set_experiment_name(self, name: str) -> None:
        """
        Sets experiment name

        name (str): name of cyto-dl experiment
        """
        self._experiment_name = name

    def get_checkpoint(self) -> str:
        """
        Gets checkpoint
        """
        return self._checkpoint
    
    def set_checkpoint(self, checkpoint: str) -> None:
        """
        Sets checkpoint

        checkpoint (str): name of checkpoint to use
        """
        self._checkpoint = checkpoint

    def get_experiment_type(self) -> TrainingType:
        """
        Gets experiment type
        """
        return self._experiment_type

    def set_experiment_type(self, training_type: str) -> None:
        """
        Sets experiment type

        training_type (str): name of cyto-dl experiment to run
        """
        # convert string to enum
        self._experiment_type = TrainingType(training_type)

    def get_hardware_type(self) -> Hardware:
        """
        Gets hardware type
        """
        return self._hardware_type

    def set_hardware_type(self, hardware_type: str) -> None:
        """
        Sets hardware type

        hardware_type (Path): what hardware to train on, "cpu" or "gpu"
        """
        # convert string to enum
        self._hardware_type = Hardware(hardware_type.lower())

    def get_image_dims(self) -> int:
        """
        Gets image dimensions
        """
        return self._image_dims

    def set_image_dims(self, image_dims: int) -> None:
        """
        Sets image dimensions

        image_dims (int): number of dimensions to train model on. "2" for 2D, "3" for 3D
        """
        if image_dims != 2 and image_dims != 3:
            raise ValueError("No support for non 2D and 3D images.")
        self._image_dims = image_dims

    def get_max_epoch(self) -> int:
        """
        Gets max epoch
        """
        return self._max_epoch

    def set_max_epoch(self, max: int) -> None:
        """
        Sets max epoch

        max_epoch (int): max number of epochs to train for
        """
        self._max_epoch = max

    def get_current_epoch(self) -> int:
        """
        Gets current epoch
        """
        return self._current_epoch

    def set_current_epoch(self, current: int) -> None:
        """
        Sets current epoch

        current_epoch (int): current epoch number
        """
        self._current_epoch = current
        self.dispatch(Event.PROCESS_TRAINING_PROGRESS)

    def get_images_directory(self) -> Path:
        """
        Gets images directory
        """
        return self._images_directory

    def set_images_directory(self, images_path: Path) -> None:
        """
        Sets images directory

        images_path (Path): path to images directory
        """
        self._images_directory = images_path

    def get_channel_index(self) -> Union[int, None]:
        """
        Gets channel index
        """
        return self._channel_index

    def set_channel_index(self, index: Union[int]) -> None:
        """
        Sets channel index

        channel_index (int | None): channel index for training, can be None for no channel index splicing
        """
        self._channel_index = index

    def get_model_path(self) -> Union[Path, None]:
        """
        Gets model path
        """
        return os.path.join(self._main_model.get_experiment_model().get_cyto_dl_config().get_user_experiments_path(), self._experiment_name, "checkpoints", self._checkpoint)

    def get_patch_size(self) -> PatchSize:
        """
        Gets patch size
        """
        return self._patch_size

    def set_patch_size(self, patch_size: str) -> None:
        """
        Sets patch size

        patch_size (str): patch size for training
        """
        # convert string to enum
        patch_size = patch_size.upper()
        if patch_size not in [x.name for x in PatchSize]:
            raise ValueError(
                "No support for non small, medium, and large patch sizes."
            )
        self._patch_size = PatchSize[patch_size]

    def get_max_time(self) -> int:
        """
        Gets max runtime (in seconds)
        """
        return self._max_time

    def set_max_time(self, max_time: int) -> None:
        """
        Sets max runtime (in seconds)

        max_time (int): maximum runtime for training, in seconds
        """
        self._max_time = max_time

    def get_config_dir(self) -> Path:
        """
        Gets config directory
        """
        return self._config_dir

    def set_config_dir(self, config_dir: Path) -> None:
        """
        Sets config directory

        config_dir (str): path to config directory
        """
        self._config_dir = config_dir

    def is_training_running(self) -> bool:
        """
        Gets whether training is running
        """
        return self._is_training_running

    def set_training_running(self, is_training_running: bool) -> None:
        """
        Sets whether training is running

        is_training_running (bool): whether training is running
        """
        self._is_training_running = is_training_running
        self.dispatch(Event.PROCESS_TRAINING)

    result_images: list = []

    def get_result_images(self) -> list:
        """
        Gets result images
        """
        return self.result_images
    
    def set_result_images(self, images: list) -> None:
        """
        Sets result images

        images (list): list of images to display
        """
        self.result_images = images

    def get_cyto_dl_path(self) -> Path:
        """
        Gets cyto-dl path
        """
        return self._main_model.get_experiment_model().get_cyto_dl_config().get_cyto_dl_home_path()
    
    def get_user_experiments_path(self) -> Path:
        """
        Gets user experiments path
        """
        return self._main_model.get_experiment_model().get_cyto_dl_config().get_user_experiments_path()
    
    def get_experiments(self) -> dict:
        """
        Gets experiments
        """
        return self._main_model.get_experiment_model().get_experiments()