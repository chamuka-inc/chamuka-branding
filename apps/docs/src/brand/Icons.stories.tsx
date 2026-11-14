import type { Meta, StoryObj } from "@storybook/react";
import {
  AppIconDrawIt,
  LockupDrawIt,
  LockupFormIt,
  LockupHorizontal,
  LockupPlay,
  LockupStacked,
  Mark,
  MarkSimple,
  Wordmark,
} from "@chamuka/icons";
import { Stack } from "@chamuka/ui";

const meta: Meta = { title: "Brand/Icons" };
export default meta;

export const MarksAndLockups: StoryObj = {
  render: () => (
    <Stack gap="6">
      <Stack direction="row" gap="6" align="center">
        <Mark title="Chamuka mark" height={64} />
        <MarkSimple title="Simple mark" height={64} />
        <AppIconDrawIt title="DrawIt icon" height={64} />
      </Stack>
      <LockupHorizontal title="Chamuka" height={48} />
      <LockupStacked title="Chamuka stacked" height={96} />
      <LockupDrawIt title="Chamuka DrawIt" height={48} />
      <LockupFormIt title="Chamuka FormIt" height={48} />
      <LockupPlay title="Chamuka Play" height={48} />
      <Wordmark title="Chamuka" height={32} />
    </Stack>
  ),
};
