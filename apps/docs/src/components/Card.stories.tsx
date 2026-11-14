import type { Meta, StoryObj } from "@storybook/react";
import { Button, Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@chamuka/ui";

const meta: Meta<typeof Card> = { title: "Components/Card", component: Card };
export default meta;

export const Default: StoryObj<typeof Card> = {
  render: () => (
    <Card>
      <CardHeader>
        <CardTitle>Draw together</CardTitle>
        <CardDescription>A canvas for humans and agents.</CardDescription>
      </CardHeader>
      <CardFooter>
        <Button>Open DrawIt</Button>
      </CardFooter>
    </Card>
  ),
};
