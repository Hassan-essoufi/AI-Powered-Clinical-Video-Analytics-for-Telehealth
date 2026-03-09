import numpy as np
import cv2

def resize_frame(frame, width=224, height=224):
    """
    Resizing the frame to the given (width, height).
    """
    resized = cv2.resize(frame, (width, height))
    return resized

def normalize_frame(fram2):
    """
    Scaling pixel values to range [0, 1] for ai processing.
    """
    frame = frame.astype("float32") / 255.0
    return frame

def bgr_to_rgb(frame):
    """
    Converting BGR frame to RGB image.
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb
