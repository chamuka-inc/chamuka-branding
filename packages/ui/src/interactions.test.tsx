import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import type { ReactNode } from "react";
import { describe, expect, it } from "vitest";
import { Accordion, AccordionHeader, AccordionItem, AccordionPanel, AccordionTrigger } from "./accordion";
import { Button } from "./button";
import { Checkbox } from "./checkbox";
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from "./dialog";
import { Label } from "./label";
import { Switch } from "./switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./tabs";
import { ThemeProvider } from "./theme-provider";
import { ToastProvider } from "./toast";
import { TooltipProvider } from "./tooltip";

function wrap(ui: ReactNode) {
  return (
    <ThemeProvider>
      <ToastProvider>
        <TooltipProvider delayDuration={0}>{ui}</TooltipProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}

describe("keyboard interactions", () => {
  it("Tabs moves between tabs with arrow keys", async () => {
    const user = userEvent.setup();
    render(
      wrap(
        <Tabs defaultValue="one">
          <TabsList aria-label="Sections">
            <TabsTrigger value="one">One</TabsTrigger>
            <TabsTrigger value="two">Two</TabsTrigger>
          </TabsList>
          <TabsContent value="one">First</TabsContent>
          <TabsContent value="two">Second</TabsContent>
        </Tabs>,
      ),
    );

    const one = screen.getByRole("tab", { name: "One" });
    one.focus();
    await user.keyboard("{ArrowRight}");
    expect(screen.getByRole("tab", { name: "Two" })).toHaveAttribute("aria-selected", "true");
    await waitFor(() => {
      expect(screen.getByRole("tabpanel")).toHaveTextContent("Second");
    });
  });

  it("Dialog opens from its trigger and closes on Escape", async () => {
    const user = userEvent.setup();
    render(
      wrap(
        <Dialog>
          <DialogTrigger asChild>
            <Button>Open</Button>
          </DialogTrigger>
          <DialogContent>
            <DialogTitle>Invite</DialogTitle>
            <DialogDescription>Send an invite to a teammate.</DialogDescription>
          </DialogContent>
        </Dialog>,
      ),
    );

    await user.click(screen.getByRole("button", { name: "Open" }));
    expect(await screen.findByRole("dialog", { name: "Invite" })).toBeInTheDocument();
    await user.keyboard("{Escape}");
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument();
    });
  });

  it("Checkbox toggles with Space", async () => {
    const user = userEvent.setup();
    render(
      wrap(
        <div className="flex items-center gap-2">
          <Checkbox id="tos" />
          <Label htmlFor="tos">Accept terms</Label>
        </div>,
      ),
    );

    const checkbox = screen.getByRole("checkbox", { name: "Accept terms" });
    checkbox.focus();
    await user.keyboard(" ");
    expect(checkbox).toHaveAttribute("aria-checked", "true");
  });

  it("Switch toggles with Space", async () => {
    const user = userEvent.setup();
    render(
      wrap(
        <div className="flex items-center gap-2">
          <Switch id="alerts" />
          <Label htmlFor="alerts">Alerts</Label>
        </div>,
      ),
    );

    const control = screen.getByRole("switch", { name: "Alerts" });
    control.focus();
    await user.keyboard(" ");
    expect(control).toHaveAttribute("aria-checked", "true");
  });

  it("Accordion trigger expands its panel", async () => {
    const user = userEvent.setup();
    render(
      wrap(
        <Accordion>
          <AccordionItem value="shipping">
            <AccordionHeader>
              <AccordionTrigger>Shipping</AccordionTrigger>
            </AccordionHeader>
            <AccordionPanel>Ships in 5 days.</AccordionPanel>
          </AccordionItem>
        </Accordion>,
      ),
    );

    const trigger = screen.getByRole("button", { name: "Shipping" });
    expect(trigger).toHaveAttribute("aria-expanded", "false");
    await user.click(trigger);
    expect(trigger).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByText("Ships in 5 days.")).toBeVisible();
  });
});
