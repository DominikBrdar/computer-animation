import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

def load_texture(filename):
    surface = pygame.image.load(filename)
    data = pygame.image.tostring(surface, "RGB")
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    gluBuild2DMipmaps(GL_TEXTURE_2D, 3, surface.get_width(), surface.get_height(), GL_RGB, GL_UNSIGNED_BYTE, data)
    return texture
