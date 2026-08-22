# Signal Garden visual design

The profile uses a personal, editorial creative-computation visual system.

## Hero artwork

`assets/signal-garden-hero-v2.png` was generated with the built-in OpenAI image-generation tool. The deterministic asset builder embeds it into `assets/hero-signal-garden.svg`, where it is combined with accessible identity copy and lightweight animation.

Final prompt:

```text
Use case: stylized-concept
Asset type: text-safe GitHub profile README hero background
Input images: Image 1 is a style and material reference only; generate a new composition rather than editing or copying it.
Primary request: Create a premium editorial 3D "signal garden" that represents curiosity, machine learning, computer vision, research, and making useful software. It should feel like an art-directed personal identity piece, not a generic technology wallpaper.
Scene/backdrop: Deep midnight-indigo studio void with a restrained perspective grid and faint atmospheric particles.
Subject: One concentrated living glass-and-light ecosystem occupying the right 55–60% of the canvas: translucent botanical stems, a few sculptural leaves, delicate neural filaments, small floating glass seeds, and one elegant flowing data ribbon. The system should read as one coherent specimen, not many scattered objects.
Style/medium: High-end cinematic 3D render with glass, iridescent mesh, fine wireframe detail, tactile translucent materials, and tasteful editorial restraint. Sophisticated, distinctive, and polished.
Composition/framing: Very wide 3:1 banner. Reserve the left 38–42% as genuinely calm, dark negative space for large typography. Keep all important subject detail on the center-right. Preserve generous safe margins. The right subject should have a strong silhouette and clear focal hierarchy.
Lighting/mood: Cyan, electric blue, violet, and a tiny coral accent against near-black navy; soft volumetric glow; crisp highlights; luminous but not neon-noisy.
Constraints: No text, no letters, no logos, no watermark, and no people. Avoid dense detail on the left, symmetrical centre placement, or stock futurist clichés.
```

## Research artwork

`assets/research-seed-lab-v1.png` was generated in the same visual language and embedded into `assets/research-observatory.svg`. It is explicitly labelled as a conceptual visual; measured results remain in the paper.

Final prompt:

```text
Use case: stylized-concept
Asset type: conceptual research centerpiece background for a GitHub profile README
Input images: Image 1 is a style, palette, and material reference only; create a new composition and new subject.
Primary request: Create an art-directed 3D "quantum seed laboratory" that conceptually represents a careful comparison between classical and hybrid quantum generative models. It must feel like the same Signal Garden world, with scientific restraint and a clear focal hierarchy.
Scene/backdrop: Deep midnight-indigo studio void, subtle glass work-surface, very faint atmospheric particles.
Subject: On the left 48–52%, one elegant translucent seed-shaped glass chamber containing a small luminous neural lattice and a few tiny monochrome pixel tiles suggesting binary image generation. Three small orbiting glass nodes with distinct simple ring counts suggest 3, 5, and 7 model variants without using labels. A thin flowing ribbon enters the chamber and a restrained set of output tiles leaves it. This is conceptual artwork, not a data chart.
Style/medium: Premium cinematic 3D render; realistic glass, pearlescent filaments, fine wireframe, editorial science-visualisation polish; consistent with Image 1.
Composition/framing: Wide 2:1 banner. Keep the complete visual subject on the left half. Reserve the right 42–46% as calm dark negative space suitable for typography and a small metrics panel. Generous safe margins and no important elements at the edges.
Lighting/mood: Cyan and violet glass light with a restrained coral accent; quietly curious, precise, credible, sophisticated.
Constraints: No text, no letters, no numbers, no equations, no logos, no watermark, no people. Do not imply measured results or performance. Avoid clutter, dashboards, interfaces, stock cyberpunk motifs, or symmetrical centre placement.
```

## Generated SVG system

`python scripts/build_assets.py` produces eleven deterministic, accessible SVGs:

- `hero-signal-garden.svg`
- `studio-manifesto.svg`
- six `project-*.svg` specimens
- `research-observatory.svg`
- `craft-map.svg`
- `signal-footer.svg`

They use native SVG, embedded raster artwork, and CSS animation. No JavaScript or external network resource is required. A reduced-motion media query disables decorative animation for visitors who request it.

## GitHub 3D limitation

Normal GitHub README rendering cannot host an interactive WebGL canvas or an embedded 3D model viewer. The generated hero and research centerpiece provide the 3D depth, while the SVG assets add lightweight mesh motion that remains compatible with GitHub's image rendering.
