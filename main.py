import moderngl
import glfw

from camera import Camera
from object import Object
from program import Program
from mathlib import Vector3

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
ASPECT_RATIO = WINDOW_WIDTH / WINDOW_HEIGHT

glfw.init()
window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "PyRender", None, None)
glfw.make_context_current(window)

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

glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

last_x, last_y = WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2
first_mouse = True

while glfw.window_should_close(window) == False:
    glfw.poll_events()

    xpos, ypos = glfw.get_cursor_pos(window)
    if first_mouse:
        last_x = xpos
        last_y = ypos
        first_mouse = False

    xoffset = xpos - last_x
    yoffset = last_y - ypos  # reversed since Y-coordinates go from bottom to top
    last_x = xpos
    last_y = ypos
    camera.process_mouse_movement(xoffset, yoffset)

    # get the state of all keyboard buttons
    camera.process_keyboard_input(window)

    # update the view matrix each frame
    shaders.update_view_matrix(camera.get_view_matrix())

    # update camera position uniform for correct specular lighting
    prog['viewPos'].write(camera.position.tobytes())
    ctx.clear(0.05, 0.05, 0.05, depth=1.0)  # clear color and depth buffers
    vao.render(moderngl.TRIANGLES)
    glfw.swap_buffers(window)