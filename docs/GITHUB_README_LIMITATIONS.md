# GitHub README animation and interactivity limits

GitHub profile READMEs support Markdown and a safe subset of HTML, but they do not support arbitrary JavaScript.

This bundle uses GitHub-compatible methods:

- Local animated SVGs referenced through HTML image elements.
- Five local generated 3D scenes and a checked-in parametric mesh preview.
- Native Markdown anchors.
- Expandable details and summary sections.
- CSS animation inside self-contained SVG files.
- Native text equivalents and alternative text for the visual material.
- CSS animation that honors the user's reduced-motion preference.

Interactive WebGL scenes, embedded 3D model viewers, custom JavaScript, and pointer-driven 3D controls are not supported inside a normal GitHub profile README. The Spatial Portfolio therefore combines rendered 3D scenes, animated SVG meshes, linked STL/OBJ files, and native expandable drawers. Opening the linked STL page uses GitHub's separate interactive model preview with solid, surface-angle, and wireframe modes.

The implementation avoids putting essential information behind animation or images. See [ACCESSIBILITY.md](./ACCESSIBILITY.md) for the complete reading, motion, interaction, and fallback strategy.
