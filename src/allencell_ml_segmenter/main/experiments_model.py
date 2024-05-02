from pathlib import Path
from typing import List, Optional
from allencell_ml_segmenter.config.i_user_settings import IUserSettings

import copy

from allencell_ml_segmenter.core.event import Event
from allencell_ml_segmenter.main.i_experiments_model import IExperimentsModel


class ExperimentsModel(IExperimentsModel):
    def __init__(self, config: IUserSettings) -> None:
        super().__init__()
        self.user_settings = config

        # options
        self.experiments = []
        self.refresh_experiments()

        # state
        self._experiment_name: Optional[str] = None

    def get_experiment_name(self) -> Optional[str]:
        """
        Gets experiment name
        """
        return self._experiment_name

    def set_experiment_name(self, name: Optional[str]) -> None:
        """
        Sets experiment name

        name (str): name of cyto-dl experiment
        """
        self._experiment_name = name
        self.dispatch(Event.ACTION_EXPERIMENT_SELECTED)

    def get_checkpoint(self) -> Optional[str]:
        """
        Gets checkpoint
        """
        return self._get_best_ckpt()

    def refresh_experiments(self) -> None:
        # TODO: make a FileUtils method for this?
        self.experiments = []
        for (
            experiment
        ) in self.user_settings.get_user_experiments_path().iterdir():
            if (
                experiment not in self.experiments
                and not experiment.name.startswith(".")
            ):
                self.experiments.append(experiment.name)

    """
    Returns a defensive copy of Experiments list.
    """

    def get_experiments(self) -> List[str]:
        return copy.deepcopy(self.experiments)

    def get_user_settings(self) -> IUserSettings:
        return self.user_settings

    def get_user_experiments_path(self) -> Path:
        return self.get_user_settings().get_user_experiments_path()

    def get_model_test_images_path(self, experiment_name: str) -> Path:
        return (
            self.get_user_settings().get_user_experiments_path()
            / experiment_name
            / "test_images"
            if experiment_name
            else None
        )

    def get_model_checkpoints_path(
        self, experiment_name: str, checkpoint: str
    ) -> Path:
        """
        Gets checkpoints for model path
        """
        if experiment_name is None:
            raise ValueError(
                "Experiment name cannot be None in order to get model_checkpoint_path"
            )

        if checkpoint is None:
            raise ValueError(
                "Checkpoint cannot be None in order to get model_checkpoint_path"
            )
        return (
            self.get_user_experiments_path()
            / experiment_name
            / "checkpoints"
            / checkpoint
        )

    def get_csv_path(self) -> Path:
        if self.get_user_experiments_path() is not None and self.get_experiment_name() is not None:
            return (
                self.get_user_experiments_path()
                / self.get_experiment_name()
                / "data"
            )
        return None

    def get_metrics_csv_path(self) -> Path:
        return (
            self.get_user_experiments_path()
            / self.get_experiment_name()
            / "csv"
        )

    def get_latest_metrics_csv_version(self) -> int:
        """
        Returns version number of the most recent version directory within
        the cyto-dl CSV folder (self._csv_path) or -1 if no version directories
        exist
        """
        last_version: int = -1
        if self.get_metrics_csv_path().exists():
            for child in self.get_metrics_csv_path().glob("version_*"):
                if child.is_dir():
                    version_str: str = child.name.split("_")[-1]
                    try:
                        last_version = (
                            int(version_str)
                            if int(version_str) > last_version
                            else last_version
                        )
                    except ValueError:
                        continue
        return last_version

    def get_train_config_path(self, experiment_name: str) -> Path:
        return (
            self.get_user_experiments_path()
            / experiment_name
            / "train_config.yaml"
            if experiment_name
            else None
        )

    def get_current_epoch(self) -> Optional[int]:
        ckpt: Optional[str] = self.get_checkpoint()
        if not ckpt:
            return None
        # assumes checkpoint format: epoch_001.ckpt
        return int(ckpt.split(".")[0].split("_")[-1])

    def _get_best_ckpt(self) -> Optional[str]:
        if not self._experiment_name:
            return None

        checkpoints_path = (
            Path(self.user_settings.get_user_experiments_path())
            / self._experiment_name
            / "checkpoints"
        )
        if not checkpoints_path.exists():
            return None

        files: List[Path] = [
            entry
            for entry in checkpoints_path.iterdir()
            if entry.is_file() and not "last" in entry.name.lower()
        ]
        if not files:
            return None

        files.sort(key=lambda file: file.stat().st_mtime)
        return files[-1].name
