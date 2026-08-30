# Accessibility notes

This profile is designed to remain useful when its visual effects are unavailable, motion is reduced, or navigation happens without a mouse.

## Reading and navigation

- Essential biography, skills, experience, project, and contact information is native Markdown or HTML text. No factual claim exists only inside an image.
- A plain-text navigation row near the top links to the major sections.
- Headings form a consistent hierarchy, so screen-reader users can move through the profile by section.
- Link labels describe their destination or action instead of relying on vague phrases such as “click here.”

## Images and contrast

- Informative images have concise alternative text. The closing orbit is decorative and therefore uses an empty alt attribute.
- The SVG artwork includes its own title and description metadata if it is opened directly.
- Text embedded in the generated dark-theme SVGs uses light, high-contrast foreground colors. The same information is repeated as native text below the artwork so it can be resized, selected, translated, or read aloud normally.
- Separate desktop and mobile SVG compositions keep visual text from becoming unnecessarily small on narrow screens.

Core palette spot checks use the WCAG relative-luminance formula: warm white on the main night background is **19.07:1**, body text on that background is **11.90:1**, and cyan labels on capability cards are **10.55:1**. Automated tests protect those pairings from dropping below **7:1**.

## Motion and interaction

- Generated SVG motion is CSS-based and stops when the operating system or browser requests reduced motion.
- The profile avoids autoplaying video, flashing effects, hover-only information, and pointer-dependent controls.
- Expandable project and experience sections use native `details` and `summary` elements, which GitHub exposes to keyboard users.
- Important skill disclosures start open, so their content is available without an extra action.

## GitHub constraints

GitHub profile READMEs do not allow custom JavaScript, custom focus styling, or a fully interactive 3D viewer inside the page. The profile therefore uses GitHub-native links and disclosures, responsive SVG images, and downloadable STL/OBJ files. The STL link opens GitHub’s own model viewer on a separate page.

This is an accessibility-oriented design, not a claim of formal conformance certification. If any part of the profile creates an access barrier, please [email Kun Ming](mailto:kunmingaden@gmail.com).
