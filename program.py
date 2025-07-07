import numpy as np

class Program:

    def __init__(self, ctx, camera, vertex_shader, fragment_shader):
        self.vertex_shader = vertex_shader
        self.fragment_shader = fragment_shader
        self.program = ctx.program(vertex_shader=self.vertex_shader, fragment_shader=self.fragment_shader)

        self.projection_uniform = self.program['projection']
        self.model_uniform = self.program['model']
        self.view_uniform = self.program['view']
        
        self.set_defaults(camera)


    def set_defaults(self, camera):
        projection_matrix = camera.getProjectionMatrix()
        self.update_projection_matrix(projection_matrix)

        view_matrix = camera.getViewMatrix()
        self.update_view_matrix(view_matrix)
        
        model_matrix = np.identity(4, dtype=None)
        self.update_model_matrix(model_matrix)

        
    def update_projection_matrix(self, projection_matrix):
        self.projection_uniform.write(projection_matrix.astype('f4').tobytes())

    def update_model_matrix(self, model_matrix):
        self.model_uniform.write(model_matrix.astype('f4').tobytes())

    def update_view_matrix(self, view_matrix):
        self.view_uniform.write(view_matrix.astype('f4').tobytes())