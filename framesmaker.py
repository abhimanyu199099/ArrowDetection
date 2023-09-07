import cv2
import os

# Path to the input video file
video_path = r"C:\Users\Abhim\Downloads\vid9.mp4"

# Open the video file
cap = cv2.VideoCapture(video_path)

# Check if the video file was opened successfully
if not cap.isOpened():
    print("Error opening video file.")
    exit()

# Create a directory to store the frames
output_dir = r"E:\Dataset\frames9"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

frame_number = 0

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    
    # Break the loop if we have reached the end of the video
    if not ret:
        break
    
    # Save the frame as an image
    frame_filename = os.path.join(output_dir, f"vid9frame{frame_number:04d}.png")
    cv2.imwrite(frame_filename, frame)
    
    frame_number += 1

# Release the video capture object
cap.release()

print(f"Total frames extracted: {frame_number}")
