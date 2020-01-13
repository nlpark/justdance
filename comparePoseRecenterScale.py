import sys
import cv2
import os
from sys import platform
import argparse
import math

from findPose import findPose
from savedFrames import savedFrames

def comparePoseRecenterScale(frames, threshold, doScale):
    c = 0
    score = 0
    for f in frames:
        # let's just call neck the center for semantic's sake
        # person 1: adjust points so neck is the (0,0)
        personOne = recenter(f[0])

        # person 2: adjust points so neck is the (0,0)
        personTwo = recenter(f[1])

        # if we want to scale from height, do that
        if doScale == 1:
            personTwo = scale(personOne, personTwo)

        # compare points, calculate score
        # everywhere that the distances between points is within threshold
        # add points
        dists = []
        for key in personOne:
            coord1 = personOne[key]
            coordX1 = coord1[0]
            coordY1 = coord1[1]
            coord2 = personTwo[key]
            coordX2 = coord2[0]
            coordY2 = coord2[1]

            dist = euclidean(coordX1, coordY1, coordX2, coordY2) 
            dists.append(dist)
            c+=1
            if dist <= threshold :
                score += 1

    print(c)
    return score


def recenter(person):
    center = person['Neck']
    cX = center[0]
    cY = center[1]
    newPerson = dict()

    for key in person:
        coord = person[key]
        coordX = coord[0]
        coordY = coord[1]

        coordX = coordX - cX
        coordY = coordY - cY
        newPerson[key] = coordX, coordY 
    if newPerson['Neck'][0] != newPerson['Neck'][1] != 0 :
        print ("Big uh oh, neck is wrong")
        print ("Neck x =", newPerson['Neck'][0], " Neck y =", newPerson['Neck'][1])
    return newPerson

def scale(person1, person2):
    # since it's already zeroed to the neck, we can judge height from neck
    # to heel
    newPerson = dict()

    rheel1 = person1['RHeel']
    lheel1 = person1['LHeel']
    rheel2 = person2['RHeel']
    lheel2 = person2['LHeel']

    # in case one leg is bent and the other isn't, take the larger value
    rdist1 = euclidean(0, 0, rheel1[0], rheel1[1])
    ldist1 = euclidean(0, 0, lheel1[0], lheel1[1])
    rdist2 = euclidean(0, 0, rheel2[0], rheel2[1])
    ldist2 = euclidean(0, 0, lheel2[0], lheel2[1])
    # pick the longer leg
    height1 = rdist1
    height2 = rdist2
    if ldist1 > rdist1: 
        height1 = ldist1
    if ldist2 > rdist2:
        height2 = ldist2

    factor = height1 / height2
    for key in person2:
        coord = person2[key]
        coordX = coord[0]
        coordY = coord[1]

        coordX = coordX * factor
        coordY = coordY * factor
        newPerson[key] = coordX, coordY 

    # test to make sure height is now the same
    testheel = newPerson['RHeel']
    if height2 == ldist2 : 
        testheel = newPerson['LHeel']
    testdist = euclidean(0, 0, testheel[0], testheel[1])
    if math.fabs(testdist - height1) > 0.01 :
        print("Error in height adjustment", testdist, " ", height1)
    return newPerson

def euclidean(x1, y1, x2, y2):
    distx = x1 - x2
    disty = y1 - y2
    distx = distx**2
    disty = disty**2
    dist = math.sqrt(distx + disty)
    return dist

        
if __name__ == "__main__":
    # frames = findPose("../../../examples/media/01_allaboutthatbass_split_Trim.mp4", "../../../results/01_allaboutbass")
    frames = savedFrames()

    score = comparePoseRecenterScale(frames, 50, 0)
    print(score)
    score = comparePoseRecenterScale(frames, 50, 1)
    print(score)