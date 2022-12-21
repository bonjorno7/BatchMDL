from math import radians
from pathlib import Path

import bmesh
import bpy
from bpy.types import Context, Object
from mathutils import Euler, Matrix

SMD_MATRIX = Euler((0, 0, radians(-90))).to_matrix().to_4x4()
FBX_MATRIX = Euler((0, 0, radians(180))).to_matrix().to_4x4()


def export_mesh(context: Context, path: Path, objects: set[Object], origin: Object | None, format: str):
    path.parent.mkdir(parents=True, exist_ok=True)

    collection = bpy.data.collections.new('TEMP')
    context.scene.collection.children.link(collection)

    object_matrix_world: dict[Object, Matrix] = {}
    object_hide_viewport: dict[Object, bool] = {}
    object_hide_select: dict[Object, bool] = {}
    object_select: dict[Object, bool] = {}

    matrix = {'SMD': SMD_MATRIX, 'FBX': FBX_MATRIX}[format]
    if origin:
        matrix = matrix @ origin.matrix_world.inverted_safe()

    def add_parent_recursive(object: Object):
        if object.parent:
            objects.add(object.parent)
            add_parent_recursive(object.parent)

    for object in objects.copy():
        add_parent_recursive(object)

    for object in objects:
        collection.objects.link(object)

        if not object.parent:
            object_matrix_world[object] = object.matrix_world.copy()
            object.matrix_world = matrix @ object.matrix_world

        object_hide_viewport[object] = object.hide_viewport
        object.hide_viewport = False

        object_hide_select[object] = object.hide_select
        object.hide_select = False

    for object in bpy.data.objects:
        object_select[object] = object.select_get()
        object.select_set(object in objects)

    try:
        function = {'SMD': export_smd, 'FBX': export_fbx}[format]
        function(context, path)

    except:
        raise

    finally:
        for object, select in object_select.items():
            object.select_set(select)

        for object, hide_select in object_hide_select.items():
            object.hide_select = hide_select

        for object, hide_viewport in object_hide_viewport.items():
            object.hide_viewport = hide_viewport

        for object, matrix_world in object_matrix_world.items():
            object.matrix_world = matrix_world

        bpy.data.collections.remove(collection)


def export_smd(context: Context, path: Path):
    with open(path, 'w') as file:
        file.write('version 1\n')

        file.write('nodes\n')
        file.write('0 "root" -1\n')
        file.write('end\n')

        file.write('skeleton\n')
        file.write('time 0\n')
        file.write('0  0 0 0  0 0 0\n')
        file.write('end\n')

        file.write('triangles\n')

        depsgraph = context.evaluated_depsgraph_get()

        for object in context.selected_objects:
            if object.type not in ('MESH', 'CURVE', 'SURFACE', 'FONT'):
                continue

            evaluated = object.evaluated_get(depsgraph)
            mesh = bpy.data.meshes.new_from_object(
                object=evaluated,
                preserve_all_data_layers=True,
                depsgraph=depsgraph,
            )

            bm = bmesh.new()
            bm.from_mesh(mesh)

            bmesh.ops.transform(bm, matrix=object.matrix_world, space=Matrix.Identity(4), verts=bm.verts)
            bmesh.ops.triangulate(bm, faces=bm.faces)

            bm.normal_update()
            bm.to_mesh(mesh)
            bm.free()

            mesh.calc_normals_split()

            for polygon in mesh.polygons:
                material_name = 'no_material'

                if polygon.material_index < len(mesh.materials):
                    material = mesh.materials[polygon.material_index]

                    if material:
                        material_name = material.name

                file.write(f'{material_name}\n')

                for loop_index in polygon.loop_indices:
                    loop = mesh.loops[loop_index]
                    vertex = mesh.vertices[loop.vertex_index]

                    position = ' '.join(f'{value:.6f}' for value in vertex.co[0:3])
                    normal = ' '.join(f'{value:.6f}' for value in loop.normal[0:3])

                    uv = mesh.uv_layers.active.data[loop_index].uv[0:2] if mesh.uv_layers else [0.0, 0.0]
                    uv = ' '.join(f'{value:.6f}' for value in uv)

                    file.write(f'0  {position}  {normal}  {uv}\n')

            bpy.data.meshes.remove(mesh)

        file.write('end\n')


def export_fbx(context: Context, path: Path):
    bpy.ops.export_scene.fbx(
        filepath=str(path),
        use_selection=True,
        use_triangles=True,
        global_scale=0.01,
    )


def export_qc(
    path: Path,
    name: str,
    use_collision: bool,
    surface_property: str,
    material_folder: str,
    mesh_format: str,
):
    path.parent.mkdir(parents=True, exist_ok=True)
    prefix = name.rpartition('/')[2]

    with open(path, 'w') as file:
        file.write(f'$modelname "{name}"\n')
        file.write('$staticprop\n')

        file.write(f'$surfaceprop "{surface_property}"\n')
        file.write(f'$cdmaterials "{material_folder}"\n')

        file.write(f'$body "reference" "{prefix}_reference.{mesh_format.lower()}"\n')
        file.write(f'$sequence "idle" "{prefix}_reference.{mesh_format.lower()}"\n')

        if use_collision:
            file.write(f'$collisionmodel "{prefix}_collision.{mesh_format.lower()}" {{ $concave }}\n')
