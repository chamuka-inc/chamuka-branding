import type { Meta, StoryObj } from "@storybook/react";
import { Button, Stack, ThemeProvider, useTheme } from "@chamuka/ui";

const meta: Meta<typeof ThemeProvider> = {
  title: "Components/ThemeProvider",
  component: ThemeProvider,
};
export default meta;

function Toggle() {
  const { resolved, setTheme } = useTheme();
  return (
    <Stack>
      <p>Resolved: {resolved}</p>
      <Button onClick={() => setTheme(resolved === "dark" ? "light" : "dark")}>
        Toggle theme
      </Button>
    </Stack>
  );
}

export const Default: StoryObj<typeof ThemeProvider> = {
  render: () => <Toggle />,
};
