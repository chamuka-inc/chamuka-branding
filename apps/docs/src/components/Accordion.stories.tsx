import type { Meta, StoryObj } from "@storybook/react";
import {
  Accordion,
  AccordionHeader,
  AccordionItem,
  AccordionPanel,
  AccordionTrigger,
} from "@chamuka/ui";

const meta: Meta<typeof Accordion> = { title: "Components/Accordion", component: Accordion };
export default meta;

export const Default: StoryObj<typeof Accordion> = {
  render: () => (
    <Accordion defaultValue="shipping">
      <AccordionItem value="shipping">
        <AccordionHeader>
          <AccordionTrigger>Shipping</AccordionTrigger>
        </AccordionHeader>
        <AccordionPanel>Standard shipping takes 5 to 7 days.</AccordionPanel>
      </AccordionItem>
      <AccordionItem value="returns">
        <AccordionHeader>
          <AccordionTrigger>Returns</AccordionTrigger>
        </AccordionHeader>
        <AccordionPanel>Unused items can be returned within 30 days.</AccordionPanel>
      </AccordionItem>
    </Accordion>
  ),
};
