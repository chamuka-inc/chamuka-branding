import * as AvatarPrimitive from "@radix-ui/react-avatar";
import type { ComponentPropsWithoutRef } from "react";
import { cn } from "./lib/cn";

export function Avatar({
  className,
  size = "md",
  ...props
}: ComponentPropsWithoutRef<typeof AvatarPrimitive.Root> & {
  size?: "sm" | "md" | "lg";
}) {
  return (
    <AvatarPrimitive.Root className={cn("ck-avatar", `ck-avatar--${size}`, className)} {...props} />
  );
}

export function AvatarImage(props: ComponentPropsWithoutRef<typeof AvatarPrimitive.Image>) {
  return <AvatarPrimitive.Image {...props} />;
}

export function AvatarFallback({
  className,
  ...props
}: ComponentPropsWithoutRef<typeof AvatarPrimitive.Fallback>) {
  return <AvatarPrimitive.Fallback className={cn(className)} {...props} />;
}
