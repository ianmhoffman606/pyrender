import numpy as np

class Vector3:
    def __init__(self, vector):
        self.x = vector[0]
        self.y = vector[1]
        self.z = vector[2] # initialize x, y, z components

    def __add__(self, other):
        # vector addition
        return Vector3([self.x + other.x, self.y + other.y, self.z + other.z])
    
    def __sub__(self, other):
        # vector subtraction
        return Vector3([self.x - other.x, self.y - other.y, self.z - other.z])
    
    def __mul__(self, scalar):
        # scalar multiplication
        return Vector3([self.x * scalar, self.y * scalar, self.z * scalar])

    def normalize(self):
        # normalize the vector
        magnitude = (self.x**2 + self.y**2 + self.z**2)**0.5
        if magnitude != 0:
            return Vector3([self.x / magnitude, self.y / magnitude, self.z / magnitude])
        else:
            return self
        
    def cross(self, other):
        # cross product of two vectors
        return Vector3([
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        ])
    
    def dot(self, other):
        # dot product of two vectors
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def tobytes(self):
        # convert vector to bytes for use with moderngl
        return np.array([self.x, self.y, self.z], dtype=np.float32).tobytes()

    
class Matrix44:

    def create_perspective_projection_matrix(fov, aspect, near, far):
        # create a perspective projection matrix
        uh = 1. / np.tan(0.5 * fov * np.pi / 180)
        uw = uh / aspect
        reciprocal_depth = 1 / (near - far)
        f = (far + near) * reciprocal_depth
        fn = (2. * far * near) * reciprocal_depth

        # construct the projection matrix
        return np.array((
                (uw, 0., 0., 0.),
                (0., uh, 0., 0.),
                (0., 0., f, -1.),
                (0., 0., fn, 0.)
            ), dtype=np.float32)

    def create_look_at_matrix(eye, target, up):
        # create a look-at view matrix

        # calculate camera axes
        forward = Vector3.normalize(target - eye)
        side = Vector3.normalize(Vector3.cross(forward, up))
        up = Vector3.normalize(Vector3.cross(side, forward))

        # construct the view matrix
        return np.array((
                (side.x, up.x, -forward.x, 0.),
                (side.y, up.y, -forward.y, 0.),
                (side.z, up.z, -forward.z, 0.),
                (-Vector3.dot(side, eye), -Vector3.dot(up, eye), Vector3.dot(forward, eye), 1.0)
            ), dtype=np.float32)