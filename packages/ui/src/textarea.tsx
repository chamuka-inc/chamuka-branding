import { type TextareaHTMLAttributes, forwardRef } from "react";
import { cn } from "./lib/cn";

export type TextareaProps = TextareaHTMLAttributes<HTMLTextAreaElement>;

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, ...props }, ref) => (
    <textarea ref={ref} className={cn("ck-textarea ck-focusable", className)} {...props} />
  ),
);
Textarea.displayName = "Textarea";
