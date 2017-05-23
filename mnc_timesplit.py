#!/usr/bin/python

# Load libraries
import argparse
try:
    import numpy as np
    from pyminc.volumes.factory import *
except ImportError, e:
    print("Error: one or more python library could not be imported. See error below.")
    print(e)
    sys.exit(1)


# Parse arguments
parser = argparse.ArgumentParser(description="Split MINC .mnc timeseries into separate volumes")
parser.add_argument('file', help="Input mnc timeseries")
parser.add_argument('-o', '--outfile', help="Output nii file")
parser.add_argument('-t', '--time_axis', default=4, type=int, help="Dimension along which temporal variation is captured (default 4)")
args = parser.parse_args()

# Some default settings
all_dims = ["xspace", "yspace", "zspace"]
all_dims.insert(args.time_axis, "time")
all_starts = [0., 0., 0., 0.]

# Load image
try:
    img = volumeFromFile(args.file)
except nib.spatialimages.ImageFileError:
    print("Error: nibabel could not load image")
    sys.exit(1)

# Get data
dims = img.data.shape
data = img.data

# Check to make sure image is 1D-4D
try:
    assert len(dims) in range(1,5)
except AssertionError:
    print("Image must have between 1 to 4 dimensions (inclusive)")
    sys.exit(1)