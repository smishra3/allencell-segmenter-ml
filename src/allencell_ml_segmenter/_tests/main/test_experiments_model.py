# from pathlib import Path
from pathlib import PurePath
import pytest
from allencell_ml_segmenter.config.cyto_dl_config import CytoDlConfig

from allencell_ml_segmenter.main.experiments_model import ExperimentsModel


@pytest.fixture
def config() -> CytoDlConfig:
    """
    Fixture for MainModel testing.
    """
    return CytoDlConfig()


def test_refresh_experiments() -> None:
    model = ExperimentsModel(
        CytoDlConfig(
            cyto_dl_home_path=PurePath(__file__).parent / "cyto_dl_home",
            user_experiments_path=PurePath(__file__).parent
            / "experiments_home",
        )
    )
    expected = {"0_exp": set(), "1_exp": set(), "2_exp": {"0.ckpt", "1.ckpt"}}
    assert model.get_experiments() == expected
