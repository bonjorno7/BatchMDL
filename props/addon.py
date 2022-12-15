from bpy.props import CollectionProperty, IntProperty
from bpy.types import AddonPreferences, Context

from ..utils.common import get_addon_module, save_user_prefs
from .game import GameProps


class AddonPrefs(AddonPreferences):
    bl_idname = get_addon_module()

    def update_game_index(self, context: Context):
        save_user_prefs(context)

    game_items: CollectionProperty(type=GameProps)
    game_index: IntProperty(name='Active Game', update=update_game_index)
