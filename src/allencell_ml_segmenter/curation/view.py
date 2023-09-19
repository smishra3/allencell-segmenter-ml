from allencell_ml_segmenter.core.view import View
from allencell_ml_segmenter.main.main_model import MainModel
from allencell_ml_segmenter.widgets.input_button_widget import InputButton, FileInputMode
from allencell_ml_segmenter.widgets.label_with_hint_widget import LabelWithHint
from allencell_ml_segmenter.curation.curation_model import CurationModel
from qtpy.QtCore import Qt
from qtpy.QtWidgets import (
    QSizePolicy,
    QLabel,
    QFrame,
    QGridLayout,
    QVBoxLayout,
    QComboBox,
    QPushButton

)

class CurationView(View):
    """
    View for Curation UI
    """

    def __init__(self, main_model: MainModel):
        super().__init__()
        self._model = CurationModel()

        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(Qt.AlignTop)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        self._title: QLabel = QLabel("CURATION UI", self)
        self._title.setObjectName("title")
        self.layout().addWidget(
            self._title, alignment=Qt.AlignHCenter | Qt.AlignTop
        )

        frame: QFrame = QFrame()
        frame.setLayout(QVBoxLayout())
        frame.setObjectName("frame")
        self.layout().addWidget(frame)

        input_images_label = QLabel("Input images")
        frame.layout().addWidget(input_images_label)

        raw_grid_layout: QGridLayout = QGridLayout()

        # First Row in Gridlayout
        raw_image_label = LabelWithHint("Raw")
        # TODO set hint
        raw_grid_layout.addWidget(raw_image_label, 0, 0, alignment=Qt.AlignLeft)
        raw_grid_layout.addWidget(QLabel("Directory"), 0, 1, alignment=Qt.AlignRight)
        self._raw_directory_select: InputButton = InputButton(
            self._model,
            lambda dir: self._model.set_raw_directory(dir),
            "Select directory...",
            FileInputMode.DIRECTORY,
        )
        raw_grid_layout.addWidget(self._raw_directory_select, 0, 2)

        # Second Row in Gridlayout
        raw_grid_layout.addWidget(QLabel("Image channel"), 1, 1, alignment=Qt.AlignRight)
        self._raw_image_channel_combo: QComboBox = QComboBox()
        raw_grid_layout.addWidget(self._raw_image_channel_combo, 1, 2, alignment=Qt.AlignLeft)

        # add grid to frame
        frame.layout().addLayout(raw_grid_layout)

        seg1_grid_layout: QGridLayout = QGridLayout()
        # First Row in Gridlayout
        seg1_image_label = LabelWithHint("Seg 1")
        # TODO set hint
        seg1_grid_layout.addWidget(seg1_image_label, 0, 0, alignment=Qt.AlignLeft)
        seg1_grid_layout.addWidget(QLabel("Directory"), 0, 1, alignment=Qt.AlignRight)
        # TODO update model accordingly
        self._seg1_directory_select: InputButton = InputButton(
            self._model,
            lambda dir: self._model.set_raw_directory(dir),
            "Select directory...",
            FileInputMode.DIRECTORY,
        )
        seg1_grid_layout.addWidget(self._seg1_directory_select, 0, 2)

        # Second Row in Gridlayout
        seg1_grid_layout.addWidget(QLabel("Image channel"), 1, 1, alignment=Qt.AlignRight)
        self._seg1_image_channel_combo: QComboBox = QComboBox()
        seg1_grid_layout.addWidget(self._seg1_image_channel_combo, 1, 2, alignment=Qt.AlignLeft)

        # add grid to frame
        frame.layout().addLayout(seg1_grid_layout)

        seg2_grid_layout: QGridLayout = QGridLayout()
        # First Row in Gridlayout
        seg2_image_label = LabelWithHint("Seg 2")
        # TODO set hint
        seg2_grid_layout.addWidget(seg2_image_label, 0, 0, alignment=Qt.AlignLeft)
        seg2_grid_layout.addWidget(QLabel("Directory"), 0, 1, alignment=Qt.AlignRight)
        # TODO update model accordingly
        self._seg2_directory_select: InputButton = InputButton(
            self._model,
            lambda dir: self._model.set_raw_directory(dir),
            "Select directory...",
            FileInputMode.DIRECTORY,
        )
        seg2_grid_layout.addWidget(self._seg2_directory_select, 0, 2)

        # Second Row in Gridlayout
        seg2_grid_layout.addWidget(QLabel("Image channel"), 1, 1, alignment=Qt.AlignRight)
        self._seg2_image_channel_combo: QComboBox = QComboBox()
        seg2_grid_layout.addWidget(self._seg2_image_channel_combo, 1, 2, alignment=Qt.AlignLeft)

        # add grid to frame
        frame.layout().addLayout(seg2_grid_layout)

        self._start_btn = QPushButton("Start")
        #TODO wire button
        frame.layout().addWidget(self._start_btn)


    def doWork(self):
        print("work")

    def getTypeOfWork(self):
        print("getwork")

    def showResults(self):
        print("show result")




