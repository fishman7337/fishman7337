# Curiosity Workshop visual design

The profile is designed as a tactile creative-computing atelier rather than a conventional technology résumé. Warm paper, copper, dark wood, frosted glass, cyan, violet, coral, and plant green create one consistent material world.

## Hero artwork

<code>assets/curiosity-workshop-hero-v1.png</code> was created with the built-in OpenAI image-generation tool and is embedded into <code>assets/hero-curiosity-workshop.svg</code>. The SVG adds accessible identity copy and lightweight decorative motion.

Final prompt:

~~~text
Use case: stylized-concept
Asset type: text-safe GitHub profile README hero background
Primary request: Create a premium isometric 3D “curiosity workshop” for an applied AI and analytics student—a creative computing atelier where ideas become experiments and useful tools.
Scene/backdrop: midnight-navy studio void with a subtle matte floor and a few suspended dust particles.
Subject: on the right 55–60%, one coherent sculptural workbench/diorama containing translucent notebook or data sheets, a geometric leaf specimen, a small pixel-tile panel, an elegant route/path object, a soft waveform ribbon, modular code-like blocks, and a tiny living plant. Objects should feel intentionally composed and symbolic, not like a cluttered desk.
Style/medium: high-end editorial 3D render, isometric three-quarter view, tactile glass, frosted acrylic, anodized metal, warm paper, soft clay accents; sophisticated product-visualisation polish.
Composition/framing: very wide 3:1 banner. Reserve the left 40–42% as genuinely calm dark negative space for typography. Keep the complete workbench on the center-right with safe margins.
Lighting/mood: warm ivory and copper practical light balanced with cyan, violet, and restrained coral accents; curious, welcoming, crafted, quietly futuristic.
Constraints: no text, no letters, no logos, no watermark, no people, no military, institutional, surveillance, aircraft, or defense motifs; no dashboards or fake UI.
Avoid: generic cyberpunk neon clutter, symmetrical center placement, floating random icons, stock technology wallpaper.
~~~

## Project-cabinet artwork

<code>assets/project-cabinet-v1.png</code> uses the hero as its visual-system reference. It is embedded in <code>assets/project-cabinet.svg</code> and paired with six native GitHub <code>&lt;details&gt;</code> drawers in the README.

Final prompt:

~~~text
Image 1 is the exact visual-system reference for materials, palette, lighting, and editorial 3D polish.

Use case: stylized-concept
Asset type: GitHub profile README project-collection centerpiece
Primary request: Create a premium 3D museum cabinet of exactly six creative-computing project specimens, in the same tactile curiosity-workshop world as Image 1.
Scene/backdrop: midnight-navy atelier void with a matte floor and subtle warm practical lighting.
Subject: one coherent modular display cabinet arranged as two columns by three rows, with all six open compartments clearly separated and fully visible. Each compartment contains exactly one distinctive symbolic exhibit: (1) a translucent neural orb with a few elegant circuit-like rings for generative models, (2) a geometric green leaf inside precise framing corners for visual detection, (3) folded paper strips and a small crescent for a haiku-making tool, (4) layered archival paper connected by branching threads for newspaper restoration, (5) a sculptural route path with waypoints for trip planning, and (6) a friendly progress ring with a subtle pulse ribbon for a fitness quest.
Style/medium: high-end editorial isometric 3D render; frosted glass, warm paper, anodized metal, dark wood, porcelain and soft clay; use the same cyan, violet, coral, copper, ivory, and plant-green accents as Image 1.
Composition/framing: wide 2:1 composition, cabinet centered, all six compartments readable at a glance, generous safe margins. Slight three-quarter/isometric view, but front faces remain clear.
Lighting/mood: warm, crafted, intelligent, playful without becoming toy-like; gallery lighting with soft shadows.
Constraints: exactly six compartments; no text, no letters, no labels, no logos, no watermark, no people, no weapons, aircraft, military, institutional, surveillance, or defense motifs; no fake dashboard.
Avoid: generic cyberpunk neon, chaotic clutter, random floating icons, inaccessible dark-on-dark compartments, stock technology wallpaper.
~~~

## Generated SVG system

<code>python scripts/build_assets.py</code> produces six deterministic, accessible SVGs:

- <code>hero-curiosity-workshop.svg</code>
- <code>workbench-now.svg</code>
- <code>project-cabinet.svg</code>
- <code>making-machine.svg</code>
- <code>current-curiosities.svg</code>
- <code>workshop-footer.svg</code>

They use native SVG, embedded raster artwork, CSS/SMIL motion, no JavaScript, and no external network resource. A reduced-motion media query disables decorative animation when requested.

## Why the 3D is rendered

Normal GitHub README rendering cannot host an interactive WebGL canvas or embedded model viewer. The two generated stills provide convincing 3D depth, the SVG layer adds motion, and the expandable project drawers provide reliable interaction inside GitHub.
