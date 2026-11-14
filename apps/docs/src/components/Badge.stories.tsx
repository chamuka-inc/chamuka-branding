import type { Meta, StoryObj } from "@storybook/react";
import { Badge, Stack } from "@chamuka/ui";

const meta: Meta<typeof Badge> = { title: "Components/Badge", component: Badge };
export default meta;

export const Variants: StoryObj<typeof Badge> = {
  render: () => (
    <Stack direction="row" gap="2" style={{ flexWrap: "wrap" }}>
      <Badge>Default</Badge>
      <Badge variant="secondary">Secondary</Badge>
      <Badge variant="outline">Outline</Badge>
      <Badge variant="success">Success</Badge>
      <Badge variant="warning">Warning</Badge>
      <Badge variant="danger">Danger</Badge>
    </Stack>
  ),
};
