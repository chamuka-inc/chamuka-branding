import type { Meta, StoryObj } from "@storybook/react";
import { Button, Popover, PopoverContent, PopoverTrigger } from "@chamuka/ui";

const meta: Meta<typeof Popover> = { title: "Components/Popover", component: Popover };
export default meta;

export const Default: StoryObj<typeof Popover> = {
  render: () => (
    <Popover>
      <PopoverTrigger asChild>
        <Button variant="outline">Details</Button>
      </PopoverTrigger>
      <PopoverContent>A quiet supporting panel.</PopoverContent>
    </Popover>
  ),
};
