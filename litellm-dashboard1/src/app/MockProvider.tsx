"use client";

import LoadingScreen from "@/components/common_components/LoadingScreen";
import { isMockMode } from "@/mocks/config";
import dynamic from "next/dynamic";
import { useCallback, useState } from "react";

const MswInitializer = dynamic(() => import("@/app/MswInitializer"), { ssr: false });

export default function MockProvider({ children }: { children: React.ReactNode }) {
  const [ready, setReady] = useState(!isMockMode());
  const onReady = useCallback(() => setReady(true), []);

  if (!isMockMode()) {
    return <>{children}</>;
  }

  if (!ready) {
    return (
      <>
        <MswInitializer onReady={onReady} />
        <LoadingScreen />
      </>
    );
  }

  return <>{children}</>;
}
