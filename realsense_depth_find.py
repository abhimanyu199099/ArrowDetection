import cv2
import numpy as np
import imutils
from ultralytics import YOLO
import math
import torch
import json
import pyrealsense2 as rs

def draw_centroids_on_image(output_image, json_results):   
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
        #print(cx,cy)
    
        cv2.circle(output_image, (cx,cy), 2, (0, 0, 255), 2, cv2.FILLED) #draw center dot on detected object
        cv2.putText(output_image, str(str(cx)+" , "+str(cy)), (int(cx)-40, int(cy)+30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)

    return (output_image)

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

def find_x_ends (output_image, json_results):
    data = json.loads(json_results) # Converting JSON array to Python List
    # Accessing each individual object and then getting its xmin, ymin, xmax and ymax to calculate its centroid
    for objects in data:
        xmin = objects["xmin"]
        xmax = objects["xmax"]
        ymin = objects["ymin"]
        ymax = objects["ymax"]
    
    ends = [xmin, xmax, ymin, ymax]
    return ends

def find_angle (ends, depth_frame):

    zdepth1 = depth_frame.get_distance(int(ends[0]),int(ends[2]))
    zdepth2 = depth_frame.get_distance(int(ends[1]),int(ends[3]))

    depth = zdepth1 - zdepth2
    slant = 0.3

    x = depth/slant
    angle = np.arcsin(x)
    return angle



model = torch.hub.load('ultralytics/yolov5', 'custom', path= 'yolov5m_25epochs.pt')
model.eval()
model.classes = [0]
classNames = ['arrow','not arrow']

pipe = rs.pipeline()
cfg = rs.config()

cfg.enable_stream (rs.stream.color, 640, 480, rs.format.bgr8, 30)
cfg.enable_stream (rs.stream.depth, 640, 480, rs.format.z16, 30)

pipe.start (cfg)


while True:

    try:
        frame = pipe.wait_for_frames()
        depth_frame = frame.get_depth_frame()
        color_frame = frame.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
    
        depth_cm = cv2.applyColorMap (cv2.convertScaleAbs (depth_image, alpha = 0.5), cv2.COLORMAP_JET)

        results = model (color_image)
        results.show()
        json_results = results.pandas().xyxy[0].to_json(orient="records") # im predictions (JSON)
        results.render()  # updates results.imgs with boxes and labels                    
        output_image = results.ims[0] #output image after rendering // results.ims is correct (not results.imgs)
        output_image = cv2.cvtColor(output_image, cv2.COLOR_RGB2BGR)           
        output_image = draw_centroids_on_image(output_image, json_results) # Draw Centroids on the deteted objects and returns updated imag
        color_image = output_image

        centroids = find_centroids(output_image, json_results)
        zdepth = depth_frame.get_distance((int(centroids[0])),int((centroids[1])))
        ends = find_x_ends (output_image, json_results)
        angle = find_angle (ends, depth_frame)


    
        print (f"obj centre is at xyz: {centroids},{zdepth},{angle}")
    
        cv2.imshow ('rgb', color_image)
        cv2.imshow ('depth', depth_cm)

        if cv2.waitKey(1) == ord ('q'):
            break

    except TypeError:
        continue

pipe.stop()