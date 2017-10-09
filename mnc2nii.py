#!/usr/bin/python

# Load libraries
import argparse
import os
import sys
from import nibabel as nib
import numpy as np
from pyminc.volumes.factory import *


# Parse arguments
parser = argparse.ArgumentParser(description="Convert MINC .mnc files to NIfTI .nii format")
parser.add_argument('file', help="Input mnc file")
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

dimnames = img.dimnames
steps = img.separations
starts = [all_starts[i] for i in range(len(dims))]
sizes = dims

affine = np.diag([1, 2, 3, 1])
header = nib.Nifti1Header()
header['pixdim'][range(1,len(dims)+1)] = steps

out_img = nib.Nifti1Image(data, affine=affine, header=header)

nib.save(out_img, args.outfile)