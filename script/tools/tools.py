from script.generator import generate

__all__ = ["get_train_data", "get_example_data"]

def get_train_data(output: str) -> None:
    """Generates train data."""
    
    generate(f"{output}.train", time=300, additional=True)

def get_example_data(output: str) -> None:
    """Generates example data."""
    
    generate(f"{output}.example", time=300)