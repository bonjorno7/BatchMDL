from math import radians
from pathlib import Path

import bpy
from bpy.types import Context, Object
from mathutils import Matrix


def export_fbx(context: Context, path: Path, objects: set[Object], origin: Object | None):
    path.parent.mkdir(parents=True, exist_ok=True)

    collection = bpy.data.collections.new('TEMP')
    context.scene.collection.children.link(collection)

    active_layer_collection = context.view_layer.active_layer_collection
    context.view_layer.active_layer_collection = context.view_layer.layer_collection.children[-1]

    object_hide_viewport: dict[Object, bool] = {}
    object_matrix_world: dict[Object, Matrix] = {}

    if origin:
        origin_matrix = origin.matrix_world.inverted_safe()

    rotation_matrix = Matrix.Rotation(radians(180), 4, 'Z')

    def add_parent_recursive(object: Object):
        if object.parent:
            objects.add(object.parent)
            add_parent_recursive(object.parent)

    for object in objects.copy():
        add_parent_recursive(object)

    for object in objects:
        collection.objects.link(object)

        object_hide_viewport[object] = object.hide_viewport
        object.hide_viewport = False

        if not object.parent:
            object_matrix_world[object] = object.matrix_world.copy()

            if origin:
                object.matrix_world = origin_matrix @ object.matrix_world

            object.matrix_world = rotation_matrix @ object.matrix_world

    try:
        bpy.ops.export_scene.fbx(
            filepath=str(path),
            use_active_collection=True,
            use_triangles=True,
            global_scale=0.01,
        )

    except:
        raise

    finally:
        for object, hide_viewport in object_hide_viewport.items():
            object.hide_viewport = hide_viewport

        for object, matrix_world in object_matrix_world.items():
            object.matrix_world = matrix_world

        context.view_layer.active_layer_collection = active_layer_collection
        bpy.data.collections.remove(collection)


def export_qc(
    path: Path,
    name: str,
    use_collision: bool,
    surface_property: str,
    material_folder: str,
):
    path.parent.mkdir(parents=True, exist_ok=True)
    prefix = name.rpartition('/')[2]

    with open(path, 'w') as file:
        file.write(f'$modelname "{name}"\n')
        file.write('$staticprop\n')

        file.write(f'$surfaceprop "{surface_property}"\n')
        file.write(f'$cdmaterials "{material_folder}"\n')

        file.write(f'$body "reference" "{prefix}_reference.fbx"\n')
        file.write(f'$sequence "idle" "{prefix}_reference.fbx"\n')

        if use_collision:
            file.write(f'$collisionmodel "{prefix}_collision.fbx" {{ $concave }}\n')
