import type { Meta, StoryObj } from "@storybook/react";
import { color, semantic } from "@chamuka/tokens";

const meta: Meta = {
  title: "Foundations/Colour",
};
export default meta;

function Swatch({ name, hex }: { name: string; hex: string }) {
  return (
    <div className="sb-swatch">
      <div className="sb-swatch-chip" style={{ background: hex }} />
      <div className="sb-swatch-meta">
        <strong>{name}</strong>
        <div>{hex}</div>
      </div>
    </div>
  );
}

export const Core: StoryObj = {
  render: () => (
    <div className="sb-swatch-grid">
      {(["ember", "gold", "slate", "paper", "mist", "ink", "muted"] as const).map((name) => (
        <Swatch key={name} name={name} hex={color[name]} />
      ))}
    </div>
  ),
};

export const Semantic: StoryObj = {
  render: () => (
    <div className="sb-swatch-grid">
      {(["success", "warning", "danger", "info", "play", "forest", "mineral"] as const).map(
        (name) => (
          <Swatch key={name} name={name} hex={color[name]} />
        ),
      )}
    </div>
  ),
};

export const NeutralRamp: StoryObj = {
  render: () => (
    <div className="sb-swatch-grid">
      {Object.entries(color.neutral).map(([step, hex]) => (
        <Swatch key={step} name={`neutral-${step}`} hex={hex} />
      ))}
    </div>
  ),
};

export const LightTheme: StoryObj = {
  render: () => (
    <div className="sb-swatch-grid">
      {Object.entries(semantic.light)
        .filter(([key]) => key !== "productAccent")
        .map(([name, hex]) => (
          <Swatch key={name} name={name} hex={String(hex)} />
        ))}
    </div>
  ),
};
