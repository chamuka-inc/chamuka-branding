import * as RadioGroupPrimitive from "@radix-ui/react-radio-group";
import type { ComponentPropsWithoutRef } from "react";
import { cn } from "./lib/cn";

export type RadioGroupProps = ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Root>;

export function RadioGroup({ className, ...props }: RadioGroupProps) {
  return (
    <RadioGroupPrimitive.Root className={cn("ck-stack", className)} {...props} />
  );
}

export type RadioGroupItemProps = ComponentPropsWithoutRef<typeof RadioGroupPrimitive.Item>;

export function RadioGroupItem({ className, ...props }: RadioGroupItemProps) {
  return (
    <RadioGroupPrimitive.Item className={cn("ck-radio ck-focusable", className)} {...props}>
      <RadioGroupPrimitive.Indicator className="ck-radio-dot" />
    </RadioGroupPrimitive.Item>
  );
}
