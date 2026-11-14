import { Slot } from "@radix-ui/react-slot";
import { type AnchorHTMLAttributes, forwardRef } from "react";
import { cn } from "./lib/cn";

export type LinkProps = AnchorHTMLAttributes<HTMLAnchorElement> & {
  asChild?: boolean;
};

export const Link = forwardRef<HTMLAnchorElement, LinkProps>(
  ({ className, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "a";
    return <Comp ref={ref} className={cn("ck-link ck-focusable", className)} {...props} />;
  },
);
Link.displayName = "Link";
