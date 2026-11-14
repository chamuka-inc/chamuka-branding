import { cva, type VariantProps } from "class-variance-authority";
import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "./lib/cn";

const alertVariants = cva("ck-alert", {
  variants: {
    variant: {
      default: "",
      success: "ck-alert--success",
      warning: "ck-alert--warning",
      danger: "ck-alert--danger",
      info: "ck-alert--info",
    },
  },
  defaultVariants: { variant: "default" },
});

export type AlertProps = HTMLAttributes<HTMLDivElement> &
  VariantProps<typeof alertVariants> & {
    title?: ReactNode;
  };

export function Alert({ className, variant, title, children, ...props }: AlertProps) {
  return (
    <div role="status" className={cn(alertVariants({ variant }), className)} {...props}>
      <div>
        {title ? <p className="ck-alert-title">{title}</p> : null}
        {children ? <div className="ck-alert-body">{children}</div> : null}
      </div>
    </div>
  );
}
