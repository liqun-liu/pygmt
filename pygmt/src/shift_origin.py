"""
shift_origin - Shift plot origin in x and/or y directions.
"""

from contextlib import contextmanager

from pygmt.clib import Session
from pygmt.exceptions import GMTInvalidInput


def _opposite_shift(shift):
    """
    Return the opposite value for a shift.

    Parameters
    ----------
    shift : int or float or str
        A shift value.

    Examples
    --------
    >>> _opposite_shift(5)
    -5.0
    >>> _opposite_shift(-5)
    5.0
    >>> _opposite_shift("5")
    '-5.0'
    >>> _opposite_shift("-5")
    '5.0'
    >>> _opposite_shift("5c")
    '-5c'
    >>> _opposite_shift("-5c")
    '5c'
    >>> _opposite_shift("h+5c")
    '-h-5c'
    >>> _opposite_shift("h-5c")
    '-h+5c'
    >>> _opposite_shift("h/3+2c")
    '-h/3-2c'
    >>> _opposite_shift("-h/3-2c")
    'h/3+2c'
    >>> _opposite_shift("0.5h+2c")
    '-0.5h-2c'
    >>> _opposite_shift("-0.5h+2c")
    '0.5h-2c'
    """
    if shift is None:
        return None
    if isinstance(shift, (int, float)):  # is a number
        return -float(shift)
    if isinstance(shift, str):  # is a string
        try:
            return str(-float(shift))  # the string is a number
        except ValueError:
            if shift.startswith("-"):
                shift = shift[1:]
            elif not shift.startswith("+"):
                shift = "+" + shift
            return shift.replace("+", "#").replace("-", "+").replace("#", "-")
    else:
        raise GMTInvalidInput(f"'{shift}' is not a valid shift.")


@contextmanager
def shift_origin(self, xshift=None, yshift=None):
    """
    Shift plot origin in x and/or y directions.

    This method shifts the plot origin relative to the current origin
    by (*xshift*, *yshift*). Optionally, append the length unit (**c**,
    **i**, or **p**). Default unit if not given is **c** for centimeters.

    Prepend **a** to shift the origin back to the original position after
    plotting, prepend **c** to center the plot on the center of the paper
    (optionally add shift), prepend **f** to shift the origin relative to
    the fixed lower left corner of the page, or prepend **r** [Default] to
    move the origin relative to its current location.

    Detailed usage at
    :gmt-docs:`cookbook/options.html#plot-positioning-and-layout-the-x-y-options`

    Parameters
    ----------
    xshift : str
        Shift plot origin in x direction.
    yshift : str
        Shift plot origin in y direction.
    """
    self._preprocess()  # pylint: disable=protected-access
    old_xshift = _opposite_shift(xshift)
    old_yshift = _opposite_shift(xshift)

    try:
        print("In try")
        args = ["-T"]
        if xshift:
            args.append(f"-X{xshift}")
        if yshift:
            args.append(f"-Y{yshift}")
        with Session() as lib:
            yield lib.call_module(module="plot", args=" ".join(args))
    finally:
        print("In finally")
        args = ["-T"]
        if old_xshift:
            args.append(f"-X{old_xshift}")
        if old_yshift:
            args.append(f"-Y{old_yshift}")
        with Session() as lib:
            lib.call_module(module="plot", args=" ".join(args))
