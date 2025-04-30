"use client";

import Image from "next/image";
import styles from "./page.module.css";
import { useEffect } from "react";
import { io } from "socket.io-client";

export default function Home() {
  useEffect(() => {
    const server = io("http://localhost:8089", {
      transports: ["websocket"],
    }); 

    server.connect();

    server.on("connect", () => {
      server.on("xgb_response", (msg) => {
        console.log("XGB response:", msg);
      });

      server.on("random_forest_response", (msg) => {
        console.log("RandomForest response:", msg);
      });

      server.on("neuron_response", (msg) => {
        console.log("Neuron response:", msg);
      });

      server.emit("xgb", [588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,110,109,108,107,106,105,104,103,102,101,100]);

      server.emit("random_forest", [588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,110,109,108,107,106,105,104,103,102,101,100]);

      server.emit("neuron", [588,580,567,547,532,517,493,485,467,462,459,452,447,438,417,406,396,392,380,372,370,364,359,351,344,329,320,305,298,277,277,273,274,254,240,221,205,196,177,170,164,157,151,128,126,122,122,115,111,110,109,108,107,106,105,104,103,102,101,100]);
    });
  }, [])

  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <Image
          className={styles.logo}
          src="/next.svg"
          alt="Next.js logo"
          width={180}
          height={38}
          priority
        />
        <ol>
          <li>
            Get started by editing <code>src/app/page.tsx</code>.
          </li>
          <li>Save and see your changes instantly.</li>
        </ol>

        <div className={styles.ctas}>
          <a
            className={styles.primary}
            href="https://vercel.com/new?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Image
              className={styles.logo}
              src="/vercel.svg"
              alt="Vercel logomark"
              width={20}
              height={20}
            />
            Deploy now
          </a>
          <a
            href="https://nextjs.org/docs?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.secondary}
          >
            Read our docs
          </a>
        </div>
      </main>
      <footer className={styles.footer}>
        <a
          href="https://nextjs.org/learn?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/file.svg"
            alt="File icon"
            width={16}
            height={16}
          />
          Learn
        </a>
        <a
          href="https://vercel.com/templates?framework=next.js&utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/window.svg"
            alt="Window icon"
            width={16}
            height={16}
          />
          Examples
        </a>
        <a
          href="https://nextjs.org?utm_source=create-next-app&utm_medium=appdir-template&utm_campaign=create-next-app"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Go to nextjs.org →
        </a>
      </footer>
    </div>
  );
}
