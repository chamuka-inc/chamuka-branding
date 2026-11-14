import "@testing-library/jest-dom/vitest";

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

if (!globalThis.crypto?.randomUUID) {
  Object.defineProperty(globalThis, "crypto", {
    value: { randomUUID: () => "test-id" },
  });
}

HTMLCanvasElement.prototype.getContext = () => null;
