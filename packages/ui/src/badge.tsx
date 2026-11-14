import { cva, type VariantProps } from "class-variance-authority";
import type { HTMLAttributes } from "react";
import { cn } from "./lib/cn";

const badgeVariants = cva("ck-badge", {
  variants: {
    variant: {
      default: "ck-badge--default",
      secondary: "ck-badge--secondary",
      outline: "ck-badge--outline",
      success: "ck-badge--success",
      warning: "ck-badge--warning",
      danger: "ck-badge--danger",
    },
  },
  defaultVariants: { variant: "default" },
});

export type BadgeProps = HTMLAttributes<HTMLSpanElement> & VariantProps<typeof badgeVariants>;

export function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}
