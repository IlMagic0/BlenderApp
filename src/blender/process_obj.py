import bpy
import sys
import os

try:
    # Get arguments
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) < 2:
        print("Error: Missing input or output path")
        sys.exit(1)

    input_path = args[0]
    output_path = args[1]

    # Verify that the input file exists
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        sys.exit(1)

    # Clear existing objects
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # Import OBJ
    bpy.ops.import_scene.obj(filepath=input_path)

    # Check if anything was imported
    if not bpy.context.selected_objects:
        print("Error: No objects were imported from the OBJ file")
        sys.exit(1)

    # Example processing - scale all objects
    for obj in bpy.context.selected_objects:
        obj.scale = (2.0, 2.0, 2.0)

    # Export OBJ
    bpy.ops.export_scene.obj(
        filepath=output_path,
        use_selection=True,
        use_mesh_modifiers=True
    )

    print(f"Successfully processed {input_path} to {output_path}")
    sys.exit(0)

except Exception as e:
    print(f"Error during processing: {str(e)}")
    sys.exit(1)