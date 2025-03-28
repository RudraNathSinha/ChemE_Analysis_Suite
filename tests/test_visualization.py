import unittest
import numpy as np
from app.utils.visualization import create_bubble_plot

class TestVisualization(unittest.TestCase):
    def setUp(self):
        self.test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        self.test_circles = np.array([[[50, 50, 20], [70, 70, 15]]])
        self.test_scale = 1.0
        self.test_dimensions = (100, 100)

    def test_create_bubble_plot(self):
        fig = create_bubble_plot(
            self.test_image,
            self.test_circles,
            self.test_scale,
            self.test_dimensions
        )
        self.assertIsNotNone(fig)
        self.assertEqual(fig.layout.width, 800)
        self.assertEqual(fig.layout.height, 800)

if __name__ == '__main__':
    unittest.main()
