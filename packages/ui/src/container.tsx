import type { HTMLAttributes } from "react";
import { cn } from "./lib/cn";

export function Container({
  className,
  size = "lg",
  ...props
}: HTMLAttributes<HTMLDivElement> & { size?: "sm" | "md" | "lg" | "full" }) {
  return <div className={cn("ck-container", `ck-container--${size}`, className)} {...props} />;
}
