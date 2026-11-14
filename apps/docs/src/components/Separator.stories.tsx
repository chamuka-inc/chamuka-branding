import type { Meta, StoryObj } from "@storybook/react";
import { Separator, Stack } from "@chamuka/ui";

const meta: Meta<typeof Separator> = { title: "Components/Separator", component: Separator };
export default meta;

export const Default: StoryObj<typeof Separator> = {
  render: () => (
    <Stack>
      <p>Above</p>
      <Separator />
      <p>Below</p>
    </Stack>
  ),
};
