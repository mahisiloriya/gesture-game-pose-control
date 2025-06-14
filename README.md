# Subway Surfers Gesture Control 

**Play Subway Surfers using real-time body movements detected via webcam.**

## 🧠 What Is This?

This Python application captures your body pose using a webcam and translates physical movements—leaning left/right or jumping/crouching—into keyboard commands to control Subway Surfers in real time.

## Why It Matters

- Demonstrates real-time Human–Computer Interaction using open-source tools  
- Combines MediaPipe, OpenCV, and PyAutoGUI for a complete gesture-to-action pipeline  
- Great example of practical pose detection that interacts with real applications  

## Built With

- **Python 3.12.6**
- [MediaPipe](https://mediapipe.dev) – pose estimation  
- [OpenCV](https://opencv.org) – video input and image processing  
- [PyAutoGUI](https://pyautogui.readthedocs.io) – keyboard control automation  
- [Matplotlib](https://matplotlib.org) – visualization (optional/display mode)  

## Prerequisites

Install the required Python packages:

```bash
pip install opencv-python mediapipe pyautogui matplotlib
