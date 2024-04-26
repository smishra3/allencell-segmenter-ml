import numpy as np
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from napari.layers import Shapes


@dataclass
class CurationRecord:
    raw_file: Path
    seg1: Path
    seg2: Optional[Path]
    excluding_mask: Optional[np.ndarray]
    merging_mask: Optional[Shapes]
    base_image_index: str
    to_use: bool
