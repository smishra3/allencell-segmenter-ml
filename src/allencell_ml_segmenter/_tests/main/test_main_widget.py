from typing import Set

import pytest
import napari
from pytestqt.qtbot import QtBot

from allencell_ml_segmenter.core.view import View
from allencell_ml_segmenter.main.main_widget import MainTabWidget
from unittest.mock import Mock


@pytest.fixture
def viewer() -> napari.Viewer:
    return Mock(spec=napari.Viewer)


@pytest.fixture
def main_tab_widget(qtbot: QtBot) -> MainTabWidget:
    return MainTabWidget(viewer)


def test_handle_action_change_view_event(
    main_tab_widget: MainTabWidget,
) -> None:
    # ARRANGE
    views: Set[View] = main_tab_widget._view_to_index.keys()

    for view in views:
        # ACT: have the model dispatch the action change view event
        main_tab_widget._model.set_current_view(view)

        # ASSERT: check that the main widget's current view (after setting) is same as the model's current view
        assert (
            main_tab_widget._view_container.currentIndex()
            == main_tab_widget._view_to_index[view]
        )
