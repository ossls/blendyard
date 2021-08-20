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


# This script runs a Watchdog (https://pythonhosted.org/watchdog) it must be installed with PIP

# This watchdog will run on execution
# You may provide a path to watch as the first parameter of the script.
# Example:
#   python watchdog\\blendyard_watchdog "D:\MyProject"
# If no path is provided, the watchdog will run on the script's current folder
#
# This script depends on batch_export.py in order to invoke Blender's export
# process.
#
# This script relies on settings.json for the destination path to save the
# exported .fbx files into

import os
import json
import sys
import time
import pathlib
import subprocess
import argparse

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

sys.path.append(os.path.abspath('src/blender/utilities'))

import blendyard_utilities

parser = argparse.ArgumentParser(description='Recursively watch a folder with .blend files in order to convert them to .fbx if they are modified')
parser.add_argument('--settings', help='The .json file that holds the configuration for exporting Blender files to FBX')
parser.add_argument('--watchfolder', help='The folder to watch')
parser.add_argument('--destination', help='destination path for the produced .FBX files')
parser.add_argument('--verbose', help='Displays additional information', action='store_true', default=False)

args = parser.parse_args()


previousTimeStamp = 0

settings = {}
if args.settings == None:
    settings = blendyard_utilities.ReadSettings(None)
else:
    settings = blendyard_utilities.ReadSettings(args.settings)

if settings["watchdog"]["verbose"] != 0:
    print("VERBOSE")

# Source folder is the folder the watchdog will be recusively observing
# any changes in files will prompt an export
source_folder = settings["watchdog"]["watched_folder"]

# Target folder is the first level folder to export into, this exporter will
# use the relative path for files being watched and replicate the folder
# structure at the destination
target_folder = settings["models"]["target_folder"]

# Path to the Blender executable
converter_bin = settings["general"]["blender_exe"]

running_tasks = []

def PrintHeader():
    global target_folder

    print("\n"
    "      .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .\n"
    "'`._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.' \n\n"
    "                                    Blender FBX Exporter Watchdog\n\n"
    "Detecting changes to .blend files will convert them into .fbx\n\n" +
    "Source Folder:\n%s\n"%os.path.abspath(source_folder) +
    "\nTarget Folder:\n%s\n"%(target_folder) +
    "\nTo shutdown the watchdog press Ctrl+C\n"
    "\n"
    "      .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .-.     .\n"
    "'`._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'   `._.'  \n\n")

# This invokes batch_export.py in order to perform the Blender to FBX export procedure
def RunFBXExport(filePath):
    
    global converter_bin
    global source_folder
    global target_folder
    global running_tasks

    if settings["watchdog"]["verbose"] > 0:
        print("Running FBX Export: %s"%filePath)

    if filePath in running_tasks:
        print ("SKIPPING")
        return

    running_tasks.append(filePath)

    blendyard_utilities.InvokeBlenderExporter(
                                            converter=converter_bin,
                                            source_path=source_folder,
                                            source_file=filePath,
                                            destination=target_folder,
                                            script=os.path.join("src/blender/exporters", "batch_export.py"),
                                            verbose=False
                                            )

    running_tasks.remove(filePath)

    PrintHeader()

# When the watchdog detects a change (new or modified) blender file
# it will invoke the process function of this handler
class ChangeHandler(PatternMatchingEventHandler):
    
    patterns=["*.blend"]


    # Process the file
    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        if event.is_directory is True:
            return

        if str.endswith(event.src_path, "@"):
            return

        if settings["watchdog"]["verbose"] != 0:
            print("EVENT %s"%str(event))

        # A valid change has been detected in a Blender file, export it as FBX
        # if event.event_type == 'moved':
        #     if not str.endswith(event.dest_path, "blend"):
        #         if settings["watchdog"]["verbose"] != 0:
        #             print("Not running")
        #         return

        if event.event_type == 'modified' or event.event_type == 'created' or event.event_type == 'moved':
            RunFBXExport(event.src_path)

    # A Blender file has been modified
    def on_modified(self, event):
        global previousTimeStamp

        statbuf = os.stat(event.src_path)
        timeStamp = statbuf.st_mtime

        # The watchdog sometimes invokes two on_modified handler so this will gate it to make
        # sure only one is processed
        timeDelta = timeStamp - previousTimeStamp
        
        if (timeDelta) > settings["watchdog"]["delta_throttle"]:
            previousTimeStamp = timeStamp
            self.process(event)

    # A Blender file has been created
    def on_created(self, event):
        self.process(event)

    def on_moved(self, event):
        self.process(event)

if __name__ == '__main__':

    PrintHeader()
   
    # You may pass the path to watch, if no path is provided it will watch
    # the current folder
    args = sys.argv[1:]
    override_source_folder = args[0] if args else '.'
    if override_source_folder != ".":
        source_folder = override_source_folder
    else:
        source_folder = settings["watchdog"]["watched_folder"]

    if settings["watchdog"]["verbose"] > 0:
        print("Watching folder: %s"%source_folder)

    observer = Observer()
    observer.schedule(ChangeHandler(), source_folder, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()