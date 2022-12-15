from bpy.types import Collection, UILayout

from ..utils.common import get_collection_props
from .base_panel import BasePanel
from .collection_list import CollectionList


class CollectionPanel(BasePanel):

    def draw_collection(self, layout: UILayout, collection: Collection, list_id: str):
        collection_props = get_collection_props(collection)
        multiple_children = len(collection.children) > 1

        layout.template_list(
            *(CollectionList.bl_idname, list_id),
            *(collection, 'children'),
            *(collection_props, 'active'),
            rows=5 if multiple_children else 3,
        )

        if collection_props.active in range(len(collection.children)):
            sub_collection: Collection = collection.children[collection_props.active]
            sub_collection_props = get_collection_props(sub_collection)

            layout.prop(sub_collection_props, 'surface_property')
            layout.prop(sub_collection_props, 'material_folder')
