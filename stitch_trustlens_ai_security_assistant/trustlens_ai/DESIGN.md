---
name: TrustLens AI
colors:
  surface: '#081425'
  surface-dim: '#081425'
  surface-bright: '#2f3a4c'
  surface-container-lowest: '#040e1f'
  surface-container-low: '#111c2d'
  surface-container: '#152031'
  surface-container-high: '#1f2a3c'
  surface-container-highest: '#2a3548'
  on-surface: '#d8e3fb'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#d8e3fb'
  inverse-on-surface: '#263143'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#6bd8cb'
  on-secondary: '#003732'
  secondary-container: '#29a195'
  on-secondary-container: '#00302b'
  tertiary: '#ffb786'
  on-tertiary: '#502400'
  tertiary-container: '#df7412'
  on-tertiary-container: '#461f00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#89f5e7'
  secondary-fixed-dim: '#6bd8cb'
  on-secondary-fixed: '#00201d'
  on-secondary-fixed-variant: '#005049'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb786'
  on-tertiary-fixed: '#311400'
  on-tertiary-fixed-variant: '#723600'
  background: '#081425'
  on-background: '#d8e3fb'
  surface-variant: '#2a3548'
typography:
  headline-xl:
    fontFamily: Manrope
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.25'
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Manrope
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
  label-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
    letterSpacing: 0.01em
  code-mono:
    fontFamily: Geist
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style

The design system is anchored in the intersection of high-stakes cybersecurity and sophisticated financial intelligence. The brand personality is defined by "Guardian Intelligence"—a calm, authoritative presence that empowers users rather than inducing panic. It avoids the "hacker" tropes of neon greens on black, opting instead for a refined, professional atmosphere.

The design style is **Corporate Minimalist** with **Tonal Layering**. It utilizes deep, dark backgrounds to provide a sense of stability and focus, while employing precise, high-contrast typography and subtle "glass-like" depth to signify modern AI capabilities. Every element is intentional, reducing cognitive load to ensure that critical risk data is processed with clarity and confidence.

## Colors

This design system uses a "Dark-First" philosophy to minimize eye strain and emphasize critical data visualizations. 

- **Primary & Accent:** Electric Blue (#3B82F6) is used for primary actions and highlights, symbolizing technological precision. Teal (#0D9488) serves as a secondary accent for financial data or secondary growth metrics.
- **Surface Strategy:** The background uses Deep Navy (#0F172A). UI containers and cards utilize Charcoal (#1E293B) to create a subtle hierarchy of depth.
- **Semantic Risk Spectrum:** A strictly defined four-tier system handles risk communication. These colors should be used sparingly against the dark backdrop to ensure maximum "pop" and immediate recognition of threat levels.

## Typography

The typographic system balances the geometric modernity of **Manrope** for headlines with the utilitarian clarity of **Inter** for data and body text. 

- **Headlines:** Use tight letter-spacing and bold weights to create a sense of strength.
- **Body:** Prioritize legibility with generous line heights (1.5x - 1.6x) to ensure complex financial reports are easy to scan.
- **Labels:** Use medium weights for metadata and labels to differentiate them from standard body text.
- **Monospace:** For transaction hashes or technical data, use a clean monospaced font like Geist or JetBrains Mono at a smaller scale.

## Layout & Spacing

The design system employs a **Fluid-to-Fixed Grid**. On mobile, it uses a 4-column system with 16px margins. As the screen scales to desktop, it transitions to a 12-column grid with a maximum content width of 1280px.

- **Rhythm:** An 8px linear scale (4, 8, 16, 24, 32, 40, 64) drives all margins and paddings.
- **Mobile-First:** Elements stack vertically by default. Cards should occupy full width on mobile with 16px side margins to maximize screen real estate for data tables and charts.
- **Safe Areas:** Generous whitespace (the "Breathable Void") is required around high-level risk indicators to ensure they are the primary focal point of the dashboard.

## Elevation & Depth

Hierarchy is established through **Tonal Layering** rather than heavy shadows. 

1. **Floor (Level 0):** Deep Navy (#0F172A). Used for the main application background.
2. **Surface (Level 1):** Charcoal (#1E293B). Used for cards, navigation bars, and structural blocks.
3. **Overlay (Level 2):** A lighter tint of Charcoal or a 10% opacity white overlay. Used for hover states or active items.
4. **Shadows:** When necessary, use extremely soft, large-radius shadows (Blur: 24px, Spread: -4px) with a color tint of `#000000` at 40% opacity. This creates a "lifted" effect for modals and dropdowns without breaking the dark aesthetic.

## Shapes

The shape language is "Approachable Professionalism." The standard border radius is **16px** for cards and primary containers, creating a friendly, modern feel that softens the "coldness" of technical data. 

- **Buttons:** Use 8px (Soft) for a more precise, tool-like appearance, or fully rounded (Pill) for prominent "Call to Action" buttons.
- **Inputs:** Match the button radius (8px) for consistency in form-heavy views.
- **Icons:** Use a 2px stroke weight with slightly rounded corners to match the UI's geometry.

## Components

- **Cards:** The primary container. Must have a 16px corner radius. In dark mode, use a 1px border of `#ffffff` at 5% opacity to define the edges against the deep background.
- **Buttons:** 
  - *Primary:* Electric Blue background, white text, bold weight.
  - *Secondary:* Ghost style with a 1px border of the Primary color.
- **Risk Badges (Chips):** Small, high-contrast labels with a 10% opacity background of the semantic color and a 100% opacity text color (e.g., Critical uses Red text on a faint red tint).
- **Inputs:** Darker than the card surface (#0F172A) with a subtle 1px border. The border should transition to Electric Blue on focus.
- **Progress Bars & Gauges:** Use the semantic risk colors. For AI-confidence scores, use a gradient transitioning from Teal to Electric Blue.
- **Data Tables:** Remove vertical borders. Use horizontal dividers at 5% white opacity. Ensure "Row Hover" states use a slightly lighter charcoal for subtle feedback.