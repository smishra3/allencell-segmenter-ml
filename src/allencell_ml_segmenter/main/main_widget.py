import napari
from qtpy.QtWidgets import (
    QVBoxLayout,
    QSizePolicy,
    QStackedWidget,
)

from allencell_ml_segmenter.core.subscriber import Subscriber
from allencell_ml_segmenter.core.event import Event
from allencell_ml_segmenter.main.main_model import MainModel
from allencell_ml_segmenter.prediction.view import PredictionView
from allencell_ml_segmenter.views.view import View
from allencell_ml_segmenter.sample.sample_view import SampleView
from allencell_ml_segmenter.widgets.selection_widget import SelectionWidget
from allencell_ml_segmenter.prediction.file_input_widget import (
    PredictionFileInput,
)


class MainMeta(type(QStackedWidget), type(Subscriber)):
    """
    Metaclass for MainWidget

    """

    pass


class MainWidget(QStackedWidget, Subscriber, metaclass=MainMeta):
    """
    Main widget that is displayed in the plugin window. This widget is an empty Qwidget that supports adding and removing different
    views from the main layout by responding to MainEvents.

    """

    def __init__(self, viewer: napari.Viewer):
        super().__init__()
        self.viewer: napari.Viewer = viewer

        # basic styling
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.MinimumExpanding)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # Model
        self.model: MainModel = MainModel()
        self.model.subscribe(Event.ACTION_CHANGE_VIEW, self)

        # Dictionaries of views to index values
        self.view_to_index = dict()

        # add sample page
        sample_view = SampleView(self.model)
        self.initialize_view(sample_view)

        # add selection page
        selection_view = SelectionWidget(self.model)
        self.initialize_view(selection_view)

        # add prediction page
        prediction_view = PredictionView(self.model)
        self.initialize_view(prediction_view)

        # start on selection views
        self.model.set_current_view(selection_view)

    def handle_event(self, event: Event) -> None:
        """
        Handle event function for the main widget, which handles MainEvents.

        inputs:
            event - MainEvent
        """
        self.set_view(self.model.get_current_view())

    def set_view(self, view: View) -> None:
        """
        Set the current views, must be initialized first
        """
        self.setCurrentIndex(self.view_to_index[view])

    def initialize_view(self, view: View) -> None:
        # QStackedWidget count method keeps track of how many child widgets have been added
        self.view_to_index[view] = self.count()
        self.addWidget(view)
