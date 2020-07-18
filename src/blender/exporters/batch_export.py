"""
MIT License

Copyright (c) 2020 ossls

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


# This is a Blender python script. 
# When executed it will select all the objects in the scene
# and export them in a way that makes the compatible with Amazon Lumberyard.

import bpy
import os
import sys

from bpy.app.handlers import persistent

basedir = os.path.dirname(bpy.data.filepath)
view_layer = bpy.context.view_layer

# When invoking this script, the destination folder needs
# to be passed in as a command line argument, you need to use
# Blender's -- command line option which does the following:
# -- "End option processing, following arguments passed unchanged. Access via Python's 'sys.argv'"
destinationPath = sys.argv[6]

# Once the .blend file is loaded, this function will select
# all the objects in Object mode, set Edit mode
# then export the scene as an FBX file that is compatible
# with Lumberyard. 
# 
# Currently it only exports the MESH.
#
def doExport(fileName):
    
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.object.select_all(action='SELECT')

    selection = bpy.context.selected_objects
    bpy.ops.object.mode_set(mode='EDIT')

    for object in selection:
        bpy.ops.mesh.select_all(action='SELECT')

        # Cleanup some of the geometry to avoid artifacts
        bpy.ops.mesh.delete_loose(use_verts=True, use_edges=True, use_faces=False) # Delete loose vertices, edges or faces
        bpy.ops.mesh.dissolve_degenerate(threshold=0.0001) # Dissolve zero area faces and zero length edges
        bpy.ops.mesh.normals_make_consistent(inside=False) # Make face and vertex normals point either outside or inside the mesh

        # TODO: Currently I found no benefit to doing any operations on the normals
        #bpy.ops.mesh.set_normals_from_faces()
        #bpy.ops.mesh.split_normals()
        #bpy.ops.mesh.average_normals(average_type='FACE_AREA')

    bpy.ops.export_scene.fbx(   filepath=fileName, 
                                check_existing=True, 
                                axis_forward='Y', 
                                axis_up='Z', 
                                use_selection=True, 
                                global_scale=1.0, 
                                apply_unit_scale=True, 
                                bake_space_transform=True, 
                                object_types={'MESH'}, 
                                use_mesh_modifiers=False, 
                                use_mesh_modifiers_render=False, 
                                mesh_smooth_type='EDGE', 
                                use_mesh_edges=True, 
                                use_tspace=True, 
                                use_custom_props=False, 
                                add_leaf_bones=True, 
                                primary_bone_axis='Y', 
                                secondary_bone_axis='X', 
                                use_armature_deform_only=False, 
                                armature_nodetype='NULL', 
                                path_mode='AUTO', 
                                embed_textures=False, 
                                batch_mode='OFF', 
                                use_batch_own_dir=True, 
                                use_metadata=True 
                                # filter_glob="*.fbx", 
                                # version='BIN7400', 
                                # ui_tab='MAIN', 
                                # bake_anim=True, 
                                # bake_anim_use_all_bones=True, 
                                # bake_anim_use_nla_strips=True, 
                                # bake_anim_use_all_actions=True, 
                                # bake_anim_force_startend_keying=True, 
                                # bake_anim_step=1.0, 
                                # bake_anim_simplify_factor=1.0, 
                                # use_anim=True, 
                                # use_anim_action_all=True, 
                                # use_default_take=True, 
                                # use_anim_optimize=True, 
                                # anim_optimize_precision=6.0, 
                                )
                                
    view_layer.objects.active = None

    print ("Exported: %s"%fileName)

# The load handler will trigger the export
@persistent
def load_handler(dummy):
    print("Load Handler:", bpy.data.filepath)

    path, filename = os.path.split(bpy.data.filepath)

    targetPath = os.path.dirname(destinationPath)
    targetFile = os.path.join(targetPath, filename.replace(".blend", ".fbx"))

    if not os.path.exists(targetPath):
        os.mkdir(targetPath)

    print("Starting export: %s"%targetFile)
    doExport(targetFile)

# Install the load handler
bpy.app.handlers.load_post.append(load_handler)

# Open the .blend file
bpy.ops.wm.open_mainfile(filepath=bpy.data.filepath)