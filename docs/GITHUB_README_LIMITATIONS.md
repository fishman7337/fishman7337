# GitHub README animation and interactivity limits

GitHub profile READMEs support Markdown and a safe subset of HTML, but they do not support arbitrary JavaScript.

This bundle uses GitHub-compatible methods:

- Local animated SVGs referenced through HTML image elements.
- Two local generated 3D scenes and checked-in GitHub telemetry cards.
- Native Markdown anchors.
- Expandable details and summary sections.
- CSS/SMIL-style animation inside self-contained SVG files.

Interactive WebGL scenes, embedded 3D model viewers, custom JavaScript, and pointer-driven 3D controls are not supported in a normal GitHub profile README. The Curiosity Workshop therefore combines rendered 3D scenes, animated SVG meshes, and native expandable drawers that work reliably inside GitHub.
