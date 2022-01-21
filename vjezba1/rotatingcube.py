import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from pyrr.quaternion import conjugate
from lab1pom import *
import time

vertex_src = """
# version 300 es
precision mediump float;
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
uniform mat4 rotation;
out vec3 v_color;
void main()
{
    gl_Position = rotation * vec4(a_position, 1.0);
    v_color = a_color;
}
"""

fragment_src = """
# version 300 es
precision mediump float;
in vec3 v_color;
out vec4 out_color;
void main()
{
    out_color = vec4(v_color, 1.0);
}
"""

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

# initializing glfw library
if not glfw.init():
    raise Exception("glfw can not be initialized!")

# creating the window
window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

# check if window was created
if not window:
    glfw.terminate()
    raise Exception("glfw window can not be created!")

# set window's position
glfw.set_window_pos(window, 400, 200)

# set the callback function for window resize
glfw.set_window_size_callback(window, window_resize)

# make the context current
glfw.make_context_current(window)

vertices = [-0.5, -0.5, 0.5, 
             0.5, -0.5, 0.5,
             0.5,  0.5, 0.5,
            -0.5,  0.5, 0.5,

            -0.5, -0.5, -0.5,
             0.5, -0.5, -0.5,
             0.5,  0.5, -0.5,
            -0.5,  0.5, -0.5,]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           4, 5, 1, 1, 0, 4,
           6, 7, 3, 3, 2, 6,
           5, 6, 2, 2, 1, 5,
           7, 4, 0, 0, 3, 7]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Element Buffer Object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

glUseProgram(shader)
glEnable(GL_DEPTH_TEST)

rotation_loc = glGetUniformLocation(shader, "rotation")
def orijentacija(der):
    r = []
    q = Quaternion.from_axis_rotation([0, 1, 0], 0)
    for i in range(1, len(der)):
        rv = np.cross(der[i-1], der[i])
        angle = np.rad2deg(np.arccos(np.dot(der[i], der[i-1])/(np.linalg.norm(der[i]) * np.linalg.norm(der[i-1]))))
        q = Quaternion.from_axis_rotation(rv, angle) 
        r.append(q)
    return r

v, f = loadModel("./kocka.obj")
cp = BSplineLoadControlPoints("./B-spline.txt")   
step = 0.01
p = BSpline(cp, step)
der = smjer(cp, step)
r = orijentacija(der)

rot_q = pyrr.Matrix44.from_quaternion(r[0])
der2 = drugaderivacija(cp, step)
m = orijentacija2(der, der2)
# the main application loop
i = 0
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    rot_q = rot_q * r[i]
    i = (i + 1) % (len(der) -1)
    glUniformMatrix4fv(rotation_loc, 1, GL_FALSE, rot_q)

    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)
    time.sleep(0.3)

# terminate glfw, free up allocated resources
glfw.terminate()