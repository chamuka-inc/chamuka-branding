import { forwardRef } from "react";
import { Button, type ButtonProps } from "./button";
import { cn } from "./lib/cn";

export type IconButtonProps = Omit<ButtonProps, "size"> & {
  label: string;
  size?: "sm" | "md" | "lg";
};

export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ label, className, size = "md", children, ...props }, ref) => (
    <Button
      ref={ref}
      size="icon"
      aria-label={label}
      className={cn("ck-icon-button", `ck-button--${size}`, className)}
      {...props}
    >
      {children}
    </Button>
  ),
);
IconButton.displayName = "IconButton";
