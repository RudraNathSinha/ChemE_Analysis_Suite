import unittest
import numpy as np
from PIL import Image
import io
import cv2
from app.utils.bubble_detection import detect_circles, analyze_image

class TestBubbleDetection(unittest.TestCase):
    def setUp(self):
        # Create a test image with a white circle
        self.test_image = Image.new('RGB', (200, 200), color='black')
        draw = Image.Draw(self.test_image)
        draw.ellipse([50, 50, 150, 150], fill='white')
        
        img_byte_arr = io.BytesIO()
        self.test_image.save(img_byte_arr, format='PNG')
        self.test_image_bytes = img_byte_arr.getvalue()
        
        self.bubble_params = {
            'dp': 1.2,
            'minDist': 20,
            'param1': 50,
            'param2': 30,
            'minRadius': 0,
            'maxRadius': 100,
            'speed_mode': True
        }

    def test_detect_circles(self):
        circles = detect_circles(self.test_image, self.bubble_params)
        self.assertIsInstance(circles, np.ndarray)
        self.assertEqual(len(circles[0]), 1)  # Should detect one circle

    def test_analyze_image(self):
        circles, processed_img, scale, dims = analyze_image(
            self.test_image_bytes,
            self.bubble_params,
            100.0
        )
        self.assertIsInstance(circles, np.ndarray)
        self.assertEqual(len(dims), 2)
        self.assertTrue(0 < scale <= 1)
        self.assertEqual(processed_img.shape[:2], (100, 100))  # Test scaled dimensions

if __name__ == '__main__':
    unittest.main()
