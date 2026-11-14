import { Label as UiLabel } from "@ui-sdk/react/label";
import {
  Children,
  cloneElement,
  isValidElement,
  useId,
  type ComponentPropsWithoutRef,
  type ReactElement,
  type ReactNode,
} from "react";
import { cn } from "./lib/cn";

export type LabelProps = ComponentPropsWithoutRef<"label"> & {
  required?: boolean;
};

export function Label({ className, required, children, ...props }: LabelProps) {
  return (
    <UiLabel
      className={cn("text-sm font-medium leading-none text-foreground", className)}
      data-required={required ? "true" : undefined}
      {...props}
    >
      {children}
      {required ? (
        <span className="text-destructive" aria-hidden="true">
          {" "}
          *
        </span>
      ) : null}
    </UiLabel>
  );
}

export function FieldHelp({
  id,
  children,
  className,
}: {
  id?: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <p id={id} className={cn("text-sm text-muted-foreground", className)}>
      {children}
    </p>
  );
}

export function FieldError({
  id,
  children,
  className,
}: {
  id?: string;
  children: ReactNode;
  className?: string;
}) {
  if (!children) return null;
  return (
    <p id={id} className={cn("text-sm font-medium text-destructive", className)} role="alert">
      {children}
    </p>
  );
}

export function Field({
  label,
  htmlFor,
  help,
  error,
  required,
  children,
  className,
}: {
  label?: ReactNode;
  htmlFor?: string;
  help?: ReactNode;
  error?: ReactNode;
  required?: boolean;
  children: ReactNode;
  className?: string;
}) {
  const uid = useId();
  const helpId = help ? `${uid}-help` : undefined;
  const errorId = error ? `${uid}-error` : undefined;
  const describedBy = [helpId, errorId].filter(Boolean).join(" ") || undefined;

  const control = Children.map(children, (child) => {
    if (!isValidElement(child)) return child;
    const el = child as ReactElement<{ id?: string }>;
    return cloneElement(el, {
      id: htmlFor ?? el.props.id,
      "aria-invalid": error ? true : undefined,
      "aria-describedby": describedBy,
      "aria-required": required || undefined,
    } as never);
  });

  return (
    <div className={cn("grid gap-2", className)}>
      {label ? (
        <Label htmlFor={htmlFor} required={required}>
          {label}
        </Label>
      ) : null}
      {control}
      {help ? <FieldHelp id={helpId}>{help}</FieldHelp> : null}
      <FieldError id={errorId}>{error}</FieldError>
    </div>
  );
}
