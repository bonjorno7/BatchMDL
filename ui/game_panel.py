from bpy.app.translations import pgettext_iface
from bpy.types import Context

from ..ops.list import ListOperator
from ..utils.common import get_addon_prefs, get_game_props
from .base_panel import BasePanel
from .generic_list import GenericList
from .main_panel import MainPanel


class GamePanel(BasePanel):
    bl_parent_id = MainPanel.bl_idname
    bl_idname = 'BATCHMDL_PT_game'
    bl_label = 'Games'

    def draw(self, context: Context):
        layout = self.split_layout()

        addon_prefs = get_addon_prefs(context)
        game_props = get_game_props(context)
        multiple_games = len(addon_prefs.game_items) > 1

        if not context.preferences.use_preferences_save:
            row = layout.row()
            row.operator_context = 'EXEC_DEFAULT'
            text = pgettext_iface('Save') + (' *' if context.preferences.is_dirty else '')
            row.operator('wm.save_userpref', text=text)

        row = layout.row()
        row.template_list(
            *(GenericList.bl_idname, 'BATCHMDL_UL_game'),
            *(addon_prefs, 'game_items'),
            *(addon_prefs, 'game_index'),
            rows=5 if multiple_games else 3,
        )

        col = row.column(align=True)
        op = col.operator(ListOperator.bl_idname, text='', icon='ADD')
        op.list, op.type = 'GAMES', 'ADD'
        op = col.operator(ListOperator.bl_idname, text='', icon='REMOVE')
        op.list, op.type = 'GAMES', 'REMOVE'

        col.separator()
        op = col.operator(ListOperator.bl_idname, text='', icon='DUPLICATE')
        op.list, op.type = 'GAMES', 'COPY'

        if multiple_games:
            col.separator()
            op = col.operator(ListOperator.bl_idname, text='', icon='TRIA_UP')
            op.list, op.type = 'GAMES', 'MOVE_UP'
            op = col.operator(ListOperator.bl_idname, text='', icon='TRIA_DOWN')
            op.list, op.type = 'GAMES', 'MOVE_DOWN'

        if game_props:
            for property_name in ('game', 'compiler', 'viewer', 'source', 'target'):
                layout.prop(game_props, property_name, translate=False)
