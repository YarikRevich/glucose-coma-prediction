import torch
from typing import Any
from server.tools import NEURON_MODEL, XGB_MODEL, RANDOM_FOREST_MODEL, get_delta
from model.trainer.ff.ff import FFNetwork
from flask import Flask, request
from flask_socketio import SocketIO, emit

__all__ = ["run"]

app = Flask(__name__)
socketio = SocketIO(app,debug=True,cors_allowed_origins='*',async_mode='eventlet')

# Represents all the loaded models.
models: dict[str, Any] = {
    NEURON_MODEL: None,
    XGB_MODEL: None,
    RANDOM_FOREST_MODEL: None
}

@socketio.on("connect")
def connect():
    pass

@socketio.on("xgb")
def xgb(data: list[float]) -> None:
    slopes = get_delta(data)
    
    prediction = models[XGB_MODEL].predict([data + slopes + get_delta(slopes)])
    
    emit("xgb_response", {"prediction": int(prediction[0])}, room=request.sid)

@socketio.on("random_forest")
def random_forest(data: list[float]) -> None:
    slopes = get_delta(data)
    
    prediction = models[RANDOM_FOREST_MODEL].predict([data + slopes + get_delta(slopes)])
    
    emit("random_forest_response", {"prediction": round(prediction[0])}, room=request.sid)

@socketio.on("neuron")
def neuron(data: list[float]) -> None:
    slopes = get_delta(data)
    
    outputs = models[NEURON_MODEL](torch.tensor([data + slopes + get_delta(slopes)], dtype=torch.float32)).squeeze()
    
    preds = torch.round(torch.sigmoid(outputs)).detach().numpy()
    
    emit("neuron_response", {"prediction": int(preds)}, room=request.sid)

@socketio.on("disconnect")
def disconnect():
    pass

def run(xgb_model: FFNetwork, random_forest_model: FFNetwork, neuron_model: FFNetwork) -> None:
    """Starts REST API server."""
    
    models[XGB_MODEL] = xgb_model
    models[RANDOM_FOREST_MODEL] = random_forest_model
    models[NEURON_MODEL] = neuron_model
    
    socketio.run(app, host="0.0.0.0", port=8089)