import {
  Menu,
  MenuContent,
  MenuGroup,
  MenuGroupLabel,
  MenuItem,
  MenuSeparator,
  MenuTrigger,
} from "@ui-sdk/react/menu";
import { useId, type ComponentPropsWithoutRef, type ReactNode } from "react";
import { asChildRender, type NativeButtonProps, type NativeDivProps } from "./lib/as-child";
import { cn } from "./lib/cn";
import { focusRing, itemInteractive, popupSurface } from "./lib/classes";

export function DropdownMenu({
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
    <Menu
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
    </Menu>
  );
}

export function DropdownMenuTrigger({
  asChild,
  className,
  children,
  ...props
}: NativeButtonProps & { asChild?: boolean }) {
  const render = asChildRender(asChild, children);
  return (
    <MenuTrigger className={cn(!render && focusRing, className)} render={render} {...props}>
      {render ? undefined : children}
    </MenuTrigger>
  );
}

export function DropdownMenuPortal({ children }: { children?: ReactNode }) {
  return <>{children}</>;
}

export function DropdownMenuGroup({ className, ...props }: NativeDivProps) {
  return <MenuGroup className={className} {...props} />;
}

export function DropdownMenuContent({
  className,
  ...props
}: NativeDivProps) {
  return (
    <MenuContent
      sideOffset={6}
      className={cn(popupSurface, "z-dropdown min-w-32 p-1", className)}
      {...props}
    />
  );
}

export function DropdownMenuItem({
  className,
  children,
  disabled,
  onSelect,
  ...props
}: NativeDivProps & {
  disabled?: boolean;
  onSelect?: () => void;
}) {
  const generated = useId();
  const value = typeof children === "string" ? children : generated;
  return (
    <MenuItem
      value={value}
      label={typeof children === "string" ? children : undefined}
      disabled={disabled}
      onSelect={onSelect}
      className={cn(itemInteractive, className)}
      {...props}
    >
      {children}
    </MenuItem>
  );
}

export function DropdownMenuSeparator({
  className,
  ...props
}: NativeDivProps) {
  return <MenuSeparator className={cn("-mx-1 my-1 h-px bg-border", className)} {...props} />;
}

export function DropdownMenuLabel({
  className,
  ...props
}: ComponentPropsWithoutRef<"div">) {
  return (
    <MenuGroupLabel
      className={cn("px-2 py-1.5 text-sm font-medium text-foreground", className)}
      {...props}
    />
  );
}
