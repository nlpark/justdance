# From Python
# It requires OpenCV installed for Python
import sys
import cv2
import os
from sys import platform
import argparse

def findPose(videoPath, resultsPath):
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
        parser.add_argument("--video", default=videoPath)
        # parser.add_argument("--number_people_max", default = "2")
        # parser.add_argument("--write_video", default= "testResults.avi")
        args = parser.parse_known_args()

        # Custom Params (refer to include/openpose/flags.hpp for more parameters)
        params = dict()
        params["model_folder"] = "../../../models/"
        params["number_people_max"] = 2
        params["write_images"] = resultsPath
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
            
            cv2.imwrite(resultsPath +'/video'+str(i)+'.jpg', datum.cvOutputData)
            # cv2.waitKey(20)
            # cv2.imwrite('video'+str(i)+'.jpg',frame)
            i+=1
            count+=int(fps)
            capture.set(1, count)

            # if count >= 100:
            #     break
    
        capture.release()

        return frames

    except Exception as e:
        print(e)
        sys.exit(-1)


def buildFrame25(keypoints, i):
    if len(keypoints) != 2:
        raise ValueError("keypoint array is wrong length.... length = ", len(keypoints))

    print("Frame #", i)
    frame = []

    # crazy print statements here are so that you can take terminal output, save it, clean it a little
    # and put it in savedFrames.py, so that you don't have to run the findPose every time u change comparePose thresholding
    # v tedious, feel free to improve i would love that

    print("[")

    for i in range(1, 3):
        person = dict()
        print("{")
        person['Nose'] = keypoints[i-1][0]
        print('"Nose": [' +  str(keypoints[i-1][0][0]) + "," +  str(keypoints[i-1][0][1]) + "," +  str(keypoints[i-1][0][2]) + "],")

        person['Neck' ] = keypoints[i-1][1]
        print('"Neck": [' +  str(keypoints[i-1][1][0]) + "," +  str(keypoints[i-1][1][1]) + "," +  str(keypoints[i-1][1][2]) + "],")

        person['RShoulder'] = keypoints[i-1][2]
        print('"RShoulder": [' + str(keypoints[i-1][2][0]) + "," + str(keypoints[i-1][2][1]) + "," + str(keypoints[i-1][2][2]) + "],")

        person['RElbow'] = keypoints[i-1][3]
        print('"RElbow": [' + str(keypoints[i-1][3][0]) + "," + str(keypoints[i-1][3][1]) + "," + str(keypoints[i-1][3][2]) + "],")

        person['RWrist'] = keypoints[i-1][4]
        print('"RWrist": [' + str(keypoints[i-1][4][0]) + "," + str(keypoints[i-1][4][1]) + "," + str(keypoints[i-1][4][2]) + "],")

        person['LShoulder'] = keypoints[i-1][5]
        print('"LShoulder": [' + str(keypoints[i-1][5][0]) + "," + str(keypoints[i-1][5][1]) + "," + str(keypoints[i-1][5][2]) + "],")

        person['LElbow'] = keypoints[i-1][6]
        print('"LElbow": [' + str(keypoints[i-1][6][0]) + "," + str(keypoints[i-1][6][1]) + "," + str(keypoints[i-1][6][2]) + "],")

        person['LWrist'] = keypoints[i-1][7]
        print('"LWrist": [' + str(keypoints[i-1][7][0]) + "," + str(keypoints[i-1][7][1]) + "," + str(keypoints[i-1][7][2]) + "],")

        person['MidHip'] = keypoints[i-1][8]
        print('"MidHip": [' + str(keypoints[i-1][8][0]) + "," + str(keypoints[i-1][8][1]) + "," + str(keypoints[i-1][8][2]) + "],")

        person['RHip'] = keypoints[i-1][9]
        print('"RHip": [' + str(keypoints[i-1][9][0]) + "," + str(keypoints[i-1][9][1]) + "," + str(keypoints[i-1][9][2]) + "],")

        person['RKnee'] = keypoints[i-1][10]
        print('"RKnee": [' + str(keypoints[i-1][10][0]) + "," + str(keypoints[i-1][10][1]) + "," + str(keypoints[i-1][10][2]) + "],")

        person['RAnkle'] = keypoints[i-1][11]
        print('"RAnkle": [' + str(keypoints[i-1][11][0]) + "," + str(keypoints[i-1][11][1]) + "," + str(keypoints[i-1][11][2]) + "],")

        person['LHip'] = keypoints[i-1][12]
        print('"LHip": [' + str(keypoints[i-1][12][0]) + "," + str(keypoints[i-1][12][1]) + "," + str(keypoints[i-1][12][2]) + "],")

        person['LKnee'] = keypoints[i-1][13]
        print('"LKnee": [' + str(keypoints[i-1][13][0]) + "," + str(keypoints[i-1][13][1]) + "," + str(keypoints[i-1][13][2]) + "],")

        person['LAnkle'] = keypoints[i-1][14]
        print('"LAnkle": [' + str(keypoints[i-1][14][0]) + "," + str(keypoints[i-1][14][1]) + "," + str(keypoints[i-1][14][2]) + "],")

        person['REye'] = keypoints[i-1][15]
        print('"REye": [' + str(keypoints[i-1][15][0]) + "," + str(keypoints[i-1][15][1]) + "," + str(keypoints[i-1][15][2]) + "],")

        person['LEye'] = keypoints[i-1][16]
        print('"LEye": [' + str(keypoints[i-1][16][0]) + "," + str(keypoints[i-1][16][1]) + "," + str(keypoints[i-1][16][2]) + "],")

        person['REar'] = keypoints[i-1][17]
        print('"REar": [' + str(keypoints[i-1][17][0]) + "," + str(keypoints[i-1][17][1]) + "," + str(keypoints[i-1][17][2]) + "],")

        person['LEar'] = keypoints[i-1][18]
        print('"LEar": [' + str(keypoints[i-1][18][0]) + "," + str(keypoints[i-1][18][1]) + "," + str(keypoints[i-1][18][2]) + "],")

        person['LBigToe'] = keypoints[i-1][19]
        print('"LBigToe": [' + str(keypoints[i-1][19][0]) + "," + str(keypoints[i-1][19][1]) + "," + str(keypoints[i-1][19][2]) + "],")

        person['LSmallToe'] = keypoints[i-1][20]
        print('"LSmallToe": [' + str(keypoints[i-1][20][0]) + "," + str(keypoints[i-1][20][1]) + "," + str(keypoints[i-1][20][2]) + "],")

        person['LHeel'] = keypoints[i-1][21]
        print('"LHeel": [' + str(keypoints[i-1][21][0]) + "," + str(keypoints[i-1][21][1]) + "," + str(keypoints[i-1][21][2]) + "],")

        person['RBigToe'] = keypoints[i-1][22]
        print('"RBigToe": [' + str(keypoints[i-1][22][0]) + "," + str(keypoints[i-1][22][1]) + "," + str(keypoints[i-1][22][2]) + "],")

        person['RSmallToe'] = keypoints[i-1][23]
        print('"RSmallToe": [' + str(keypoints[i-1][23][0]) + "," + str(keypoints[i-1][23][1]) + "," + str(keypoints[i-1][23][2]) + "],")

        person['RHeel'] = keypoints[i-1][24]
        if i == 1:
            print('"RHeel": [' + str(keypoints[i-1][24][0]) + "," + str(keypoints[i-1][24][1]) + "," + str(keypoints[i-1][24][2]) + "]},")
        else:
            print('"RHeel": [' + str(keypoints[i-1][24][0]) + "," + str(keypoints[i-1][24][1]) + "," + str(keypoints[i-1][24][2]) + "]}")

        frame.append(person)

    print("]")

    # print(frame)
    print("------------------------------------------------------------------------------------------------")

    return frame

if __name__ == "__main__":
    findPose()