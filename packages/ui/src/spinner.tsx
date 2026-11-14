import { type HTMLAttributes, forwardRef } from "react";
import { cn } from "./lib/cn";

export const Spinner = forwardRef<HTMLSpanElement, HTMLAttributes<HTMLSpanElement>>(
  ({ className, ...props }, ref) => (
    <span
      ref={ref}
      className={cn(
        "inline-block size-5 animate-spin rounded-full border-2 border-border border-t-primary motion-reduce:animate-none",
        className,
      )}
      role="status"
      aria-label="Loading"
      {...props}
    />
  ),
);
Spinner.displayName = "Spinner";
