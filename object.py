import numpy as np

class Object:
    def __init__(self):
        # initialize vertex data and vertices list
        self.vertex_data = np.array([], dtype=np.float32)
        self.vertices = []

    def read_from_obj(self, filename):
        indices = []
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.split()
                    self.vertices.append([float(parts[1]), float(parts[2]), float(parts[3])])
                elif line.startswith('f '):
                    # OBJ indices are 1-based. We extract the vertex index only.
                    parts = line.split()[1:]
                    face_indices = [int(p.split('/')[0]) - 1 for p in parts]
                    # assuming triangles; if quads, you'd need to triangulate here
                    indices.append(face_indices)
        # calculate normals and produce shared per-vertex arrays + triangle indices
        self.vertex_data, self.indices = self.calculate_vertex_normals(indices)


    def calculate_vertex_normals(self, indices):
        # reshape the flat list of vertices into an array of shape (N/3, 3)
        verts = np.array(self.vertices, dtype=np.float32).reshape(-1, 3)

        # weld duplicate vertices by position (quantize to avoid tiny FP differences)
        quant = np.round(verts, decimals=6)
        unique_verts, inverse = np.unique(quant, axis=0, return_inverse=True)

        # accumulate normals per unique vertex (averaged face normals)
        normals = np.zeros_like(unique_verts)

        # triangulate faces (handle n-gons by fan triangulation) and map to unique verts
        triangles = []
        for face in indices:
            if len(face) == 3:
                triangles.append([inverse[face[0]], inverse[face[1]], inverse[face[2]]])
            elif len(face) > 3:
                for i in range(1, len(face) - 1):
                    triangles.append([inverse[face[0]], inverse[face[i]], inverse[face[i + 1]]])

        for tri in triangles:
            v1_idx, v2_idx, v3_idx = tri
            v1 = unique_verts[v1_idx]
            v2 = unique_verts[v2_idx]
            v3 = unique_verts[v3_idx]

            edge1 = v2 - v1
            edge2 = v3 - v1
            face_normal = np.cross(edge1, edge2)

            normals[v1_idx] += face_normal
            normals[v2_idx] += face_normal
            normals[v3_idx] += face_normal

        # normalize the accumulated vectors
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = np.divide(normals, norms, out=np.zeros_like(normals), where=norms!=0)

        # build interleaved per-vertex data (shared unique vertices)
        per_vertex = np.hstack((unique_verts, normals))  # shape (V,6)

        # create triangle index list (flattened)
        if len(triangles) == 0:
            return per_vertex.astype(np.float32).flatten(), np.array([], dtype=np.uint32)

        tri_indices = np.array(triangles, dtype=np.uint32).flatten()

        return per_vertex.astype(np.float32).flatten(), tri_indices