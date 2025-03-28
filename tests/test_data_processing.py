import unittest
import numpy as np
import pandas as pd
from app.utils.data_processing import validate_data, calculate_dimensionless_numbers

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'Re': [100, 200, 300],
            'Sc': [0.7, 0.7, 0.7],
            'Sh': [10, 15, 20]
        })
        
        self.test_raw_data = {
            'velocity': np.array([1.0, 2.0, 3.0]),
            'diameter': np.array([0.01, 0.01, 0.01]),
            'viscosity': np.array([1e-6, 1e-6, 1e-6]),
            'diffusivity': np.array([1e-9, 1e-9, 1e-9])
        }

    def test_validate_data(self):
        valid, message = validate_data(self.test_data, ['Re', 'Sc', 'Sh'])
        self.assertTrue(valid)
        self.assertEqual(message, "Data validation successful")

    def test_calculate_dimensionless_numbers(self):
        results = calculate_dimensionless_numbers(self.test_raw_data)
        self.assertIn('Re', results)
        self.assertIn('Sc', results)
