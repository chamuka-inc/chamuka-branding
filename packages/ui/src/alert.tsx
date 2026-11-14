import { cva, type VariantProps } from "class-variance-authority";
import { type HTMLAttributes, forwardRef, type ReactNode } from "react";
import { cn } from "./lib/cn";

const alertVariants = cva("relative w-full rounded-lg border p-4", {
  variants: {
    variant: {
      default: "border-border bg-card text-card-foreground",
      success: "border-success/30 bg-success/10 text-foreground",
      warning: "border-warning/40 bg-warning/15 text-foreground",
      danger: "border-destructive/30 bg-destructive/10 text-foreground",
      info: "border-info/30 bg-info/10 text-foreground",
    },
  },
  defaultVariants: { variant: "default" },
});

export type AlertProps = HTMLAttributes<HTMLDivElement> &
  VariantProps<typeof alertVariants> & {
    title?: ReactNode;
  };

export const Alert = forwardRef<HTMLDivElement, AlertProps>(
  ({ className, variant, title, children, ...props }, ref) => (
    <div
      ref={ref}
      role="status"
      className={cn(alertVariants({ variant }), className)}
      {...props}
    >
      <div className="grid gap-1">
        {title ? <p className="font-display text-sm font-medium">{title}</p> : null}
        {children ? <div className="text-sm text-muted-foreground">{children}</div> : null}
      </div>
    </div>
  ),
);
Alert.displayName = "Alert";

export { alertVariants };
