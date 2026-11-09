
export interface PotholeData {
  latitude: number;
  longitude: number;
  confidence: number;
  timestamp: string;
}

export interface SavedPotholeData extends PotholeData {
  id: number;
}

export async function GetPotholeData(): Promise<SavedPotholeData[] | null> {
    try {
        const response = await fetch("/api/detections", { method: "GET" });
        if (!response.ok) {
            throw new Error("Failed to fetch pothole data");
        }
        const data: SavedPotholeData[] = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching pothole data:", error);
        return null;
    }
}

export async function SetPotholeData(potholeData: PotholeData){
    try {
        const response = await fetch("/api/detections", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(potholeData),
        })

        if (!response.ok) {
            throw new Error("Failed to send pothole data");
        }

        const data = await response;
        return data;
    } catch (error){
        console.error("Error sending pothole data:", error);
        return null;
    }
}