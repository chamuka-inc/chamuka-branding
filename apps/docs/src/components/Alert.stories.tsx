import type { Meta, StoryObj } from "@storybook/react";
import { Alert, Stack } from "@chamuka/ui";

const meta: Meta<typeof Alert> = { title: "Components/Alert", component: Alert };
export default meta;

export const Variants: StoryObj<typeof Alert> = {
  render: () => (
    <Stack>
      <Alert title="Saved">The form was saved.</Alert>
      <Alert variant="info" title="Heads up">
        Invites expire in seven days.
      </Alert>
      <Alert variant="success" title="Connected">
        Waypoint is reachable.
      </Alert>
      <Alert variant="warning" title="On ink">
        Warning colour fails on paper — this band is ink.
      </Alert>
      <Alert variant="danger" title="Could not save">
        Check the network and try again.
      </Alert>
    </Stack>
  ),
};
