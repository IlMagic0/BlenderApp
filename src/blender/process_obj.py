import bpy
import sys
import os

# Enable OBJ add-on
bpy.ops.preferences.addon_enable(module="io_scene_obj")

# Verify it's enabled
if not hasattr(bpy.ops.import_scene, 'obj'):
    print("ERROR: Failed to enable OBJ importer")
    sys.exit(1)

def main():
    try:
        # Get arguments after --
        args = sys.argv[sys.argv.index("--") + 1:]
        input_path = args[0]
        output_path = args[1]

        # Clear existing data
        bpy.ops.wm.read_factory_settings(use_empty=True)

        # Verify OBJ importer is available
        if not hasattr(bpy.ops.import_scene, 'obj'):
            print("ERROR: OBJ importer not available in this Blender build")
            return 1

        # Import OBJ
        print(f"Importing {input_path}...")
        bpy.ops.import_scene.obj(filepath=input_path)

        # Verify import succeeded
        if not bpy.data.objects:
            print("ERROR: No objects imported")
            return 1

        # Example processing - scale all objects
        print("Processing objects...")
        for obj in bpy.data.objects:
            obj.scale = (2.0, 2.0, 2.0)

        # Export OBJ
        print(f"Exporting to {output_path}...")
        bpy.ops.export_scene.obj(
            filepath=output_path,
            use_selection=False,
            use_mesh_modifiers=True
        )

        print("Processing completed successfully")
        return 0

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())