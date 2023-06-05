import pytest
from unittest.mock import Mock
from allencell_ml_segmenter.views.view import View
from allencell_ml_segmenter.models.main_model import MainModel
from allencell_ml_segmenter.core.publisher import Event
from allencell_ml_segmenter._tests.fakes.fake_subscriber import FakeSubscriber


@pytest.fixture
def main_model():
    return MainModel()


@pytest.fixture
def fake_subscriber():
    return FakeSubscriber()


def test_init(main_model):
    assert main_model._current_view == None
    assert len(main_model._subscribers) == 0


def test_get_current_view(main_model):
    assert main_model.get_current_view() == None
    mock_view = Mock(spec=View)
    main_model._current_view = mock_view

    assert main_model.get_current_view() == mock_view


def test_set_current_view(main_model, fake_subscriber):
    # set a mock views
    mock_view = Mock(spec=View)
    main_model.set_current_view(mock_view)
    assert main_model._current_view == mock_view
    # set subscriber
    assert len(main_model._subscribers) == 0
    main_model.subscribe(fake_subscriber)

    main_model.set_current_view(mock_view)

    assert main_model._current_view == mock_view
    assert len(main_model._subscribers) == 1
    assert fake_subscriber.handled_event == Event.CHANGE_VIEW
