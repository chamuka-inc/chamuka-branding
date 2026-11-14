import * as SwitchPrimitive from "@radix-ui/react-switch";
import type { ComponentPropsWithoutRef } from "react";
import { cn } from "./lib/cn";

export type SwitchProps = ComponentPropsWithoutRef<typeof SwitchPrimitive.Root>;

export function Switch({ className, ...props }: SwitchProps) {
  return (
    <SwitchPrimitive.Root className={cn("ck-switch ck-focusable", className)} {...props}>
      <SwitchPrimitive.Thumb className="ck-switch-thumb" />
    </SwitchPrimitive.Root>
  );
}
