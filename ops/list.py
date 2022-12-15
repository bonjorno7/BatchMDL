from bpy.props import EnumProperty
from bpy.types import Context, Operator

from ..utils.common import get_addon_prefs
from ..utils.list import list_add, list_copy, list_move, list_remove


class ListOperator(Operator):
    bl_idname = 'batchmdl.list'
    bl_label = 'List'
    bl_description = 'Manage list items'
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    list: EnumProperty(
        items=[
            ('GAMES', 'Games', 'Manage the games list'),
        ],
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    type: EnumProperty(
        items=[
            ('ADD', 'Add', 'Add a new item'),
            ('REMOVE', 'Remove', 'Remove the selected item'),
            ('COPY', 'Copy', 'Copy the selected item'),
            ('MOVE_UP', 'Move Up', 'Move the selected item up'),
            ('MOVE_DOWN', 'Move Down', 'Move the selected item down'),
        ],
        options={'HIDDEN', 'SKIP_SAVE'},
    )

    def execute(self, context: Context) -> set[str]:
        data, list_prop, index_prop = {
            'GAMES': (get_addon_prefs(context), 'game_items', 'game_index'),
        }[self.list]

        if self.type == 'ADD':
            setattr(data, index_prop, list_add(getattr(data, list_prop)))
        elif self.type == 'REMOVE':
            setattr(data, index_prop, list_remove(getattr(data, list_prop), getattr(data, index_prop)))
        elif self.type == 'COPY':
            setattr(data, index_prop, list_copy(getattr(data, list_prop), getattr(data, index_prop)))
        elif self.type == 'MOVE_UP':
            setattr(data, index_prop, list_move(getattr(data, list_prop), getattr(data, index_prop), -1))
        elif self.type == 'MOVE_DOWN':
            setattr(data, index_prop, list_move(getattr(data, list_prop), getattr(data, index_prop), 1))

        return {'FINISHED'}
