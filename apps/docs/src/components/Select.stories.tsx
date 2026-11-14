import type { Meta, StoryObj } from "@storybook/react";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@chamuka/ui";

const meta: Meta<typeof Select> = { title: "Components/Select", component: Select };
export default meta;

export const Default: StoryObj<typeof Select> = {
  render: () => (
    <Select>
      <SelectTrigger aria-label="Role">
        <SelectValue placeholder="Choose a role" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem value="admin">Admin</SelectItem>
        <SelectItem value="editor">Editor</SelectItem>
      </SelectContent>
    </Select>
  ),
};
