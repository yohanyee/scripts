import argparse
import numpy as np
from pyminc.volumes.factory import *

parser = argparse.ArgumentParser(description="Average MINC timeseries across the time dimension")
parser.add_argument('file', help="Input mnc timeseries")
parser.add_argument('-o', '--outfile', help="Output mnc file")
parser.add_argument('-t', '--time_axis', default=4, type=int, help="Dimension along which temporal variation is captured (default 4)")
args = parser.parse_args()

infile = args.file
outfile = args.outfile

invol = volumeFromFile(infile)
timeseries = invol.data


dimnames = invol.dimnames
steps = invol.separations
starts = invol.starts
sizes = list(timeseries.shape)

averaged_volume = np.mean(timeseries, axis=(args.time_axis-1))
dimnames.pop(args.time_axis-1)
steps.pop(args.time_axis-1)
starts.pop(args.time_axis-1)
sizes.pop(args.time_axis-1)

outvol = volumeFromDescription(outfile, dimnames, sizes, starts, steps)
outvol.data = averaged_volume
outvol.writeFile()
outvol.closeVolume()
