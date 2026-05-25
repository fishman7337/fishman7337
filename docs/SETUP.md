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

## 4. Enable GitHub Actions for the snake animation

The bundle includes:

```text
.github/workflows/snake.yml
```

After the workflow runs, you can uncomment the contribution snake section in `README.md`.

## 5. Optional local preview

Run:

```bash
python scripts/render_preview.py
```

It creates preview screenshots under `screenshots/`.
