# Zaslav Display

Hand-drawn Cyrillic display typeface for Belarusian and Ukrainian, work in progress.

Рукописний кириличний шрифт для заголовків (Заслаў, Zaslau): білоруська та українська абетки, у розробці.

Traced from the "ЗАСЛАЎ" logo and a historic Cyrillic specimen sheet, then
built into real font files with [fontTools](https://github.com/fonttools/fonttools).

![preview](preview.png)

## Status

**Version 11.000 — 31 uppercase letters + Ꙗ:**

```
А Б В Г Ґ Д Е Є Ж З И І Ї Й К Л М Н О П Р С Т Ў Х Ч Ш Щ Ь Ю Я Ꙗ
```

`Ш` and `Щ` weren't in either source image — they're constructed from the
same stem/serif shapes as `І`, with `Щ`'s descender tail drawn to match a
photo reference, then run through the same trace pipeline as the rest of the
glyphs for a consistent texture.

`Ґ` (v11) follows a light-painting reference: the lower `І` stem, cut on a
slant, runs into a loop that sweeps left and up into the top bar, which ends
in a hanging teardrop on the right.

`Ч` (v11) is the ustav Y-form from a small printed specimen («КАЧІЕ ІХА»):
two nearly symmetric arms with flat serifs meet at about 40 % of the height
on the lower `І` stem.

`Х` (v11) comes from the same specimen: a heavy diagonal from top left to
bottom right, a hairline from top right to bottom left, flat serifs on all
four ends. The build script is `tools/build_v11.py`.

The font also has a `space` glyph (280 units, mapped to U+0020 and U+00A0),
so spaces in running text come from the font instead of a fallback.

Kerning: 413 pairs in a GPOS `kern` feature, source in `kern.fea`
(РА, ТА, ГА, ЗА, АТ, АЧ, ХА, ДЕ, ТО…). Browsers apply it automatically.

`Е` was redrawn from a small photo reference (about 20 px tall, too small to
trace directly): heavy straight stem without left serifs, hairline arms, a
teardrop beak at the top, a tall thin spur on the middle arm and a wedge at
the bottom. It was rebuilt at high resolution and run through potrace with a
light edge roughening so its texture matches the traced glyphs.

`Ю` is constructed as well: the `І` stem and the `О` bowl joined by a short
bracketed crossbar at mid-height; only the bar was roughened, the stem and
bowl keep their traced outlines.

`Ь` is built from the top of `І` (stem with both serifs) and the lower bowl
of `В`, joined with a curved bracket where the bowl meets the stem.

`Ꙗ` (iotified A, U+A656; lowercase `ꙗ` U+A657 maps to the same glyph) is
the `І` stem and `А` joined by a crossbar that runs into the diagonal of `А`,
with a small gap left between the feet at the baseline.

`Я` follows the handwritten я of Bohdan-Ihor Antonych (his «ся» and «Ясна»)
on the left and `А` on the right. Left: a loop that starts with a hanging
drop, a small eye where the pen crosses its own stroke, and a leg ending in
a heavy rounded drop at the baseline. Right: `А` without its crossbar —
flagged head, stem, foot and the diagonal, which runs down from the head
and joins the leg at the bottom. Built from the mirrored `Р` bowl, the left
leg of `Л` and `А`.

Still missing: `У Ф Ц` and all lowercase letters.
More glyphs get added as source material comes in.

## Versioning

The version is stored the standard OpenType way and kept the same in all
three files: `head.fontRevision` = 11.000, name ID 5 = `Version 11.000`,
name ID 3 (unique ID) = `11.000;NOWXEL;ZaslavDisplay-Regular`, and the CFF
`version` in the OTF. Git tag: `v11.000`. The next release should bump all
of these together (e.g. 11.001 for fixes, 12.000 for new letters).

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
