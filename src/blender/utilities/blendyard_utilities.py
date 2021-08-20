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

import os
import json
import subprocess
import pathlib

# Opens the settings JSON file and returns it in an easy to use
# dictionary
def ReadSettings(settingsFileName):

    if settingsFileName == None or len(settingsFileName) == 0:
        settingsFileName = os.path.join("%s.."%os.path.sep, 'settings.json')

    current_folder = os.path.dirname(os.path.realpath(__file__))

    settingsFile = current_folder + settingsFileName
    with open(settingsFile, "r") as read_file:
        settings = json.load(read_file)

    return settings

def InvokeBlenderExporter(**args):

    sourcePath = args["source_path"]
    sourceFile = args["source_file"]
    converter = args["converter"]
    script = args["script"]
    destination = args["destination"]
    verbose = args["verbose"]
    
    if verbose == True:
        print("-------------------------")
        print("InvokeBlenderExporter: Arguments")
        print(args)
        print("-------------------------")
    
    relative_source_path = os.path.relpath(sourceFile, sourcePath)
    target_file = os.path.join(destination, relative_source_path)

    target_path = os.path.dirname(target_file)

    # potential cleanup, blender sometimes leaves these lying around
    target_file = target_file.replace("@", "")

    if not os.path.exists(target_path):
        if verbose == True:
            print("-------------------------")
            print("Created Folder: %s"%target_path)
            print("-------------------------")

        pathlib.Path(target_path).mkdir(parents=True, exist_ok=True)

    if verbose == True:
        print("-------------------------")
        print("Source File: %s"%sourceFile)
        print("Target File: %s"%target_file)
        print("-------------------------")

    print("->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->")
    print("Exporting %s"%sourceFile)

    scriptPath = os.path.join(os.getcwd(), script)

    cmdLine = [
    converter,
    sourceFile,
    "-b",
    "--python",
    scriptPath,
    "--",
    target_file
    ]

    subprocess.call(cmdLine)

    print("%s EXPORT COMPLETE"%os.path.join(target_path, sourceFile))
    print("->->->->->->->->->->->->->->->->->->->->->->->->->->->->->->\n\n")


def InvokeBlenderImporter(file, sub_folder, relativePath, target_folder, converter_bin, blender_import_script):

    # Generate the absolute path using the target_folder
    absolute_path = os.path.dirname("%s\\%s"%(target_folder, file.replace(".\\", "")))
    target_path = os.path.dirname(absolute_path)

    print("MAKING FOLDER: %s"%target_path)
    if not os.path.exists(target_path):
        pathlib.Path(target_path).mkdir(parents=True, exist_ok=True)

    print("-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<\n")

    absPath = os.path.join(os.getcwd(), sub_folder)
    absPath = os.path.join(absPath, file)
    absPath = absPath.replace(".\\", "")
    
    print("Importing: %s"%(absPath))

    scriptPath = os.path.join(os.getcwd(), blender_import_script)

    cmdLine = [
    converter_bin,
    "-b",
    "--python",
    scriptPath,
    "--",
    absolute_path,
    absPath,
    relativePath
    ]

    print(cmdLine)
    subprocess.call(cmdLine)

    print("Import and Save Blend Complete")
    print("%s"%os.path.join(absolute_path, file))
    print("-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<-<\n\n")