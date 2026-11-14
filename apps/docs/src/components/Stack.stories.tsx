import type { Meta, StoryObj } from "@storybook/react";
import { Badge, Stack } from "@chamuka/ui";

const meta: Meta<typeof Stack> = { title: "Components/Stack", component: Stack };
export default meta;

export const Default: StoryObj<typeof Stack> = {
  render: () => (
    <Stack direction="row" gap="2">
      <Badge>One</Badge>
      <Badge variant="secondary">Two</Badge>
    </Stack>
  ),
};
