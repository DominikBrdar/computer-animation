import math
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame import Vector3

class Izvor:
    pos: Vector3
    c_r: float
    c_g: float
    c_b: float
    size: float

    def __init__(self, vrh, c_r, c_g, c_b, size, tip='tocka'):
        self.pos = vrh
        self.c_r = c_r
        self.c_g = c_g
        self.c_b = c_b
        self.size = size
        self.tip = tip

    def get_spawning_point(self):
        if self.tip == 'tocka':
            return self.pos
        if self.tip == 'poligon':
            return Vector3(random.uniform(-1, 1) * 20, 25, 0)


class Cestica:
    pos: Vector3
    r: float
    g: float
    b: float
    v: float
    t: int
    direction: Vector3
    rotVec: Vector3
    angle: float
    size: float

    def __init__(self, direction, v, izvor: Izvor):
        self.izvor = izvor
        self.pos = izvor.get_spawning_point()
        self.r = izvor.c_r
        self.g = izvor.c_g
        self.b = izvor.c_b
        self.v = v
        self.t = random.randint(60, 80)
        self.direction = direction
        self.rotVec = Vector3(0, 0, 0)
        self.angle = 0
        self.size = random.uniform(0.6, 2.4) * izvor.size

    def nacrtaj_cesticu(self):
        glColor3f(self.r, self.g, self.b)
        glTranslatef(self.pos.x, self.pos.y, self.pos.z)
        glRotatef(self.angle, self.rotVec.x, self.rotVec.y, self.rotVec.z)

        glBegin(GL_QUADS)
        glTexCoord2d(0.0, 0.0)
        glVertex3f(-self.size, -self.size, 0.0)
        glTexCoord2d(1.0, 0.0)
        glVertex3f(self.size, -self.size, 0.0)
        glTexCoord2d(1.0, 1.0)
        glVertex3f(self.size, self.size, 0.0)
        glTexCoord2d(0.0, 1.0)
        glVertex3f(-self.size, self.size, 0.0)
        glEnd()

        glRotatef(-self.angle, self.rotVec.x, self.rotVec.y, self.rotVec.z)
        glTranslatef(-self.pos.x, -self.pos.y, -self.pos.z)

    def promijeni_poziciju_cestice(self):
        self.pos += self.v * self.direction

    def promijeni_boju_i_velicinu(self):
        self.r -= 0.01
        if self.t < 20:
            self.g -= 0.01
        else:
            self.g += 0.01
        self.b -= 0.01
        if self.izvor.tip == "tocka":
            self.size += 0.03

    def postavi_vekor_rotacije(self, rotVec):
        self.rotVec = rotVec

    def postavi_kut_rotacije(self, angle):
        self.angle = math.radians(angle)
