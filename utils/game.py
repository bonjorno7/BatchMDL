from pathlib import Path

from bpy.types import Context

from .common import get_game_props


def check_game(context: Context) -> bool:
    game_props = get_game_props(context)
    if not game_props:
        return False

    dir_paths = (game_props.game, game_props.source, game_props.target)
    if any(not Path(dir_path).is_dir() for dir_path in dir_paths):
        return False

    file_paths = (game_props.compiler, game_props.viewer)
    if any(not Path(file_path).is_file() for file_path in file_paths):
        return False

    return True


def find_executable(game_path: Path, *stems: str) -> Path | None:
    bin_path = game_path.parent.joinpath('bin')

    for stem in stems:
        for path in bin_path.rglob(f'{stem}*'):
            if path.is_file() and path.stem == stem and path.suffix in ('', '.exe'):
                return path

    return None


def find_source(game_path: Path) -> Path:
    content_path = game_path.parent.parent.joinpath('content', game_path.name, 'models')
    return content_path if content_path.is_dir() else game_path.joinpath('modelsrc')
