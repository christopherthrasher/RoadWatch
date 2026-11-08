import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import React from "react";

const inter = Inter({subsets: ["latin"]})

export const metadata: Metadata = {
  title: "RoadWatch",
  description: "Pothole detector and mapper",
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) /* LayoutRoutes<"/"> */ {
  return (
    <html lang="en">
      <body className={inter.className}>
        {/* probably wrap all this in a theme provider if dark and light mode */}
        {/* Navbar */}
        <main>
          <div>{children}</div>
        </main>
        {/* Footer */}
      </body>
    </html>
  );
}
