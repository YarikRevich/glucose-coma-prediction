from flask import Flask

__all__ = ["run"]

app = Flask(__name__)

def run() -> None:
    """Starts REST API server."""
    
    app.run(host="0.0.0.0", port=8089)