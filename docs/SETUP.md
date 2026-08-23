# Setup

## 1. Create / open your profile repository

Your GitHub profile README repository should be named exactly:

```text
fishman7337
```

It must be public and contain a non-empty `README.md` at the repository root.

## 2. Upload these files

Copy the full contents of this bundle into the root of the `fishman7337` repository:

```text
README.md
assets/
content/
scripts/
docs/
.github/workflows/
```

## 3. Edit your content

Edit:

```text
content/profile.yml
```

Then regenerate the SVGs:

```bash
python scripts/build_assets.py
python scripts/build_3d_mesh.py
```

The first command rebuilds the responsive scene wrappers. The second rebuilds the STL, OBJ, and animated wireframe preview from the parametric mesh source.

## 4. Optional local preview

Run:

```bash
python scripts/render_preview.py
```

Where Cairo is available, it creates `screenshots/spatial-portfolio-preview.png` for visual QA. Otherwise, open `preview/visual-gallery.html` in a browser; it uses the same checked-in assets without a native rendering dependency.
