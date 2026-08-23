# Curiosity Knot

This directory contains the real 3D mesh used in the profile README:

- `curiosity-knot.stl` — ASCII STL for inspection, printing, or import into modelling tools.
- `curiosity-knot.obj` — Wavefront OBJ for broad 3D-tool compatibility.

Both files describe the same closed parametric **(2, 3) torus-knot tube** with 1,728 vertices and 3,456 triangular faces. Regenerate them, together with the animated README preview, from the repository root:

```text
python scripts/build_3d_mesh.py
```

The mesh is decorative portfolio artwork, not a calibrated engineering or manufacturing model.
