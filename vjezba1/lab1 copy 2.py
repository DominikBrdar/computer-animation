from lab1pom import *
import pygame
from pygame import display
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import numpy.linalg as LA

v, f = loadModel("./kocka.obj")
cp = BSplineLoadControlPoints("./B-spline.txt")   
step = 0.01
p = BSpline(cp, step)
der = smjer(cp, step)
r = orijentacija(der)

pygame.init()
display = (1000, 800)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 5000)
glTranslatef(-3, -3, -70)


i = 0

def probarotacije():
    r = []
    q = Quaternion.from_axis_rotation([0.5, 0.5, 0], 0)
    for i in range(360):
        q = Quaternion.from_axis_rotation([0.5, 0.5, 0], 10) * q
        r.append([q.axis, q.angle])
    return r
r = probarotacije()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    i = (i + 1) % 360

    # nacrtaj model
    print(r[i][1], r[i][0][0], r[i][0][1], r[i][0][2])
    
    glPushMatrix()
    glScale(3, 3, 4)
    #glTranslate(p[i][0], p[i][1], p[i][2])
    glRotate(r[i][1], r[i][0][0], r[i][0][1], r[i][0][2])
    
    glScale(2, 2, 2)
    glBegin(GL_TRIANGLES)
    glColor([0.0, 1.0, 0.0])
    for F in f:
        glVertex3fv(v[F[0]])
        glVertex3fv(v[F[1]])
        glVertex3fv(v[F[2]])
    glEnd()
    glPopMatrix()

    # nacrtaj putanju
    glBegin(GL_LINES)
    glColor3fv([0.0, 0.5, 0.6])
    for j in range(1, len(p)): 
        glVertex3fv(p[j-1])
        glVertex3fv(p[j])

    # nacrtaj tangentu
    glColor3fv([1, 0, 0])
    glVertex3fv(p[i])
    glVertex3fv(p[i] + der[i])
    glEnd()

    pygame.time.wait(50)
    pygame.display.flip()
