"""
shift_origin - Shift plot origin in x and/or y directions.
"""

from pygmt.clib import Session
from contextlib import contextmanager

def managed_resource(*args, **kwds):
    # Code to acquire resource, e.g.:
    resource = acquire_resource(*args, **kwds)
    try:
        yield resource
    finally:
        # Code to release resource, e.g.:
        release_resource(resource)


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
    try:
        args = ["-T"]
        if xshift:
            args.append(f"-X{xshift}")
        if yshift:
            args.append(f"-Y{yshift}")
        with Session() as lib:
            lib.call_module(module="plot", args=" ".join(args))
    finally:
        args = ["-T"]
        if xshift:
            args.append(f"-X-{xshift}")
        if yshift:
            args.append(f"-Y-{yshift}")
        with Session() as lib:
            lib.call_module(module="plot", args=" ".join(args))
