from bpy.types import Collection, Context

from ..utils.common import get_collection_props, get_scene_props
from .collection_panel import CollectionPanel
from .group_panel import GroupPanel


class ModelPanel(CollectionPanel):
    bl_parent_id = GroupPanel.bl_idname
    bl_idname = 'BATCHMDL_PT_model'
    bl_label = 'Models'

    @classmethod
    def poll(cls, context: Context):
        scene_props = get_scene_props(context.scene)
        collection: Collection = scene_props.root_collection

        collection_props = get_collection_props(collection)
        return collection_props.active in range(len(collection.children))

    def draw(self, context: Context):
        layout = self.split_layout()
        scene_props = get_scene_props(context.scene)

        collection: Collection = scene_props.root_collection
        collection_props = get_collection_props(collection)

        sub_collection: Collection = collection.children[collection_props.active]
        self.draw_collection(layout, sub_collection, 'BATCHMDL_UL_model')
