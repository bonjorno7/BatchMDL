from bpy.props import EnumProperty, StringProperty
from bpy.types import Context, PropertyGroup

from ..utils.common import resolve_path, save_user_prefs
from ..utils.game import find_executable, find_source


class GameProps(PropertyGroup):

    def update_name(self, context: Context):
        name = str.strip(self.name)
        self['name'] = name if name else 'Game'
        save_user_prefs(context)

    name: StringProperty(
        name='Name',
        description='Display name in the list',
        default='Game',
        update=update_name,
    )

    def update_game(self, context: Context):
        game_path = resolve_path(self.game)
        self['game'] = game_path.as_posix()

        if executable := find_executable(game_path, 'quickmdl', 'studiomdl'):
            self['compiler'] = executable.as_posix()

        if executable := find_executable(game_path, 'hlmv'):
            self['viewer'] = executable.as_posix()

        self['source'] = find_source(game_path).as_posix()
        self['target'] = game_path.joinpath('models').as_posix()

        save_user_prefs(context)

    game: StringProperty(
        name='Game',
        description='.\n'.join((
            'The game folder, containing gameinfo.txt',
            'Editing this path will autofill the other paths',
        )),
        subtype='DIR_PATH',
        update=update_game,
    )

    def update_compiler(self, context: Context):
        self['compiler'] = resolve_path(self.compiler).as_posix()
        save_user_prefs(context)

    compiler: StringProperty(
        name='Compiler',
        description='Executable for compiling models, typically <bin>/studiomdl',
        subtype='FILE_PATH',
        update=update_compiler,
    )

    def update_viewer(self, context: Context):
        self['viewer'] = resolve_path(self.viewer).as_posix()
        save_user_prefs(context)

    viewer: StringProperty(
        name='Viewer',
        description='Executable for viewing models, typically <bin>/hlmv',
        subtype='FILE_PATH',
        update=update_viewer,
    )

    def update_source(self, context: Context):
        self['source'] = resolve_path(self.source).as_posix()
        save_user_prefs(context)

    source: StringProperty(
        name='Source',
        description='Folder for QC files, typically <game>/modelsrc',
        subtype='DIR_PATH',
        update=update_source,
    )

    def update_target(self, context: Context):
        self['target'] = resolve_path(self.target).as_posix()
        save_user_prefs(context)

    target: StringProperty(
        name='Target',
        description='Folder for MDL files, typically <game>/models',
        subtype='DIR_PATH',
        update=update_target,
    )

    def update_format(self, context: Context):
        save_user_prefs(context)

    format: EnumProperty(
        name='Format',
        description='File format for meshes',
        items=[
            ('SMD', 'SMD', 'Slower but supports older games'),
            ('FBX', 'FBX', 'Faster and supports two UV layers'),
        ],
        default='SMD',
        update=update_format,
    )
