from pathlib import Path

from bpy.types import Collection, Context, Object, Operator

from ..utils.common import get_collection_props, get_game_props, get_scene_props
from ..utils.compile import Compiler, sanitize_model_name
from ..utils.export import export_fbx, export_qc
from ..utils.game import check_game


class ExportOperator(Operator):
    bl_idname = 'batchmdl.export'
    bl_label = 'Export'
    bl_description = 'Export selected models in selected model groups'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        if not check_game(context):
            return False

        scene_props = get_scene_props(context.scene)
        root_collection: Collection = scene_props.root_collection

        for group_collection in root_collection.children:
            group_props = get_collection_props(group_collection)
            if not group_props.export:
                continue

            for model_collection in group_collection.children:
                model_props = get_collection_props(model_collection)
                if not model_props.export:
                    continue

                return True

        return False

    def execute(self, context: Context) -> set[str]:
        Compiler.abort()

        game_props = get_game_props(context)
        game_path = Path(game_props.game)
        compiler_path = Path(game_props.compiler)
        source_path = Path(game_props.source)
        target_path = Path(game_props.target)

        scene_props = get_scene_props(context.scene)
        root_collection: Collection = scene_props.root_collection

        for group_collection in root_collection.children:
            group_props = get_collection_props(group_collection)
            if not group_props.export:
                continue

            for object in group_collection.objects:
                if object.name.lower().endswith(('orig', 'origin')):
                    group_origin = object
                    break
            else:
                group_origin = None

            if group_props.surface_property:
                group_surface_property = group_props.surface_property
            else:
                group_surface_property = 'default'

            if group_props.material_folder:
                group_material_folder = group_props.material_folder
            else:
                group_material_folder = '/'

            for model_collection in group_collection.children:
                model_props = get_collection_props(model_collection)
                if not model_props.export:
                    continue

                reference_objects: set[Object] = set()
                collision_objects: set[Object] = set()

                for collection in model_collection.children:
                    if collection.name.lower().endswith(('col', 'collision', 'phys', 'physics')):
                        collision_objects.update(collection.all_objects)
                    else:
                        reference_objects.update(collection.all_objects)

                for object in model_collection.objects:
                    if object.name.lower().endswith(('col', 'collision', 'phys', 'physics')):
                        collision_objects.add(object)
                    else:
                        reference_objects.add(object)

                for object in model_collection.objects:
                    if object.name.lower().endswith(('orig', 'origin')):
                        model_origin = object
                        break
                else:
                    model_origin = group_origin

                if model_props.surface_property:
                    model_surface_property = model_props.surface_property
                else:
                    model_surface_property = group_surface_property

                if model_props.material_folder:
                    model_material_folder = model_props.material_folder
                else:
                    model_material_folder = group_material_folder

                model_name = sanitize_model_name(f'{group_collection.name}/{model_collection.name}')
                model_file = model_name.rpartition('/')[2]

                path = source_path.joinpath(model_name, f'{model_file}_reference.fbx')
                export_fbx(context, path, reference_objects, model_origin)

                if collision_objects:
                    path = source_path.joinpath(model_name, f'{model_file}_collision.fbx')
                    export_fbx(context, path, collision_objects, model_origin)

                path = source_path.joinpath(model_name, f'{model_file}.qc')
                export_qc(path, model_name, bool(collision_objects), model_surface_property, model_material_folder)

                Compiler.compile(game_path, compiler_path, source_path, target_path, model_name)

        Compiler.start()

        self.report({'INFO'}, 'Exported')
        return {'FINISHED'}
