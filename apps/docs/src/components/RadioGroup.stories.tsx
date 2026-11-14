import type { Meta, StoryObj } from "@storybook/react";
import { Label, RadioGroup, RadioGroupItem } from "@chamuka/ui";

const meta: Meta<typeof RadioGroup> = { title: "Components/RadioGroup", component: RadioGroup };
export default meta;

export const Default: StoryObj<typeof RadioGroup> = {
  render: () => (
    <RadioGroup defaultValue="starter" aria-label="Plan">
      <div className="ck-control-row">
        <RadioGroupItem value="starter" id="starter" />
        <Label htmlFor="starter">Starter</Label>
      </div>
      <div className="ck-control-row">
        <RadioGroupItem value="team" id="team" />
        <Label htmlFor="team">Team</Label>
      </div>
    </RadioGroup>
  ),
};
