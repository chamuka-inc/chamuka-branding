import type { Meta, StoryObj } from "@storybook/react";
import { Card, Container } from "@chamuka/ui";

const meta: Meta<typeof Container> = { title: "Components/Container", component: Container };
export default meta;

export const Default: StoryObj<typeof Container> = {
  render: () => (
    <Container size="sm">
      <Card>Reading measure for a form.</Card>
    </Container>
  ),
};
