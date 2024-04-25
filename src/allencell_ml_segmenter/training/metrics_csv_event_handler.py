from watchdog.events import FileSystemEvent, FileSystemEventHandler
from pathlib import Path
from csv import DictReader
from typing import Callable


class MetricsCSVEventHandler(FileSystemEventHandler):
    """
    A MetricsCSVEventHandler calls progress_callback upon any changes to
    the provided target_path CSV file, passing the latest epoch in the modified
    CSV to the callback.
    """

    def __init__(self, target_path: Path, progress_callback: Callable):
        super().__init__()
        self._target_path: Path = target_path
        self._progress_callback: Callable = progress_callback

    def _get_num_epochs(self) -> int:
        with self._target_path.open("r", newline="") as fr:
            dict_reader: DictReader = DictReader(fr)
            epochs = [int(row["epoch"]) for row in dict_reader]

        return len(set(epochs))

    # override
    def on_any_event(self, event: FileSystemEvent) -> None:
        if self._target_path.exists() and self._target_path.samefile(
            event.src_path
        ):
            # this is a consequence of a cyto-dl quirk: the test metrics are
            # logged as the n+1'th epoch, even though it uses the n'th epoch's
            # parameters. Test metrics are calculated at the end of training,
            # so we want it to appear that training is complete once the metrics
            # are calculated.
            output: int = max(0, self._get_num_epochs() - 1)
            self._progress_callback(output)
