# utils/device.py
import torch


def get_device(verbose: bool = True) -> str:
    """
    Detects the best available compute device (CUDA, MPS, or CPU).

    Parameters
    ----------
    verbose : bool, optional
        If True, prints the selected device.

    Returns
    -------
    device : str
        The name of the selected device ('cuda', 'mps', or 'cpu').
    """
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    if verbose:
        print(f"Using device: {device}")

    return device
