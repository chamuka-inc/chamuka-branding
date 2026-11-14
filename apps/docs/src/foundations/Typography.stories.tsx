import type { Meta, StoryObj } from "@storybook/react";
import { fontSize, lineHeight } from "@chamuka/tokens";

const meta: Meta = { title: "Foundations/Typography" };
export default meta;

const steps = ["display", "h1", "h2", "h3", "h4", "body", "small", "caption", "code"] as const;

export const Scale: StoryObj = {
  render: () => (
    <div>
      {steps.map((step) => (
        <p
          key={step}
          className="sb-type-row"
          style={{
            fontFamily: step === "code" ? "var(--font-mono)" : step === "body" || step === "small" || step === "caption" ? "var(--font-sans)" : "var(--font-display)",
            fontSize: fontSize[step],
            lineHeight: lineHeight[step],
            fontWeight: step === "h4" ? 500 : step === "body" || step === "small" || step === "caption" || step === "code" ? 400 : 600,
            margin: "0 0 16px",
          }}
        >
          {step} — {fontSize[step]} / {lineHeight[step]} — The morning holds.
        </p>
      ))}
    </div>
  ),
};
