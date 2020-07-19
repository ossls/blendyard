# blendyard

A collection of tools to make it easier to create art for Lumberyard using Blender.

## blendyard Converters

Converts .blend files directly into a .fbx format compatible with Amazon Lumberyard

## blendyard Watchdog

Watches a specified folder for any .blend files to change, when they do, they are automatically exported.

Set the target folder to be within your active Amazon Lumberyard project and any time you save a .blend file in Blender, it will automatically be exported to .fbx and Lumberyard's Asset Processor will pick up the change and build it.

**Note:** Lumberyard may not display the change unless you make the select the application and put it on the foreground. Alt+Tab from Blender to Lumberyard to see your updated Blender file in Lumberyard.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=sfu9E7HPy4s" target="_blank"><img src="http://img.youtube.com/vi/sfu9E7HPy4s/0.jpg" alt="blendyard" width="240" height="180" border="10" /><br/>See it in action!</a>

### Requirements

Python 3.8+

Install Watchdog (https://pythonhosted.org/watchdog)

pip install watchdog

### Instructions

1. Open settings.json and configure the paths

```
{
    "general":
    {
        "comment": "Find and provide the path to your Blender executeable",
        "blender_exe": "C:\\Program Files\\Blender Foundation\\Blender 2.82\\blender.exe"
    },
    "models":
    {
        "comment_source": "Provide the folder in which your source .blend files are stored, the ones you intend to export into .fbx for use in Amazon Lumberyard",
        "source_folder": "C:\\Example\\MyBlenderFiles",
        "comment_target": "Provide the folder into which the exporter .fbx files need to be saved, this is usually a Lumberyard project or gem (gem recommended)",
        "target_folder": "C:\\Example\\Lumberyard\\dev\\Gems\\MyGem\\Assets\\Models"
    },
    "watchdog":
    {
        "comment": "Provide the folder in which your source .blend files are stored, the ones you intend to export into .fbx for use in Amazon Lumberyard",
        "watched_folder": "C:\\Example\\MyBlenderFiles",
        "verbose": 1,
        "delta_throttle": 200
    }
}
```

**blender_exe** Path to the Blender executable
**source_folder** Path to the folder that will hold your source .blend files (do not put this within the Lumberyard folders)
**target_folder** Path to the folder to which the .fbx files will be exported to, usually a Lumberyard project or gem, gem recommended (see Lumberyard's instructions for Asset gems)
**watched_folder** Path to the folder the watchdog will watch, usually this is the same as the **source_folder**

2. Run the watchdog from the root of blendyard, this window will need to remain open as long as you want the Watchdog to automatically convert your .blend files into .fbx files

- Open a new console window (WinKey+R, cmd, enter)
- Navigate to the blendyard folder
- Run the watchdog:
    python src\blender\watchdog\blendyard_watchdog.py

3. In Blender, open a file within your specified **source_folder**, modify it and save it

4. Alt+Tab into Lumberyard, if you have not yet setup an entity with a Mesh component set to your FBX file see step 5, otherwise you will see your model update

5. If you have not yet created an entity in Lumberyard, add an Entity, Add a Mesh Component, set the Asset to your desired .FBX file

