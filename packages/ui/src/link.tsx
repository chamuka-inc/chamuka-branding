import { Slot } from "@radix-ui/react-slot";
import { type AnchorHTMLAttributes, forwardRef } from "react";
import { cn } from "./lib/cn";
import { focusRing } from "./lib/classes";

export type LinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  asChild?: boolean;
};

export const Link = forwardRef<HTMLAnchorElement, LinkProps>(
  ({ className, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "a";
    return (
      <Comp
        ref={ref}
        className={cn(
          "font-medium text-primary underline-offset-4 hover:underline",
          "motion-reduce:transition-none",
          focusRing,
          className,
        )}
        {...props}
      />
    );
  },
);
Link.displayName = "Link";
