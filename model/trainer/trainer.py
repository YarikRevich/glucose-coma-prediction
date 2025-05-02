import numpy as np
import xgboost as xgb
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from model.tools import check_accuracy
from model.trainer.ff import FFNetwork
from sklearn.ensemble import RandomForestRegressor

__all__ = ["train_xgb_model", "train_random_forest_model", "train_neural_model"]

def train_xgb_model(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, output: str) -> None:
    """Trains XGB regression model with provided data."""
    
    print("Training XGB model!")
    
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        use_label_encoder=False,
        eval_metric='logloss',
        scale_pos_weight=3.01
    )
    
    model.fit(X_train, y_train)

    y_pred = (model.predict_proba(X_test)[:, 1] > 0.3).astype(int)
    
    check_accuracy(y_test, y_pred)
    
    pickle.dump(model, open(f"{output}.xgb", "wb"))
    
def train_random_forest_model(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, output: str) -> None:
    """Trains RandomForest regression model with provided data."""
    
    print("Training RandomForest model!")
    
    model = RandomForestRegressor(n_estimators=100, max_features=100, random_state=0)
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    
    y_pred = [round(x) for x in y_pred]

    check_accuracy(y_test, y_pred)
    
    pickle.dump(model, open(f"{output}.random_forest", "wb"))


# Represents max amount of epochs used for neural network model training.
MAX_EPOCHS = 100

# Represents patience level used to wait for loss updates before stoping training process.
PATIENCE = 10

def train_neural_model(size: int, train_loader: DataLoader, test_loader: DataLoader, valid_loader: DataLoader, output: str) -> None:
    """Trains NeuralNetwork model with provided data."""
    
    print("Training NeuralNetwork model!")
    
    device = torch.device("cpu")
    
    model = FFNetwork(size).to(device)
    
    criterion = nn.BCEWithLogitsLoss()
    
    optimizer = optim.Adam(model.parameters(), lr=0.0005)
    
    dataloaders = {"train": train_loader, "val": valid_loader, "test": test_loader}

    patience = 100
    best_val_loss = float('inf')
    epochs_without_improvement = 0

    losses = {"train": [], "val": []}

    all_preds = {"train": [], "val": []}
    all_labels = {"train": [], "val": []}

    for epoch in range(MAX_EPOCHS):
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            total_samples = 0

            for inputs, labels in dataloaders[phase]:
                inputs, labels = inputs.to(device), labels.to(device)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs).squeeze()

                    probs = torch.sigmoid(outputs)
                    preds = torch.round(probs)

                    all_preds[phase].extend(preds.detach().cpu().numpy())
                    all_labels[phase].extend(labels.cpu().numpy())

                    loss = criterion(outputs, labels)
                    running_loss += loss.item() * inputs.size(0)
                    total_samples += inputs.size(0)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

            epoch_loss = running_loss / total_samples
            losses[phase].append(epoch_loss)

            print(f"Epoch: {epoch + 1} Phase: {phase} Loss: {epoch_loss:.4e}")

            if phase == 'val':
                if epoch_loss < best_val_loss:
                    best_val_loss = epoch_loss
                    epochs_without_improvement = 0
                else:
                    epochs_without_improvement += 1
                    print(f"No improvement in {epochs_without_improvement} epochs.")

        if epochs_without_improvement >= patience:
            print(f"Early stopping at epoch {epoch + 1}.")
            break

    for phase in ["train", "val"]:
        check_accuracy(all_labels[phase], all_preds[phase])
        
    torch.save(model, f"{output}.neuron")