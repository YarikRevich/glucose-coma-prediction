// "use client";

// import Image from "next/image";
// import styles from "./page.module.css";
// import { useEffect } from "react";
// import { io } from "socket.io-client";

// export default function Home() {
//   useEffect(() => {
//     const server = io("http://localhost:8089", {
//       transports: ["websocket"],
//     }); 

//     server.connect();

//     server.on("connect", () => {
//       server.on("xgb_response", (msg) => {
//         console.log("XGB response:", msg);
//       });

//       server.on("random_forest_response", (msg) => {
//         console.log("RandomForest response:", msg);
//       });

//       server.on("neuron_response", (msg) => {
//         console.log("Neuron response:", msg);
//       });

//       server.emit("xgb", [588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,110,109,108,107,106,105,104,103,102,101,100]);

//       server.emit("random_forest", [588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,110,109,108,107,106,105,104,103,102,101,100]);

//       server.emit("neuron", [588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,110,109,108,107,106,105,104,103,102,101,100]);
//     });
//   }, [])

//   return (
//     <div className={styles.page}>
//       <main className={styles.main}>
//         <Image
//           className={styles.logo}
//           src="/next.svg"
//           alt="Next.js logo"
//           width={180}
//           height={38}
//           priority
//         />
//         <ol>
//           <li>
//             Get started by editing <code>src/app/page.tsx</code>.
//           </li>
//           <li>Save and see your changes instantly.</li>
//         </ol>

//         <div className={styles.ctas}>
//           <a
//             className={styles.primary}
//             href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//           >
//             <Image
//               className={styles.logo}
//               src="/vercel.svg"
//               alt="Vercel logomark"
//               width={20}
//               height={20}
//             />
//             Deploy now
//           </a>
//           <a
//             href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
//             target="_blank"
//             rel="noopener noreferrer"
//             className={styles.secondary}
//           >
//             Read our docs
//           </a>
//         </div>
//       </main>
//       <footer className={styles.footer}>
//         <a
//           href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           <Image
//             aria-hidden
//             src="/file.svg"
//             alt="File icon"
//             width={16}
//             height={16}
//           />
//           Learn
//         </a>
//         <a
//           href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           <Image
//             aria-hidden
//             src="/window.svg"
//             alt="Window icon"
//             width={16}
//             height={16}
//           />
//           Examples
//         </a>
//         <a
//           href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           <Image
//             aria-hidden
//             src="/globe.svg"
//             alt="Globe icon"
//             width={16}
//             height={16}
//           />
//           Go to nextjs.org →
//         </a>
//       </footer>
//     </div>
//   );
// }

"use client";

import { useEffect, useState } from "react";
import { io } from "socket.io-client";

export default function Home() {
  const [values, setValues] = useState<number[]>(Array(60).fill(100));
  const [xgbResult, setXgbResult] = useState<string>("");
  const [randomForestResult, setRandomForestResult] = useState<string>("");
  const [neuronResult, setNeuronResult] = useState<string>("");
  const [socket, setSocket] = useState<any>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Connect to the socket server when component mounts
  useEffect(() => {
    const server = io("http://localhost:8089", {
      transports: ["websocket"],
    });

    server.connect();

    server.on("connect", () => {
      console.log("Connected to socket server");
      setSocket(server);

      server.on("xgb_response", (msg) => {
        console.log("XGB response:", msg);
        setXgbResult(JSON.stringify(msg, null, 2));
        setIsLoading(false);
      });

      server.on("random_forest_response", (msg) => {
        console.log("RandomForest response:", msg);
        setRandomForestResult(JSON.stringify(msg, null, 2));
      });

      server.on("neuron_response", (msg) => {
        console.log("Neuron response:", msg);
        setNeuronResult(JSON.stringify(msg, null, 2));
      });
    });

    return () => {
      server.disconnect();
    };
  }, []);

  // Handle form submission
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

  // Handle input change
  const handleInputChange = (index: number, value: string) => {
    const newValues = [...values];
    newValues[index] = value === "" ? 0 : Number(value);
    setValues(newValues);
  };

  // Generate random values
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
            <button 
              type="button" 
              className="action-button generate-button"
              onClick={generateRandomValues}
            >
              <div className="button-content">
                <div className="button-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                    <polyline points="7.5 4.21 12 6.81 16.5 4.21"></polyline>
                    <polyline points="7.5 19.79 7.5 14.6 3 12"></polyline>
                    <polyline points="21 12 16.5 14.6 16.5 19.79"></polyline>
                    <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
                    <line x1="12" y1="22.08" x2="12" y2="12"></line>
                  </svg>
                </div>
                <span className="button-text">Generate Random Values</span>
              </div>
            </button>
            
            <button 
              type="submit" 
              className="action-button submit-button"
              disabled={isLoading}
            >
              <div className="button-content">
                <div className="button-icon">
                  {isLoading ? (
                    <svg className="spinner" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="10"></circle>
                      <path d="M12 6v6l4 2"></path>
                    </svg>
                  ) : (
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                      <polyline points="22 4 12 14.01 9 11.01"></polyline>
                    </svg>
                  )}
                </div>
                <span className="button-text">
                  {isLoading ? "Processing..." : "Test All Models"}
                </span>
              </div>
            </button>
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

      <style jsx>{`
        :root {
          --primary-color: #3b82f6;
          --secondary-color: #64748b;
          --accent-color: #0f172a;
          --background-color: #f8fafc;
          --card-background: #ffffff;
          --border-color: #e2e8f0;
          --text-primary: #1e293b;
          --text-secondary: #64748b;
          --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
          --radius: 8px;
        }

        .app-container {
          min-height: 100vh;
          background-color: var(--background-color);
          padding: 2rem;
          display: flex;
          justify-content: center;
        }
        
        .card {
          background-color: var(--card-background);
          border-radius: var(--radius);
          box-shadow: var(--shadow);
          overflow: hidden;
        }
        
        .main-card {
          width: 100%;
          max-width: 1200px;
          padding: 2rem;
        }
        
        .app-header {
          margin-bottom: 2rem;
          text-align: center;
        }
        
        .app-header h1 {
          font-size: 2.25rem;
          font-weight: 700;
          color: var(--accent-color);
          margin: 0 0 0.5rem 0;
        }
        
        .subtitle {
          color: var(--text-secondary);
          font-size: 1rem;
          margin: 0;
        }
        
        .action-buttons-container {
          display: flex;
          gap: 1.5rem;
          margin-bottom: 2rem;
          justify-content: center;
        }
        
        .action-button {
          position: relative;
          border: none;
          border-radius: 12px;
          cursor: pointer;
          transition: all 0.3s ease;
          overflow: hidden;
          min-width: 220px;
          padding: 0;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        .button-content {
          display: flex;
          align-items: center;
          padding: 0;
          height: 100%;
          width: 100%;
        }
        
        .button-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 1rem;
          height: 100%;
        }
        
        .button-text {
          padding: 1rem 1.5rem 1rem 0;
          font-weight: 600;
          font-size: 0.95rem;
          letter-spacing: 0.025em;
          white-space: nowrap;
        }
        
        .action-button:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
        }
        
        .action-button:active {
          transform: translateY(0);
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .generate-button {
          background: linear-gradient(135deg, #667eea, #764ba2);
          color: white;
        }
        
        .generate-button .button-icon {
          background-color: rgba(255, 255, 255, 0.15);
        }
        
        .submit-button {
          background: linear-gradient(135deg, #3b82f6, #2563eb);
          color: white;
        }
        
        .submit-button .button-icon {
          background-color: rgba(255, 255, 255, 0.15);
        }
        
        .submit-button:disabled {
          background: linear-gradient(135deg, #93c5fd, #60a5fa);
          cursor: not-allowed;
          transform: none;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        
        .form-section, .results-section {
          margin-bottom: 3rem;
        }
        
        h2 {
          font-size: 1.5rem;
          color: var(--accent-color);
          margin-bottom: 1.5rem;
          font-weight: 700;
          text-align: center;
          padding-bottom: 0.75rem;
          position: relative;
        }
        
        h2:after {
          content: '';
          position: absolute;
          bottom: 0;
          left: 50%;
          transform: translateX(-50%);
          width: 60px;
          height: 4px;
          background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
          border-radius: 2px;
        }
        
        .input-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
          gap: 1rem;
          background-color: #f9fafc;
          padding: 1.5rem;
          border-radius: 12px;
          box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
        }
        
        .input-group {
          display: flex;
          flex-direction: column;
          position: relative;
        }
        
        .input-group label {
          font-size: 0.75rem;
          margin-bottom: 0.25rem;
          color: var(--accent-color);
          font-weight: 600;
          display: inline-block;
          background-color: #e2e8f0;
          padding: 0.25rem 0.5rem;
          border-radius: 4px;
          text-align: center;
        }
        
        .input-group input {
          padding: 0.75rem;
          border: 2px solid var(--border-color);
          border-radius: 8px;
          transition: all 0.2s ease;
          font-size: 0.875rem;
          background-color: white;
          text-align: center;
          font-weight: 500;
          color: var(--accent-color);
          box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
        }
        
        .input-group input:focus {
          outline: none;
          border-color: var(--primary-color);
          box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.25);
          transform: translateY(-2px);
        }
        
        .input-group input:hover:not(:focus) {
          border-color: #cbd5e1;
        }
        
        .results-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1.5rem;
        }
        
        .result-card {
          border: none;
          border-radius: 16px;
          overflow: hidden;
          transition: transform 0.3s ease, box-shadow 0.3s ease;
          background-color: white;
          box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .result-card:hover {
          transform: translateY(-4px);
          box-shadow: 0 12px 24px rgba(0, 0, 0, 0.12);
        }
        
        .result-header {
          background: linear-gradient(135deg, #f8fafc, #e2e8f0);
          padding: 1.25rem;
          display: flex;
          align-items: center;
          gap: 0.75rem;
          border-bottom: 2px solid #e2e8f0;
        }
        
        .result-header svg {
          background-color: white;
          padding: 0.5rem;
          border-radius: 50%;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
        }
        
        .result-header h3 {
          margin: 0;
          font-size: 1.125rem;
          font-weight: 700;
          color: var(--accent-color);
          letter-spacing: 0.01em;
        }
        
        .result-content {
          min-height: 250px;
          padding: 1.5rem;
          position: relative;
          background-color: white;
        }
        
        .result-content pre {
          margin: 0;
          white-space: pre-wrap;
          font-family: 'Menlo', 'Monaco', 'Courier New', monospace;
          font-size: 0.875rem;
          color: var(--text-primary);
          background-color: #f8fafc;
          padding: 0.75rem;
          border-radius: var(--radius);
          overflow-x: auto;
        }
        
        .empty-state {
          display: flex;
          align-items: center;
          justify-content: center;
          height: 100%;
          min-height: 150px;
          color: var(--text-secondary);
          text-align: center;
        }
        
        .loader-container {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 150px;
        }
        
        .loader {
          border: 3px solid #f3f3f3;
          border-radius: 50%;
          border-top: 3px solid var(--primary-color);
          width: 24px;
          height: 24px;
          animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
        
        .spinner {
          animation: spin 1s linear infinite;
          margin-right: 0.25rem;
        }
        
        @media (max-width: 768px) {
          .app-container {
            padding: 1rem;
          }
          
          .main-card {
            padding: 1.5rem;
          }
          
          .results-grid {
            grid-template-columns: 1fr;
          }
          
          .action-bar {
            flex-direction: column;
          }
          
          .app-header h1 {
            font-size: 1.75rem;
          }
        }
      `}</style>
    </div>
  );
}