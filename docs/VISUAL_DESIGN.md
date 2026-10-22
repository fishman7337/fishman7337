# Visual design

## Identity and reading order

Compact isometric geometry references Kun Ming's Minecraft-inspired website. Mathematical and data motifs connect that identity to research and practical AI work. Navy, warm white, teal, coral, and violet unify the artwork.

The first screen introduces the person, current internship, specialisms, website, résumé, and contact links. Five featured projects and five animated additional projects remain visible. Featured order is hybrid generative models, EstateScope (02), VeggieAI, HDB analytics, and consumption forecasting. EstateScope appears once; leaf detection is no longer showcased. Selected experience includes the publicly documented RSAF RAiD · AETHER internship. Toolkit and process sections explain breadth without implying equal depth or deployment experience in every technology.

Beyond projects is a visible section with Education, Professional certificates, and Outside work. It includes Singapore Polytechnic (2024–2027, in progress), Yuhua Secondary School (2020–2023), and the publicly documented interests in gaming, music, food, coffee, family, and travel.

Public calls to action lead to projects or contact channels. Build scripts, asset exports, review metadata, and historical mesh downloads stay outside the reading path. Publication-index framing remains outside this presentation.

## Thirteen active visual families

| Family | Visual purpose |
| --- | --- |
| `profile-hero` | Introduce a builder/researcher through isometric blocks and mathematical motifs. |
| `portfolio-quantum` | Compare alternative classical and circuit-based latent priors feeding a classical GAN generator. |
| `portfolio-product` | Show Flask requests, model-serving alternatives, predictions, and SQLite history. |
| `portfolio-data` | Connect cleaned Singapore housing records to Tableau exploration. |
| `portfolio-housing` | Connect attributes and optional descriptions/images to available-input averaging and a price estimate. |
| `portfolio-forecast` | Connect monthly utility history to preparation, ARIMA/SARIMAX, and forecasts. |
| `portfolio-student` | Connect GPA/attendance threshold rules to three exploratory tiers and Dash views. |
| `portfolio-haiku` | Connect Markov word transitions, a 5–7–5 target, and WAV narration. |
| `portfolio-restoration` | Connect damaged text and prefix tries to wildcard/edit-distance candidates. |
| `portfolio-fitness` | Connect browser actions, authenticated Express APIs, MySQL, and game progression. |
| `portfolio-pendulum` | Connect Pendulum-v1 state, a DQN-family agent, discretised torque actions, and replay/target-network learning. |
| `process-applied` | Engage stakeholders and frame needs → inspect data → baseline/evaluate → integrate product → validate/release → monitor/iterate. |
| `process-research` | Literature/gap → question → controlled study design → experiments → analysis → reproduce/communicate. |

Pulses, data movement, and highlights reveal relationships. Project panels are conceptual diagrams rather than screenshots or measured plots. The Pendulum panel is a schematic learning loop, not a policy rollout or proof of improved reward or stable control. Process panels describe methods, not proof that every system reached production or every study was published. Preserve distinctions in [public evidence](./TRUTH_GROUNDING.md).

The applied-AI panel runs from shared success criteria to a useful system. Stakeholder engagement establishes needs and constraints; baseline evaluation considers metrics, trade-offs, and review; product integration includes co-design, interfaces, and serving; validation/release includes tests, usability, and handover; monitoring combines stakeholder and system feedback. Its footer states that stakeholder feedback informs each iteration. These labels describe the working method, not measured stakeholder outcomes.

Every family has desktop/mobile GIF compositions and complete PNG stills: **52 active assets: 26 GIFs and 26 PNGs**. The static image is the default; media conditions enable motion when the visitor has no reduced-motion preference. Adjacent native text carries essential meaning. See [accessibility](./ACCESSIBILITY.md) and [GitHub boundaries](./GITHUB_README_LIMITATIONS.md).

## Generators and retained alternatives

`scripts/build_portfolio_animations.py` supplies five active featured-project families and retains leaf detection as an archive. `scripts/build_more_project_animations.py`, with `scripts/additional_project_scenes.py`, generates the five more-project families. `scripts/build_profile_motion.py` generates the hero and both process families. Keep `manifest.json`, generators, and README aligned.

Leaf-detection assets, earlier recruiter SVGs, spatial scene assets, the generic learning-loop animation, and Curiosity Knot remain source material or historical alternatives. They are not displayed in the current README. Earlier design constraints do not exclude the restored public RSAF RAiD · AETHER experience. See [editing guidance](./EDITING_SVGS.md).
