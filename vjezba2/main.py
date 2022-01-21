from typing import List

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from pygame import Vector3

from load_texture import *
from cestica import *
from krivulja import *

class SustavCestica:
    def __init__(self, izvor, ociste, krivulja=None):
        self.current_time = 0
        self.past_time = 0
        self.krivulja = krivulja
        self.izvor = izvor
        self.cestice: List[Cestica] = []
        self.ociste = ociste
        self.iteration = 0

    def update(self):
        self.current_time = glutGet(GLUT_ELAPSED_TIME)
        if self.current_time - self.past_time > 20:
            self.iteration += 1
            if self.krivulja: # pomicanje po krivulji
                self.izvor.pos = self.krivulja.get_next_point()
            self.stvori_cestice()
            self.osvjezi_cestice()
            self.past_time = self.current_time
        my_display()

    def stvori_cestice(self):
        n = random.randint(1, 3)
        for j in range(n):
            if self.krivulja:
                x = random.uniform(-1, 1)
                y = random.uniform(-1, 1)
                z = random.uniform(-1, 1)
                v = random.uniform(0.2, 0.6)
            else:
                x = 0
                y = -1
                z = 0
                v = random.uniform(0.4, 0.6)
            self.cestice.append(Cestica(Vector3(x, y, z), v, self.izvor))
            
    def osvjezi_cestice(self):
        for cestica in self.cestice:
            os, kut = self.izracunaj_podatke_o_cestici(cestica)
            cestica.postavi_kut_rotacije(kut)
            cestica.postavi_vekor_rotacije(os)
            cestica.promijeni_poziciju_cestice()
            cestica.t -= 1
            cestica.promijeni_boju_i_velicinu()
            self.zavrsi_zivot_cestice(cestica)

    def izracunaj_podatke_o_cestici(self, cestica):
        s = Vector3(0, 0, 1)
        e = (cestica.pos - self.ociste).normalize()
        os = s.cross(e)
        kut = math.acos(s.dot(e))
        return os, kut

    def zavrsi_zivot_cestice(self, cestica):
        if cestica.t <= 0:
            self.cestice.remove(cestica)

    def nacrtaj_cestice(self):
        for cestica in self.cestice:
            cestica.nacrtaj_cesticu()


WIDTH = 800
HEIGHT = 600

def my_display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(ociste.x, ociste.y, -ociste.z)
    sustav_cestica.nacrtaj_cestice()
    sustav_cestica2.nacrtaj_cestice()
    glutSwapBuffers()

def my_reshape(w, h):
    global WIDTH, HEIGHT
    WIDTH = w
    HEIGHT = h
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, WIDTH / HEIGHT, 0.1, 150)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(1)
    glColor3f(0, 0, 0)

def my_keyboard(the_key, mouse_x, mouse_y):
    if krivulja:
        if the_key == b'd': ociste.x -= 0.5
        if the_key == b'a': ociste.x += 0.5
        if the_key == b'w': ociste.y -= 0.5
        if the_key == b's': ociste.y += 0.5
   
    my_display

def update():
    sustav_cestica2.update()
    sustav_cestica.update()

## način rada
krivulja = True
mouse = True

ociste = Vector3(0, 0, 50)
if krivulja:
    izvor1 = Izvor(Vector3(0, 0, 0), 0.3, 0.1, 1, 0.8, tip='tocka') 
    izvor2 = Izvor(Vector3(0, 0, 0), 0.9, 0.5, 0, 0.8, tip='tocka')
    sustav_cestica = SustavCestica(izvor1, ociste, Krivulja('B-spline.txt'))
    sustav_cestica2 = SustavCestica(izvor2, ociste, Krivulja('B-spline1.txt'))
else:
    izvor = Izvor(Vector3(0, 0, 0), 1, 1, 1, 0.8, tip='poligon')
    sustav_cestica = SustavCestica(izvor, ociste)

glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(200, 100)
glutInit()
window = glutCreateWindow("Sustav cestica")
glutDisplayFunc(my_display)
glutReshapeFunc(my_reshape)
glutKeyboardFunc(my_keyboard)
glutIdleFunc(update)

if krivulja:
    texture = load_texture("cestica.bmp")
    #texture = load_texture("explosion.bmp")
else:
    texture = load_texture("snow.bmp")

glBlendFunc(GL_SRC_ALPHA, GL_ONE)
glEnable(GL_BLEND)
glEnable(GL_TEXTURE_2D)
glBindTexture(GL_TEXTURE_2D, texture)

glutMainLoop()
