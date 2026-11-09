import { Container } from "@/components/Container";
import { GetDataTemp } from "@/components/GetDataTemp";
import Image from "next/image";

export default function Home() {

  return (
    <Container>
      <div className="flex-col">
        <p>home page with a button that gets pothole data and displays it RAW</p>
        
        <GetDataTemp />

      </div>
    </Container>
  );
}
