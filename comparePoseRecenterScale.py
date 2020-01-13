import sys
import cv2
import os
from sys import platform
import argparse
import math
from scipy.spatial.distance import euclidean

from findPose import findPose
from savedFrames import savedFrames

def comparePoseRecenterScale(frames, threshold, scale):
    c = 0
    score = 0
    for f in frames:
        # let's just call neck the center for semantic's sake
        # person 1: adjust points so neck is the (0,0)
        personOne = recenter(f[0])

        # person 2: adjust points so neck is the (0,0)
        personTwo = recenter(f[1])

        # if we want to scale from height, do that
        if (scale == 1):
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

            dist = math.sqrt((coordX1 - coordX2)**2 + (coordY1 - coordY2)**2) 
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
    newPerson = person

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
    rheel1 = person1['RHeel']
    lheel1 = person1['LHeel']
    rheel2 = person2['RHeel']
    lheel2 = person2['LHeel']
    
    x1 = ( rheel1[0] + lheel1[0] ) / 2
    y1 = ( rheel1[1] + lheel1[1] ) / 2
    x2 = ( rheel2[0] + lheel2[0] ) / 2
    y2 = ( rheel2[1] + lheel2[1] ) / 2

    # in case one leg is bent and the other isnt, take the larger value


        
if __name__ == "__main__":
    # frames = findPose("../../../examples/media/01_allaboutthatbass_split_Trim.mp4", "../../../results/01_allaboutbass")
    frames = savedFrames()

    score = comparePoseRecenterScale(frames, 50, 0)
    print(score)