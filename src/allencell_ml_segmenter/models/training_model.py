from allencell_ml_segmenter.core.publisher import Publisher
from allencell_ml_segmenter.core.event import Event


class TrainingModel(Publisher):
    """
    Model used for training activities
    """

    def __init__(self):
        super().__init__()
        # Current state of models training
        self._model_training: bool = False

    def get_model_training(self) -> bool:
        """
        Getter to get the current state of the models training
        """
        return self._model_training

    def set_model_training(self, running: bool) -> None:
        """
        Setter to set the current state of the models training
        """
        self._model_training = running
        self.dispatch(Event.PROCESS_TRAINING)