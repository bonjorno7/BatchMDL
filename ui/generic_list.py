from bpy.types import UIList


class GenericList(UIList):
    bl_idname = 'BATCHMDL_UL_generic'

    def draw_item(self, context, layout, data, item, icon, active_data, active_property, index, flt_flag):
        layout.prop(item, 'name', text='', emboss=False)
