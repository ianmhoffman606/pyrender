import pywavefront
import numpy as np

class Object:
    def __init__(self):
        # initialize vertex data and vertices list
        self.vertex_data = np.array([], dtype=np.float32)
        self.vertices = []

    def read_from_obj(self, filename):
        # read object data from .obj file
        data = pywavefront.Wavefront(filename, cache=True, parse=True)
        obj = data.materials.popitem()[1]
        self.vertices = obj.vertices
        self.vertex_data = self.calculate_vertex_normals()

    def calculate_vertex_normals(self):
        # reshape the flat list of vertices into an array of shape (N/3, 3)
        verts = np.array(self.vertices, dtype=np.float32).reshape(-1, 3)

        # a dictionary to map vertex coordinates (as tuples) to their accumulated normal.
        # using tuples as dict keys because numpy arrays are not hashable.
        normal_accumulator = {}

        # iterate over triangles to calculate face normals and accumulate them for each vertex.
        for i in range(0, len(verts), 3):
            # Get the vertices of the triangle
            v1, v2, v3 = verts[i], verts[i+1], verts[i+2]

            # calculate two edges of the triangle
            edge1 = v2 - v1
            edge2 = v3 - v1
            
            # the face normal is the cross product of the two edges.
            face_normal = np.cross(edge1, edge2)
            
            # skip degenerate triangles
            if np.allclose(face_normal, 0):
                continue
            
            # add this face normal to the accumulator for each of the three vertices.
            for v in [v1, v2, v3]:
                v_tuple = tuple(v)
                normal_accumulator.setdefault(v_tuple, np.zeros(3, dtype=np.float32))
                normal_accumulator[v_tuple] += face_normal
        
        # normalize the accumulated normals for each unique vertex.
        for v_tuple in normal_accumulator:
            normal = normal_accumulator[v_tuple]
            norm_len = np.linalg.norm(normal)
            if norm_len > 0:
                normal_accumulator[v_tuple] = normal / norm_len
        
        # create the final interleaved vertex data array by looking up the smooth normal for each vertex.
        interleaved_data = np.empty((verts.shape[0], 6), dtype=np.float32)
        for i, v in enumerate(verts):
            interleaved_data[i, :3] = v
            interleaved_data[i, 3:] = normal_accumulator[tuple(v)]
        
        # flatten the interleaved array for the VBO
        return interleaved_data.flatten()