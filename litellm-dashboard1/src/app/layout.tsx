import type { Metadata } from "next";
import "./globals.css";

import MockProvider from "@/app/MockProvider";
import AntdGlobalProvider from "@/contexts/AntdGlobalProvider";
import ReactQueryProvider from "@/contexts/ReactQueryProvider";

export const metadata: Metadata = {
  title: "LiteLLM Dashboard",
  description: "LiteLLM Proxy Admin UI",
  icons: { icon: "./favicon.ico" },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <MockProvider>
          <ReactQueryProvider>
            <AntdGlobalProvider>{children}</AntdGlobalProvider>
          </ReactQueryProvider>
        </MockProvider>
      </body>
    </html>
  );
}
