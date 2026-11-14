import type { Meta, StoryObj } from "@storybook/react";
import { Button, Tooltip, TooltipContent, TooltipTrigger } from "@chamuka/ui";

const meta: Meta<typeof Tooltip> = { title: "Components/Tooltip", component: Tooltip };
export default meta;

export const Default: StoryObj<typeof Tooltip> = {
  render: () => (
    <Tooltip>
      <TooltipTrigger asChild>
        <Button variant="secondary">Hover</Button>
      </TooltipTrigger>
      <TooltipContent>Short, useful, not a paragraph</TooltipContent>
    </Tooltip>
  ),
};
