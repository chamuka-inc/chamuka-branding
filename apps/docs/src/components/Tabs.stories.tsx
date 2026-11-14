import type { Meta, StoryObj } from "@storybook/react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@chamuka/ui";

const meta: Meta<typeof Tabs> = { title: "Components/Tabs", component: Tabs };
export default meta;

export const Default: StoryObj<typeof Tabs> = {
  render: () => (
    <Tabs defaultValue="overview">
      <TabsList>
        <TabsTrigger value="overview">Overview</TabsTrigger>
        <TabsTrigger value="settings">Settings</TabsTrigger>
      </TabsList>
      <TabsContent value="overview">What the workspace is.</TabsContent>
      <TabsContent value="settings">How it is configured.</TabsContent>
    </Tabs>
  ),
};
