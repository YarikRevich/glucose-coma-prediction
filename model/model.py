import sys

from loader import CSVDataset
from tools import get_train_data
from trainer import train_xgb_model, train_random_forest_model

def main(data: str, output: str) -> None:
    """Parses dataset and performs training on multiple model implementations."""
    
    dataset = CSVDataset(data)
    
    X_train, y_train, X_test, y_test = get_train_data(dataset)
    
    train_xgb_model(X_train, y_train, X_test, y_test, output)
    
    train_random_forest_model(X_train, y_train, X_test, y_test, output)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise Exception("Not enough arguments provided!")
    
    main(sys.argv[1], sys.argv[2])