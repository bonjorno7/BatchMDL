from bpy.props import FloatProperty, PointerProperty
from bpy.types import Collection, PropertyGroup


class SceneProps(PropertyGroup):
    root_collection: PointerProperty(
        name='Root Collection',
        description='The collection containing model groups',
        type=Collection,
    )

    def get_compile_progress(self) -> float:
        return self.get('compile_progress', 0.0)

    def set_compile_progress(self, value: float):
        pass

    compile_progress: FloatProperty(
        name='Compile Progress',
        description='The percentage of models that have finished compiling',
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE',
        get=get_compile_progress,
        set=set_compile_progress,
    )
