import sys
import cv2
import os
from sys import platform
import argparse
import math

from findPose import findPose
from savedFrames import savedFrames

def comparePoseLimbVectors(frames, threshold):
    c = 0
    score = 0
    for f in frames:
        # get the angles of each of the limbs relative to the neck
        personOne = getLimbs(f[0])
        # get the angles of each of the limbs relative to the neck
        personTwo = getLimbs(f[1])

        # compare points, calculate score
        # everywhere that the distances between points is within threshold
        # add points
        dists = []
        for i in range(len(personOne)):
            if personOne[i] != 404 and personTwo[i] != 404 :
                dist = abs(personOne[i] - personTwo[i])
                if dist > math.pi:
                    dist -= math.pi
                dists.append(dist)
                c+=1
                if dist <= threshold :
                    score += 1

    print(c)
    return score


def getLimbs(person):
    limbs = []
    neckBase = getAngle("Nose", "Neck", person)
    if neckBase == 404:
        neckBase = 0
    limbs.append(getAngle("Neck", "RShoulder", person) - neckBase)
    limbs.append(getAngle("Neck", "LShoulder", person) - neckBase)
    limbs.append(getAngle("Neck", "RHip", person) - neckBase)
    limbs.append(getAngle("Neck", "LHip", person) - neckBase)
    limbs.append(getAngle("RShoulder", "RElbow", person) - neckBase)
    limbs.append(getAngle("LShoulder", "LElbow", person) - neckBase)
    limbs.append(getAngle("RWrist", "RElbow", person) - neckBase)
    limbs.append(getAngle("LWrist", "LElbow", person) - neckBase)
    limbs.append(getAngle("RHip", "RKnee", person) - neckBase)
    limbs.append(getAngle("LHip", "LKnee", person) - neckBase)
    limbs.append(getAngle("RAnkle", "RKnee", person) - neckBase)
    limbs.append(getAngle("LAnkle", "LKnee", person) - neckBase)
    return limbs

def getAngle(key1, key2, person):
    if key1 in person:
        if key2 in person: 
            limbx = person[key1][0] - person[key2][0]
            limby = person[key1][1] - person[key2][1]
            if limbx == 0:
                if limby == 0:
                    return 404
                return math.pi / 2
            angle = math.atan(limby / limbx)
            if (limbx < 0):
                angle += math.pi
            return angle
    return 404
        
if __name__ == "__main__":
    # frames = findPose("../../../examples/media/01_allaboutthatbass_split_Trim.mp4", "../../../results/01_allaboutbass")
    frames = savedFrames()

    score = comparePoseLimbVectors(frames, 1)
    print(score)
    