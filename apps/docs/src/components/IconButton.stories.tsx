import type { Meta, StoryObj } from "@storybook/react";
import { IconButton } from "@chamuka/ui";
import { Plus } from "lucide-react";

const meta: Meta<typeof IconButton> = {
  title: "Components/IconButton",
  component: IconButton,
  args: { label: "Add", children: <Plus size={18} strokeWidth={1.75} /> },
};
export default meta;
type Story = StoryObj<typeof IconButton>;

export const Default: Story = {};
export const Ghost: Story = { args: { variant: "ghost" } };
