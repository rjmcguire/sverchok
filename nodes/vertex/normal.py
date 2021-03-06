# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
import bmesh

from sverchok.node_tree import SverchCustomTreeNode
from sverchok.utils.sv_bmesh_utils import bmesh_from_pydata


class VectorNormalNode(bpy.types.Node, SverchCustomTreeNode):
    ''' Find Vector's normals '''
    bl_idname = 'VectorNormalNode'
    bl_label = 'Vertex Normal'
    bl_icon = 'OUTLINER_OB_EMPTY'

    def sv_init(self, context):
        self.inputs.new('VerticesSocket', "Vertices", "Vertices")
        self.inputs.new('StringsSocket', "Polygons", "Polygons")
        self.outputs.new('VerticesSocket', "Normals", "Normals")

    def process(self):
        vers = self.inputs['Vertices'].sv_get()
        pols = self.inputs['Polygons'].sv_get()

        normalsFORout = []
        for i, obj in enumerate(vers):
            """
            mesh_temp = bpy.data.meshes.new('temp')
            mesh_temp.from_pydata(obj, [], pols[i])
            mesh_temp.update(calc_edges=True)
            """
            bm = bmesh_from_pydata(obj, [], pols[i])

            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            bm.verts.ensure_lookup_table()
            verts = bm.verts
            tempobj = []

            for idx in range(len(verts)):
                tempobj.append(verts[idx].normal[:])

            normalsFORout.append(tempobj)
            bm.free()

        if self.outputs['Normals'].is_linked:
            self.outputs['Normals'].sv_set(normalsFORout)


def register():
    bpy.utils.register_class(VectorNormalNode)


def unregister():
    bpy.utils.unregister_class(VectorNormalNode)
