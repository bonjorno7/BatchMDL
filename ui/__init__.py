from bpy.utils import register_class, unregister_class

from .collection_list import CollectionList
from .export_panel import ExportPanel
from .game_panel import GamePanel
from .generic_list import GenericList
from .group_panel import GroupPanel
from .main_panel import MainPanel
from .model_panel import ModelPanel

classes = (
    GenericList,
    CollectionList,
    MainPanel,
    GamePanel,
    ExportPanel,
    GroupPanel,
    ModelPanel,
)


def register():
    for cls in classes:
        register_class(cls)


def unregister():
    for cls in reversed(classes):
        unregister_class(cls)
