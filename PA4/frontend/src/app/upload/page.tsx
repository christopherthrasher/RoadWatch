import { Container } from "@/components/Container";
import { SetDataTemp } from "@/components/SetDataTemp";
import Image from "next/image";

export default function Upload() {
  return (
    <Container>
      <div className="flex-col">
              <p>upload page with a button that sets temp pothole data</p>
              <p>Current Data being set is the following:</p>
              <p>
                latitude: -90,
                longitude: -180,
                confidence: 0,
                timestamp: "2026-11-09T04:04:47.170Z"
              </p>
              
              <SetDataTemp />

            </div>
    </Container>
  );
}
