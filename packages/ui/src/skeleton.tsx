import type { HTMLAttributes } from "react";
import { cn } from "./lib/cn";

export function Skeleton({ className, style, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("ck-skeleton", className)}
      style={{ minHeight: 16, ...style }}
      aria-hidden="true"
      {...props}
    />
  );
}
