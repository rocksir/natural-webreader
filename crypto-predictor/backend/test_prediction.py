import pandas as pd
import numpy as np
from services.prediction_engine import PredictionEngine

def test_prediction_engine():
    # Create mock data
    data = {
        'time': range(100),
        'open': np.random.uniform(100, 200, 100),
        'high': np.random.uniform(200, 300, 100),
        'low': np.random.uniform(0, 100, 100),
        'close': np.random.uniform(100, 200, 100),
        'volume': np.random.uniform(1000, 2000, 100)
    }
    df = pd.DataFrame(data)

    try:
        result = PredictionEngine.calculate_signals(df)
        print("Success!")
        print(result['overall_signal'])
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prediction_engine()
