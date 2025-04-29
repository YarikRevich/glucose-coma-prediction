import torch.nn as nn
import torch.nn.functional as F

__all__ = ["FFNetwork"]

class FFNetwork(nn.Module):
    # In the initialization we define the weights of the model:
    def __init__(self, input_size):
        super(FFNetwork, self).__init__()
        # Hidden layer 1:
        self.fc1 = nn.Linear(in_features=input_size, out_features=128, bias=True)
        # Hidden layer 2:
        self.fc2 = nn.Linear(128, 64)
        # Output (final) layer:
        self.fc3 = nn.Linear(64, 1)

    # Here we define how the model works:
    def forward(self, x):
        x = F.relu(self.fc1(x))   # 1st hidden layer
        x = F.relu(self.fc2(x))   # 2nd hidden layer
        x = self.fc3(x)           # output
        return x