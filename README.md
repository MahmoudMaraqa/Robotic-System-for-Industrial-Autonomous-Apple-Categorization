# 🍎 Apple Sorting System using Raspberry Pi and CNN

## 📌 Project Overview

The automation of fruit sorting is revolutionizing the food processing industry by enhancing efficiency, lowering operational costs, and reducing human error.

This project introduces an affordable, automated apple sorting system based on color classification. The system is designed with small to mid-sized food processing facilities in mind, offering a cost-effective and scalable alternative to industrial-grade sorting machines.

## 🎯 Objectives

* Automate the apple sorting process based on color (Red, Green, Yellow)
* Utilize low-cost, widely available hardware
* Provide real-time feedback and record-keeping via a web interface
* Improve sorting accuracy and reduce manual labor requirements

## 🧠 How It Works

1. Apples move along a conveyor belt.
2. A **Raspberry Pi 4** captures images using the **Pi Camera Module**.
3. A **Convolutional Neural Network (CNN)** processes each image and classifies the apple by color.
4. The Raspberry Pi activates a **servo motor** to push the apple into the correct bin based on its color.
5. Sorting data is sent to a **web dashboard** that displays:

   * Apple counts per color
   * Logs of past sorting operations

## 🛠️ Hardware Components

* Raspberry Pi 4
* Pi Camera Module
* Infrared sensors
* Servo motor
* Conveyor mechanism (homemade or recycled)
* Power supply

## 💻 Software & Technologies

* Python
* OpenCV
* TensorFlow/Keras (CNN model)
* Flask (for the web server)
* HTML/CSS/JavaScript (web dashboard)
* GPIO (for hardware control)

## 🌐 Web Interface

The web dashboard allows users to:

* Monitor the sorting process in real time
* View apple color statistics
* Access historical records of sorting batches

## 📈 Results & Performance

* High accuracy in color classification (based on testing data)
* Smooth integration of hardware and software
* Reliable real-time feedback through the web interface

## 🚀 Future Improvements

* Add size-based or defect detection
* Improve model accuracy with a larger dataset
* Introduce mobile access to the dashboard
* Optimize conveyor speed based on camera detection
