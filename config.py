import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')

TARGET_COL = 'amount' # Will dynamically read from dataset if needed
DATE_COL = 'date'

# Hyperparameters
TEST_SIZE_RATIO = 0.2
RANDOM_STATE = 42

os.makedirs(DATA_DIR, exist_ok=True)
