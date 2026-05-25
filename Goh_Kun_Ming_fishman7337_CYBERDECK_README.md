<!--
  fishman7337 / Goh Kun Ming GitHub profile README
  Visual system: edit content/profile.yml, then run python scripts/build_assets.py.
  GitHub-compatible interactivity only: no JavaScript required.
-->

<div align="center">

<img src="./assets/hero-cyberdeck.svg" alt="Goh Kun Ming fishman7337 animated AI research cyberdeck banner" width="100%" />

<br />

<img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=900&size=28&duration=2450&pause=700&center=true&vCenter=true&width=1200&height=82&color=38BDF8&lines=AI+Research+Intern+%40+RSAF+RAiD+(AETHER);Applied+AI+%26+Analytics+%40+Singapore+Polytechnic;Quantum+GANs+%E2%80%A2+Computer+Vision+%E2%80%A2+Sensor+Fusion+%E2%80%A2+MLOps;Research-grade+AI+systems+with+honest+evaluation+and+strong+documentation" alt="Animated typing intro for Goh Kun Ming" />

<br />

<a href="https://github.com/fishman7337"><img src="https://img.shields.io/badge/GitHub-fishman7337-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub fishman7337" /></a>
<a href="https://www.linkedin.com/in/goh-kun-ming-58573430a/"><img src="https://img.shields.io/badge/LinkedIn-Goh%20Kun%20Ming-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn Goh Kun Ming" /></a>
<a href="mailto:kunmingaden@gmail.com"><img src="https://img.shields.io/badge/Email-kunmingaden%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email kunmingaden@gmail.com" /></a>
<a href="https://orcid.org/0009-0008-7666-781X"><img src="https://img.shields.io/badge/ORCID-0009--0008--7666--781X-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
<a href="https://arxiv.org/abs/2508.09209"><img src="https://img.shields.io/badge/arXiv-2508.09209-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white" alt="arXiv 2508.09209" /></a>

<br />
<br />

<img src="https://komarev.com/ghpvc/?username=fishman7337&label=PROFILE%20VIEWS&style=for-the-badge&color=7c3aed" alt="Profile views" />
<img src="https://img.shields.io/github/followers/fishman7337?style=for-the-badge&logo=github&label=Followers&color=38BDF8" alt="GitHub followers" />
<img src="https://img.shields.io/github/stars/fishman7337?affiliations=OWNER%2CCOLLABORATOR&style=for-the-badge&logo=github&label=Total%20Stars&color=22C55E" alt="GitHub stars" />
<img src="https://img.shields.io/badge/Focus-Research%20%2B%20Systems-F472B6?style=for-the-badge" alt="Focus research plus systems" />

<br />
<br />

<a href="#mission-control">Mission Control</a> ·
<a href="#research-spotlight">Research</a> ·
<a href="#selected-research-and-builds">Builds</a> ·
<a href="#technical-stack">Stack</a> ·
<a href="#github-telemetry">Telemetry</a> ·
<a href="#contact">Contact</a>

</div>

---

## `~/whoami`

```ts
const fishman7337 = {
  name: "Goh Kun Ming",
  handle: "fishman7337",
  base: "Singapore",
  education: "Diploma in Applied AI & Analytics, Singapore Polytechnic",
  currentRole: "AI Research Intern @ RSAF RAiD (AETHER)",
  publicResearch: "Quantum-Enhanced GANs preprint · arXiv:2508.09209",
  operatingMode: "research → reproducibility → evaluation → deployable systems",
  proofPoints: ["Qiskit", "FID/KID", "pytest", "CI/CD", "Docker", "model cards"]
};
```

I’m focused on a practical arc: **ask a research question, build a reproducible baseline, measure it honestly, then turn the useful pieces into documented systems.**

The common thread across the work below is **quantum ML, computer vision, geospatial preparation, MLOps, and responsible release discipline**.

---

## Mission Control

<img src="./assets/mission-control.svg" alt="Animated mission control visual for research systems governance and MLOps" width="100%" />

<table>
  <tr>
    <td width="25%" valign="top"><h3>🧠 Research</h3><p>Hybrid quantum-classical ML, GAN baselines, reproducible experiments, and evaluation discipline.</p></td>
    <td width="25%" valign="top"><h3>🛰️ Perception</h3><p>Computer vision, satellite imagery preparation, sensor fusion, remote-sensing features, and detection pipelines.</p></td>
    <td width="25%" valign="top"><h3>⚙️ Systems</h3><p>Flask/FastAPI apps, Docker workflows, CI/CD, model serving, tests, security checks, and MLOps docs.</p></td>
    <td width="25%" valign="top"><h3>🛡️ Governance</h3><p>Responsible AI thinking, model cards, data cards, threat models, and accountable release practices.</p></td>
  </tr>
</table>

<details>
<summary><b>🧩 Expand the operating principles</b></summary>

<br />

| Principle | How I apply it |
|---|---|
| **Truth-grounded claims** | I prefer honest baselines, clear limitations, and reproducible evidence over inflated results. |
| **Systems thinking** | A model is only useful when the surrounding data, testing, deployment, monitoring, and docs are coherent. |
| **Research-to-product loop** | I like converting experiments into usable, reviewable, well-documented artifacts. |
| **Safety and governance** | I treat documentation, access control, threat modeling, and risk controls as first-class engineering work. |

</details>

---

## Research Spotlight

<img src="./assets/quantum-lab.svg" alt="Animated HQCGAN research pipeline with quantum circuit latent priors and FID KID evaluation" width="100%" />

<table>
  <tr>
    <td width="62%" valign="top">
      <h3>Quantum-Enhanced Generative Adversarial Networks</h3>
      <p><b>Comparative Analysis of Classical and Hybrid Quantum-Classical Generative Adversarial Networks</b></p>
      <p>
        My arXiv preprint investigates whether parameterised quantum circuits can act as useful latent priors for generative modelling under near-term quantum constraints.
        The work compares a classical GAN against multiple HQCGAN variants and keeps the claims bounded by image-quality metrics and limitations.
      </p>
      <ul>
        <li>Compared a classical GAN against <b>3-, 5-, and 7-qubit</b> HQCGAN variants.</li>
        <li>Used <b>Qiskit's AerSimulator</b> with realistic noise models.</li>
        <li>Focused on <b>binary MNIST digits 0 and 1</b> to align with constrained quantum latent dimensions.</li>
        <li>Ran <b>150-epoch</b> experiments and evaluated image-generation quality with <b>FID</b> and <b>KID</b>.</li>
      </ul>
    </td>
    <td width="38%" valign="middle" align="center">
      <a href="https://arxiv.org/abs/2508.09209"><img src="https://img.shields.io/badge/Read%20the%20preprint-arXiv%3A2508.09209-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white" alt="Read the arXiv preprint" /></a>
      <br /><br />
      <img src="https://img.shields.io/badge/Domain-Quantum%20Machine%20Learning-7C3AED?style=flat-square" alt="Quantum Machine Learning" />
      <img src="https://img.shields.io/badge/Model-GANs-2563EB?style=flat-square" alt="GANs" />
      <img src="https://img.shields.io/badge/Tool-Qiskit-6929C4?style=flat-square" alt="Qiskit" />
      <img src="https://img.shields.io/badge/Eval-FID%20%2F%20KID-0F766E?style=flat-square" alt="FID and KID" />
      <br /><br />
      <sub>Quantum AI × Generative Modelling × Evaluation Discipline</sub>
    </td>
  </tr>
</table>

<details>
<summary><b>🔬 Open the research mental model</b></summary>

```mermaid
flowchart LR
  A[Research Question] --> B[Classical Baseline]
  A --> C[Quantum Circuit Latent Prior]
  C --> D[3 / 5 / 7 Qubit HQCGAN Variants]
  B --> E[Training + Samples]
  D --> E
  E --> F[FID / KID Evaluation]
  F --> G[Bounded Claims + Limitations]
  G --> H[Reproducible Repository + arXiv]
```

</details>

---

## Selected Research And Builds

<img src="./assets/project-nebula.svg" alt="Animated project constellation showing fishman7337 public GitHub projects" width="100%" />

### Featured builds

<table>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/fishman7337/hybrid-quantum-classical-gan-research"><img src="https://github-readme-stats.vercel.app/api/pin/?username=fishman7337&repo=hybrid-quantum-classical-gan-research&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=38BDF8&text_color=C9D1D9&icon_color=A78BFA" alt="HQCGAN repository card" /></a>
      <h3>🧬 Hybrid Quantum-Classical GAN Research</h3>
      <p>HQCGAN experiments comparing classical GAN baselines with noisy quantum-circuit latent priors on binary MNIST.</p>
      <p><b>Signal stack:</b> Qiskit · TensorFlow · GANs · FID/KID · experiment configs · reproducibility · arXiv.</p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/fishman7337/ISR"><img src="https://github-readme-stats.vercel.app/api/pin/?username=fishman7337&repo=ISR&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=38BDF8&text_color=C9D1D9&icon_color=A78BFA" alt="ISR repository card" /></a>
      <h3>🛰️ ISR Satellite Imagery Pipeline</h3>
      <p>Satellite imagery preparation, geometry/topology feature engineering, preliminary model screening, and W&B-tracked orchestration.</p>
      <p><b>Signal stack:</b> remote sensing · computer vision · PyTorch · W&B · geospatial features · governance docs.</p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/fishman7337/global-security-policy-intelligence"><img src="https://github-readme-stats.vercel.app/api/pin/?username=fishman7337&repo=global-security-policy-intelligence&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=38BDF8&text_color=C9D1D9&icon_color=A78BFA" alt="Global Security Policy Intelligence repository card" /></a>
      <h3>🌐 Global Security Policy Intelligence</h3>
      <p>Historical security analytics, governance/public-policy panels, ML/DL, graph intelligence, RAG safety, and reproducible MLOps.</p>
      <p><b>Signal stack:</b> React · ML · graph analytics · Neo4j · data engineering · RAG guardrails.</p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/fishman7337/sp-daaa-doaa-ca2-vegetable-classification-application"><img src="https://github-readme-stats.vercel.app/api/pin/?username=fishman7337&repo=sp-daaa-doaa-ca2-vegetable-classification-application&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=38BDF8&text_color=C9D1D9&icon_color=A78BFA" alt="VeggieAI repository card" /></a>
      <h3>🥬 VeggieAI MLOps Platform</h3>
      <p>Vegetable image classifier with model serving, auth, prediction history, CI/CD, pytest, security checks, Docker, and MLOps docs.</p>
      <p><b>Signal stack:</b> Flask · TensorFlow serving · model registry · CI/CD · security scanning · operational docs.</p>
    </td>
  </tr>
</table>

<details>
<summary><b>Open the full project map</b></summary>

<br />

| Arena | Repository | What it demonstrates |
|---|---|---|
| 🧬 Quantum / Generative AI | [`hybrid-quantum-classical-gan-research`](https://github.com/fishman7337/hybrid-quantum-classical-gan-research) | HQCGAN research, noisy quantum circuits, GAN evaluation, reproducible experiments |
| 🛰️ Geospatial / ISR | [`ISR`](https://github.com/fishman7337/ISR) | Satellite imagery preparation, feature engineering, PyTorch screening, W&B orchestration |
| 🌐 Policy Intelligence | [`global-security-policy-intelligence`](https://github.com/fishman7337/global-security-policy-intelligence) | Historical analytics, graph intelligence, RAG safety, governance panels |
| 🥬 MLOps Product | [`sp-daaa-doaa-ca2-vegetable-classification-application`](https://github.com/fishman7337/sp-daaa-doaa-ca2-vegetable-classification-application) | Model serving, CI/CD, security scans, Docker, classification app |
| 🏙️ Multimodal ML App | [`sp-daaa-doaa-ca1-housing-price-ml-application`](https://github.com/fishman7337/sp-daaa-doaa-ca1-housing-price-ml-application) | Tabular + NLP + image signals, Flask, Docker, tests, MLOps docs |
| 🔐 Secure Systems | [`yubikey-secure-endpoint-system`](https://github.com/fishman7337/yubikey-secure-endpoint-system) | Rust endpoint watchdog, security-key checks, audit logging, threat thinking |
| 📈 Math + Regression | [`sp-daaa-mai-ca3-wage-modelling`](https://github.com/fishman7337/sp-daaa-mai-ca3-wage-modelling) | Regression modelling, gradient descent, pytest, LaTeX reporting |
| 💬 NLP / Deep Learning | [`sp-daaa-dele-ca1-movie-review-sentiment-analysis`](https://github.com/fishman7337/sp-daaa-dele-ca1-movie-review-sentiment-analysis) | RNN, LSTM, GRU sentiment/rating prediction workflows |
| 🕹️ Reinforcement Learning | [`sp-daaa-dele-ca2-pendulum-reinforcement-learning`](https://github.com/fishman7337/sp-daaa-dele-ca2-pendulum-reinforcement-learning) | DQN-style experimentation and control-task learning |
| 📊 Visual Analytics | [`sp-daaa-davi-ca1-hdb-price-dashboard`](https://github.com/fishman7337/sp-daaa-davi-ca1-hdb-price-dashboard) | HDB resale analytics, Tableau workbook, cleaning/validation scripts |

</details>

---

## Technical Stack

<img src="./assets/skill-constellation.svg" alt="Animated skill constellation across machine learning vision quantum MLOps data and security" width="100%" />

<div align="center">

<img src="https://skillicons.dev/icons?i=python,pytorch,tensorflow,sklearn,opencv,flask,fastapi,docker,git,githubactions,postgres,sqlite,react,js,ts,rust,linux,vscode&perline=9" alt="Technology skill icons" />

</div>

<details>
<summary><b>Open the capability matrix</b></summary>

<br />

| Capability | Tools / methods | Portfolio signal |
|---|---|---|
| Machine Learning | Python, scikit-learn, TensorFlow, PyTorch, evaluation metrics | Classification, regression, GANs, RL, practical ML apps |
| Vision + Geospatial | OpenCV, image pipelines, satellite imagery, feature engineering | ISR, CV classification, object detection, image-derived signals |
| Quantum AI | Qiskit, parameterised quantum circuits, NISQ-aware design | HQCGAN research and arXiv preprint |
| MLOps + Backend | Flask, FastAPI, Docker, GitHub Actions, pytest | Model serving, CI/CD, security checks, deployable apps |
| Data + Analytics | Pandas, NumPy, SQL, dashboards, Plotly/Tableau | HDB/job market/student/audience analytics projects |
| Governance + Security | threat models, audit logs, model cards, risk controls, Rust | Responsible AI docs and secure endpoint tooling |

</details>

---

## Roadmap / Build Log

<img src="./assets/timeline-roadmap.svg" alt="Animated build roadmap timeline for Goh Kun Ming" width="100%" />

```mermaid
mindmap
  root((fishman7337))
    Applied AI Research
      Quantum GANs
      Honest Baselines
      Reproducible Experiments
    Perception Intelligence
      Computer Vision
      Sensor Fusion
      Remote Sensing
    AI Systems Engineering
      Flask and FastAPI
      Docker and CI/CD
      Model Serving
      Testing
    Data + Governance
      Dashboards
      Graph Intelligence
      RAG Safety
      Model Cards
```

---

## Profile Source

<img src="./assets/terminal-lab.svg" alt="Animated research terminal card with profile commands" width="100%" />

<details>
<summary><b>Open profile source controls</b></summary>

<br />

This README is not just a static markdown file. It ships with an editable visual system:

```bash
# change profile text, project labels, visual copy, and theme colors
code content/profile.yml

# regenerate all local animated SVGs
python scripts/build_assets.py

# optional: create local screenshots for QA
python scripts/render_preview.py
```

The SVGs are generated with native `<text>` elements, stable IDs, and layer comments, so you can edit them manually in VS Code, Figma, Illustrator, or Inkscape without dealing with flattened image text.

</details>

---

## GitHub Telemetry

<div align="center">

<img width="49%" src="https://github-readme-stats.vercel.app/api?username=fishman7337&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=38BDF8&text_color=C9D1D9&icon_color=A78BFA" alt="GitHub stats for fishman7337" />
<img width="49%" src="https://streak-stats.demolab.com?user=fishman7337&theme=tokyonight&hide_border=true&background=0D1117&ring=38BDF8&fire=F472B6&currStreakLabel=38BDF8" alt="GitHub streak stats for fishman7337" />

<img width="98%" src="https://github-readme-activity-graph.vercel.app/graph?username=fishman7337&theme=react-dark&hide_border=true&bg_color=0D1117&color=38BDF8&line=A78BFA&point=34D399" alt="GitHub activity graph for fishman7337" />

<img width="49%" src="https://github-readme-stats.vercel.app/api/top-langs/?username=fishman7337&layout=compact&theme=tokyonight&hide_border=true&bg_color=0D1117&title_color=38BDF8&text_color=C9D1D9" alt="Top languages for fishman7337" />
<img width="49%" src="https://github-profile-summary-cards.vercel.app/api/cards/productive-time?username=fishman7337&theme=tokyonight&utcOffset=8" alt="Productive time card for fishman7337" />

<img width="98%" src="https://github-profile-trophy.vercel.app/?username=fishman7337&theme=tokyonight&no-frame=true&no-bg=true&margin-w=15&margin-h=15&column=6" alt="GitHub profile trophies" />

</div>

<details>
<summary><b>🐍 Contribution snake setup</b></summary>

<br />

The bundle includes `.github/workflows/snake.yml`. After you push it, GitHub Actions can generate this contribution snake on the `output` branch:

```md
![fishman7337 contribution snake](https://raw.githubusercontent.com/fishman7337/fishman7337/output/github-contribution-grid-snake-dark.svg)
```

Uncomment the snake section below once the workflow has run at least once.

</details>

<!--
<div align="center">
  <img src="https://raw.githubusercontent.com/fishman7337/fishman7337/output/github-contribution-grid-snake-dark.svg" alt="fishman7337 contribution snake animation" />
</div>
-->

---

## Editable Visual System

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>1. Edit content once</h3>
      <p>Update <code>content/profile.yml</code> to change names, projects, stack labels, mission cards, timeline items, and theme colors.</p>
    </td>
    <td width="33%" valign="top">
      <h3>2. Regenerate visuals</h3>
      <p>Run <code>python scripts/build_assets.py</code>. All SVGs refresh from the same source of truth.</p>
    </td>
    <td width="33%" valign="top">
      <h3>3. Fine-tune manually</h3>
      <p>Every SVG keeps native text and stable IDs, so editing in VS Code, Figma, Illustrator, or Inkscape stays clean.</p>
    </td>
  </tr>
</table>

<details>
<summary><b>🛠️ What can be customised?</b></summary>

<br />

| Area | File | What to change |
|---|---|---|
| Profile identity | `content/profile.yml` | Name, handle, email, LinkedIn, ORCID, role, education, tagline |
| Visual theme | `content/profile.yml` | Neon palette, panel colors, muted text, highlight colors |
| SVG layout/text | `scripts/build_assets.py` | Coordinates, animation timing, card layouts, charts, icon labels |
| README structure | `README.md` | Section order, cards, external widgets, project writeups |
| GitHub automations | `.github/workflows/*.yml` | Contribution snake and optional automatic SVG regeneration |

</details>

---

## Contact

<div align="center">

<a href="mailto:kunmingaden@gmail.com"><img src="https://img.shields.io/badge/Email-kunmingaden%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>
<a href="https://www.linkedin.com/in/goh-kun-ming-58573430a/"><img src="https://img.shields.io/badge/LinkedIn-Goh%20Kun%20Ming-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="https://github.com/fishman7337"><img src="https://img.shields.io/badge/GitHub-fishman7337-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
<a href="https://arxiv.org/abs/2508.09209"><img src="https://img.shields.io/badge/Research-arXiv%3A2508.09209-B31B1B?style=for-the-badge&logo=arxiv&logoColor=white" alt="Research arXiv" /></a>

<br />
<br />

<img src="./assets/footer-wave.svg" alt="Animated footer wave with motto" width="100%" />

</div>

<!--
README maintenance note:
- Keep repository name exactly: fishman7337
- Keep README.md in repository root
- Edit content/profile.yml for SVG text/theme changes
- Regenerate SVGs with: python scripts/build_assets.py
-->
