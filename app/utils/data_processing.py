import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def validate_data(data: pd.DataFrame, required_columns: List[str]) -> Tuple[bool, str]:
    """Validate input data for required columns and data types."""
    missing_cols = [col for col in required_columns if col not in data.columns]
    if missing_cols:
        return False, f"Missing required columns: {', '.join(missing_cols)}"
    
    numeric_error = False
    for col in required_columns:
        if not np.issubdtype(data[col].dtype, np.number):
            numeric_error = True
            break
    
    if numeric_error:
        return False, "All required columns must contain numeric data"
    
    return True, "Data validation successful"

def calculate_dimensionless_numbers(data: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
    """Calculate additional dimensionless numbers if needed."""
    results = data.copy()
    
    if 'velocity' in data and 'diameter' in data and 'viscosity' in data:
        results['Re'] = data['velocity'] * data['diameter'] / data['viscosity']
    
    if 'diffusivity' in data and 'viscosity' in data:
        results['Sc'] = data['viscosity'] / data['diffusivity']
    
    return results
