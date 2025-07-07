import moderngl
import sys
import pygame

from camera import Camera
from object import Object
from program import Program
from mathlib import Vector3

pygame.init()

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ASPECT_RATIO = WINDOW_WIDTH / WINDOW_HEIGHT
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), flags=pygame.OPENGL | pygame.DOUBLEBUF, vsync=True)

ctx = moderngl.get_context()

camera = Camera(ASPECT_RATIO, 60, 0.1, 0.2)

shaders = Program(
    ctx=ctx, 
    camera=camera, 
    vertex_shader= open("shaders/default.vert", "r").read(), 
    fragment_shader= open("shaders/default.frag", "r").read()
)

# get the moderngl program object from the Program wrapper
prog = shaders.program 

# load the 3d object
teapot = Object()
teapot.read_from_obj("models/teapot.obj") 


# Put the array into a VBO
vbo = ctx.buffer(teapot.vertex_data.astype('f4').tobytes())
vao = ctx.vertex_array(prog, [(vbo, '3f 3f', 'in_vert', 'in_normals')])

# blinn phong uniforms

lightPos = Vector3([5.0, 12.0, 0.0])
prog['lightPos'].write(lightPos.tobytes())

lightAmbient = Vector3([0.2, 0.2, 0.2])
prog['lightAmbient'].write(lightAmbient.tobytes())

lightDiffuse = Vector3([2.0, 2.0, 2.0])
prog['lightDiffuse'].write(lightDiffuse.tobytes())

lightSpecular = Vector3([2.0, 2.0, 2.0])
prog['lightSpecular'].write(lightSpecular.tobytes())

materialAmbient = Vector3([1.2, 0.2, 0.2])
prog['materialAmbient'].write(materialAmbient.tobytes())

materialDiffuse = Vector3([0.2, 0.2, 1.2])
prog['materialDiffuse'].write(materialDiffuse.tobytes())

materialSpecular = Vector3([0.5, 2.5, 0.5])
prog['materialSpecular'].write(materialSpecular.tobytes())

shininess = 200.0
prog['shininess'].value = shininess

# ------

ctx.enable(moderngl.DEPTH_TEST)  # enable depth testing for 3D

pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # get mouse movement and process it
    mouse_dx, mouse_dy = pygame.mouse.get_rel()
    camera.process_mouse_movement(mouse_dx, -mouse_dy) # Invert Y-axis

    # get the state of all keyboard buttons
    keys = pygame.key.get_pressed()
    # process keyboard input for camera movement
    camera.process_keyboard_input(keys)

    # update the view matrix each frame
    shaders.update_view_matrix(camera.get_view_matrix())

    # update camera position uniform for correct specular lighting
    prog['viewPos'].write(camera.position.tobytes())

    ctx.clear(0.05, 0.05, 0.05, depth=1.0)  # clear color and depth buffers
    vao.render(moderngl.TRIANGLES)
    pygame.display.flip()