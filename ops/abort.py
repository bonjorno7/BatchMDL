from bpy.types import Context, Operator

from ..utils.compile import Compiler


class AbortOperator(Operator):
    bl_idname = 'batchmdl.abort'
    bl_label = 'Abort'
    bl_description = 'Abort the current compilation'
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context: Context) -> set[str]:
        count = Compiler.total - Compiler.count
        Compiler.abort()

        self.report({'INFO'}, f'Aborted {count} compiles')
        return {'FINISHED'}
