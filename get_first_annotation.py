import matplotlib.pyplot as plt

from get_yolo_data import *
import cv2
import imutils
import argparse
import os


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", type=str, default="/home/jiangcx/桌面/足球视频/offside1.mp4",
                help="path to input video file")
ap.add_argument("-s", "--xml_path", type=str, default="xml/",
                help="save_xml_path")
ap.add_argument("-m", "--image_path", type=str, default="img/",
                help="save_image_path")
args = vars(ap.parse_args())

scale = 2

if __name__ == "__main__":
    vs = cv2.VideoCapture(args["video"])
    frame = vs.read()
    frame = frame[1] if args.get("video", False) else frame
    print(frame.shape[0], frame.shape[1])
    # frame = frame[:,280:-280]
    frame = imutils.resize(frame, width=1920, height=1080)
    frame_clone = frame.copy()
    frame_clone = imutils.resize(frame_clone, width=1920//scale, height=1080//scale)
    cv2.imshow("Frame", frame_clone)
    cv2.imwrite(args["image_path"]+str(1)+".jpg",frame)
    initBB = []
    xmin_tuple = []
    ymin_tuple = []
    xmax_tuple = []
    ymax_tuple = []
    cls_ids = []
    while True:
        key = cv2.waitKey(0) & 0xFF
        if key == ord("s"):
            initBB = cv2.selectROI("Frame", frame_clone, fromCenter=False,showCrosshair=True)
            choice = cv2.waitKey(0) & 0xFF
            if choice == ord("d"):
                cls_ids.append(0)
            elif choice == ord("a"):
                cls_ids.append(1)
            cv2.rectangle(frame_clone, (initBB[0],initBB[1]), (initBB[0]+initBB[2],initBB[1]+initBB[3]), (0, 0, 255) if cls_ids[-1] == 1 else (255, 0, 0), 2)
            xmin_tuple.append(initBB[0]*scale)
            ymin_tuple.append(initBB[1]*scale)
            xmax_tuple.append(initBB[0]*scale+initBB[2]*scale)
            ymax_tuple.append(initBB[1]*scale+initBB[3]*scale)
        elif key == ord("q"):
            break
        elif key == ord("w"):
            frame_clone = frame.copy()
            frame_clone = imutils.resize(frame_clone, width=1920 // scale, height=1080 // scale)
            xmin_tuple = []
            ymin_tuple = []
            xmax_tuple = []
            ymax_tuple = []
            cls_ids = []
            cv2.imshow("Frame",frame_clone)
    file_xml = make_xml(xmin_tuple,ymin_tuple,xmax_tuple,ymax_tuple,str(1), cls_ids)
    xml_name = os.path.join(args["xml_path"], str(1)+ '.xml')
    with open(xml_name, 'w') as f:
        f.write(file_xml.toprettyxml(indent='\t'))
