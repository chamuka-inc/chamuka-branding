import {
  isValidElement,
  type ComponentPropsWithoutRef,
  type ReactElement,
  type ReactNode,
} from "react";

export type NativeButtonProps = Omit<
  ComponentPropsWithoutRef<"button">,
  "value" | "defaultValue" | "onChange" | "onSelect"
>;
export type NativeDivProps = Omit<
  ComponentPropsWithoutRef<"div">,
  "value" | "defaultValue" | "onChange" | "onSelect"
>;
export type NativeInputProps = Omit<
  ComponentPropsWithoutRef<"input">,
  "value" | "defaultValue" | "onChange" | "onSelect"
>;

/** Maps our `asChild` API onto UI SDK's `render` element. */
export function asChildRender(
  asChild: boolean | undefined,
  children: ReactNode,
): ReactElement<Record<string, unknown>> | undefined {
  if (!asChild || !isValidElement(children)) return undefined;
  return children as ReactElement<Record<string, unknown>>;
}
