# Editing the SVGs

This bundle is designed so the SVGs are not painful to update.

## Recommended path

1. Edit `content/profile.yml`.
2. Run:

```bash
python scripts/build_assets.py
python scripts/build_3d_mesh.py
```

The first command regenerates the eight Spatial Portfolio scene wrappers. The second regenerates the Curiosity Knot STL, OBJ, and animated wireframe preview.

The responsive artwork is generated from the five `assets/*-v1.png` scene sources listed in `manifest.json`; keep those source files in place when rebuilding.

## Direct SVG editing path

You can also open `assets/*.svg` directly in VS Code, Figma, Illustrator, or Inkscape.

The SVGs intentionally use:

- Native `<text>` elements, not converted outlines.
- Self-contained CSS animations inside the SVG.
- No JavaScript and no external resources.

## What to avoid

- Avoid adding `<script>` tags; GitHub will not allow them in normal README contexts.
- Avoid relying on hover-only interactions inside SVGs; when SVGs are shown via `<img>`, internal links and pointer interactions are not reliable.
- Avoid giant paragraphs inside SVGs. Keep longer content in the README and keep SVGs punchy.

## Animation control

Animations live in the shared `<style>` block produced by `scripts/build_assets.py`.
The main motion classes are `.pulse`, `.dash`, `.draw`, `.orbit`, `.orbitReverse`, `.float`, and `.scan`.
The SVGs also honour `prefers-reduced-motion`.
