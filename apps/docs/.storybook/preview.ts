import type { Preview } from "@storybook/react";
import { ThemeProvider, ToastProvider, TooltipProvider } from "@chamuka/ui";
import "@chamuka/tokens/tokens.css";
import "@chamuka/tokens/theme.css";
import "@fontsource/sora/500.css";
import "@fontsource/sora/600.css";
import "@fontsource/sora/700.css";
import "@fontsource/ibm-plex-sans/400.css";
import "@fontsource/ibm-plex-sans/500.css";
import "@fontsource/ibm-plex-sans/600.css";
import "@fontsource/ibm-plex-mono/400.css";
import "@fontsource/ibm-plex-mono/500.css";
import { createElement } from "react";
import "./preview.css";

const preview: Preview = {
  globalTypes: {
    theme: {
      description: "Daybreak colour mode",
      defaultValue: "light",
      toolbar: {
        title: "Theme",
        items: [
          { value: "light", title: "Light" },
          { value: "dark", title: "Dark" },
        ],
      },
    },
  },
  decorators: [
    (Story, context) =>
      createElement(
        ThemeProvider,
        {
          defaultTheme: context.globals.theme === "dark" ? "dark" : "light",
          key: String(context.globals.theme ?? "light"),
        },
        createElement(
          ToastProvider,
          null,
          createElement(TooltipProvider, { delayDuration: 150 }, createElement(Story)),
        ),
      ),
  ],
  parameters: {
    controls: { matchers: { color: /(background|color)$/i } },
    backgrounds: { disable: true },
    options: {
      storySort: {
        order: ["Introduction", "Foundations", "Guidelines", "Components", "Brand"],
      },
    },
  },
};

export default preview;
