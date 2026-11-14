import type { CSSProperties, HTMLAttributes } from "react";
import { cn } from "./lib/cn";

export function Stack({
  className,
  direction = "column",
  gap = "4",
  align,
  justify,
  style,
  ...props
}: HTMLAttributes<HTMLDivElement> & {
  direction?: "row" | "column";
  gap?: "1" | "2" | "3" | "4" | "5" | "6" | "8";
  align?: CSSProperties["alignItems"];
  justify?: CSSProperties["justifyContent"];
}) {
  return (
    <div
      className={cn("ck-stack", className)}
      style={{
        flexDirection: direction,
        gap: `var(--spacing-${gap})`,
        alignItems: align,
        justifyContent: justify,
        ...style,
      }}
      {...props}
    />
  );
}
