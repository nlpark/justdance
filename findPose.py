# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse

def findPose():
    try:
        # Import Openpose (Windows/Ubuntu/OSX)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            # Windows Import
            if platform == "win32":
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append(dir_path + '/../../python/openpose/Release');
                os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
                import pyopenpose as op
            else:
                # Change these variables to point to the correct folder (Release/x64 etc.)
                sys.path.append('../../python');
                # If you run `make install` (default path is `/usr/local/python` for Ubuntu), you can also access the OpenPose/python module from there. This will install OpenPose and the python library at your desired installation path. Ensure that this is in your python path in order to use it.
                # sys.path.append('/usr/local/python')
                from openpose import pyopenpose as op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        # Flags
        parser = argparse.ArgumentParser()
        # parser.add_argument("--image_path", default="../../../examples/media/COCO_val2014_000000000428.jpg", help="Process an image. Read all standard formats (jpg, png, bmp, etc.).")
        parser.add_argument("--video", default="../../../examples/media/01_allaboutthatbass_split_Trim.mp4")
        # parser.add_argument("--number_people_max", default = "2")
        # parser.add_argument("--write_video", default= "testResults.avi")
        args = parser.parse_known_args()

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "../../../models/"
        params["number_people_max"] = 2
        # params["write_video"] = "testResults.avi"

        # Add others in path?
        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1])-1: next_item = args[1][i+1]
            else: next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-','')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-','')
                if key not in params: params[key] = next_item

        print("args", args)
        print("params",params)

        #Construct it from system arguments
        # op.init_argv(args[1])
        # oppython = op.OpenposePython()

        #Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()

        # Process Video
        datum = op.Datum()
        capture  = cv2.VideoCapture(args[0].video)
        fps = capture.get(cv2.CAP_PROP_FPS)
        
        frames = []

        print('fps: ', fps)
        i = 0
        count = 0

        while(capture.isOpened()):
            ret, frame = capture.read()
            if ret == False:
                break
            datum.cvInputData = frame
            opWrapper.emplaceAndPop([datum])

            keypoints = datum.poseKeypoints
            frame = buildFrame25(keypoints, i)
            frames.append(frame)

            # print("Body keypoints: \n" + str(keypoints))
            
            cv2.imshow('video'+str(i)+'.jpg', datum.cvOutputData)
            cv2.waitKey(20)
            # cv2.imwrite('video'+str(i)+'.jpg',frame)
            i+=1
            count+=int(fps)
            capture.set(1, count)

            if count >= 100:
                break
    
        capture.release()

    except Exception as e:
        print(e)
        sys.exit(-1)


def buildFrame25(keypoints, i):
    if len(keypoints) != 2:
        raise ValueError("keypoint array is wrong length.... length = ", len(keypoints))

    print("Frame #", i)
    frame = []

    for i in range(1, 3):
        person = dict()
        person['Nose-' + str(i)] = keypoints[i-1][0]
        person['Neck-'  + str(i)] = keypoints[i-1][1]
        person['RShoulder-' + str(i)] = keypoints[i-1][2]
        person['RElbow-' + str(i)] = keypoints[i-1][3]
        person['RWrist-' + str(i)] = keypoints[i-1][4]
        person['LShoulder-' + str(i)] = keypoints[i-1][5]
        person['LElbow-' + str(i)] = keypoints[i-1][6]
        person['LWrist-' + str(i)] = keypoints[i-1][7]
        person['MidHip-' + str(i)] = keypoints[i-1][8]
        person['RHip-' + str(i)] = keypoints[i-1][9]
        person['RKnee-' + str(i)] = keypoints[i-1][10]
        person['RAnkle-' + str(i)] = keypoints[i-1][11]
        person['LHip-' + str(i)] = keypoints[i-1][12]
        person['LKnee-' + str(i)] = keypoints[i-1][13]
        person['LAnkle-' + str(i)] = keypoints[i-1][14]
        person['REye-' + str(i)] = keypoints[i-1][15]
        person['LEye-' + str(i)] = keypoints[i-1][16]
        person['REar-' + str(i)] = keypoints[i-1][17]
        person['LEar-' + str(i)] = keypoints[i-1][18]
        person['LBigToe-' + str(i)] = keypoints[i-1][19]
        person['LSmallToe-' + str(i)] = keypoints[i-1][20]
        person['LHeel-' + str(i)] = keypoints[i-1][21]
        person['RBigToe-' + str(i)] = keypoints[i-1][22]
        person['RSmallToe-' + str(i)] = keypoints[i-1][23]
        person['RHeel-' + str(i)] = keypoints[i-1][24]
        frame.append(person)

    # print(frame)
    print("------------------------------------------------------------------------------------------------")

    return frame

if __name__ == "__main__":
    findPose()