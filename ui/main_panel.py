from bpy.types import Context

from .base_panel import BasePanel


class MainPanel(BasePanel):
    bl_idname = 'BATCHMDL_PT_main'
    bl_label = 'BatchMDL'

    def draw(self, context: Context):
        pass
