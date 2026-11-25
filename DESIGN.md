# Design system — Agentic AI Systems & Business Automation Template

`SN-W00020` · ai-saas · dark mode · Sinera Atlas theme `circuit` · language `en`

## Direction

A black stage carries a red-tinted, high-contrast figure image behind the hero, with a large white sans headline that turns red in its second line. Red (#e50914) is the signature for both the image tint and the emphasised phrase, while the nav and call to action stay small and neutral. Light grey body text is set centred under the headline.

**Mood:** dramatic, intense, dark, bold

## Colour

| Role | Value | Use |
|---|---|---|
| Background | `#050505` | Page ground |
| Surface | `#111111` | Cards, panels, raised areas |
| Text | `#f5f5f5` | Headings and primary copy |
| Muted text | `#ffffff` | Secondary copy, captions |
| Border | `#2a2a2a` | Hairlines, dividers, outlines |
| Accent | `#e50914` | Primary action and highlights |

Palette by frequency of use: `#ffffff` · `#e50914` · `#b8b8b8` · `#2a2a2a` · `#111111` · `#050505` · `#0a0a0a` · `#181818` · `#ff1e1e` · `#000000`.

Roles are inferred from how often and where each colour is used; check them against the page before relying on them.

## Typography

- **Display:** Inter
- **Body:** Inter
- **Loaded families:** Inter, JetBrains Mono
- **Scale (largest breakpoint):** h1 96px · h2 48px · h3 20px · body 14px
- **Weights in use:** semibold, medium, normal
- **Letter spacing:** `tracking-tight`, `tracking-wide`

## Shape, spacing and layout

- **Corner radius:** `rounded-full` (9999px), `rounded-2xl` (16px), `rounded-xl` (12px)
- **Shadows:** `shadow-[0_0_30px_rgba(229,9,20,0.1)]`, `shadow-[0_0_10px_rgba(229,9,20,0.1)]`, `shadow-[0_0_15px_rgba(255,255,255,0.05)]`
- **Content width:** `max-w-7xl`, `max-w-[320px]`
- **Section padding:** `py-24`
- **Common gaps:** `gap-2`, `gap-4`, `gap-6`

**Primary button**

```html
<a class="w-full sm:w-auto px-8 py-4 rounded-lg bg-[#E50914] hover:bg-[#ff1e1e] text-base font-medium tracking-wide transition-all shadow-[0_0_20px_rgba(229,9,20,0.4)] text-white">…</a>
```

## Page structure

Blocks in page order:

1. Navigation bar (`navbar`)
2. Hero (`hero`)
3. Process / steps (`how-it-works`)
4. Feature grid (`features`)
5. Services (`services`)
6. Bento grid (`bento-grid`)
7. Contact form (`contact-form`)
8. Footer (`footer`)

## Motion, effects and stack

- **Effects:** backdrop blur (glass panels), gradient fills, blend modes, CSS animations, large blurred glow shapes
- **Libraries:** Tailwind CSS (CDN)
- **Icons:** Lucide, Iconify

## Tokens

```css
:root {
  --color-background: #050505;
  --color-surface: #111111;
  --color-text: #f5f5f5;
  --color-muted: #ffffff;
  --color-border: #2a2a2a;
  --color-accent: #e50914;
  --font-display: "Inter", sans-serif;
  --font-body: "Inter", sans-serif;
  --radius: 9999px;
}
```

```js
// tailwind.config
theme: { extend: {
  colors: {
    background: '#050505',
    surface: '#111111',
    ink: '#f5f5f5',
    muted: '#ffffff',
    line: '#2a2a2a',
    accent: '#e50914',
  },
  fontFamily: { display: ['Inter'], sans: ['Inter'] },
} }
```

## Do and don't

- **Do:** Tint hero imagery in red (#e50914) and keep the rest of the page black
- **Do:** Set the second headline phrase in red and the first in white
- **Do:** Keep the nav and the call to action neutral with a dark outline button
- **Don't:** Don't use red for body text or long paragraphs
- **Don't:** Don't place red text over the bright areas of the image
- **Don't:** Don't add a second brand colour to the hero

## Use as a prompt

Paste this file into an AI coding tool with: "Build [YOUR PAGE] using this design system. Keep the colours, type, corner radius and spacing exactly; reuse the block order where it fits."
