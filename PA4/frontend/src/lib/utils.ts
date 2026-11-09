
export async function GetPotholeData(): Promise<PotholeData[] | null> {
    try {
        const response = await fetch("http://localhost:8000/detections", {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });
        if (!response.ok) {
            throw new Error("Failed to fetch pothole data");
        }
        const data = await response.json();
        console.log("Pothole Data:", data);
        return data;
    } catch (error) {
        console.error("Error fetching pothole data:", error);
        return null;
    }
}

interface PotholeData {
  latitude: Number,
  longitude: Number,
  confidence: Number,
  timestamp: String
}

export async function SetPotholeData(potholeData: PotholeData) {
    try {
        const response = await fetch("http://localhost:8000/detections", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(potholeData),
        })

        if (!response.ok) {
            throw new Error("Failed to send pothole data");
        }

        const data = await response.json();
        console.log("Pothole Data Sent:", data);
        return data;
    } catch (error){
        console.error("Error fetching pothole data:", error);
        return null;
    }
}