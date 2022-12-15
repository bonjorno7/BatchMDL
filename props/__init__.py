from bpy.props import PointerProperty
from bpy.types import Collection, Scene
from bpy.utils import register_class, unregister_class

from .addon import AddonPrefs
from .collection import CollectionProps
from .game import GameProps
from .scene import SceneProps

classes = (
    CollectionProps,
    SceneProps,
    GameProps,
    AddonPrefs,
)


def register():
    for cls in classes:
        register_class(cls)

    Collection.batchmdl = PointerProperty(type=CollectionProps)
    Scene.batchmdl = PointerProperty(type=SceneProps)


def unregister():
    del Scene.batchmdl
    del Collection.batchmdl

    for cls in reversed(classes):
        unregister_class(cls)
