from pathlib import Path
from allencell_ml_segmenter.core.subscriber import Subscriber
from allencell_ml_segmenter.main.i_experiments_model import IExperimentsModel
from typing import Dict, Callable
from allencell_ml_segmenter.core.event import Event


class FakeExperimentModel(IExperimentsModel):
    def __init__(self):
        self._experiment_name = None
        self._checkpoint = None
        self._events_to_subscriber_handlers: Dict[
            Dict[Subscriber, Callable]
        ] = {event: dict() for event in [e.value for e in Event]}

    def get_experiment_name(self) -> str:
        return self._experiment_name

    def set_experiment_name(self, name: str) -> None:
        self._experiment_name = name

    def get_checkpoint(self) -> str:
        return self._checkpoint

    def set_checkpoint(self, checkpoint: str):
        self._checkpoint = checkpoint

    def get_experiments(self):
        return {"0_exp": {}, "1_exp": {}, "2_exp": {"0.ckpt", "1.ckpt"}}

    def refresh_experiments(self):
        pass

    def refresh_checkpoints(self, experiment: str):
        pass

    def get_user_experiments_path(self) -> Path:
        return Path()

    def get_model_checkpoints_path(self) -> Path:
        return Path()