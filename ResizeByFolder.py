import os
import cv2

def resize_images(input_folder, new_size):
    
    image_files = os.listdir(input_folder)
    for image_file in image_files:
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(input_folder, image_file)
            output_path = os.path.join(input_folder, image_file)
            img = cv2.imread(image_path)
            if img is None:
                print(f"Error reading {image_path}. Skipping.")
                continue
            
            img = cv2.resize(img, new_size)
            cv2.imwrite(output_path, img)
            print(f"Resized and saved {image_file} in {input_folder}")
    
    print("Image resizing and saving completed.")

input_folder = r"E:\Dataset\frames9"
new_size = (192, 108)  # New dimensions (width, height)

resize_images(input_folder, new_size)
