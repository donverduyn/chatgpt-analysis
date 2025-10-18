# utils/progress.py
from typing import Iterable, Tuple

from IPython.display import HTML, display
from ipywidgets import FloatProgress, Label, VBox


def bar(
    items: Iterable, desc: str = "Processing", outer_batch: int = 64
) -> Iterable[Tuple[list, int]]:
    """
    Wrap an iterable with a notebook progress bar.

    Parameters
    ----------
    items : iterable
        The items to iterate over.
    desc : str
        Description shown above the progress bar.
    outer_batch : int
        Number of items per progress bar update.

    Yields
    ------
    batch : list
        Sublist of items for current iteration.
    batch_len : int
        Length of this batch.
    """
    items = list(items)
    n = len(items)

    # Inject custom style for dark/transparent background
    display(
        HTML(
            """
    <style>
    .cell-output-ipywidget-background {
        background-color: transparent !important;
    }
    </style>
    """
        )
    )

    progress_label = Label(value=f"{desc}: 0 / {n}")
    progress_label.style.text_color = "white"
    progress_bar = FloatProgress(value=0, min=0, max=n)
    progress_bar.layout.width = "100%"
    progress_bar.style.bar_color = "#33d68d"
    display(VBox([progress_label, progress_bar]))

    for i in range(0, n, outer_batch):
        batch = items[i : i + outer_batch]
        yield batch, len(batch)
        progress_bar.value = min(i + outer_batch, n)
        progress_label.value = f"{desc}: {min(i + outer_batch, n)} / {n}"
