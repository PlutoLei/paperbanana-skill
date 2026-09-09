# Lightweight previews

These WebP files are display derivatives. Full-resolution originals remain at their existing paths in `examples/` and are linked from the gallery. No source image content was regenerated or overwritten.

Historical images were resized with macOS `sips` to a maximum edge of 1200 px, keeping aspect ratio, then encoded with `cwebp` quality 86 through the baoyu-compress-image CLI (`--keep`). `manifest.json` records each original file hash and source/preview size. The native PPTX example is rendered separately from its source deck, then encoded at quality 88.

Keep preview filenames stable when replacing derivatives, inspect small labels at their displayed size, and update the manifest after intentional source changes. Do not crop away scientific content to fill a thumbnail.
