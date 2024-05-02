import numpy as np
from vpython import *

scene.width = 1366
scene.height = 700

scene.camera.pos = vector(0, -5, 0)
scene.camera.axis = vector(0, 5, 0)
scene.camera.up = vector(0, 0, 1)

offsets = [vector(0, 0, 3), vector(3, 0, 0), vector(3, 0, 0)]
axises = [vector(0, 0, 1), vector(1, 0, 0), vector(1, 0, 0)]

angle1 = 0
angle2 = 0
angle3 = 0

xVecMult = 1.5
lineR = 0.03

p0 = vector(-2, 2, -3)
p1 = p0 + offsets[0]
p2 = p1 + offsets[1]

diff = vector(0, -0.5, 0)

r34 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
r23 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
r12 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

matrices = [r34, r23, r12]

def calculateMatrices():
    global angle1, angle2, angle3, r34, r23, r12, matrices
    r34 = np.array([[np.cos(angle3), -np.sin(angle3), 0, np.cos(angle3) * offsets[2].x],
                    [np.sin(angle3), np.cos(angle3), 0, np.sin(angle3) * offsets[2].x],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    
    r23 = np.array([[np.cos(angle2), -np.sin(angle2), 0, np.cos(angle2) * offsets[1].x],
                    [np.sin(angle2), np.cos(angle2), 0, np.sin(angle2) * offsets[1].x],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    r12 = np.array([[np.cos(angle1), -np.sin(angle1), 0, 0],
                    [np.sin(angle1), np.cos(angle1), 0, 0],
                    [0, 0, 1, offsets[0].z],
                    [0, 0, 0, 1]])
    r12t = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    r12 = np.dot(r12, r12t)

    matrices = [r34, r23, r12]

def getPosFromBase(p, n):
    global matrices
    p = [p.x, p.y, p.z, 1]
    for i in range(3 - n, 3):
        p = np.dot(matrices[i], [p[0], p[1], p[2], 1])

    return vector(p[0], p[1], p[2]) + p0

def angle1Func(evt):
    global angle1
    angle1 = evt.value
def angle2Func(evt):
    global angle2
    angle2 = evt.value
def angle3Func(evt):
    global angle3
    angle3 = evt.value

slider1 = slider(min=-pi, max=pi, length=400, bind=angle1Func, value=0)
slider2 = slider(min=-pi, max=pi, length=400, bind=angle2Func, value=0)
slider3 = slider(min=-pi, max=pi, length=400, bind=angle3Func, value=0)

# draw cylinder
c1 = cylinder(pos=p0, axis=vector(0, 0, 1), radius=0.3, color=color.blue)
c2 = cylinder(pos=p1 + diff, axis=vector(0, 1, 0), radius=0.3, color=color.green)
c3 = cylinder(pos=p2 + diff, axis=vector(0, 1, 0), radius=0.3, color=color.green)

line1 = curve(pos=[p0, p1], radius=lineR)

#1
line2 = curve(pos=[p0, p0], radius=lineR)

line4 = curve(pos=[p0, p0], radius=lineR)
line5 = curve(pos=[p0, p0], radius=lineR)

line6 = curve(pos=[p0, p0], radius=lineR)

line7 = curve(pos=[p0, p0], radius=lineR)

#2
line8 = curve(pos=[p0, p0], radius=lineR)

line10 = curve(pos=[p0, p0], radius=lineR)
line11 = curve(pos=[p0, p0], radius=lineR)

line12 = curve(pos=[p0, p0], radius=lineR)

line13 = curve(pos=[p0, p0], radius=lineR)

while 1:
    calculateMatrices()

    axp0 = getPosFromBase(vector(-3, 0, 1), 2)
    axp1 = getPosFromBase(vector(-3, 0, -1), 2)
    line2.modify(0, pos=axp0)
    line2.modify(1, pos=axp1)

    c2.pos = getPosFromBase(vector(0, 0, 0.5), 1)
    c2.axis = (axp1 - axp0).norm()

    line4.modify(0, pos=getPosFromBase(vector(-3, 0, 1), 2))
    line4.modify(1, pos=getPosFromBase(vector(xVecMult - 3, 0, 1), 2))

    line5.modify(0, pos=getPosFromBase(vector(-3, 0, -1), 2))
    line5.modify(1, pos=getPosFromBase(vector(xVecMult - 3, 0, -1), 2))

    line6.modify(0, pos=getPosFromBase(vector(xVecMult - 3, 0, 1), 2))
    line6.modify(1, pos=getPosFromBase(vector(xVecMult - 3, 0, -1), 2))

    line7.modify(0, pos=getPosFromBase(vector(-xVecMult, 0, 0), 2))
    line7.modify(1, pos=getPosFromBase(vector(0, 0, 0), 2))

    axp0 = getPosFromBase(vector(-3, 0, 1), 3)
    axp1 = getPosFromBase(vector(-3, 0, -1), 3)
    line8.modify(0, pos=axp0)
    line8.modify(1, pos=axp1)

    c3.pos = getPosFromBase(vector(0, 0, 0.5), 2)
    c3.axis = (axp1 - axp0).norm()

    line10.modify(0, pos=getPosFromBase(vector(-3, 0, 1), 3))
    line10.modify(1, pos=getPosFromBase(vector(xVecMult - 3, 0, 1), 3))

    line11.modify(0, pos=getPosFromBase(vector(-3, 0, -1), 3))
    line11.modify(1, pos=getPosFromBase(vector(xVecMult - 3, 0, -1), 3))

    line12.modify(0, pos=getPosFromBase(vector(xVecMult - 3, 0, 1), 3))
    line12.modify(1, pos=getPosFromBase(vector(xVecMult - 3, 0, -1), 3))

    line13.modify(0, pos=getPosFromBase(vector(xVecMult - 3, 0, 0), 3))
    line13.modify(1, pos=getPosFromBase(vector(0, 0, 0), 3))

    rate(1000)