import zarr
import numpy as np

z = zarr.zeros((10000, 10000), chunks=(1000, 1000), dtype='i4')
