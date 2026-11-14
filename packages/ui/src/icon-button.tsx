import { forwardRef } from "react";
import { Button, type ButtonProps } from "./button";
import { cn } from "./lib/cn";

const iconSizes = {
  sm: "size-8",
  md: "size-10",
  lg: "size-11",
} as const;

export type IconButtonProps = Omit<ButtonProps, "size"> & {
  label: string;
  size?: keyof typeof iconSizes;
};

export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ label, className, size = "md", children, ...props }, ref) => (
    <Button
      ref={ref}
      size="icon"
      aria-label={label}
      className={cn(iconSizes[size], className)}
      {...props}
    >
      {children}
    </Button>
  ),
);
IconButton.displayName = "IconButton";
