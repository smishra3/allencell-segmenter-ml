from qtpy.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from allencell_ml_segmenter.core.event import Event
from allencell_ml_segmenter.models.main_model import MainModel
from allencell_ml_segmenter.widgets.check_box_list_widget import CheckBoxListWidget


class SelectionWidget(QWidget):
    """
    A sample widget with two buttons for selecting between training and prediction views.
    """

    def __init__(self, model: MainModel):
        super().__init__()
        # self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Controller
        self.training_button = QPushButton("Training View")
        self.training_button.clicked.connect(
            lambda: self.model.dispatch(Event.TRAINING_SELECTED)
        )
        self.prediction_button = QPushButton("Prediction View")
        self.prediction_button.clicked.connect(
            lambda: self.model.dispatch(Event.PREDICTION_SELECTED)
        )

        test_widget = CheckBoxListWidget()
        test_widget.add_item("test1")
        test_widget.add_item("test2")
        test_widget.add_item("test3")

        # add buttons
        self.layout().addWidget(self.training_button)
        self.layout().addWidget(self.prediction_button)
        self.layout().addWidget(test_widget)


        # models
        self.model = model
        self.model.subscribe(self)

    def handle_event(self, event: Event) -> None:
        if event == Event.MAIN_SELECTED:
            self.model.set_current_view(self)
