import numpy as np
import xgboost as xgb
import pickle
from tools import check_accuracy
from sklearn.ensemble import RandomForestRegressor

__all__ = ["train_xgb_model", "train_random_forest_model", "train_neural_model"]

def train_xgb_model(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, output: str) -> None:
    """Trains XGB regression model with provided data."""
    
    print("Training XGB model!")

    model = xgb.XGBClassifier(
        objective='binary:logistic',
        n_estimators=300,
        learning_rate=0.1,
        max_depth=10,
        use_label_encoder=False,
        eval_metric='merror'
    )
    
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    
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


def train_neural_model(X_train: np.ndarray, y_train: np.ndarray, X_test: np.ndarray, y_test: np.ndarray, output: str) -> None:
    pass