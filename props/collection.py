from bpy.props import BoolProperty, IntProperty, StringProperty
from bpy.types import PropertyGroup


class CollectionProps(PropertyGroup):
    export: BoolProperty(name='Export', description='Export the contents of this collection', default=True)
    active: IntProperty(name='Active', description='The active child of this collection')

    surface_property: StringProperty(
        name='Surface Property',
        description='.\n'.join((
            'What subtance this object is made of',
            'This affects sound and decals',
            'Leave empty to use value from parent or default',
        )),
    )

    material_folder: StringProperty(
        name='Material Folder',
        description='.\n'.join((
            'Path relative to the game materials folder',
            'This folder contains the materials for your models',
            'Leave empty to use value from parent or default',
        )),
    )
