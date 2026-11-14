import { type HTMLAttributes, forwardRef } from "react";
import { cn } from "./lib/cn";

export const Skeleton = forwardRef<HTMLDivElement, HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("min-h-4 animate-pulse rounded-md bg-muted motion-reduce:animate-none", className)}
      aria-hidden="true"
      {...props}
    />
  ),
);
Skeleton.displayName = "Skeleton";
