from os.path import commonpath
from pathlib import Path
from typing import TYPE_CHECKING

import bpy
from bpy.path import abspath
from bpy.types import Collection, Context, Scene

if TYPE_CHECKING:
    from ..props.addon import AddonPrefs
    from ..props.collection import CollectionProps
    from ..props.game import GameProps
    from ..props.scene import SceneProps


def get_addon_module() -> str:
    return __name__.partition('.')[0]


def get_addon_prefs(context: Context) -> 'AddonPrefs':
    return context.preferences.addons[get_addon_module()].preferences


def get_game_props(context: Context) -> 'GameProps | None':
    addon_prefs = get_addon_prefs(context)

    if addon_prefs.game_index in range(len(addon_prefs.game_items)):
        return addon_prefs.game_items[addon_prefs.game_index]

    return None


def get_scene_props(scene: Scene) -> 'SceneProps':
    return scene.batchmdl


def get_collection_props(collection: Collection) -> 'CollectionProps':
    return collection.batchmdl


def save_user_prefs(context: Context):
    if context.preferences.use_preferences_save:
        bpy.ops.wm.save_userpref()


def tag_redraw(context: Context):
    for window in context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'VIEW_3D':
                area.tag_redraw()


def resolve_path(path: str | Path) -> Path:
    return Path(abspath(path)).resolve()


def find_common_path(*paths: str | Path) -> Path:
    return Path(commonpath(paths))
