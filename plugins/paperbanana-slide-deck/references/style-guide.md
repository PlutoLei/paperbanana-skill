# Choosing and preserving a deck style

Start with the user's style or an existing deck. For a new deck without a chosen
style, recommend a small number of relevant directions, not the entire catalog.

| Need | Bundled reference |
| --- | --- |
| Restrained academic presentation | [Academia](styles/academia.md) |
| Technical architecture | [Blueprint](styles/blueprint-schematic-drawing.md) |
| Hand-drawn teaching slides | [Color sketchnote](styles/color-sketchnote.md) |
| Simple professional composition | [Minimalist](styles/minimalist.md) |

These documents describe appearance; they are not necessarily accepted CLI
`--style` names. Query `slide --list-styles` in the chosen backend for its presets.
Optional external libraries are used only when the host exposes an authorized
location. Do not search other runtimes' private caches.

Record the palette, title/body hierarchy, background and recurring treatments in
the outline. Repeat these design tokens in each image prompt. A one-page revision
inherits them without regenerating the rest of the deck.

For editable output, choose a theme supported by the spec schema and implement
layout with native objects. An image style reference does not make native objects
look identical to a generated illustration. Keep labels readable and inspect the
rendered result at its actual presentation size.
