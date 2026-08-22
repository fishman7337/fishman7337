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
```

## 4. Enable GitHub Actions for the contribution animation

The bundle includes:

```text
.github/workflows/snake.yml
```

After the workflow runs, the contribution animation referenced by `README.md` is available from the `output` branch.

## 5. Optional local preview

Run:

```bash
python scripts/render_preview.py
```

Where Cairo is available, it creates `screenshots/curiosity-workshop-preview.png` for visual QA. Otherwise, open `preview/visual-gallery.html` in a browser; it uses the same checked-in assets without a native rendering dependency.
