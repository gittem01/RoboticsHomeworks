from vpython import *
import numpy as np
import serial
import math
from scipy.spatial.transform import Rotation as R

s = serial.Serial("/dev/cu.usbserial-140")
s.flushInput()

calibrationConstants = [0, 0, 0]

angles = [0, 0, 0]

class GyroData:
    def __init__(self, lx, ly, lz, ax, ay, az):
        self.lx = lx
        self.ly = ly
        self.lz = lz
        self.ax = ax
        self.ay = ay
        self.az = az

gData = GyroData(0, 0, 0, 0, 0, 0)

def loadData():
    try:
        data = s.readline().decode("utf-8")
        data = data.split(" ")
        
        gData.lx = float(data[0])
        gData.ly = float(data[1])
        gData.lz = float(data[2])
        gData.ax = float(data[3])
        gData.ay = float(data[4])
        gData.az = float(data[5])
    except:
        return

scene.width = 1366
scene.height = 768

arr0 = arrow(pos=vector(0, 0, 0), axis=vector(1, 0, 0), color=color.blue, round=True, shaftwidth=0.05)
arr1 = arrow(pos=vector(0, 0, 0), axis=vector(0, 1, 0), color=color.green, round=True, shaftwidth=0.05)
arr2 = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 1), color=color.red, round=True, shaftwidth=0.05)

def generateRotationMatrix(type, angle):
    rotMatrix = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    if type == 0:
        rotMatrix = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
    elif type == 1:
        rotMatrix = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
    elif type == 2:
        rotMatrix = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    
    return rotMatrix

while 1:
    loadData()

    r = R.from_rotvec([0, 0, -gData.az])
    newX = r.apply([1, 0, 0])
    newY = r.apply([0, 1, 0])

    r = R.from_rotvec(gData.ay * newY)
    newX = r.apply(newX)
    newZ = r.apply([0, 0, 1])

    r = R.from_rotvec(-gData.ax * newX)
    newY = r.apply(newY)
    newZ = r.apply(newZ)

    r = R.from_rotvec([0, 0, math.pi * 0.5])
    newX = r.apply(newX)
    newY = r.apply(newY)
    newZ = r.apply(newZ)

    rotationMatrix = generateRotationMatrix(0, -gData.ax)
    rotationMatrix = np.dot(rotationMatrix, generateRotationMatrix(1, gData.ay))
    rotationMatrix = np.dot(rotationMatrix, generateRotationMatrix(2, -gData.az))

    arr0.axis = vector(newX[0], newX[1], newX[2])
    arr1.axis = vector(newY[0], newY[1], newY[2])
    arr2.axis = vector(newZ[0], newZ[1], newZ[2])

    # res = np.dot(rotationMatrix, [1, 0, 0])
    # arr0.axis = vector(res[0], res[1], res[2])

    # res = np.dot(rotationMatrix, [0, 1, 0])
    # arr1.axis = vector(res[0], res[1], res[2])

    # res = np.dot(rotationMatrix, [0, 0, 1])
    # arr2.axis = vector(res[0], res[1], res[2])

    rate(1000)