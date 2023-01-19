bl_info = {
    'name': 'BatchMDL',
    'author': 'bonjorno7',
    'description': 'Batch export static props to Source Engine',
    'blender': (3, 2, 0),
    'version': (1, 1, 2),
    'category': 'Import-Export',
    'location': 'View3D',
}

from . import ops, props, ui

modules = (
    props,
    ops,
    ui,
)


def register():
    for module in modules:
        module.register()


def unregister():
    for module in reversed(modules):
        module.unregister()
