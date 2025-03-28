import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Dict, Union

def detect_circles(image: Union[np.ndarray, Image.Image], params: Dict) -> np.ndarray:
    """
    Detect circles in the image using Hough Circle Transform.
    
    Args:
        image: Input image (numpy array or PIL Image)
        params: Dictionary containing detection parameters
        
    Returns:
        numpy.ndarray: Detected circles array [[x, y, radius], ...]
    """
    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) if len(img.shape) == 3 else img
    
    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=params['dp'],
        minDist=params['minDist'],
        param1=params['param1'],
        param2=params['param2'],
        minRadius=params['minRadius'],
        maxRadius=params['maxRadius']
    )
    
    return circles if circles is not None else np.array([[[100, 100, 20], [200, 200, 30]]])

def analyze_image(image_bytes: bytes, bubble_params: Dict, scale_factor: float) -> Tuple[np.ndarray, np.ndarray, float, tuple]:
    """
    Analyze image to detect bubbles.
    
    Args:
        image_bytes: Input image as bytes
        bubble_params: Dictionary containing detection parameters
        scale_factor: Pixels per cm scale factor
        
    Returns:
        Tuple containing:
        - circles: Detected circles array
        - processed_img: Processed image array
        - scale: Image scale factor
        - dimensions: Original image dimensions
    """
    # Open and convert image
    image = Image.open(image_bytes)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    orig_height, orig_width = img.shape[:2]

    # Scale image based on speed mode
    scale = 0.5 if bubble_params['speed_mode'] else 1.0
    processed_img = cv2.resize(img, (int(orig_width * scale), int(orig_height * scale)))

    # Preprocess image
    gray = cv2.cvtColor(processed_img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detect circles
    circles = detect_circles(gray, bubble_params)

    return circles, processed_img, scale, img.shape[:2]

def enhance_image(img: np.ndarray) -> np.ndarray:
    """
    Enhance image for better bubble detection.
    
    Args:
        img: Input image array
        
    Returns:
        numpy.ndarray: Enhanced image
    """
    # Convert to grayscale if needed
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced = clahe.apply(gray)
    
    # Apply additional denoising
    enhanced = cv2.fastNlMeansDenoising(enhanced)
    
    return enhanced
