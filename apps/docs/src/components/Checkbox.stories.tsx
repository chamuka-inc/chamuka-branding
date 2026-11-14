import type { Meta, StoryObj } from "@storybook/react";
import { Checkbox, Label } from "@chamuka/ui";

const meta: Meta<typeof Checkbox> = { title: "Components/Checkbox", component: Checkbox };
export default meta;

export const Default: StoryObj<typeof Checkbox> = {
  render: () => (
    <div className="ck-control-row">
      <Checkbox id="tos" />
      <Label htmlFor="tos">Accept terms</Label>
    </div>
  ),
};
