from model.loader import CSVDataset
from model.tools import get_processed_train_data, get_raw_train_data
from model.trainer import train_xgb_model, train_random_forest_model, train_neural_model

__all__ = ["run"]

def run(data: str, output: str) -> None:
    """Parses dataset and performs training on multiple model implementations."""
    
    dataset = CSVDataset(data)
    
    X_train, y_train, X_test, y_test = get_processed_train_data(dataset)
    
    train_xgb_model(X_train, y_train, X_test, y_test, output)
    
    # train_random_forest_model(X_train, y_train, X_test, y_test, output)
    
    # train_loader, test_loader, valid_loader = get_raw_train_data(dataset)
    
    # train_neural_model(X_train.shape[1], train_loader, test_loader, valid_loader, output)