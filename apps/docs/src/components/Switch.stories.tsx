import type { Meta, StoryObj } from "@storybook/react";
import { Label, Switch } from "@chamuka/ui";

const meta: Meta<typeof Switch> = { title: "Components/Switch", component: Switch };
export default meta;

export const Default: StoryObj<typeof Switch> = {
  render: () => (
    <div className="ck-control-row">
      <Switch id="alerts" />
      <Label htmlFor="alerts">Email alerts</Label>
    </div>
  ),
};
