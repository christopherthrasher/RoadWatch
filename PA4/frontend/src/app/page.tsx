import { Container } from "@/components/Container";
import Image from "next/image";

export default function Home() {
  return (
    <Container>
      <div className="flex">
        <p>home page</p>
        <Image
          src={"/globe.svg"}
          alt="globe icon"
          width={256}
          height={256}
          className="object-cover"
          loading="eager"
          rel="preload"
          fetchPriority="high"
        />
      </div>
    </Container>
  );
}
