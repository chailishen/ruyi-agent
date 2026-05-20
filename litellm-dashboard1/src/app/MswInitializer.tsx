"use client";

import { useEffect } from "react";

let workerStarted = false;

export default function MswInitializer({ onReady }: { onReady: () => void }) {
  useEffect(() => {
    if (workerStarted) {
      onReady();
      return;
    }

    async function start() {
      const { setupWorker } = await import("msw/browser");
      const { handlers } = await import("@/mocks/handlers");
      const worker = setupWorker(...handlers);
      await worker.start({
        onUnhandledRequest: "bypass",
        quiet: false,
        serviceWorker: { url: "/mockServiceWorker.js" },
      });
      workerStarted = true;
      onReady();
    }

    start().catch((err) => {
      console.error("[MswInitializer]", err);
      onReady();
    });
  }, [onReady]);

  return null;
}
