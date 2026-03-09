import cv2
from backend.utils.logger import get_logger

logger = get_logger("preprocessing")

def extract_roi(frame):
    """
    Extract region of interest(face) in an image
    """
    try:
        frm_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(frm_gray, scaleFactor=1, minNeighbors=5)

        roi_frame = None
        if len(faces) > 0:
            x, y, w, h = faces[0]
            roi_frame = frame[y:y+h, x:x+w]
        
        return roi_frame
    except Exception as e:
        logger.error(f"Roi extraction failed: {e}")

    
        


def resize_frame(frame, width=224, height=224):
    """
    Resizing the frame to the given (width, height).
    """
    try:
        resized = cv2.resize(frame, (width, height))
        return resized
    except Exception as e:
        logger.error(f"Resizing failed: {e}")
        return None

def normalize_frame(frame):
    """
    Scaling pixel values to range [0, 1] for ai processing.
    """
    try:
        frame = frame.astype("float32") / 255.0
        return frame
    except Exception as e:
        logger.error(f"Normalization failed: {e}")
        return None


def bgr_to_rgb(frame):
    """
    Converting BGR frame to RGB image.
    """
    try:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame_rgb
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return None
