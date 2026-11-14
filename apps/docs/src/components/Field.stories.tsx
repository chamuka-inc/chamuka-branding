import type { Meta, StoryObj } from "@storybook/react";
import { Field, Input } from "@chamuka/ui";

const meta: Meta<typeof Field> = { title: "Components/Field", component: Field };
export default meta;

export const WithHelpAndError: StoryObj<typeof Field> = {
  render: () => (
    <Field label="Workspace" htmlFor="ws" help="Lowercase kebab-case" error="Use a shorter name" required>
      <Input id="ws" />
    </Field>
  ),
};
