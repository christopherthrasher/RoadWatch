import React from "react";
import { Inter } from "next/font/google";
import { Navbar } from "@/components/Navbar";
import type { Metadata } from "next";
import "./globals.css";

const inter = Inter({subsets: ["latin"]})

export const metadata: Metadata = {
  title: "RoadWatch",
  description: "Pothole detector and mapper",
  icons: "/img/logo.svg" //having an icon.png or icon.svg in app folder works too
};

export default function RootLayout({
  children
}: Readonly<{
  children: React.ReactNode;
}>) /* LayoutRoutes<"/"> */ {
  return (
    <html lang="en" data-lt-installed="true">
      <body className={inter.className}>

        {/* probably wrap all this in a theme provider if dark and light mode */}
        {/* Themeprovider */} {/* uses next-themes pckg need to be installed */}

        <div className="lg:flex">
          <Navbar />
          <main>
            <div>{children}</div>
          </main>
          {/* Footer */}
        </div>
      </body>
    </html>
  );
}
