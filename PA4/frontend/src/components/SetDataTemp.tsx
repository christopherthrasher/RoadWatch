'use client'

import { useState } from "react";
import { SetPotholeData } from "@/lib/utils";

const tempData = {
  latitude: -90,
  longitude: -180,
  confidence: 0,
  timestamp: "2026-11-09T04:04:47.170Z"
}

export function SetDataTemp() {
  const [result, setResult] = useState<Awaited<ReturnType<typeof SetPotholeData>>>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSetData() {
    setLoading(true);
    setError(null);
    const response = await SetPotholeData(tempData);
    setResult(response);
    if (response === null) {
      setError("Failed to save pothole data.");
    }
    setLoading(false);
  }

  return (
    <div>
      <button
        onClick={handleSetData}
        disabled={loading}
        className="px-4 py-2 bg-main-primary text-main-text rounded-md hover:bg-main-secondary focus:outline-none disabled:opacity-50"
      >
        {loading ? "Saving..." : "Set Pothole Data"}
      </button>
      <div>
        {error && <p role="alert">{error}</p>}
        {result !== null && <pre>{JSON.stringify(result, null, 2)}</pre>}
      </div>
    </div>
  );
}