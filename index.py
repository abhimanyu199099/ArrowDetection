#!/usr/bin/env python3
import pyrealsense2 as rs
import numpy as np
import imutils
from ultralytics import YOLO
import torch
import json
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import MultiArrayDimension
import rospy


def find_centroids (output_image, json_results):
    data = json.loads(json_results) # Converting JSON array to Python List
    # Accessing each individual object and then getting its xmin, ymin, xmax and ymax to calculate its centroid
    for objects in data:
        xmin = objects["xmin"]
        ymin = objects["ymin"]
        xmax = objects["xmax"]
        ymax = objects["ymax"]
        
        #print("Object: ", data.index(objects))
        #print ("xmin", xmin)
        #print ("ymin", ymin)
        #print ("xmax", xmax)
        #print ("ymax", ymax)
        
        #Centroid Coordinates of detected object
        cx = int((xmin+xmax)/2.0)
        cy = int((ymin+ymax)/2.0)   

        return (cx,cy)

def talker():


    frame = pipe.wait_for_frames()
    depth_frame = frame.get_depth_frame()
    color_frame = frame.get_color_frame()
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    
    results = model(color_image)
    json_results = results.pandas().xyxy[0].to_json(orient="records") # im predictions (JSON)
    output_image = results.ims[0]
    center = find_centroids (output_image, json_results)
    print ('--------------------------',center,'-------------------------------')
    print ('--------------------------',results.pandas().xyxy[0][0],results.pandas().xyxy[0][1],results.pandas().xyxy[0][2],results.pandas().xyxy[0][3],'-----------')

    arr1 = [depth_image,color_image,json_results,output_image]
    arr = Float64MultiArray()
    arr.data = arr1
    rospy.loginfo(arr)
    pub.publish(arr)





if __name__ == '__main__':

    global pub, rate, pipe, cfg, model
    pub = rospy.Publisher('chatter',Float64MultiArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(60)
    pipe = rs.pipeline()
    cfg = rs.config()
    cfg.enable_stream (rs.stream.color, 640, 480, rs.format.bgr8, 30)
    cfg.enable_stream (rs.stream.depth, 640, 480, rs.format.z16, 30)
    model = torch.hub.load('ultralytics/yolov5', 'custom', path= '/home/abhimanyu/yolov5/yolov5m_25epochs.pt')
    model.eval()
    model.classes = [0]

    pipe.start (cfg)
    while True:
        try:
            talker()
        except (rospy.ROSInterruptException):
            continue