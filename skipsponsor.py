import cv2
import numpy as np
import pytesseract

def is_sponsored(frame):
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray)

    keywords = ["sponsored", "ad", "promoted", "free trial"]
    for keyword in keywords:
        if keyword in text.lower():
            return True

    return False

def skip_sponsored(video_path):
    
    cap = cv2.VideoCapture(video_path)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    out = cv2.VideoWriter('Desktop/output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, (frame_width, frame_height))

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if not is_sponsored(frame):
            out.write(frame)

    cap.release()
    out.release()

skip_sponsored("Desktop/nv.mp4")

