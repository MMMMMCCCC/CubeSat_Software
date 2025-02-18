from adafruit_lsm6ds.lsm6dsox import LSM6DSOX as LSM6DS
from adafruit_lis3mdl import LIS3MDL
import time
import os
import board
import busio
from picamera2 import Picamera2
import numpy as np
import sys
import matplotlib.pyplot as plt
import math
import cv2
from auto_camera_V2 import capture

def detect_fire(dir='roll', target_angle=70, margin=5, max_cycle=30, altitude_m=2.5, fov_m=62):
    """use the image saved by the auto_camera_V2 file
       detect red.orange/yellow sections in the image, that will represent the wildfire
       calculate the area of those sections and get the time interval of each area
       plot the data
    """
    
    data1 = []  # values for area of fire in m2 
    data2 = []  # values for percentage area
    time_x = []  # time that each value is collected

    start_time = time.time()

    for cycle in range(max_cycle):
        minute = (time.time() - start_time) / 60
        file = "CaptureIMG_{minute}.jpg"
        capture(file,dir,target_angle,margin) #call this function to capture the image
        
        m2, percent = calc_area(file,(3280,2464),2.5,62) #calculate area of the fire in each image
        time.sleep(1)  # Wait for 1 second to ensure the file is saved before loading

        # Append the data to the lists
        data1.append(m2)
        data2.append(percent)
        time_x.append(minute)
    
    # Plotting the collected data
    print(data1)
    print(data2)
    fig, ax1 = plt.subplots()
    ax1.plot(time_x, data1, color='red', label="Area of Fire in m^2")
    ax1.set_xlabel("Time (mins)")
    ax1.set_ylabel("Area of Fire in m^2", color="red")
    ax1.tick_params(axis='y', labelcolor="red")
    
    ax2 = ax1.twinx()  # Using the same plot but different line graphs
    ax2.plot(time_x, data2, color='blue', label="Percentage Area Covered")
    ax2.set_ylabel("Area of Fire Percentage Compared to Forest", color="blue")
    ax2.tick_params(axis='y', labelcolor="blue")

    # Save the plot as an image
    plt.savefig("Images/fire_plot.png")
    print("Plot saved in Images/fire_plot.png")
    
    # Other plot setups
    plt.title("Forest Fire Data Collection with Twin Axes")
    plt.show()

def calc_area(image, img_resolution, altitude_m, fov_m):
    img = cv2.imread(image)  # Read the image file
        
    if img is None:
        print(f"Failed to load image: {image}")
        raise ValueError("Failed to load the captured image.")
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
    # First mask for darker red
    fire1 = np.array([0, 100, 100])
    fire2 = np.array([10, 255, 255])
        
    # Second mask for lighter red
    fire3 = np.array([160, 100, 100])
    fire4 = np.array([179, 255, 255])
        
    mask1 = cv2.inRange(hsv, fire1, fire2)  # Darker red
    mask2 = cv2.inRange(hsv, fire3, fire4)  # Lighter red
        
    fMask = cv2.bitwise_or(mask1, mask2)
        
    region = cv2.countNonZero(fMask)  # Fire region
    total_pixels = img.shape[0] * img.shape[1]
    area_percent = (region / total_pixels) * 100  # Percentage area of the fire compared to the whole image

    width, height = img_resolution  # For calculating actual area of fire
        
    rad = math.radians(fov_m)  # Convert it to radians to be used in calculations
    fov = 2 * (altitude_m * math.tan(rad / 2))  # Field of view
    GSD = (altitude_m * width) / fov  # Find GSD based on FOV
        
    area_m = region * (GSD)**2  # Convert area to meters squared
    
    return area_m, area_percent

if __name__ == "__main__":
    detect_fire()  # Start the fire detection process


