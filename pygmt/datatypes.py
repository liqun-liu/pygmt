"""
GMT standard data types.

These data types are defined in the GMT source code "src/gmt_resources.h".
"""
import ctypes as ctp

import numpy as np
import xarray as xr
from pygmt.clib.session import Session

# Lenghts of grid header variables
with Session() as lib:
    GMT_GRID_UNIT_LEN80 = lib["GMT_GRID_UNIT_LEN80"]
    GMT_GRID_TITLE_LEN80 = lib["GMT_GRID_TITLE_LEN80"]
    GMT_GRID_COMMAND_LEN320 = lib["GMT_GRID_COMMAND_LEN320"]
    GMT_GRID_REMARK_LEN160 = lib["GMT_GRID_REMARK_LEN160"]

# GMT uses single-precision for grids by default, but can be built to use
# double-precision. Currently, only single-precision is supported.
gmt_grdfloat = ctp.c_float


class GMT_GRID_HEADER(ctp.Structure):
    """
    Structure for GMT grid header.
    """

    _fields_ = [
        # items stored in grids
        ("n_columns", ctp.c_uint32),  # number of columns
        ("n_rows", ctp.c_uint32),  # number of rows
        ("registration", ctp.c_uint32),  # grid registration (0 or 1)
        ("wesn", ctp.c_double * 4),  # minimum/maximum x and y coordinates
        ("z_min", ctp.c_double),  # minimum z value
        ("z_max", ctp.c_double),  # maximum z value
        ("inc", ctp.c_double * 2),  # x and y increments
        ("z_scale_factor", ctp.c_double),  # grid values must be multiplied by this
        ("z_add_offset", ctp.c_double),  # after scaling, add this
        ("x_units", ctp.c_char * GMT_GRID_UNIT_LEN80),  # units in x-direction
        ("y_units", ctp.c_char * GMT_GRID_UNIT_LEN80),  # units in y-direction
        ("z_units", ctp.c_char * GMT_GRID_UNIT_LEN80),  # grid value units
        ("title", ctp.c_char * GMT_GRID_TITLE_LEN80),  # name of data set
        ("command", ctp.c_char * GMT_GRID_COMMAND_LEN320),  # name of generating command
        ("remark", ctp.c_char * GMT_GRID_REMARK_LEN160),  # comments for this data set
        # items used internally by GMT
        # number of data points (n_columns * n_rows) [padding is excluded]
        ("nm", ctp.c_size_t),
        # actual number of items (not bytes) required to hold this grid (mx * my)
        ("size", ctp.c_size_t),
        ("bits", ctp.c_uint),  # bits per data value
        # complex grid
        # 0 for normal
        # GMT_GRID_IS_COMPLEX_REAL = real part of complex grid
        # GMT_GRID_IS_COMPLEX_IMAG = imag part of complex grid
        ("complex_mode", ctp.c_uint),
        ("type", ctp.c_uint),  # grid format
        ("n_bands", ctp.c_uint),  # number of bands [1]
        ("mx", ctp.c_uint),  # actual x-dimension in memory, allowing for padding
        ("my", ctp.c_uint),  # actual y-dimension in memory, allowing for padding
        ("pad", ctp.c_uint * 4),  # padding on west, east, south, north sides [2,2,2,2]
        # Three or four char codes T|B R|C S|R|S (grd) or B|L|P + A|a (img)
        # describing array layout in mem and interleaving
        ("mem_layout", ctp.c_char * 4),
        ("nan_value", gmt_grdfloat),  # missing value as stored in grid file
        ("xy_off", ctp.c_double),  # 0.0 for gridline grid and 0.5 for pixel grid
        ("ProjRefPROJ4", ctp.c_char_p),  # referencing system string in PROJ.4 format
        ("ProjRefWKT", ctp.c_char_p),  # referencing system string in WKT format
        ("ProjRefEPSG", ctp.c_int),  # referencing system EPSG code
        ("hidden", ctp.c_void_p),  # lower-level information for GMT use only
    ]


class GMT_GRID(ctp.Structure):
    """
    Structure for GMT grid.
    """

    _fields_ = [
        ("header", ctp.POINTER(GMT_GRID_HEADER)),  # pointer to grid header
        ("data", ctp.POINTER(gmt_grdfloat)),  # pointer to grid data
        ("x", ctp.POINTER(ctp.c_double)),  # pointer to x coordinate vector
        ("y", ctp.POINTER(ctp.c_double)),  # pointer to y coordinate vector
        ("hidden", ctp.c_void_p),  # low-level information for GMT use only
    ]

    def to_dataarray(self):
        header = self.header.contents
        pad = header.pad[:]
        x = self.x[: header.n_columns]
        y = self.y[: header.n_rows]
        data = np.array(self.data[: header.mx * header.my]).reshape(
            (header.my, header.mx)
        )[pad[2] : header.my - pad[3], pad[0] : header.mx - pad[1]]
        if x[0] > x[1]:
            x = list(reversed(x))
            data = np.fliplr(data)
        if y[0] > y[1]:
            y = list(reversed(y))
            data = np.flipud(data)
        return xr.DataArray(data, coords=[y, x], dims=["lat", "lon"])
