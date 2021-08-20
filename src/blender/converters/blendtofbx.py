"""
MIT License

Copyright (c) 2020-2021 ossls

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# This script will export a single, specified .blend file into a .fbx file
# it will use the settings.json to determine the destination folder to export to
# unless the CLI argument is used

import sys
import os
import json
import shutil
import subprocess
import argparse

sys.path.append(os.path.abspath('src/blender/utilities'))

import blendyard_utilities

parser = argparse.ArgumentParser(description='Convert a specified .blend files to FBX.')
parser.add_argument('--file', help='path to the blender file to convert', required=True)
parser.add_argument('--destination', help='destination path for the produced .FBX file')
parser.add_argument('--verbose', help='Displays additional information', action='store_true', default=False)

args = parser.parse_args()

if args.file == None:
    print(parser.print_help())
    exit()

print(args.file)
if args.file.endswith('.blend') != True:
    print("a .blend file must be provided")
    exit()    

overridePath = None
if args.destination != None:
    overridePath = args.destination

settings = []

filePath = args.file

def main():

    verbose = args.verbose 

    print("--------------------------------------------------------")
    print("FBX Convert")
    print("--------------------------------------------------------\n")

    settings = blendyard_utilities.ReadSettings(None)
    converter_bin = settings["general"]["blender_exe"]
    source_folder = settings["models"]["source_folder"]
    target_folder = settings["models"]["target_folder"]

    if overridePath != None:
        target_folder = overridePath

    if verbose == True:
        print("Converter: %s"%converter_bin)
        print("Target: %s"%target_folder)
        print("File: %s"%filePath)

    if filePath.endswith(".blend"):
        blendyard_utilities.InvokeBlenderExporter( converter=converter_bin,
                                                    source_path=source_folder,
                                                    source_file=filePath,
                                                    destination=target_folder,
                                                    script=os.path.join("src/blender/exporters", "batch_export.py"),
                                                    verbose=True
                                                    )

if __name__== "__main__":
    main()
