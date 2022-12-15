from bpy.types import UIList

from ..utils.common import get_collection_props


class CollectionList(UIList):
    bl_idname = 'BATCHMDL_UL_collection'

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        collection_props = get_collection_props(item)

        row = layout.row(align=True)
        icon = 'CHECKBOX_HLT' if collection_props.export else 'CHECKBOX_DEHLT'

        row.prop(collection_props, 'export', text='', icon=icon, emboss=False)
        row.prop(item, 'name', text='', emboss=False)
