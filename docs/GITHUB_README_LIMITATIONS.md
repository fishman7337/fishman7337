# GitHub README animation and interactivity limits

GitHub profile READMEs support Markdown and a safe subset of HTML, but they do not support arbitrary JavaScript.

This bundle uses GitHub-compatible methods:

- Local animated SVGs referenced through `<img>`.
- External dynamic image widgets such as readme-typing-svg and GitHub stats cards.
- Native Markdown anchors.
- `<details>` / `<summary>` expandable sections.
- Mermaid diagrams, which GitHub renders in Markdown.
- GitHub Actions workflows to generate assets like the contribution snake.

The SVGs do not rely on scripts. They use CSS/SMIL-style animation patterns embedded inside the SVG files.
