import { render } from "@testing-library/react";
import axe from "axe-core";
import type { ReactNode } from "react";
import { describe, expect, it } from "vitest";
import { Alert } from "./alert";
import { Avatar, AvatarFallback } from "./avatar";
import { Badge } from "./badge";
import { Button } from "./button";
import { Card, CardDescription, CardHeader, CardTitle } from "./card";
import { Checkbox } from "./checkbox";
import { Container } from "./container";
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from "./dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "./dropdown-menu";
import { IconButton } from "./icon-button";
import { Input } from "./input";
import { Field, Label } from "./label";
import { Link } from "./link";
import { Popover, PopoverContent, PopoverTrigger } from "./popover";
import { RadioGroup, RadioGroupItem } from "./radio-group";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./select";
import { Separator } from "./separator";
import { Skeleton } from "./skeleton";
import { Spinner } from "./spinner";
import { Stack } from "./stack";
import { Switch } from "./switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./tabs";
import { Textarea } from "./textarea";
import { ThemeProvider } from "./theme-provider";
import { ToastProvider } from "./toast";
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "./tooltip";

function wrap(ui: ReactNode) {
  return (
    <ThemeProvider>
      <ToastProvider>
        <TooltipProvider delayDuration={0}>{ui}</TooltipProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}

async function expectAccessible(ui: ReactNode) {
  const { container } = render(wrap(ui));
  const results = await axe.run(container, {
    rules: { "color-contrast": { enabled: false } },
  });
  expect(results.violations).toEqual([]);
}

describe("components are accessible", () => {
  it("Button", async () => {
    await expectAccessible(<Button>Save</Button>);
  });

  it("IconButton", async () => {
    await expectAccessible(
      <IconButton label="Close">
        <span aria-hidden>×</span>
      </IconButton>,
    );
  });

  it("Link", async () => {
    await expectAccessible(<Link href="https://chamuka.ai">chamuka.ai</Link>);
  });

  it("Field with Input and error", async () => {
    await expectAccessible(
      <Field label="Email" htmlFor="email" help="Work email" error="Enter an email">
        <Input id="email" />
      </Field>,
    );
  });

  it("Textarea", async () => {
    await expectAccessible(
      <>
        <Label htmlFor="notes">Notes</Label>
        <Textarea id="notes" />
      </>,
    );
  });

  it("Select", async () => {
    await expectAccessible(
      <>
        <Label htmlFor="role">Role</Label>
        <Select>
          <SelectTrigger id="role" aria-label="Role">
            <SelectValue placeholder="Choose" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="admin">Admin</SelectItem>
          </SelectContent>
        </Select>
      </>,
    );
  });

  it("Checkbox", async () => {
    await expectAccessible(
      <div className="ck-control-row">
        <Checkbox id="tos" />
        <Label htmlFor="tos">Accept terms</Label>
      </div>,
    );
  });

  it("RadioGroup", async () => {
    await expectAccessible(
      <RadioGroup aria-label="Plan" defaultValue="a">
        <div className="ck-control-row">
          <RadioGroupItem value="a" id="plan-a" />
          <Label htmlFor="plan-a">Starter</Label>
        </div>
      </RadioGroup>,
    );
  });

  it("Switch", async () => {
    await expectAccessible(
      <div className="ck-control-row">
        <Switch id="alerts" />
        <Label htmlFor="alerts">Alerts</Label>
      </div>,
    );
  });

  it("Card Badge Avatar", async () => {
    await expectAccessible(
      <Card>
        <CardHeader>
          <CardTitle>Forms</CardTitle>
          <CardDescription>Build a form.</CardDescription>
        </CardHeader>
        <Badge>New</Badge>
        <Avatar>
          <AvatarFallback>CH</AvatarFallback>
        </Avatar>
      </Card>,
    );
  });

  it("Tooltip", async () => {
    await expectAccessible(
      <Tooltip>
        <TooltipTrigger asChild>
          <Button>Hint</Button>
        </TooltipTrigger>
        <TooltipContent>Helpful</TooltipContent>
      </Tooltip>,
    );
  });

  it("Dialog", async () => {
    await expectAccessible(
      <Dialog>
        <DialogTrigger asChild>
          <Button>Open</Button>
        </DialogTrigger>
        <DialogContent>
          <DialogTitle>Invite</DialogTitle>
          <DialogDescription>Send an invite to a teammate.</DialogDescription>
        </DialogContent>
      </Dialog>,
    );
  });

  it("Popover", async () => {
    await expectAccessible(
      <Popover>
        <PopoverTrigger asChild>
          <Button>More</Button>
        </PopoverTrigger>
        <PopoverContent>Details</PopoverContent>
      </Popover>,
    );
  });

  it("DropdownMenu", async () => {
    await expectAccessible(
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <Button>Menu</Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent>
          <DropdownMenuItem>Edit</DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>,
    );
  });

  it("Tabs", async () => {
    await expectAccessible(
      <Tabs defaultValue="one">
        <TabsList>
          <TabsTrigger value="one">One</TabsTrigger>
          <TabsTrigger value="two">Two</TabsTrigger>
        </TabsList>
        <TabsContent value="one">First</TabsContent>
        <TabsContent value="two">Second</TabsContent>
      </Tabs>,
    );
  });

  it("Alert Skeleton Spinner Separator Stack Container", async () => {
    await expectAccessible(
      <Container>
        <Stack>
          <Alert title="Saved">The form was saved.</Alert>
          <Skeleton />
          <Spinner />
          <Separator />
        </Stack>
      </Container>,
    );
  });
});
