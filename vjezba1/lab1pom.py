import numpy as np
from pyrr import Quaternion

def loadModel(path):
    wf = open(path)
    v, f = [], [] # v - vertices, f - faces
    for l in wf: # load poligons
        l = l.strip().split()
        if len(l) == 0: continue
        if l[0] == 'v': 
            v.append([float(l[1]), float(l[2]), float(l[3])])
        if l[0] == 'f':
            f.append([int(l[1]) -1, int(l[2]) -1, int(l[3]) -1])
    return v, f

def BSplineLoadControlPoints(path):
    file = open(path)
    cp = []
    for line in file:
        line = line.strip().split()
        if len(line) == 0: continue
        cp.append([float(line[0]), float(line[1]), float(line[2])])
    return cp

def BSpline(cp, step):
    B = np.matrix([[-1, 3, -3, 1], 
                    [3, -6, 3, 0], 
                    [-3, 0, 3, 0], 
                    [1, 4, 1, 0]], dtype="float")
    p = []
    for s in range(1, len(cp) - 3):
        R = np.matrix([[cp[s-1][0], cp[s-1][1], cp[s-1][2], 1],
            [cp[s][0], cp[s][1], cp[s][2], 1],
            [cp[s+1][0], cp[s+1][1], cp[s+1][2], 1],
            [cp[s+2][0], cp[s+2][1], cp[s+2][2], 1]], dtype="float")
        t = 0
        while t <= 1:
            t = t + step
            T = np.matrix([[t**3, t**2, t, 1]], dtype="float")
            p.append(np.array(T * 1/6 * B * R)[0][:3])
    return p

def smjer(cp, step):
    B = np.matrix([[-1, 3, -3, 1], 
                    [2, -4, 2, 0], 
                    [-1, 0, 1, 0]], dtype="float")
    der = []
    for s in range(1, len(cp) - 3):
        R = np.matrix([[cp[s-1][0], cp[s-1][1], cp[s-1][2], 1],
            [cp[s][0], cp[s][1], cp[s][2], 1],
            [cp[s+1][0], cp[s+1][1], cp[s+1][2], 1],
            [cp[s+2][0], cp[s+2][1], cp[s+2][2], 1]], dtype="float")
        t = 0
        while t <= 1:
            t = t + step
            T = np.matrix([[t**2, t, 1]], dtype="float")
            der.append(np.array(T * 1/2 * B * R)[0][:3])
    return der

def orijentacija(der):
    r = []
    #q = Quaternion.from_axis_rotation([0, 1, 0], 0)
    for i in range(1, len(der)):
        rv = np.cross(der[i-1], der[i])
        angle = np.rad2deg(np.arccos(np.dot(der[i], der[i-1])/(np.linalg.norm(der[i]) * np.linalg.norm(der[i-1]))))
        #q = Quaternion.from_axis_rotation(rv, angle) * q
        #r.append([q.axis, q.angle])
        r.append([rv, angle])
    return r

def orijentacija3(der):
    r = []
    q = Quaternion.from_axis_rotation([0, 1, 0], 0)
    for i in range(1, len(der)):
        rv = np.cross(der[0], der[i])
        angle = np.rad2deg(np.arccos(np.dot(der[i], der[0])/(np.linalg.norm(der[i]) * np.linalg.norm(der[i-1]))))
        r.append([rv, angle])
    return r

def drugaderivacija(cp, step):
    B = np.matrix([[-1, 3, -3, 1], 
                    [3, -6, 3, 0], 
                    [-3, 0, 3, 0], 
                    [1, 4, 1, 0]], dtype="float")
    der2 = []
    for s in range(1, len(cp) - 3):
        R = np.matrix([[cp[s-1][0], cp[s-1][1], cp[s-1][2], 1],
            [cp[s][0], cp[s][1], cp[s][2], 1],
            [cp[s+1][0], cp[s+1][1], cp[s+1][2], 1],
            [cp[s+2][0], cp[s+2][1], cp[s+2][2], 1]], dtype="float")
        t = 0
        while t <= 1:
            t = t + step
            T = np.matrix([[6*t, 2, 0, 0]], dtype="float")
            der2.append(np.array(T * 1/6 * B * R)[0][:3])
    return der2

def orijentacija2(der, der2):
    m = []
    for i in range(len(der)):
        der[i] = der[i] / np.linalg.norm(der[i])
        der2[i] = der2[i] / np.linalg.norm(der2[i])
        u = np.cross(der[i], der2[i])
        #u = u / np.linalg.norm(u)
        m.append(np.linalg.inv(np.array([der[i], u, np.cross(der[i], u)], dtype="float").transpose()))
        
    return m
