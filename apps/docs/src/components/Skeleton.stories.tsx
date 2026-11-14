import type { Meta, StoryObj } from "@storybook/react";
import { Skeleton, Stack } from "@chamuka/ui";

const meta: Meta<typeof Skeleton> = { title: "Components/Skeleton", component: Skeleton };
export default meta;

export const Default: StoryObj<typeof Skeleton> = {
  render: () => (
    <Stack>
      <Skeleton style={{ height: 24, width: "40%" }} />
      <Skeleton style={{ height: 16 }} />
      <Skeleton style={{ height: 16, width: "80%" }} />
    </Stack>
  ),
};
