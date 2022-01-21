from lab1pom import *
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import numpy.linalg as LA

vertex_src = """
# version 320 es

precision mediump float;

layout(location = 0) in vec3 a_position;

void main()
{
    
    gl_Position = vec4(a_position, 1.0);
}
"""
fragment_src = """
# version 320 es

precision mediump float;
out vec4 out_color;
void main()
{
    out_color = vec4(1.0, 0.0, 0.0, 1.0);
}
"""
# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# Configure the OpenGL context.
glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
glfw.window_hint(glfw.SAMPLES, 4)

window = glfw.create_window(1280, 720, "animacija gibanja po krivulji", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# Query the actual framebuffer size so we can set the right viewport later
# -> glViewport(0, 0, framebuffer_size[0], framebuffer_size[1])
framebuffer_size = glfw.get_framebuffer_size(window)

glfw.make_context_current(window)

v, f, = loadModel("./f16.obj")
v = np.array(v, dtype=np.float32)
f = np.array(f, dtype=np.uint32)
cp = BSplineLoadControlPoints("./B-spline.txt")   
step = 0.001
p = BSpline(cp, step)
der = smjer(cp, step)

vao = GLuint(0)
glGenVertexArrays(1, vao)
glBindVertexArray(vao)

VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, v.nbytes, v, GL_STATIC_DRAW)

EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, f.nbytes, f, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

glUseProgram(shader)


i = 0
# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)
    i = i+1
    rv = np.cross(der[i-1], der[i])
    kut = np.rad2deg(np.arccos(np.dot(der[i-1], der[i]) / LA.norm(der[i-1]) / LA.norm(der[i])))

    glDrawElements(GL_TRIANGLES, len(f), GL_UNSIGNED_INT, None)


    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()