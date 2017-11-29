#!/usr/bin/env python

import argparse
import nibabel as nib
import nrrd
import numpy as np

parser = argparse.ArgumentParser(description="Convert NIFTI to NRRD")
parser.add_argument("infile", type=str, help="Input NIFTI file")
parser.add_argument("outfile", type=str, help="Output NRRD file")
parser.add_argument("--space", type=str, help="Space information (defaults to LPS (3D file) or LPST (4D file)")
args = parser.parse_args()

# Load data and determine dimensions
dat = nib.load(args.infile)
dim = dat.header['dim'][0]

# Define NIFTI units
NIFTI_unit_definitions = {0 : "unknown",
                          1 : "m" ,
                          2 : "mm",
                          3 : "um",
                          8 : "s",
                          16: "ms",
                          24: "us",
                          32: "hz",
                          40: "ppm" ,
                          48: "rad"}


# Set space information, either from provided options, or from header if not provided
if args.space is not None:
    space = args.space
else:
    space = "LPST" if dim==4 else "LPS"

# Extract relevant header information
time_code = int("{0:06b}".format(int(dat.header['xyzt_units']))[0:3] + "000", 2)
space_code = int("{0:06b}".format(int(dat.header['xyzt_units']))[3:6], 2)
time_units = ['"{}"'.format(NIFTI_unit_definitions[time_code])]
space_units = ['"{}"'.format(NIFTI_unit_definitions[space_code]) for i in range(3)] 
units = space_units + time_units if dim==4 else space_units

# Get sform matrix
# If sform_code is not set (=0), build from pixdims, otherwise set from header
if dat.header['qform_code']==0:
    qform_matrix = np.diag(np.append(dat.header['pixdim'][1:4], 1))
else:
    qform_matrix = dat.get_qform()

# Set space origin
space_origin = list(dat.get_qform()[0:3,3]) + [0]

# If 3D file (not timeseries), truncate qform matrix
if dim==3:
    qform_matrix = qform_matrix[0:3, 0:3]
    space_origin = space_origin[0:3]

# Set nrrd header output
nrrd_opts = {"space": space,
             "space units": units,
             "space origin": space_origin,
             "space directions": qform_matrix}

# Write data
nrrd.write(args.outfile, dat.get_data(), options=nrrd_opts)


