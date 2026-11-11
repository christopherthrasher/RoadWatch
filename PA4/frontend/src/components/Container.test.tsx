import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { Container } from "./Container";

describe("Container", () => {
  it("renders its children and optional class name", () => {
    render(
      <Container className="test-class">
        <span>Hello</span>
      </Container>
    );

    const child = screen.getByText("Hello");
    expect(child).toBeTruthy();
    expect(child.parentElement?.className).toContain("container");
    expect(child.parentElement?.className).toContain("test-class");
  });
});