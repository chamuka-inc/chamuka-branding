import type { Meta, StoryObj } from "@storybook/react";
import {
  Combobox,
  ComboboxContent,
  ComboboxEmpty,
  ComboboxInput,
  ComboboxItem,
  ComboboxList,
} from "@chamuka/ui";

const meta: Meta<typeof Combobox> = { title: "Components/Combobox", component: Combobox };
export default meta;

export const Default: StoryObj<typeof Combobox> = {
  render: () => (
    <Combobox>
      <ComboboxInput aria-label="Framework" placeholder="Search a framework" />
      <ComboboxContent>
        <ComboboxEmpty>No frameworks found.</ComboboxEmpty>
        <ComboboxList>
          <ComboboxItem value="next">Next.js</ComboboxItem>
          <ComboboxItem value="remix">Remix</ComboboxItem>
          <ComboboxItem value="astro">Astro</ComboboxItem>
        </ComboboxList>
      </ComboboxContent>
    </Combobox>
  ),
};
