import RPi.GPIO as GPIO
import time
import subprocess
import os
import shutil

global redapples 
global greenapples 
global yellowapples 

redapples =0
greenapples =0
yellowapples =0

data = "redapples: "+str(redapples)+"\n"+" greenapples: "+str(greenapples)+"\n"+"yellowapples: "+str(yellowapples)+"\n"
with open('output.txt', 'w') as file:
    file.write(data)

# Motor Pins
DC_ENABLE_PIN = 25
DC_INPUT_PIN1 = 18                                                      
DC_INPUT_PIN2 = 24

# Sensor Pin
SENSOR_PIN = 27

# Setup GPIO Mode
GPIO.setmode(GPIO.BCM)

# Servo Setup on Pin 11
GPIO.setup(17, GPIO.OUT)
servo1 = GPIO.PWM(17, 50)  # 50Hz PWM frequency for servo
servo1.start(0)

# Setup Motor Pins
GPIO.setup(DC_ENABLE_PIN, GPIO.OUT)
GPIO.setup(DC_INPUT_PIN1, GPIO.OUT)
GPIO.setup(DC_INPUT_PIN2, GPIO.OUT)

# Setup Sensor Pin with Pull-up
GPIO.setup(SENSOR_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to capture an image using libcamera
def capture_image(output_path="/home/myras/test.jpg"):
    try:
        command = [
            "libcamera-still", 
            "-o", output_path,
            "--nopreview",    # Disable the preview window
        ]
        # Capture image using libcamera
        result = subprocess.run(command, check=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        print(f"Image saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error capturing image: {e.stderr.decode()}")


def clear_exp_folders(output_dir="yolov5/runs/predict-cls"):
    # Remove all experiment folders starting with 'exp'
    exp_dirs = [d for d in os.listdir(output_dir) if d.startswith('exp')]
    for exp_dir in exp_dirs:
        exp_folder_path = os.path.join(output_dir, exp_dir)
        shutil.rmtree(exp_folder_path)
        
# Function to run YOLOv5 prediction
def predict_with_yolov5(image_path, model_path='/home/myras/best.pt'):
    clear_exp_folders()
    try:
        yolov5_env = '/home/myras/yolov5_env/bin/python3'  # Path to your virtual environment's Python
        yolov5_script = '/home/myras/yolov5/classify/predict.py'  # YOLOv5 prediction script
        
        # Command to run YOLOv5 classify prediction
        command = [
            yolov5_env, yolov5_script,
            '--weights', model_path,
            '--source', image_path,
            '--save-txt'
        ]
        
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Process YOLOv5 results (assuming output is in runs/predict-cls/exp/labels/test.txt)
        output_dir = "yolov5/runs/predict-cls"
        exp_dirs = [d for d in os.listdir(output_dir) if d.startswith('exp')]
        latest_exp_dir = exp_dirs[0]
        output_path = os.path.join(output_dir, latest_exp_dir, 'labels', 'test.txt')

        with open(output_path, "r") as f:
            prediction_data = f.readline().strip().split()
            label = prediction_data[1]
            predicted_class = 0 if label == "green_apples" else 1 if label == "red_apples" else 2
            return predicted_class
        
    except subprocess.CalledProcessError as e:
        print(f"Error during YOLOv5 inference: {e.stderr.decode()}")
        return None
    except FileNotFoundError:
        print("Prediction output file not found!")
        return None

# Function to drive the DC motor forward
def drive_dc_motor_forward():
    GPIO.output(DC_ENABLE_PIN, GPIO.HIGH)
    GPIO.output(DC_INPUT_PIN1, GPIO.HIGH)
    GPIO.output(DC_INPUT_PIN2, GPIO.LOW)
    print("DC Motor moving forward")

# Function to stop the DC motor
def stop_dc_motor():
    GPIO.output(DC_INPUT_PIN1, GPIO.LOW)
    GPIO.output(DC_INPUT_PIN2, GPIO.LOW)
    GPIO.output(DC_ENABLE_PIN, GPIO.LOW)
    print("DC Motor stopped")

# Function to move the servo to a certain angle
def move_servo_to_angle(angle):
    duty_cycle = 2 + (angle / 18)
    servo1.ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Wait for the servo to reach the position
    servo1.ChangeDutyCycle(0)

# Sensor interrupt callback function
def sensor_interrupt_callback(channel):
    global redapples  # Declare as global to modify the global variable
    global greenapples
    global yellowapples
    
    if GPIO.input(SENSOR_PIN) == GPIO.HIGH:
        print("Rising edge detected")
        stop_dc_motor()  # Stop motor when rising edge occurs
        capture_image()   # Capture image
        
        # Run YOLOv5 prediction
        predicted_class = predict_with_yolov5('/home/myras/test.jpg')
        print(f"Predicted class: {predicted_class}")
        
        # Handle actions based on the predicted class
        if predicted_class == 0:
            drive_dc_motor_forward()
            greenapples += 1  # Increment the global variable
            data = "redapples: "+str(redapples)+"\n"+" greenapples: "+str(greenapples)+"\n"+"yellowapples: "+str(yellowapples)+"\n"

            with open('output.txt', 'w') as file:
                file.write(data)
                
        elif predicted_class == 1:
            
            redapples += 1  # Increment the global variable
            data = "redapples: "+str(redapples)+"\n"+" greenapples: "+str(greenapples)+"\n"+"yellowapples: "+str(yellowapples)+"\n"
            with open('output.txt', 'w') as file:
                file.write(data)
                
            move_servo_to_angle(105)
            drive_dc_motor_forward()
            time.sleep(4)
            move_servo_to_angle(160)
            
        elif predicted_class == 2:
            
            yellowapples += 1  # Increment the global variable
            data = "redapples: "+str(redapples)+"\n"+" greenapples: "+str(greenapples)+"\n"+"yellowapples: "+str(yellowapples)+"\n"
            with open('output.txt', 'w') as file:
                file.write(data)
                
            drive_dc_motor_forward()
            time.sleep(3)
            move_servo_to_angle(65)
            move_servo_to_angle(160)
        else:
            print("Invalid ColorId")
    else:
        print("Falling edge detected")
        drive_dc_motor_forward()


# Set up interrupt detection on the sensor pin for rising edge
GPIO.add_event_detect(SENSOR_PIN, GPIO.BOTH, callback=sensor_interrupt_callback, bouncetime=10)

# Start the motor moving forward
try:
    drive_dc_motor_forward()
    
    
    # Infinite loop to keep program running and handling the sensor interrupt
    while True:
                                            pass
    
except KeyboardInterrupt:
    print("Program interrupted by user")
    stop_dc_motor()

finally:
    GPIO.cleanup()
    stop_dc_motor()
