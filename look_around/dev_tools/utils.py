import numpy as np
import numpy.typing as npt


def pick_several_from_array(arr: npt.NDArray, size: int = 1, replace: bool = True) -> npt.NDArray:
    """
    Picks several randomly taken elements from the array.

    arr:
    Array the sample is taken from.

    size (default 1):
    Sample size.

    replace (default True):
    Should an extracted sample be replaced (i.e. it can be picked more than once)?

    returns:
    Array with randomly chosen samples.
    """
    idx = np.random.choice(arr.shape[0], size=size, replace=replace)
    return arr[idx]


def pick_from_array(arr: npt.NDArray):
    """
    Picks one randomly chosen element from the first dimension of the array.
    This is a short cut for *pick_several_from_array(arr, size=1).

    arr:
    An array.

    returns:
    A first-dimension element from the array.
    """
    return pick_several_from_array(arr)
