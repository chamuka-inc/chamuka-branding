import type { Meta, StoryObj } from "@storybook/react";
import { Input, Label } from "@chamuka/ui";

const meta: Meta<typeof Label> = { title: "Components/Label", component: Label };
export default meta;

export const Default: StoryObj<typeof Label> = {
  render: () => (
    <>
      <Label htmlFor="name" required>
        Name
      </Label>
      <Input id="name" />
    </>
  ),
};
