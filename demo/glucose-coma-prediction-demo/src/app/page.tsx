"use client";

import { useEffect, useState } from "react";
import Button from '@mui/material/Button';
import { io } from "socket.io-client";

export default function Home() {
  const [values, setValues] = useState<number[]>(Array(60).fill(100));
  const [xgbResult, setXgbResult] = useState<string>("");
  const [randomForestResult, setRandomForestResult] = useState<string>("");
  const [neuronResult, setNeuronResult] = useState<string>("");
  const [socket, setSocket] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  useEffect(() => {
    const server = io(process.env.NEXT_PUBLIC_SERVER, {
      transports: ["websocket"],
    });

    server.connect();

    server.on("connect", () => {
      setSocket(server);

      server.on("xgb_response", (msg) => {
        setXgbResult(JSON.stringify(msg, null, 2));
        setIsLoading(false);
      });

      server.on("random_forest_response", (msg) => {
        setRandomForestResult(JSON.stringify(msg, null, 2));
        setIsLoading(false);
      });

      server.on("neuron_response", (msg) => {
        setNeuronResult(JSON.stringify(msg, null, 2));
        setIsLoading(false);
      });
    });

    return () => {
      server.disconnect();
    };
  }, []);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (socket) {
      setIsLoading(true);
      setXgbResult("");
      setRandomForestResult("");
      setNeuronResult("");
      
      socket.emit("xgb", values);
      socket.emit("random_forest", values);
      socket.emit("neuron", values);
    }
  };

  const handleInputChange = (index: number, value: string) => {
    const newValues = [...values];
    newValues[index] = value === "" ? 0 : Number(value);
    
    setValues(newValues);
  };

  const generateRandomValues = () => {
    const randomValues = Array(60).fill(0).map(() => 
      Math.floor(Math.random() * 500) + 100
    );
    
    setValues(randomValues);
  };

  return (
    <div className="app-container">
      <div className="card main-card">
        <header className="app-header">
          <h1>Glucose Coma Prediction</h1>
        </header>
        
        <form onSubmit={handleSubmit}>
          <div className="action-buttons-container">
            <Button 
            variant="contained" 
            onClick={generateRandomValues}>
              Generate Random Values
            </Button>
            
            <Button 
            variant="contained" 
            type="submit">
              Submit
            </Button>
          </div>

          <div className="form-section">
            <h2>Input Values</h2>
            <div className="input-grid">
              {values.map((value, index) => (
                <div key={index} className="input-group">
                  <label htmlFor={`value-${index}`}>{index + 1}</label>
                  <input
                    id={`value-${index}`}
                    type="number"
                    value={value}
                    onChange={(e) => handleInputChange(index, e.target.value)}
                  />
                </div>
              ))}
            </div>
          </div>
        </form>

        <div className="results-section">
          <h2>Received Predictions</h2>
          <div className="results-grid">
            <div className="result-card">
              <div className="result-header">
                <h3>XGBoost Model</h3>
              </div>
              <div className="result-content">
                {isLoading ? (
                  <div className="loader-container">
                    <div className="loader"></div>
                  </div>
                ) : xgbResult ? (
                  <pre>{xgbResult}</pre>
                ) : (
                  <div className="empty-state">
                    <p>No result yet</p>
                  </div>
                )}
              </div>
            </div>
            
            <div className="result-card">
              <div className="result-header">
                <h3>Random Forest Model</h3>
              </div>
              <div className="result-content">
                {isLoading ? (
                  <div className="loader-container">
                    <div className="loader"></div>
                  </div>
                ) : randomForestResult ? (
                  <pre>{randomForestResult}</pre>
                ) : (
                  <div className="empty-state">
                    <p>No result yet</p>
                  </div>
                )}
              </div>
            </div>
            
            <div className="result-card">
              <div className="result-header">
                <h3>Neural Network Model</h3>
              </div>
              <div className="result-content">
                {isLoading ? (
                  <div className="loader-container">
                    <div className="loader"></div>
                  </div>
                ) : neuronResult ? (
                  <pre>{neuronResult}</pre>
                ) : (
                  <div className="empty-state">
                    <p>No result yet</p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}