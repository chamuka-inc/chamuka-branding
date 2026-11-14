import * as LabelPrimitive from "@radix-ui/react-label";
import {
  Children,
  cloneElement,
  isValidElement,
  useId,
  type ComponentPropsWithoutRef,
  type ReactNode,
} from "react";
import { cn } from "./lib/cn";

export type LabelProps = ComponentPropsWithoutRef<typeof LabelPrimitive.Root> & {
  required?: boolean;
};

export function Label({ className, required, ...props }: LabelProps) {
  return (
    <LabelPrimitive.Root
      className={cn("ck-label", className)}
      data-required={required ? "true" : undefined}
      {...props}
    />
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
    <p id={id} className={cn("ck-field-help", className)}>
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
    <p id={id} className={cn("ck-field-error", className)} role="alert">
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
    return cloneElement(child, {
      id: htmlFor ?? (child.props as { id?: string }).id,
      "aria-invalid": error ? true : undefined,
      "aria-describedby": describedBy,
      "aria-required": required || undefined,
    } as Record<string, unknown>);
  });

  return (
    <div className={cn("ck-field", className)}>
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
