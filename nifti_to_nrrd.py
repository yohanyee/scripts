#!/usr/bin/env python

import argparse
import nibabel as nib
import nrrd
import numpy as np

parser = argparse.ArgumentParser(description="Convert NIFTI to NRRD")
parser.add_argument("infile", type=str, help="Input NIFTI file")
parser.add_argument("outfile", type=str, help="Output NRRD file")
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

# Extract relevant header information
space = "RAST" if dim==4 else "RAS"
time_code = int("{0:06b}".format(int(dat.header['xyzt_units']))[0:3] + "000", 2)
space_code = int("{0:06b}".format(int(dat.header['xyzt_units']))[3:6], 2)
time_units = [NIFTI_unit_definitions[time_code]]
space_units = [NIFTI_unit_definitions[space_code] for i in range(3)] 
units = space_units + time_units if dim==4 else space_units

# Get sform matrix
# If sform_code is not set (=0), build from pixdims, otherwise set from header
if dat.header['sform_code']==0:
    sform_matrix = np.diag(np.append(dat.header['pixdim'][1:4], 1))
else:
    sform_matrix = dat.get_sform()[0:3, 0:3]

# Set nrrd header output
nrrd_opts = {"space": space,
             "space units": units,
             "space origin": dat.get_sform()[0:3,3],
             "space directions": sform_matrix}

# Write data
nrrd.write(args.outfile, dat.get_data(), options=nrrd_opts)


