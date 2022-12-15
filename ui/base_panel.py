from bpy.types import Panel, UILayout


class BasePanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'BatchMDL'

    def split_layout(self) -> UILayout:
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        return self.layout
