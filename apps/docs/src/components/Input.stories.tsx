import type { Meta, StoryObj } from "@storybook/react";
import { Field, Input } from "@chamuka/ui";

const meta: Meta<typeof Input> = { title: "Components/Input", component: Input };
export default meta;

export const Default: StoryObj<typeof Input> = {
  render: () => (
    <Field label="Email" htmlFor="email" help="Work email">
      <Input id="email" placeholder="name@chamuka.ai" />
    </Field>
  ),
};

export const Error: StoryObj<typeof Input> = {
  render: () => (
    <Field label="Email" htmlFor="email-err" error="Enter an email">
      <Input id="email-err" />
    </Field>
  ),
};
