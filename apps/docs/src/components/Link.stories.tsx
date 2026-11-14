import type { Meta, StoryObj } from "@storybook/react";
import { Link } from "@chamuka/ui";

const meta: Meta<typeof Link> = {
  title: "Components/Link",
  component: Link,
  args: { href: "https://chamuka.ai", children: "chamuka.ai" },
};
export default meta;
export const Default: StoryObj<typeof Link> = {};
