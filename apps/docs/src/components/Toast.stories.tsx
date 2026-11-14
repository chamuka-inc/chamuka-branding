import type { Meta, StoryObj } from "@storybook/react";
import { Button, useToast } from "@chamuka/ui";

const meta: Meta = { title: "Components/Toast" };
export default meta;

function ToastDemo() {
  const { toast } = useToast();
  return (
    <Button
      onClick={() => toast({ title: "Saved", description: "The form was saved." })}
    >
      Show toast
    </Button>
  );
}

export const Default: StoryObj = { render: () => <ToastDemo /> };
