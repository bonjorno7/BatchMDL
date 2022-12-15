from pathlib import Path
from subprocess import PIPE, Popen
from sys import platform
from threading import Lock, Thread

import bpy
from bpy.app.timers import is_registered, register, unregister

from .common import find_common_path, get_game_props, get_scene_props, tag_redraw


def sanitize_model_name(name: str) -> str:
    name = name.replace('\\', '/').strip('/ ')

    while '//' in name:
        name = name.replace('//', '/')

    for char in ' :*?"<>|':
        name = name.replace(char, '_')

    return name.lower()


class Compiler:
    lock = Lock()
    pipes: list[Popen] = []

    count = 0
    total = 0

    @classmethod
    def start(cls):
        if not is_registered(cls.timer):
            register(cls.timer, persistent=True)

    @classmethod
    def abort(cls):
        if is_registered(cls.timer):
            unregister(cls.timer)

        with cls.lock:
            while cls.pipes:
                cls.pipes.pop().terminate()

        cls.count = 0
        cls.total = 0

    @classmethod
    def timer(cls) -> float:
        if not cls.is_compiling():
            game_props = get_game_props(bpy.context)
            cls.clean(Path(game_props.game).joinpath('models'))

            tag_redraw(bpy.context)
            return None

        scene_props = get_scene_props(bpy.context.scene)
        progress = 100.0 * cls.count / max(1, cls.total)

        if scene_props.compile_progress != progress:
            scene_props['compile_progress'] = progress
            tag_redraw(bpy.context)

        return 0.1

    @classmethod
    def is_compiling(cls) -> bool:
        return cls.count != cls.total

    @classmethod
    def compile(cls, game: Path, compiler: Path, source: Path, target: Path, name: str):
        cls.total += 1

        args = (game, compiler, source, target, name)
        Thread(target=cls.compile_worker, args=args, daemon=True).start()

    @classmethod
    def compile_worker(cls, game: Path, executable: Path, source: Path, target: Path, name: str):
        output = game.joinpath('models')
        folder, _, file = name.rpartition('/')

        model = source.joinpath(name, f'{file}.qc')
        pipe = cls.run(game, executable, model)

        with cls.lock:
            cls.pipes.append(pipe)

        stdout, _ = pipe.communicate()
        log = source.joinpath(name, f'{file}.log')
        log.write_bytes(stdout)

        with cls.lock:
            if pipe in cls.pipes:
                cls.pipes.remove(pipe)

        if target != output:
            target_folder = target.joinpath(folder)
            target_folder.mkdir(parents=True, exist_ok=True)

            for suffix in ('mdl', 'phy', 'vvd', 'dx90.vtx', 'dx80.vtx', 'sw.vtx'):
                target_file = target.joinpath(f'{name}.{suffix}')
                output_file = output.joinpath(f'{name}.{suffix}')

                target_file.unlink(missing_ok=True)
                if output_file.is_file():
                    output_file.rename(target_file)

        cls.count += 1

    @classmethod
    def view(cls, game: Path, executable: Path, target: Path, name: str):
        model = target.joinpath(f'{name}.mdl')
        cls.run(game, executable, model)

    @classmethod
    def run(cls, game: Path, executable: Path, model: Path) -> Popen:
        use_wine = platform == 'linux' and executable.suffix == '.exe'

        cwd = None
        if use_wine:
            cwd = find_common_path(game, executable, model)

            game = game.relative_to(cwd)
            executable = executable.relative_to(cwd)
            model = model.relative_to(cwd)

        args = [str(executable), '-game', str(game), str(model)]
        if use_wine:
            args.insert(0, 'wine')

        return Popen(args, stdout=PIPE, stderr=PIPE, cwd=cwd)

    @classmethod
    def clean(cls, folder: Path):
        for path in sorted(folder.rglob('**'), key=lambda path: len(path.parents), reverse=True):
            try:
                path.rmdir()
            except OSError:
                pass
