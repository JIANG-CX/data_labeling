import torch

from videoanalyst.config.config import cfg as root_cfg
from videoanalyst.config.config import specify_task
from videoanalyst.model import builder as model_builder
from videoanalyst.pipeline import builder as pipeline_builder

from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2
import os
import xml.etree.ElementTree as ET

from get_yolo_data import *

scale = 2
root_cfg.merge_from_file('./experiments/siamfcpp/siamfcpp_alexnet.yaml')

# resolve config
task, task_cfg = specify_task(root_cfg)
task_cfg.freeze()

# build model
model = model_builder.build_model(task, task_cfg.model)
# build pipeline
pipeline = pipeline_builder.build_pipeline('track', task_cfg.pipeline)
pipeline.set_model(model)
pipeline.to_device(torch.device("cuda:0"))

classes = ["player", "ball"]

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, default="/home/jiangcx/桌面/足球视频/offside1.mp4",
                help="path to input video file")
ap.add_argument("-t", "--tracker", type=str, default="kcf",
                help="OpenCV object tracker type")
ap.add_argument("-s", "--xml_path", type=str, default="xml/",
                help="save_xml_path")
ap.add_argument("-m", "--image_path", type=str, default="img/",
                help="save_image_path")
ap.add_argument("-a", "--anchors", type=str, default="anchor/",
                help="save_Anchors_image_path")
args = vars(ap.parse_args())
#/Users/wangyu/Desktop/data_collector

# extract the OpenCV version info
# My opencv：4.1.0
(major, minor) = cv2.__version__.split(".")[:2]

# if we are using OpenCV 3.2 OR BEFORE, we can use a special factory
# function to create our object tracker

# initialize the bounding box coordinates of the object we are going
# to track
initBB = []
# if a video path was not supplied, grab the reference to the web cam
if not args.get("video", False):
    print("[INFO] starting video stream...")
    vs = VideoStream(src=0).start()
    time.sleep(1.0)
# otherwise, grab a reference to the video file
else:
    vs = cv2.VideoCapture(args["video"])
# initialize the FPS throughput estimator
# loop over frames from the video stream
frame = vs.read()
frame = frame[1] if args.get("video", False) else frame
# print(frame.shape[0], frame.shape[1])
# frame = frame[:,280:-280]
frame = imutils.resize(frame, width=1920, height=1080)
frame2 = frame.copy()
frame2 = imutils.resize(frame, width=1920//scale, height=1080//scale)


in_file = open(args["xml_path"]+"1.xml")
tree=ET.parse(in_file)
root = tree.getroot()
index = 0
for obj in root.iter('object'):
    cls = obj.find('name').text
    cls_id = classes.index(cls)
    xmlbox = obj.find('bndbox')
    b = (int(xmlbox.find('xmin').text)//scale, int(xmlbox.find('ymin').text)//scale,
        int(xmlbox.find('xmax').text)//scale-int(xmlbox.find('xmin').text)//scale,
        int(xmlbox.find('ymax').text)//scale-int(xmlbox.find('ymin').text)//scale,cls_id)
    initBB.append(b)
    pipeline.addNew(frame2, initBB[-1])
    (x, y, w, h, cls_id) = initBB[-1]
    cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 0, 255) if cls_id == 1 else (255, 0, 0), 2)
    text = "{}".format(cls_id)
    cv2.putText(frame2, text, (x + w//2, y + h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255) if cls_id == 1 else (255, 0, 0) , 1)
    index += 1
cv2.imshow("Frame", frame2)
cv2.waitKey(0)
# while True:
#     key = cv2.waitKey(0) & 0xFF
#     if key == ord("s"):
#         initBB.append(cv2.selectROI("Frame", frame, fromCenter=False,showCrosshair=True))
#         pipeline.addNew(frame, initBB[-1])
#         cv2.rectangle(frame, (initBB[-1][0],initBB[-1][1]), (initBB[-1][0]+initBB[-1][2],initBB[-1][1]+initBB[-1][3]), (0, 255, 0), 2)
#     elif key == ord("q"):
#         break


image_number = 2
jmpflag=0
while True:
    # grab the current frame, then handle if we are using a
    # VideoStream or VideoCapture object
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    # check to see if we have reached the end of the stream
    if frame is None:
        break
    # frame = frame[:,280:-280]
    frame = imutils.resize(frame, width=1920, height=1080)
    frame_clone = frame.copy()
    frame2 = frame.copy()
    frame2 = imutils.resize(frame2, width=1920 // scale, height=1080 // scale)
    # check to see if we are currently tracking an object
    xmin_tuple = []
    ymin_tuple = []
    xmax_tuple = []
    ymax_tuple = []
    cls_ids = []
    if len(initBB)>0:
        result = pipeline.update(imutils.resize(frame, width=1920 // scale, height=1080 // scale))
        # check to see if the tracking was a success
        for i in range(len(result)):
            index = result[i][0]
            (x, y, w, h) = [int(v) for v in result[i][1]]
            xmin_tuple.append(x*scale)
            ymin_tuple.append(y*scale)
            xmax_tuple.append(x*scale+w*scale)
            ymax_tuple.append(y*scale+h*scale)
            cls_id = result[i][-1]
            cls_ids.append(cls_id)
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 0, 255) if cls_id == 1 else (255, 0, 0), 2)
            text = "{}".format(cls_id)
            cv2.putText(frame2, text, (x + w//2, y + h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255) if cls_id == 1 else (255, 0, 0) , 1)
    # show the output frame
    cv2.imshow("Frame", frame2)
    key = cv2.waitKey(1) & 0xFF
    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if key == ord("w"):
        pipeline = pipeline_builder.build_pipeline('track', task_cfg.pipeline)
        pipeline.set_model(model)
        pipeline.to_device(torch.device("cuda:0"))
        frame_clone = frame.copy()
        frame2 = frame.copy()
        frame2 = imutils.resize(frame2, width=1920 // scale, height=1080 // scale)
        initBB = []
        cv2.imshow("Frame", frame2)
        while True:
            tmp = list(cv2.selectROI("Frame", frame2, fromCenter=False,showCrosshair=True))
            print(tmp)
            cls_index = cv2.waitKey(0) & 0xFF
            if cls_index == ord("d"):
                cls_id = 0
            elif cls_index == ord("q"):
                break
            else:
                cls_id = 1
            (x,y,w,h) = tmp

            tmp.append(cls_id)
            initBB.append(tuple(tmp))
            pipeline.addNew(imutils.resize(frame, width=1920 // scale, height=1080 // scale), initBB[-1])
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 0, 255) if cls_id == 1 else (255, 0, 0), 2)
            text = "{}".format(cls_id)
            cv2.putText(frame2, text, (x + w//2, y + h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255) if cls_id == 1 else (255, 0, 0) , 1)
            cv2.imshow("Frame", frame2)
    elif key == ord("s"):
        print(image_number)
        while True:
            tmp = list(cv2.selectROI("Frame", frame2, fromCenter=False,showCrosshair=True))
            cls_index = cv2.waitKey(0) & 0xFF
            if cls_index == ord("d"):
                cls_id = 0
            elif cls_index == ord("q"):
                break
            elif cls_index == ord("a"):
                cls_id = 1
            (x,y,w,h) = tmp
            tmp.append(cls_id)
            initBB.append(tuple(tmp))
            pipeline.addNew(imutils.resize(frame, width=1920 // scale, height=1080 // scale), initBB[-1])
            cv2.rectangle(frame2, (x, y), (x + w, y + h), (0, 0, 255) if cls_id == 1 else (255, 0, 0), 2)
            text = "{}".format(cls_id)
            cv2.putText(frame2, text, (x + w//2, y + h//2), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (0, 0, 255) if cls_id == 1 else (255, 0, 0) , 1)
            cv2.imshow("Frame", frame2)
    if jmpflag==0:
        cv2.imwrite(args["image_path"]+str(image_number)+".jpg",frame)
        cv2.imwrite(args["anchors"]+str(image_number)+".jpg",frame2)
        file_xml = make_xml(xmin_tuple,ymin_tuple,xmax_tuple,ymax_tuple,str(image_number),cls_ids)
        xml_name = os.path.join(args["xml_path"], str(image_number)+ '.xml')
        with open(xml_name, 'w') as f:
            f.write(file_xml.toprettyxml(indent='\t'))
        image_number += 1
        jmpflag=0
        print(image_number,jmpflag)
    else:
        jmpflag-=1
        print('aaaa')
        continue
# if we are using a webcam, release the pointer
if not args.get("video", False):
    vs.stop()
# otherwise, release the file pointer
else:
    vs.release()
# close all windows
cv2.destroyAllWindows()
