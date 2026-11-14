import type { Meta, StoryObj } from "@storybook/react";
import { Button, Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from "@chamuka/ui";

const meta: Meta<typeof Dialog> = { title: "Components/Dialog", component: Dialog };
export default meta;

export const Default: StoryObj<typeof Dialog> = {
  render: () => (
    <Dialog>
      <DialogTrigger asChild>
        <Button>Invite</Button>
      </DialogTrigger>
      <DialogContent>
        <DialogTitle>Send invite</DialogTitle>
        <DialogDescription>Invite a teammate to this workspace.</DialogDescription>
        <Button>Send invite</Button>
      </DialogContent>
    </Dialog>
  ),
};
