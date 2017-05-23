#!/usr/bin/python

# Load libraries
import argparse
import os
import sys
try:
    import nibabel as nib
    import numpy as np
    from pyminc.volumes.factory import *
except ImportError, e:
    print("Error: one or more python library could not be imported. See error below.")
    print(e)
    sys.exit(1)

# Parse arguments
parser = argparse.ArgumentParser(description="Convert NIfTI .nii files to MINC .mnc format")
parser.add_argument('file', help="Input nii file")
parser.add_argument('-o', '--outfile', help="Output mnc file")
#parser.add_argument('-s', '--split_time', default=False, action='store_true', help="If time series, split into multiple files")
parser.add_argument('-t', '--time_axis', default=4, type=int, help="Dimension along which temporal variation is captured (default 4)")
parser.add_argument('--time_average', default=False, action='store_true', help="If timeseries, average along time axis (default False)")
args = parser.parse_args()

# Some default settings
all_dims = ["xspace", "yspace", "zspace"]
all_dims.insert(args.time_axis, "time")
all_starts = [0., 0., 0., 0.]

# Load image
try:
    img = nib.load(args.file)
except nib.spatialimages.ImageFileError:
    print("Error: nibabel could not load image")
    sys.exit(1)

# Check to see that image class is Nifti
try:
    assert img.__class__.__name__ == 'Nifti1Image'
except AssertionError:
    print("Error: non-NIfTI image detected")
    sys.exit(1)

# Get data
dims = img.shape
data = img.get_data()

# Check to make sure image is 1D-4D
try:
    assert len(dims) in range(1,5)
except AssertionError:
    print("Image must have between 1 to 4 dimensions (inclusive)")
    sys.exit(1)

dimnames = [all_dims[i] for i in range(len(dims))]
steps = [img.header['pixdim'][i+1] for i in range(len(dims))]
starts = [all_starts[i] for i in range(len(dims))]
sizes = list(dims)

if args.time_average:
    data = np.mean(data, axis=(args.time_axis-1))
    dimnames.pop(args.time_axis-1)
    steps.pop(args.time_axis-1)
    starts.pop(args.time_axis-1)
    sizes.pop(args.time_axis-1)

outvol = volumeFromDescription(args.outfile, dimnames, sizes, starts, steps)
outvol.data = np.ravel(data).reshape(sizes)
outvol.writeFile()
outvol.closeVolume()