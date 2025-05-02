import numpy as np
from model.loader import CSVDataset
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay

__all__ = ["get_processed_train_data", "get_raw_train_data", "check_accuracy"]

def get_processed_train_data(dataset: CSVDataset) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Splits provided raw dataset into train and test arrays."""
    
    train_dataset, test_dataset = random_split(dataset, [0.8, 0.2])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=True)
    
    X_train = []
    y_train = []

    for features, labels in train_loader:
        X_train.append(features.numpy())
        y_train.append(labels.numpy())

    X_train = np.concatenate(X_train, axis=0)
    y_train = np.concatenate(y_train, axis=0)

    X_test = []
    y_test = []

    for features, labels in test_loader:
        X_test.append(features.numpy())
        y_test.append(labels.numpy())

    X_test = np.concatenate(X_test, axis=0)
    y_test = np.concatenate(y_test, axis=0)
    
    return (X_train, y_train, X_test, y_test)


def get_raw_train_data(dataset: CSVDataset) -> tuple[DataLoader, DataLoader, DataLoader]:
    """Splits provided raw dataset into train, test and validation arrays."""
    
    train_dataset, test_dataset, valid_dataset = random_split(dataset, [0.6, 0.3, 0.2])
    
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=True)
    
    valid_loader = DataLoader(valid_dataset, batch_size=32, shuffle=True)
    
    return (train_loader, test_loader, valid_loader)


def check_accuracy(y_test: np.ndarray, y_pred: np.ndarray) -> None:
    """Checks accuracy of the received predictions."""
    
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)
    
    print(f"Test Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC AUC:   {roc_auc:.4f}")
    print(f"Confusion Matrix: True Negative = {cm[0][0]}; False Positive = {cm[0][1]}; False Negative = {cm[1][0]}; True Positive = {cm[1][1]}")