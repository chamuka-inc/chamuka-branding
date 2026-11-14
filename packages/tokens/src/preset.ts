/**
 * Tailwind CSS v3 preset. Pair with `@chamuka/tokens/tokens.css`.
 *
 * ```ts
 * import chamuka from "@chamuka/tokens/preset";
 * export default { presets: [chamuka], content: ["./src/**\/*.{ts,tsx}", "./node_modules/@chamuka/ui/dist/**\/*.js"] };
 * ```
 */
const fontDisplay = ["Sora", "ui-sans-serif", "system-ui", "sans-serif"];
const fontSans = ["IBM Plex Sans", "ui-sans-serif", "system-ui", "sans-serif"];
const fontMono = ["IBM Plex Mono", "ui-monospace", "monospace"];

const preset = {
  darkMode: ["class", '[data-theme="dark"]'] as ["class", string],
  theme: {
    extend: {
      colors: {
        ember: "#E24E1B",
        gold: "#E6B422",
        slate: "#2B4C7E",
        paper: "#FFF8F1",
        mist: "#F3EBE0",
        ink: "#17141C",
        success: "#1F8A5B",
        warning: "#E0A100",
        danger: "#C5362B",
        info: "#2B4C7E",
        play: "#D9487A",
        forest: "#2F6B4F",
        mineral: "#1F7A6B",
        neutral: {
          50: "#FBF7F2",
          100: "#F3EBE0",
          200: "#E6D9C8",
          300: "#D0C0AA",
          400: "#B3A28A",
          500: "#8F8170",
          600: "#6B645C",
          700: "#524C46",
          800: "#3A3531",
          900: "#241F1C",
          950: "#17141C",
        },
        background: "var(--background)",
        foreground: "var(--foreground)",
        card: {
          DEFAULT: "var(--card)",
          foreground: "var(--card-foreground)",
        },
        popover: {
          DEFAULT: "var(--popover)",
          foreground: "var(--popover-foreground)",
        },
        primary: {
          DEFAULT: "var(--primary)",
          foreground: "var(--primary-foreground)",
        },
        secondary: {
          DEFAULT: "var(--secondary)",
          foreground: "var(--secondary-foreground)",
        },
        muted: {
          DEFAULT: "var(--muted-bg)",
          foreground: "var(--muted-foreground)",
        },
        accent: {
          DEFAULT: "var(--accent)",
          foreground: "var(--accent-foreground)",
        },
        destructive: {
          DEFAULT: "var(--destructive)",
          foreground: "var(--destructive-foreground)",
        },
        border: "var(--border)",
        input: "var(--input)",
        ring: "var(--ring)",
      },
      fontFamily: {
        display: fontDisplay,
        sans: fontSans,
        mono: fontMono,
      },
      fontSize: {
        display: ["56px", { lineHeight: "64px", fontWeight: "600" }],
        h1: ["40px", { lineHeight: "48px", fontWeight: "600" }],
        h2: ["32px", { lineHeight: "40px", fontWeight: "600" }],
        h3: ["24px", { lineHeight: "32px", fontWeight: "600" }],
        h4: ["20px", { lineHeight: "28px", fontWeight: "500" }],
        body: ["16px", { lineHeight: "24px" }],
        small: ["14px", { lineHeight: "20px" }],
        caption: ["12px", { lineHeight: "16px" }],
        code: ["14px", { lineHeight: "22px" }],
      },
      borderRadius: {
        sm: "4px",
        md: "8px",
        lg: "12px",
        xl: "20px",
      },
      boxShadow: {
        sm: "0 1px 2px rgb(23 20 28 / 0.06)",
        md: "0 8px 20px rgb(23 20 28 / 0.08)",
        lg: "0 18px 40px rgb(23 20 28 / 0.12)",
      },
      transitionDuration: {
        fast: "150ms",
        base: "200ms",
        slow: "300ms",
      },
      zIndex: {
        dropdown: "50",
        sticky: "100",
        overlay: "200",
        modal: "300",
        toast: "400",
        tooltip: "500",
      },
    },
  },
};

export default preset;
