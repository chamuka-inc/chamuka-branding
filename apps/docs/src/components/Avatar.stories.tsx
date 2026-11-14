import type { Meta, StoryObj } from "@storybook/react";
import { Avatar, AvatarFallback } from "@chamuka/ui";

const meta: Meta<typeof Avatar> = { title: "Components/Avatar", component: Avatar };
export default meta;

export const Fallback: StoryObj<typeof Avatar> = {
  render: () => (
    <Avatar>
      <AvatarFallback>CH</AvatarFallback>
    </Avatar>
  ),
};
