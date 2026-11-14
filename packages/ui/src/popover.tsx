import {
  Popover as UiPopover,
  PopoverContent as UiPopoverContent,
  PopoverTrigger as UiPopoverTrigger,
} from "@ui-sdk/react/popover";
import type { ComponentPropsWithoutRef, ReactNode } from "react";
import { asChildRender, type NativeButtonProps } from "./lib/as-child";
import { cn } from "./lib/cn";
import { focusRing, popupSurface } from "./lib/classes";

export function Popover({
  children,
  open,
  defaultOpen,
  onOpenChange,
}: {
  children?: ReactNode;
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}) {
  return (
    <UiPopover
      open={open}
      defaultOpen={defaultOpen}
      onOpenChange={
        onOpenChange
          ? (next) => {
              onOpenChange(next);
            }
          : undefined
      }
    >
      {children}
    </UiPopover>
  );
}

export function PopoverTrigger({
  asChild,
  className,
  children,
  ...props
}: NativeButtonProps & { asChild?: boolean }) {
  const render = asChildRender(asChild, children);
  return (
    <UiPopoverTrigger
      className={cn(!render && focusRing, className)}
      render={render}
      {...props}
    >
      {render ? undefined : children}
    </UiPopoverTrigger>
  );
}

export function PopoverAnchor({
  className,
  ...props
}: ComponentPropsWithoutRef<"span">) {
  return <span className={className} {...props} />;
}

export function PopoverContent({
  className,
  ...props
}: ComponentPropsWithoutRef<"div">) {
  return (
    <UiPopoverContent
      sideOffset={6}
      className={cn(popupSurface, "z-dropdown w-72 p-4", className)}
      {...props}
    />
  );
}
