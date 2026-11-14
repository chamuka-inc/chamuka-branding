import { type InputHTMLAttributes, forwardRef } from "react";
import { cn } from "./lib/cn";

export type InputProps = InputHTMLAttributes<HTMLInputElement>;

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, type = "text", ...props }, ref) => (
    <input ref={ref} type={type} className={cn("ck-input ck-focusable", className)} {...props} />
  ),
);
Input.displayName = "Input";
