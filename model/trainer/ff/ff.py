import torch.nn as nn
import torch.nn.functional as F

__all__ = ["FFNetwork"]

class FFNetwork(nn.Module):
    def __init__(self, input_size):
        super(FFNetwork, self).__init__()
        
        self.network = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(128, 64),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),

            nn.Linear(64, 32),
            nn.BatchNorm1d(32),
            nn.ReLU(),

            nn.Linear(32, 1)
        )
        
        # self.fc1 = nn.Linear(input_size, 1024)
        # self.bn1 = nn.BatchNorm1d(1024)

        # self.fc2 = nn.Linear(1024, 512)
        # self.bn2 = nn.BatchNorm1d(512)

        # self.fc3 = nn.Linear(512, 256)
        # self.bn3 = nn.BatchNorm1d(256)
        
        # self.fc4 = nn.Linear(256, 128)
        # self.bn4 = nn.BatchNorm1d(128)
        
        # self.fc5 = nn.Linear(128, 64)
        # self.bn5 = nn.BatchNorm1d(64)

        # self.fc6 = nn.Linear(64, 1)

        # self.dropout = nn.Dropout(p=0.1)

    def forward(self, x):
        # x = F.leaky_relu(self.bn1(self.fc1(x)))
        # x = self.dropout(x)

        # x = F.relu(self.bn2(self.fc2(x)))
        # x = self.dropout(x)

        # x = F.relu(self.bn3(self.fc3(x)))
        # x = self.dropout(x)
        
        # x = F.relu(self.bn4(self.fc4(x)))
        # x = self.dropout(x)
        
        # x = F.relu(self.bn5(self.fc5(x)))
        # x = self.dropout(x)

        # return self.fc6(x)
        
        return self.network(x)
