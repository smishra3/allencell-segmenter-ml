from allencell_ml_segmenter.core.publisher import Publisher
from allencell_ml_segmenter.core.event import Event
from enum import Enum
from typing import Union, Optional, List
from pathlib import Path
from allencell_ml_segmenter.main.experiments_model import ExperimentsModel

from allencell_ml_segmenter.main.main_model import MainModel


class TrainingType(Enum):
    """
    Different cyto-dl experiment types
    """

    SEGMENTATION_PLUGIN = "segmentation_plugin"
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
    The 0th dimension is Z, which is not needed for 2d.
    """

    SMALL = [8, 8, 8]
    MEDIUM = [16, 32, 32]
    LARGE = [20, 40, 40]


class ModelSize(Enum):
    """
    Model size for training, and their respective filters overrides
    """

    SMALL = [8, 16, 32]
    MEDIUM = [16, 32, 64]
    LARGE = [32, 64, 128]


class TrainingModel(Publisher):
    """
    Stores state relevant to training processes.
    """

    def __init__(
        self, main_model: MainModel, experiments_model: ExperimentsModel
    ):
        super().__init__()
        self._main_model = main_model
        self.experiments_model = experiments_model
        self._experiment_type: TrainingType = None
        self._hardware_type: Hardware = None
        self._images_directory: Path = None
        self._channel_index: Union[int, None] = None
        self._model_path: Union[Path, None] = (
            None  # if None, start a new model
        )
        self._patch_size: List[int] = None
        self._spatial_dims: int = None
        self._num_epochs: int = None
        self._current_epoch: int = None
        self._max_time: int = None  # in minutes
        self._config_dir: Path = None
        self._max_channel = None
        self._use_max_time: bool = (
            False  # default is false. UI starts with max epoch defined rather than max time.
        )
        self._model_size: Optional[ModelSize] = None

    def get_experiment_type(self) -> Optional[str]:
        """
        Gets experiment type
        """
        if self._experiment_type is None:
            return None
        return self._experiment_type.value

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

    def get_spatial_dims(self) -> int:
        """
        Gets image dimensions
        """
        return self._spatial_dims

    def set_spatial_dims(self, spatial_dims: int) -> None:
        """
        Sets image dimensions

        image_dims (int): number of dimensions to train model on. "2" for 2D, "3" for 3D
        """
        if spatial_dims != 2 and spatial_dims != 3:
            raise ValueError("No support for non 2D and 3D images.")
        self._spatial_dims = spatial_dims

    def get_num_epochs(self) -> int:
        """
        Gets max epoch
        """
        return self._num_epochs

    def set_num_epochs(self, num_epochs: int) -> None:
        """
        Sets num epochs

        num_epochs (int): number of additional epochs to train for
        """
        self._num_epochs = num_epochs

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
        Sets images directory, and dispatches channel extraction

        images_path (Path): path to images directory
        """
        self._images_directory = images_path
        if images_path is not None:
            self.dispatch(Event.ACTION_TRAINING_DATASET_SELECTED)

    def get_channel_index(self) -> Union[int, None]:
        """
        Gets channel index
        """
        return self._channel_index

    def set_channel_index(self, index: int) -> None:
        """
        Sets channel index

        channel_index (int | None): channel index for training, can be None for no channel index splicing
        """
        self._channel_index = index

    def get_patch_size(self) -> List[int]:
        """
        Gets patch size
        """
        return self._patch_size

    def set_patch_size(self, patch_size: List[int]) -> None:
        """
        Sets patch size

        patch_size (str): patch size for training
        """
        if len(patch_size) not in [2, 3]:
            raise ValueError("Patch sizes need to be 2 or 3 dimension based on input image.")
        self._patch_size = patch_size

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

    def dispatch_training(self) -> None:
        """
        Dispatches even to start training
        """
        self.dispatch(Event.PROCESS_TRAINING)

    def set_max_channel(self, max: int) -> None:
        """
        Set the max number of channels in the images in the training dataset
        """
        self._max_channel = max
        self.dispatch(Event.ACTION_TRAINING_MAX_NUMBER_CHANNELS_SET)

    def get_max_channel(self) -> int:
        """
        Get the max number of channels in the images in the training dataset
        """
        return self._max_channel

    def use_max_time(self) -> bool:
        """
        Will training run will be based off of max time
        """
        return self._use_max_time

    def set_use_max_time(self, use_max: bool):
        """
        Set if training run will be based off of max time
        """
        self._use_max_time = use_max

    def set_model_size(self, model_size: str) -> None:
        # convert string to enum
        model_size = model_size.upper()
        if model_size not in [x.name for x in ModelSize]:
            raise ValueError(
                "No support for non small, medium, and large patch sizes."
            )
        self._model_size = ModelSize[model_size]

    def get_model_size(self) -> ModelSize:
        return self._model_size
