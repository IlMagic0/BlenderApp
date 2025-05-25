import bpy
import sys

args = sys.argv[sys.argv.index("--") + 1:]
input_path = args[0]
output_path = args[1]

bpy.ops.import_scene.obj(filepath=input_path)

# Example: scale objects
for obj in bpy.context.selected_objects:
    obj.scale = (2.0, 2.0, 2.0)

bpy.ops.export_scene.obj(filepath=output_path)
