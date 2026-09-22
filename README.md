# Zaslav Display

Hand-drawn Belarusian Cyrillic display typeface, work in progress.

Traced from the "ЗАСЛАЎ" logo and a historic Cyrillic specimen sheet, then
built into real font files with [fontTools](https://github.com/fonttools/fonttools).

![preview](preview.png)

## Status

**v1.4 — 27 uppercase glyphs:**

```
А Б В Г Ґ Д Е Є Ж З И І Ї Й К Л М Н О П Р С Т Ў Ч Ш Щ
```

`Ш`, `Щ` and `Ч` weren't in either source image — they're constructed from
the same stem/serif shapes as `І`. `Щ`'s descender tail and `Ч`'s bowl were
drawn to match a reference the user provided, then everything is run through
the same trace pipeline as the rest of the glyphs for a consistent texture.

Still missing: `У Ф Х Ц Ь Ю Я` and all lowercase letters.
More glyphs get added as source material comes in.

## Files

- `ZaslavDisplay-Regular.otf` — desktop / general use
- `ZaslavDisplay-Regular.ttf` — for apps/platforms that need TrueType outlines
- `ZaslavDisplay-Regular.woff2` — for the web
- `zaslav-display.css` — ready `@font-face` snippet
- `demo.html` — quick browser preview

## Use on the web

```css
@font-face {
  font-family: "Zaslav Display";
  src: url("ZaslavDisplay-Regular.woff2") format("woff2"),
       url("ZaslavDisplay-Regular.otf") format("opentype");
  font-weight: 400;
  font-style: normal;
  font-display: swap;
}

.zaslav {
  font-family: "Zaslav Display", serif;
}
```

## Use in an app

Bundle `ZaslavDisplay-Regular.ttf` (or `.otf`) as a normal custom font asset
for your platform (iOS/Android/Flutter/etc.) and reference it by its family
name, `Zaslav Display`.
