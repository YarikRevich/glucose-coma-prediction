import torch
import pickle
from model.trainer.ff.ff import FFNetwork
from torch.nn.modules.container import Sequential
from torch.nn.modules.linear import Linear
from torch.nn.modules.batchnorm import BatchNorm1d
from torch.nn.modules.activation import ReLU
from torch.nn.modules.dropout import Dropout

__all__ = ["get_xgb_model", "get_random_forest_model", "get_neuron_model", "NEURON_MODEL", "XGB_MODEL", "RANDOM_FOREST_MODEL"]

# Represents neuron model name.
NEURON_MODEL = "neuron_model"

# Represents xgb model name.
XGB_MODEL = "xgb_model"

# Represents random forest model name.
RANDOM_FOREST_MODEL = "random_forest_model"

def get_xgb_model(file: str) -> FFNetwork:
    """Loads xgb model."""
    
    return pickle.load(open(f"{file}.xgb", "rb"))

def get_random_forest_model(file: str) -> FFNetwork:
    """Loads random_forest model."""
    
    return pickle.load(open(f"{file}.random_forest", "rb"))

def get_neuron_model(file: str) -> FFNetwork:
    """Loads neuron model."""
    
    torch.serialization.add_safe_globals([FFNetwork, Sequential, Linear, BatchNorm1d, ReLU, Dropout])
    
    return torch.load(f"{file}.neuron")