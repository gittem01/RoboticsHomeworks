import numpy as np
from vpython import *
import time
from fontUtil import *
from threading import Lock

mutex = Lock()

scene.width = 1425
scene.height = 700

scene.camera.pos = vector(-3, -5, 0.5)
scene.camera.axis = vector(0, 5, 0)
scene.camera.up = vector(0, 0, 1)

offsets = [vector(0, 0, 3), vector(3, 0, 0), vector(3, 0, 0)]
axises = [vector(0, 0, 1), vector(1, 0, 0), vector(1, 0, 0)]

eulerAngles = [0, 0]

textStart = vector(-5.5, -2, 5)
text = ">"
charInd = 0
partInd = 0
ind = 0
finish = False
advance_width, left_side_bearing = getPoints(text[charInd])

angle1 = 1
angle2 = 1
angle3 = 1

angle4 = 0
angle5 = 0
angle6 = 0

xVecMult = 1.5
lineR = 0.03

p0 = vector(-2, 2, -3)
p1 = p0 + offsets[0]
p2 = p1 + offsets[1]

diff = vector(0, -0.5, 0)

r67 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
r56 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
r45 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
r34 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
r23 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
r12 = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

matrices = [r67, r56, r45, r34, r23, r12]

def calculateMatrices():
    global angle1, angle2, angle3, r67, r56, r45, r34, r23, r12, matrices

    r67 = np.array([[cos(angle6), -sin(angle6), 0, 0],
                    [sin(angle6), cos(angle6), 0, 0],
                    [0, 0, 1, 0.25],
                    [0, 0, 0, 1]])

    r56 = np.array([[cos(angle5), 0, -sin(angle5), -sin(angle5) * 0.5],
                    [sin(angle5), 0, cos(angle5), cos(angle5) * 0.5],
                    [0, -1, 0, 0],
                    [0, 0, 0, 1]])

    r45 = np.array([[cos(angle4), 0, sin(angle4), 0],
                    [sin(angle4), 0, -cos(angle4), 0],
                    [0, 1, 0, 0.75],
                    [0, 0, 0, 1]])

    r34 = np.array([[-sin(angle3), 0, cos(angle3), cos(angle3) * offsets[2].x],
                    [cos(angle3), 0, sin(angle3), sin(angle3) * offsets[2].x],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1]])
    
    r23 = np.array([[cos(angle2), -sin(angle2), 0, cos(angle2) * offsets[1].x],
                    [sin(angle2), cos(angle2), 0, sin(angle2) * offsets[1].x],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])
    r12 = np.array([[cos(angle1), -sin(angle1), 0, 0],
                    [sin(angle1), cos(angle1), 0, 0],
                    [0, 0, 1, offsets[0].z],
                    [0, 0, 0, 1]])
    r12t = np.array([[1, 0, 0, 0], [0, 0, -1, 0], [0, 1, 0, 0], [0, 0, 0, 1]])
    r12 = np.dot(r12, r12t)

    matrices = [r67, r56, r45, r34, r23, r12]

def itojMatrix(start, end):
    global matrices
    matrix = np.eye(4)
    for i in range(end, start, -1):
        matrix = np.dot(matrix, matrices[i])

    return matrix

def getPosFromBase(p, n):
    global matrices
    p = [p.x, p.y, p.z, 1]
    for i in range(6 - n, 6):
        p = np.dot(matrices[i], [p[0], p[1], p[2], 1])

    return vector(p[0], p[1], p[2]) + p0

def angle1Func(evt):
    eulerAngles[0] = evt.value
def angle2Func(evt):
    eulerAngles[1] = evt.value


def calculateReverseAngles(pos):
    ang1 = atan2(pos.y, pos.x)

    try:
        f1 = acos((offsets[2].x ** 2 - (offsets[1].x ** 2 + pos.x ** 2 + pos.y ** 2 + (pos.z - offsets[0].z) ** 2)) / 
                -(2 * offsets[1].x * ((pos.x ** 2 + pos.y ** 2 + (pos.z - offsets[0].z) ** 2) ** 0.5)))
        f2 = atan2(pos.z - offsets[0].z, (pos.x ** 2 + pos.y ** 2) ** 0.5)
        ang2 = f2 - f1
        
        f3 = acos((pos.x ** 2 + pos.y ** 2 + (pos.z - offsets[0].z) ** 2 - offsets[1].x ** 2 - offsets[2].x ** 2) /
                -(2 * offsets[1].x * offsets[2].x))
        ang3 = pi - f3
    except:
        ang1 = 0
        ang2 = 0
        ang3 = 0
        return ang1, ang2, ang3

    return ang1, ang2, ang3

def calculateEndAngles(requiredFrame):
    r17 = requiredFrame
    r14 = itojMatrix(2, 5)[:3, :3]

    r47 = np.dot(np.linalg.inv(r14), r17)

    r47[2, 2] = min(1.0, max(-1.0, r47[2, 2]))
    a2 = acos(r47[2, 2])
    sinReal = sin(a2)

    a1Cos = r47[0, 2] / -sinReal
    a1Sin = r47[1, 2] / -sinReal

    a3Cos = r47[2, 0] / sinReal
    a3Sin = r47[2, 1] / -sinReal

    a1 = atan2(a1Sin, a1Cos)
    a3 = atan2(a3Sin, a3Cos)

    return a1, a2, a3

def calculateJacobian():
    d0n = itojMatrix(2, 5)[:3, 3]

    firstColumn = np.cross([0, 0, 1], d0n)
    secondColumn = np.cross(itojMatrix(4, 5)[:3, 2], d0n - itojMatrix(4, 5)[:3, 3])
    thirdColumn = np.cross(itojMatrix(3, 5)[:3, 2], d0n - itojMatrix(3, 5)[:3, 3])

    jacobian = np.array([firstColumn, secondColumn, thirdColumn]).transpose()
    
    return jacobian

slider1 = slider(min=-pi, max=pi, length=400, bind=angle1Func, value=0)
slider2 = slider(min=-pi, max=pi, length=400, bind=angle2Func, value=0)

# draw cylinder
c1 = cylinder(pos=p0, axis=vector(0, 0, 1), radius=0.3, color=color.white)
c2 = cylinder(pos=p1 + diff, axis=vector(0, 1, 0), radius=0.3, color=color.green)
c3 = cylinder(pos=p2 + diff, axis=vector(0, 1, 0), radius=0.3, color=color.green)
c4 = cylinder(pos=p0, axis=vector(0, 1, 0), radius=0.15, color=color.red)
c5 = cylinder(pos=p0, axis=vector(0, 1, 0), radius=0.15, color=color.red)
c6 = cylinder(pos=p0, axis=vector(0, 1, 0), radius=0.15, color=color.red)

trailSphere = sphere(pos=p0, radius=0.0, color=color.yellow, make_trail=False,
                     interval=10, retain=99999999999999, trail_radius=0.01, trail_color=color.white)

def winInputFunc(evt):
    global text, textStart, trailSphere, charInd, partInd, ind, finish, advance_width, left_side_bearing
    mutex.acquire()
    text = evt.text
    advance_width, left_side_bearing = getPoints(text[0])
    textStart = vector(-5.5, -2, 5)
    charInd = 0
    partInd = 0
    ind = 0
    finish = False
    trailSphere.clear_trail()
    trailSphere.make_trail = False
    mutex.release()
    
winInput = winput(bind=winInputFunc, type="string", width=400)

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

#3
line14 = curve(pos=[p0, p0], radius=lineR * 0.5, color=color.cyan)
line15 = curve(pos=[p0, p0], radius=lineR * 0.5, color=color.cyan)
line16 = curve(pos=[p0, p0], radius=lineR * 0.5, color=color.cyan)

#4
lineXB = curve(pos=[p0, p0], radius=lineR, color=color.red)
lineYB = curve(pos=[p0, p0], radius=lineR, color=color.green)
lineZB = curve(pos=[p0, p0], radius=lineR, color=color.blue)

lineX = curve(pos=[p0, p0], radius=lineR, color=color.red)
lineY = curve(pos=[p0, p0], radius=lineR, color=color.green)
lineZ = curve(pos=[p0, p0], radius=lineR, color=color.blue)

calculateMatrices()

deltatime = 0
currentTime = time.time()
lastTime = time.time()
fontMult = 0.001
robotSpeed = 2

while 1:
    currentTime = time.time()
    deltatime = currentTime - lastTime
    lastTime = currentTime

    mutex.acquire()
    requestedPosition = np.array([fullPoints[partInd][ind][0] * fontMult + p0.x + textStart.x,
                                  p0.y + textStart.y,
                                  fullPoints[partInd][ind][1] * fontMult + p0.z + textStart.z])

    currentPositon = getPosFromBase(vector(0, 0, 0.25), 6)
    posdiff = (requestedPosition - np.array([currentPositon.x, currentPositon.y, currentPositon.z]))

    posdiffLen = (posdiff[0] ** 2 + posdiff[1] ** 2 + posdiff[2] ** 2) ** 0.5
    if posdiffLen < 0.005:
        trailSphere.make_trail = True
        ind = ind + 1
        if ind == len(fullPoints[partInd]):
            finish = True
            ind = 0
        if finish and ind == 2:
            finish = False
            partInd += 1
            if partInd == len(fullPoints):
                partInd = 0
                charInd += 1
                if charInd == len(text):
                    charInd = 0
                    text = "."
                    textStart = vector(0, 0, 0)
                textStart.x += advance_width * fontMult
                advance_width, left_side_bearing = getPoints(text[charInd])
                textStart.x += left_side_bearing * fontMult
                if text[charInd] == " ":
                    leadingSpaces = numLeadingSpaces(text, charInd)
                    textStart.x += advance_width * fontMult * leadingSpaces
                    charInd += leadingSpaces
                    advance_width, left_side_bearing = getPoints(text[charInd])
                    textStart.x += left_side_bearing * fontMult

            ind = 0
            trailSphere.make_trail = False

    mutex.release()

    jacobian = calculateJacobian()
    jacobianInv = np.linalg.inv(jacobian)

    robotSpeed = max(2, posdiffLen * 2)
    posdiff = robotSpeed * posdiff / posdiffLen
    angles = np.dot(jacobianInv, posdiff) * 0.001

    angle1 += angles[0]
    angle2 += angles[1]
    angle3 += angles[2]

    calculateMatrices()

    lookPos = p0
    zVec = vector(0, -1, 0)
    zVec = rotate(zVec, eulerAngles[0], vector(1, 0, 0))
    zVec = rotate(zVec, eulerAngles[1], vector(0, 0, 1))
    zVec = norm(zVec)
    xVec = cross(vector(0, 0, 1), zVec)
    xVec = norm(xVec)
    yVec = cross(zVec, xVec)
    yVec = norm(yVec)
    angle4, angle5, angle6 = calculateEndAngles(np.array([[xVec.x, yVec.x, zVec.x], [xVec.y, yVec.y, zVec.y], [xVec.z, yVec.z, zVec.z]]))

    calculateMatrices()

    trailSphere.pos = getPosFromBase(vector(0, 0, 0.25), 6)

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

    axp0 = getPosFromBase(vector(0, 1, -3), 3)
    axp1 = getPosFromBase(vector(0, -1, -3), 3)

    line8.modify(0, pos=axp0)
    line8.modify(1, pos=axp1)

    c3.pos = getPosFromBase(vector(0, 0, 0.5), 2)
    c3.axis = (axp1 - axp0).norm()

    line10.modify(0, pos=getPosFromBase(vector(0, 1, -3), 3))
    line10.modify(1, pos=getPosFromBase(vector(0, 1, xVecMult - 3), 3))

    line11.modify(0, pos=getPosFromBase(vector(0, -1, -3), 3))
    line11.modify(1, pos=getPosFromBase(vector(0, -1, xVecMult - 3), 3))

    line12.modify(0, pos=getPosFromBase(vector(0, 1, xVecMult - 3), 3))
    line12.modify(1, pos=getPosFromBase(vector(0, -1, xVecMult - 3), 3))

    line13.modify(0, pos=getPosFromBase(vector(0, 0, xVecMult - 3), 3))
    line13.modify(1, pos=getPosFromBase(vector(0, 0, 0), 3))

    axp0 = getPosFromBase(vector(0, 1, 0), 4)
    axp1 = getPosFromBase(vector(0, -1, 0), 4)
    c4.pos = getPosFromBase(vector(0, 0, 0.25), 3)
    c4.axis = (axp1 - axp0).norm() * 0.5

    line14.modify(0, pos=getPosFromBase(vector(0, -0.5, 0), 4))
    line14.modify(1, pos=getPosFromBase(vector(0, 0, 0), 4))

    axp0 = getPosFromBase(vector(0, 1, 0), 5)
    axp1 = getPosFromBase(vector(0, -1, 0), 5)
    c5.pos = getPosFromBase(vector(0, 0, -0.25), 4)
    c5.axis = (axp1 - axp0).norm() * 0.5

    line15.modify(0, pos=getPosFromBase(vector(0, 0, -0.5), 5))
    line15.modify(1, pos=getPosFromBase(vector(0, 0, 0), 5))

    axp0 = getPosFromBase(vector(0, 0, -1), 6)
    axp1 = getPosFromBase(vector(0, 0, 1), 6)
    c6.pos = getPosFromBase(vector(0, 0, -0.5), 6)
    c6.axis = (axp1 - axp0).norm() * 0.5

    line16.modify(0, pos=getPosFromBase(vector(0, 0, 0.25), 6))
    line16.modify(1, pos=getPosFromBase(vector(0, 0, 0), 6))

    axx = getPosFromBase(vector(1, 0, 0.25), 6)
    axy = getPosFromBase(vector(0, 1, 0.25), 6)
    axz = getPosFromBase(vector(0, 0, 1.25), 6)
    
    lineXB.modify(0, pos=p0 + vector(0, 0, 1))
    lineXB.modify(1, pos=p0 + vector(0, 0, 1) + xVec)

    lineYB.modify(0, pos=p0 + vector(0, 0, 1))
    lineYB.modify(1, pos=p0 + vector(0, 0, 1) + yVec)

    lineZB.modify(0, pos=p0 + vector(0, 0, 1))
    lineZB.modify(1, pos=p0 + vector(0, 0, 1) + zVec)

    lineX.modify(0, pos=getPosFromBase(vector(0, 0, 0.25), 6))
    lineX.modify(1, pos=axx)

    lineY.modify(0, pos=getPosFromBase(vector(0, 0, 0.25), 6))
    lineY.modify(1, pos=axy)

    lineZ.modify(0, pos=getPosFromBase(vector(0, 0, 0.25), 6))
    lineZ.modify(1, pos=axz)

    rate(1000)
