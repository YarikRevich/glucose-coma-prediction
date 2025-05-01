from script.generator import generate
from script.tools import get_train_data, get_example_data

__all__ = ["run"]

def run(output: str) -> None:
    """Starts data generation."""
    
    get_train_data(output)
    
    get_example_data(output)