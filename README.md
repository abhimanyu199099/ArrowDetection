# ArrowDetection

Repository for the Vision module for the CRISS Robotics rover, for the International Rover Challenge, 2024. This repo contains:

* framesmaker.py - Code for ingesting videos obtained during the data collection process, sampling frames from them and splitting them into their respective folders.
* ResizeByFolder.py - Code to resize images to a smaller size, to facilitate faster training.
* YOLOv5_Train.ipynb - Code for training a YOLOv5m model to detect arrows in the field of view.
* webcam_detect.ipynb - Testing the YOLO model trained.
* realsense_depth_find.py - Code for Depth estimation of the arrows detected using the trained YOLO model on an Intel RealSense D415, and finding the angle of adjustment for going to the next checkpoint.
* index.py - Integration with ROS Noetic to put on the rover.

