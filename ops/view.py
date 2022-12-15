from pathlib import Path

from bpy.types import Collection, Context, Operator

from ..utils.common import get_collection_props, get_game_props, get_scene_props
from ..utils.compile import Compiler, sanitize_model_name
from ..utils.game import check_game


class ViewOperator(Operator):
    bl_idname = 'batchmdl.view'
    bl_label = 'View'
    bl_description = 'View the selected model in the selected model group'
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context: Context) -> bool:
        if not check_game(context):
            return False

        game_props = get_game_props(context)
        target_path = Path(game_props.target)

        scene_props = get_scene_props(context.scene)
        root_collection: Collection = scene_props.root_collection
        root_props = get_collection_props(root_collection)
        if root_props.active not in range(len(root_collection.children)):
            return False

        group_collection = root_collection.children[root_props.active]
        group_props = get_collection_props(group_collection)
        if group_props.active not in range(len(group_collection.children)):
            return False

        model_collection = group_collection.children[group_props.active]
        model_name = sanitize_model_name(f'{group_collection.name}/{model_collection.name}')
        return target_path.joinpath(f'{model_name}.mdl').is_file()

    def execute(self, context: Context) -> set[str]:
        game_props = get_game_props(context)
        game_path = Path(game_props.game)
        viewer_path = Path(game_props.viewer)
        target_path = Path(game_props.target)

        scene_props = get_scene_props(context.scene)
        root_collection: Collection = scene_props.root_collection
        root_props = get_collection_props(root_collection)

        group_collection = root_collection.children[root_props.active]
        group_props = get_collection_props(group_collection)

        model_collection = group_collection.children[group_props.active]
        model_name = sanitize_model_name(f'{group_collection.name}/{model_collection.name}')
        Compiler.view(game_path, viewer_path, target_path, model_name)

        self.report({'INFO'}, f'Viewing "{model_name}"')
        return {'FINISHED'}
