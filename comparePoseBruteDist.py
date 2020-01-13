import sys
import cv2
import os
from sys import platform
import argparse
import math

from findPose import findPose
from savedFrames import savedFrames

def comparePoseBruteDist(frames, threshold):
    c = 0
    score = 0
    for f in frames:
        # let's just call neck the center for semantic's sake
        # person 1: calculate dist from each keypoint to neck
        personOneDist = calculateDists(f[0])

        # person 2: calculate dist from each keypoint to neck
        personTwoDist = calculateDists(f[1])

        if len(personOneDist) != len(personTwoDist):
            raise ValueError("one dist vector too long!")

        # compare distances, calculate score
        # everywhere that the diff between distances is within threshold
        # add points
            # consider making points a factor of the threshold? smaller threshold means more points?
        comparison = []
        for i in range(len(personOneDist)):
            compare = abs(personOneDist[i] - personTwoDist[i])
            comparison.append(compare)
            c += 1
            if compare <= threshold :
                score += 1 
    print(c)
    return score


def calculateDists(person):
    center = person['Neck']
    cX = center[0]
    cY = center[1]

    distances = []

    for key in person:
        if key == 'Neck':
            continue

        coord = person[key]
        coordX = coord[0]
        coordY = coord[1]

        xdiff = coordX - cX
        xdiffsq = xdiff**2

        ydiff = coordY - cY
        ydiffsq = ydiff**2

        dist = math.sqrt(xdiffsq + ydiffsq)

        distances.append(dist)

    return distances
        
if __name__ == "__main__":
    # frames = findPose("../../../examples/media/01_allaboutthatbass_split_Trim.mp4", "../../../results/01_allaboutbass")
    frames = savedFrames()

    score = comparePoseBruteDist(frames, 50)
    print(score)