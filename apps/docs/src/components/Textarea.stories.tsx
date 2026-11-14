import type { Meta, StoryObj } from "@storybook/react";
import { Field, Textarea } from "@chamuka/ui";

const meta: Meta<typeof Textarea> = { title: "Components/Textarea", component: Textarea };
export default meta;

export const Default: StoryObj<typeof Textarea> = {
  render: () => (
    <Field label="Notes" htmlFor="notes">
      <Textarea id="notes" placeholder="A short note" />
    </Field>
  ),
};
