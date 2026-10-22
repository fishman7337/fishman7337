# Editing the profile artwork

## Current displayed assets

The README displays thirteen active visual families, each with desktop/mobile GIFs and complete PNG stills: **52 active assets: 26 GIFs and 26 PNGs**. Edit the Python generators and regenerate outputs rather than editing individual frames.

```bash
python scripts/build_portfolio_animations.py
python scripts/build_more_project_animations.py
python scripts/build_profile_motion.py
```

| Generator | Families |
| --- | --- |
| `build_portfolio_animations.py` | Active: `portfolio-quantum`, `portfolio-housing`, `portfolio-product`, `portfolio-data`, `portfolio-forecast`. Retained `portfolio-vision` is archival. |
| `build_more_project_animations.py` | `portfolio-student`, `portfolio-haiku`, `portfolio-restoration`, `portfolio-fitness`, `portfolio-pendulum`; scene helper: `additional_project_scenes.py`. |
| `build_profile_motion.py` | `profile-hero`, `process-applied`, `process-research` |

Each stem has `.gif`, `-mobile.gif`, `-static.png`, `-mobile-static.png` variants. Use repository dependency files to preserve the expected rendering environment.

Keep illustrations tied to [project evidence](./TRUTH_GROUNDING.md). Preserve alternative quantum/classical priors, VeggieAI's alternative serving routes, and the HDB 202,461-record qualifier. EstateScope averages available estimates; its cited 1,517-example held-out evaluation is NLP-only. Energy uses univariate ARIMA/SARIMAX with a configured 60-month horizon; CLI forecast intervals are not exported.

For the five more-project panels, preserve explicit GPA/attendance rules, Markov generation rather than an LLM, trie/edit-distance candidate restoration rather than guaranteed recovery, FitnessQuest application flows rather than health results, and a schematic Pendulum learning loop rather than a recorded policy rollout. Pendulum uses discretised torque with DQN, Double DQN, Dueling DQN, and Rainbow-style variants; do not imply reward superiority or control stability.

The applied process stages are engage stakeholders/frame needs, inspect data, baseline/evaluate, integrate product, validate/release, monitor/iterate. Preserve success criteria and constraints; metrics, trade-offs, and review; co-design, interfaces, and serving; tests, usability, and handover; and stakeholder/system feedback. The subtitle connects shared success criteria to a useful system, and the footer states that stakeholder feedback informs each iteration. The research stages remain literature/gap, question, controlled study design, experiments, analysis, reproduce/communicate. These methods do not establish measured stakeholder outcomes, deployment, or publication.

Preserve README source order: mobile no-preference GIF, desktop no-preference GIF, mobile PNG, default PNG. Keep essential facts and stages in adjacent native text. After changes, check local references, GIF frames, complete stills, and deterministic regeneration with repository checks. Inspect desktop/mobile previews with motion enabled and reduced. Update `manifest.json` when the inventory changes. The active inventory is thirteen families; exclude retained leaf GIF/PNG files from its 52-file total. Keep EstateScope in featured position 02 without a duplicate panel, and keep Beyond projects visible with Education, Professional certificates, and Outside work.

## Retained SVGs and earlier artwork

Leaf detection is no longer displayed in the README. Its scene and previously generated files may remain for earlier revisions; they are not active assets.

`scripts/build_recruiter_assets.py` retains deterministic SVG geometry and labels for the earlier hero, workflow, and project strips. These SVGs are source material or archived alternatives, not displayed README assets.

`content/profile.yml`, `scripts/build_assets.py`, and scene sources in `manifest.json` support earlier spatial artwork. `scripts/build_3d_mesh.py` retains the Curiosity Knot STL, OBJ, and wireframe. Preserve source assets even when the README does not use them.

For retained SVGs, preserve escaped text, `title`/`desc` metadata, a complete static frame, and self-contained resources. Avoid scripts, remote fonts, hover-only controls, and long paragraphs. Editing an SVG updates current motion assets only if their generator consumes that source. Generation instructions remain in documentation rather than public calls to action.
