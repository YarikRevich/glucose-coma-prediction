import numpy as np
import torch

from server import api
from server.tools import get_xgb_model, get_random_forest_model, get_neuron_model

def run(file: str) -> None:
    """Starts server configuration."""
    
    print("Starting server!")
    
    xgb_model = get_xgb_model(file)
    
    random_forest_model = get_random_forest_model(file)
    
    neuron_model = get_neuron_model(file)
    
    api.run(xgb_model, random_forest_model, neuron_model)