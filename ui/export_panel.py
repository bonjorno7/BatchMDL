from bpy.types import Context

from ..ops.abort import AbortOperator
from ..ops.export import ExportOperator
from ..ops.view import ViewOperator
from ..utils.common import get_scene_props
from ..utils.compile import Compiler
from .base_panel import BasePanel
from .main_panel import MainPanel


class ExportPanel(BasePanel):
    bl_parent_id = MainPanel.bl_idname
    bl_idname = 'BATCHMDL_PT_export'
    bl_label = 'Export'

    def draw(self, context: Context):
        layout = self.split_layout()

        scene_props = get_scene_props(context.scene)
        layout.prop(scene_props, 'root_collection')

        row = layout.row()

        if Compiler.is_compiling():
            row.prop(scene_props, 'compile_progress')
            row.operator(AbortOperator.bl_idname, text='', icon='X')

        elif scene_props.root_collection:
            row.operator(ExportOperator.bl_idname)
            row.operator(ViewOperator.bl_idname)
