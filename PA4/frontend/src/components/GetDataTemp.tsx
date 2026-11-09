'use client'

import { useState } from "react";
import { GetPotholeData } from "@/lib/utils";

export function GetDataTemp() {
  const [data, setData] = useState<Awaited<ReturnType<typeof GetPotholeData>>>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleGetData() {
    setLoading(true);
    setError(null);

    try {
      const result = await GetPotholeData();
      if (result === null) {
        setError("Failed to load pothole data.");
        setData(null);
      } else {
        setData(result);
      }
    } catch (error) {
      console.error("Error fetching pothole data:", error);
      setError("Failed to load pothole data.");
      setData(null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button
        onClick={handleGetData}
        disabled={loading}
        className="px-4 py-2 bg-main-primary text-main-text rounded-md hover:bg-main-secondary focus:outline-none"
      >
        {loading ? "Loading..." : "Get Pothole Data"}
      </button>
      <div>
        {error && <p role="alert">{error}</p>}
        {data !== null && <pre>{JSON.stringify(data, null, 2)}</pre>}
      </div>
    </div>
  );
}