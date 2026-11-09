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

  async function handleSetData() {
    const response = await SetPotholeData(tempData);
    setResult(response);
  }

  return (
    <div>
      <button
        onClick={handleSetData}
        className="px-4 py-2 bg-main-primary text-main-text rounded-md hover:bg-main-secondary focus:outline-none"
      >
        Set Pothole Data
      </button>
      <div>
        {result !== null && <pre>{JSON.stringify(result, null, 2)}</pre>}
      </div>
    </div>
  );
}