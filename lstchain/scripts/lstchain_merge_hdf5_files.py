#!/usr/bin/env python3

"""
Merge all HDF5 files resulting 
from parallel reconstructions present in a 
directory. Every dataset in the files must be 
readable with pandas.

- Input: several hdf5 files.
- Output single hdf5 file.

Usage: 

$> python lstchain_merge_hdf5_files.py
--input-dir ./

"""

import argparse
import os
from distutils.util import strtobool
# import tables
from lstchain.io import get_dataset_keys
from lstchain.io import smart_merge_h5files, auto_merge_h5files

parser = argparse.ArgumentParser(description='Merge HDF5 files')

# Required arguments
parser.add_argument('--input-dir', '-d', type=str,
                    dest='srcdir',
                    help='path to the source directory of files',
                    )

# Optional arguments
parser.add_argument('--output-file', '-o', action='store', type=str,
                    dest='outfile',
                    help='Path of the resulting merged file',
                    default='merge.h5')

parser.add_argument('--smart', action='store', type=lambda x: bool(strtobool(x)),
                    dest='smart',
                    help='Boolean. True for smart merge, False for auto merge',
                    default=True)

parser.add_argument('--no-image', action='store', type=lambda x: bool(strtobool(x)),
                    dest='noimage',
                    help='Boolean. True to remove the images',
                    default=False)

parser.add_argument('--run-number', '-r', action='store', type=str,
                    dest='run_number',
                    help='Merge files run-wise if a run number is passed, \
                          otherwise merge all files in the directory',
                    default=None)

args = parser.parse_args()


def main():

    if args.run_number:
        file_list = sorted([os.path.join(args.srcdir, f) for f in os.listdir(args.srcdir)
                            if (f.endswith('.h5') and args.run_number in f)])
    else:
        file_list = sorted([os.path.join(args.srcdir, f) for f in os.listdir(args.srcdir)
                            if f.endswith('.h5')])

    if args.noimage:
        keys = get_dataset_keys(file_list[0])
        for k in keys:
            if 'image' in k:
                keys.remove(k)
    else:
        keys = None

    if args.smart:
        smart_merge_h5files(file_list, args.outfile, node_keys=keys)
    else:
        auto_merge_h5files(file_list, args.outfile, nodes_keys=keys)


if __name__ == '__main__':
    main()
