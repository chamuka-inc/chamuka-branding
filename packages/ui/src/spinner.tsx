import type { HTMLAttributes } from "react";
import { cn } from "./lib/cn";

export function Spinner({ className, ...props }: HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn("ck-spinner", className)}
      role="status"
      aria-label="Loading"
      {...props}
    />
  );
}
