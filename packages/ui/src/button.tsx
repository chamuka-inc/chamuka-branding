import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { type ButtonHTMLAttributes, forwardRef } from "react";
import { cn } from "./lib/cn";

const buttonVariants = cva("ck-button ck-focusable", {
  variants: {
    variant: {
      primary: "ck-button--primary",
      secondary: "ck-button--secondary",
      outline: "ck-button--outline",
      ghost: "ck-button--ghost",
      destructive: "ck-button--destructive",
      link: "ck-button--link",
    },
    size: {
      sm: "ck-button--sm",
      md: "ck-button--md",
      lg: "ck-button--lg",
      icon: "ck-button--icon ck-button--md",
    },
  },
  defaultVariants: {
    variant: "primary",
    size: "md",
  },
});

export type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  };

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, type = "button", ...props }, ref) => {
    const Comp = asChild ? Slot : "button";
    return (
      <Comp
        className={cn(buttonVariants({ variant, size }), className)}
        ref={ref}
        type={asChild ? undefined : type}
        {...props}
      />
    );
  },
);
Button.displayName = "Button";

export { buttonVariants };
