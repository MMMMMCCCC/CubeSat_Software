import math

def take_photo():
    """
    This function detects when the device is shaken (acceleration surpasses the threshold),
    pauses briefly, captures a photo, and uploads it to GitHub.
    """
    while True:
        # Read the acceleration data from the IMU (accelerometer)
        accelx, accely, accelz = accel_gyro.acceleration
        
        # Calculate the magnitude of acceleration (Euclidean norm)
        accel_magnitude = math.sqrt(accelx**2 + accely**2 + accelz**2)
        
        # Check if the acceleration exceeds the threshold
        if accel_magnitude > THRESHOLD:
            print("Shake detected!")
            
            # Pause briefly (to avoid multiple triggers from the same shake)
            time.sleep(1)  # Adjust the sleep time as needed
            
            # Generate the image filename based on the user's name
            name = "MasonM"  # Replace this with your actual name
            imgname = img_gen(name)
            
            # Take the photo and save it
            picam2.start()
            picam2.capture_file(imgname)
            picam2.stop()
            print(f"Photo taken: {imgname}")
            
            # Upload the photo to GitHub
            git_push()

        # Optional: Sleep to prevent excessive CPU usage
        time.sleep(0.1)
