from bpy.types import Collection, Context

from ..utils.common import get_scene_props
from .collection_panel import CollectionPanel
from .export_panel import ExportPanel


class GroupPanel(CollectionPanel):
    bl_parent_id = ExportPanel.bl_idname
    bl_idname = 'BATCHMDL_PT_group'
    bl_label = 'Groups'

    @classmethod
    def poll(cls, context: Context):
        scene_props = get_scene_props(context.scene)
        return scene_props.root_collection

    def draw(self, context: Context):
        layout = self.split_layout()
        scene_props = get_scene_props(context.scene)

        collection: Collection = scene_props.root_collection
        self.draw_collection(layout, collection, 'BATCHMDL_UL_group')
