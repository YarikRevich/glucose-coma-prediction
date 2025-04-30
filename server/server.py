import numpy as np
import torch

from server import api
from model.trainer.ff.ff import FFNetwork
from torch.nn.modules.container import Sequential
from torch.nn.modules.linear import Linear
from torch.nn.modules.batchnorm import BatchNorm1d
from torch.nn.modules.activation import ReLU
from torch.nn.modules.dropout import Dropout


def run(file: str) -> None:
    """Starts server configuration."""
    
    torch.serialization.add_safe_globals([FFNetwork, Sequential, Linear, BatchNorm1d, ReLU, Dropout])
    
    model = torch.load(f"{file}.neuron")
    
    q = [[588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,110,109,108,107,106,105,104,103,102,101,100]]
    
    q_tensor = torch.tensor(q, dtype=torch.float32)
    
    outputs = model(q_tensor).squeeze()
    
    probs = torch.sigmoid(outputs)
    preds = torch.round(probs)
    
    print(preds.detach().numpy())
    
    api.run()