import pandas as pd
import torch
from torch.utils.data import Dataset

__all__ = ["CSVDataset"]

class CSVDataset(Dataset):
    """Represents custom dataset loader used for CSV sample file."""
    
    def __init__(self, csv_file):
        self.data = pd.read_csv(csv_file)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        
        features = torch.tensor(row[:-1].values, dtype=torch.float32)
        label = torch.tensor(row[-1], dtype=torch.float32)

        return features, label

