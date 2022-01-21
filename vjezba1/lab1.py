from lab1pom import *
import pygame
from pygame import display
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import numpy.linalg as LA

v, f = loadModel("./f16.obj")
cp = BSplineLoadControlPoints("./B-spline.txt")   
step = 0.01
p = BSpline(cp, step)
der = smjer(cp, step)
#r = orijentacija(der)
r = orijentacija3(der)
der2 = drugaderivacija(cp, step)
m = orijentacija2(der, der2)

pygame.init()
display = (1000, 800)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
gluPerspective(45, (display[0]/display[1]), 0.1, 5000)
glTranslatef(-3, -3, -70)

i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    i = (i + 1) % (len(p) -1)

    # nacrtaj model
    glPushMatrix()
    #glMatrixMode(GL_MODELVIEW)
    
    # rotacija preko matrice
    for k in range(len(v)):
        v[k] = np.array(v[k] * m[i])
        v[k] = list(v[k][0])

    glTranslate(p[i][0], p[i][1], p[i][2])
    #for k in range(i): 
    #glRotate(r[i][1], r[i][0][0], r[i][0][1], r[i][0][2])

    glScale(8, 8, 8)
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
    glVertex3fv(p[i] + der[i] * 4)
    glEnd()

    pygame.time.wait(10)
    pygame.display.flip()
