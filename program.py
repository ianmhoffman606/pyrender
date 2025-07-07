import numpy as np

class Program:

    def __init__(self, ctx, camera, vertex_shader, fragment_shader):
        # create a moderngl program from the provided shaders
        self.program = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)

        # get uniform locations for projection, model, and view matrices
        self.projection_uniform = self.program['projection']
        self.model_uniform = self.program['model']
        self.view_uniform = self.program['view']
        
        # set initial matrix uniforms
        self.set_defaults(camera)


    def set_defaults(self, camera):
        # get and update the projection matrix from the camera
        projection_matrix = camera.get_projection_matrix()
        self.update_projection_matrix(projection_matrix)

        # get and update the view matrix from the camera
        view_matrix = camera.get_view_matrix()
        self.update_view_matrix(view_matrix)
        
        # initialize and update the model matrix to an identity matrix
        model_matrix = np.identity(4, dtype=np.float32)
        self.update_model_matrix(model_matrix)

        
    def update_projection_matrix(self, projection_matrix):
        self.projection_uniform.write(projection_matrix.astype('f4').tobytes())

    def update_model_matrix(self, model_matrix):
        self.model_uniform.write(model_matrix.astype('f4').tobytes())

    def update_view_matrix(self, view_matrix):
        self.view_uniform.write(view_matrix.astype('f4').tobytes())