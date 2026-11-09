const backendUrl = (process.env.BACKEND_API_URL ?? "http://localhost:8000").replace(/\/+$/, "");

function forwardResponse(response: Response) {
  return new Response(response.body, {
    status: response.status,
    headers: {
      "Content-Type": response.headers.get("Content-Type") ?? "application/json",
    },
  });
}

function backendUnavailable() {
  return Response.json(
    { detail: "Unable to connect to the pothole data service." },
    { status: 502 }, //502 means invalid upstream response
  );
}

export async function GET() {
  try {
    const response = await fetch(`${backendUrl}/detections`, {
      cache: "no-store",
    });
    return forwardResponse(response);
  } catch (error) {
    console.error("Failed to fetch detections from the backend:", error);
    return backendUnavailable();
  }
}

export async function POST(request: Request) {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return Response.json({ detail: "Request body must be valid JSON." }, { status: 400 });
  }

  try {
    const response = await fetch(`${backendUrl}/detections`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      cache: "no-store",
    });
    return forwardResponse(response);
  } catch (error) {
    console.error("Failed to send detection to the backend:", error);
    return backendUnavailable();
  }
}
