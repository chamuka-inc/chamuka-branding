import "@testing-library/jest-dom/vitest";
import { beforeEach } from "vitest";

class ResizeObserverMock {
  observe() {}
  unobserve() {}
  disconnect() {}
}

globalThis.ResizeObserver = ResizeObserverMock;

Object.defineProperty(Element.prototype, "hasPointerCapture", {
  value: () => false,
  configurable: true,
});
Object.defineProperty(Element.prototype, "setPointerCapture", {
  value: () => {},
  configurable: true,
});
Object.defineProperty(Element.prototype, "releasePointerCapture", {
  value: () => {},
  configurable: true,
});
Object.defineProperty(Element.prototype, "scrollIntoView", {
  value: () => {},
  configurable: true,
});

// UI SDK presence/panel motion calls getAnimations(); jsdom's implementation is missing or not iterable.
Object.defineProperty(Element.prototype, "getAnimations", {
  configurable: true,
  writable: true,
  value: function getAnimations() {
    return [];
  },
});

if (!("inert" in HTMLElement.prototype)) {
  Object.defineProperty(HTMLElement.prototype, "inert", {
    configurable: true,
    get() {
      return this.hasAttribute("inert");
    },
    set(value: boolean) {
      this.toggleAttribute("inert", Boolean(value));
    },
  });
}

if (typeof HTMLElement.prototype.showPopover !== "function") {
  HTMLElement.prototype.showPopover = function showPopover() {
    this.toggleAttribute("data-open", true);
  };
  HTMLElement.prototype.hidePopover = function hidePopover() {
    this.toggleAttribute("data-open", false);
  };
}

if (typeof Element.prototype.checkVisibility !== "function") {
  Element.prototype.checkVisibility = function checkVisibility() {
    if (!this.isConnected) return false;
    if (this instanceof HTMLElement && this.hidden) return false;
    const style = getComputedStyle(this);
    if (style.display === "none" || style.visibility === "hidden") return false;
    return this.parentElement ? this.parentElement.checkVisibility() : true;
  };
}

if (!globalThis.matchMedia) {
  Object.defineProperty(globalThis, "matchMedia", {
    configurable: true,
    writable: true,
    value: (query: string) => ({
      matches: query.includes("prefers-reduced-motion"),
      media: query,
      onchange: null,
      addListener() {},
      removeListener() {},
      addEventListener() {},
      removeEventListener() {},
      dispatchEvent() {
        return false;
      },
    }),
  });
}

if (typeof globalThis.CSS === "undefined") {
  Object.defineProperty(globalThis, "CSS", {
    configurable: true,
    value: { supports: () => false },
  });
} else if (typeof globalThis.CSS.supports !== "function") {
  globalThis.CSS.supports = () => false;
}

if (!globalThis.crypto?.randomUUID) {
  Object.defineProperty(globalThis, "crypto", {
    value: { randomUUID: () => "test-id" },
  });
}

HTMLCanvasElement.prototype.getContext = () => null;

beforeEach(() => {
  if (!document.querySelector("style[data-ui-sdk-testing]")) {
    const style = document.createElement("style");
    style.setAttribute("data-ui-sdk-testing", "");
    // Same rule UI SDK's own test mount uses: jsdom hides [popover] unless :popover-open.
    style.textContent = "[popover][data-open] { display: block !important }";
    document.head.append(style);
  }
});
