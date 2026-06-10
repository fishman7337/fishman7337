<div align="center">

<img src="./assets/hero-cyberdeck.svg" alt="Goh Kun Ming fishman7337 animated AI research cyberdeck banner" width="100%" />

<br />

<img src="./assets/typing-intro.svg" alt="Applied AI intro for Goh Kun Ming" />

<br />

<a href="https://github.com/fishman7337"><img src="./assets/profile-buttons/github.svg" width="174" alt="GitHub fishman7337" /></a>
<a href="https://www.linkedin.com/in/goh-kun-ming-58573430a/"><img src="./assets/profile-buttons/linkedin.svg" width="204" alt="LinkedIn Goh Kun Ming" /></a>
<a href="mailto:kunmingaden@gmail.com"><img src="./assets/profile-buttons/email.svg" width="174" alt="Email" /></a>

<br />

<a href="https://orcid.org/0009-0008-7666-781X"><img src="./assets/profile-buttons/orcid.svg" width="184" alt="ORCID" /></a>
<a href="https://arxiv.org/abs/2508.09209"><img src="./assets/profile-buttons/arxiv.svg" width="174" alt="arXiv 2508.09209" /></a>

<br />
<br />

<img src="./assets/profile-buttons/public-work.svg" width="184" alt="Public work" />
<img src="./assets/profile-buttons/research-grade.svg" width="206" alt="Research grade" />

<br />

<img src="./assets/profile-buttons/ai-systems.svg" width="174" alt="AI systems" />
<img src="./assets/profile-buttons/singapore.svg" width="174" alt="Singapore" />

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
  timezone: "Asia/Singapore (SGT, UTC+08:00)",
  education: "Diploma in Applied AI & Analytics, Singapore Polytechnic",
  currentRole: "Applied AI Research Intern",
  publicResearch: "Quantum-Enhanced GANs preprint · arXiv:2508.09209",
  operatingMode: "research → reproducibility → evaluation → deployable systems",
  proofPoints: ["PyTorch", "Keras", "Qiskit", "Pandas/NumPy", "SQL", "AWS", "Docker", "CI/CD"]
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
      <a href="https://arxiv.org/abs/2508.09209"><img src="./assets/profile-buttons/read-preprint.svg" width="226" alt="Read the arXiv preprint" /></a>
      <br /><br />
      <img src="./assets/profile-buttons/quantum-ml.svg" width="190" alt="Quantum Machine Learning" />
      <img src="./assets/profile-buttons/gans.svg" width="142" alt="GANs" />
      <img src="./assets/profile-buttons/qiskit.svg" width="154" alt="Qiskit" />
      <img src="./assets/profile-buttons/fid-kid.svg" width="154" alt="FID and KID" />
      <br /><br />
      <sub>Quantum AI × Generative Modelling × Evaluation Discipline</sub>
    </td>
  </tr>
</table>

<details>
<summary><b>🔬 Open the research mental model</b></summary>

<img src="./assets/research-flow.svg" alt="Research flow from question to baselines quantum priors evaluation bounded claims and public artifact" width="100%" />

</details>

---

## Selected Research And Builds

<img src="./assets/project-nebula.svg" alt="Animated project constellation showing fishman7337 public GitHub projects" width="100%" />

### Featured builds

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🧬 Hybrid Quantum-Classical GAN Research</h3>
      <p>HQCGAN experiments comparing classical GAN baselines with noisy quantum-circuit latent priors on binary MNIST.</p>
      <p><b>Signal stack:</b> Qiskit · TensorFlow · GANs · FID/KID · experiment configs · reproducibility · arXiv.</p>
      <p><a href="https://github.com/fishman7337/hybrid-quantum-classical-gan-research"><b>Open repository</b></a></p>
    </td>
    <td width="50%" valign="top">
      <h3>🛰️ ISR Satellite Imagery Pipeline</h3>
      <p>Satellite imagery preparation, geometry/topology feature engineering, preliminary model screening, and W&B-tracked orchestration.</p>
      <p><b>Signal stack:</b> remote sensing · computer vision · PyTorch · W&B · geospatial features · governance docs.</p>
      <p><a href="https://github.com/fishman7337/ISR"><b>Open repository</b></a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🌐 Global Security Policy Intelligence</h3>
      <p>Historical security analytics, governance/public-policy panels, ML/DL, graph intelligence, RAG safety, and reproducible MLOps.</p>
      <p><b>Signal stack:</b> React · ML · graph analytics · Neo4j · data engineering · RAG guardrails.</p>
      <p><a href="https://github.com/fishman7337/global-security-policy-intelligence"><b>Open repository</b></a></p>
    </td>
    <td width="50%" valign="top">
      <h3>🥬 VeggieAI MLOps Platform</h3>
      <p>Vegetable image classifier with model serving, auth, prediction history, CI/CD, pytest, security checks, Docker, and MLOps docs.</p>
      <p><b>Signal stack:</b> Flask · TensorFlow serving · model registry · CI/CD · security scanning · operational docs.</p>
      <p><a href="https://github.com/fishman7337/sp-daaa-doaa-ca2-vegetable-classification-application"><b>Open repository</b></a></p>
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

<p><b>Clickable stack map - rounded logo cards - no duplicate technologies</b></p>

<p align="center">
<a href="https://www.python.org/"><img src="./assets/tech-logos/python.svg" width="68" height="68" alt="Python" /></a> <a href="https://pytorch.org/"><img src="./assets/tech-logos/pytorch.svg" width="68" height="68" alt="PyTorch" /></a> <a href="https://www.tensorflow.org/"><img src="./assets/tech-logos/tensorflow.svg" width="68" height="68" alt="TensorFlow" /></a> <a href="https://keras.io/"><img src="./assets/tech-logos/keras.svg" width="68" height="68" alt="Keras" /></a> <a href="https://scikit-learn.org/"><img src="./assets/tech-logos/scikit-learn.svg" width="68" height="68" alt="scikit-learn" /></a> <a href="https://jupyter.org/"><img src="./assets/tech-logos/jupyter.svg" width="68" height="68" alt="Jupyter" /></a>
<br />
<a href="https://www.qiskit.org/"><img src="./assets/tech-logos/qiskit.svg" width="68" height="68" alt="Qiskit" /></a> <a href="https://pennylane.ai/"><img src="./assets/tech-logos/pennylane.svg" width="68" height="68" alt="PennyLane" /></a> <a href="https://opencv.org/"><img src="./assets/tech-logos/opencv.svg" width="68" height="68" alt="OpenCV" /></a> <a href="https://www.ros.org/"><img src="./assets/tech-logos/ros.svg" width="68" height="68" alt="ROS" /></a> <a href="https://pandas.pydata.org/"><img src="./assets/tech-logos/pandas.svg" width="68" height="68" alt="Pandas" /></a> <a href="https://numpy.org/"><img src="./assets/tech-logos/numpy.svg" width="68" height="68" alt="NumPy" /></a>
<br />
<a href="https://matplotlib.org/"><img src="./assets/tech-logos/matplotlib.svg" width="68" height="68" alt="Matplotlib" /></a> <a href="https://seaborn.pydata.org/"><img src="./assets/tech-logos/seaborn.svg" width="68" height="68" alt="Seaborn" /></a> <a href="https://www.statsmodels.org/"><img src="./assets/tech-logos/statsmodels.svg" width="68" height="68" alt="statsmodels" /></a> <a href="https://plotly.com/python/"><img src="./assets/tech-logos/plotly.svg" width="68" height="68" alt="Plotly" /></a> <a href="https://dash.plotly.com/"><img src="./assets/tech-logos/dash.svg" width="68" height="68" alt="Dash" /></a> <a href="https://www.tableau.com/"><img src="./assets/tech-logos/tableau.svg" width="68" height="68" alt="Tableau" /></a>
<br />
<a href="https://powerbi.microsoft.com/"><img src="./assets/tech-logos/power-bi.svg" width="68" height="68" alt="Power BI" /></a> <a href="https://developer.mozilla.org/en-US/docs/Web/HTML"><img src="./assets/tech-logos/html5.svg" width="68" height="68" alt="HTML5" /></a> <a href="https://developer.mozilla.org/en-US/docs/Web/CSS"><img src="./assets/tech-logos/css.svg" width="68" height="68" alt="CSS" /></a> <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript"><img src="./assets/tech-logos/javascript.svg" width="68" height="68" alt="JavaScript" /></a> <a href="https://www.typescriptlang.org/"><img src="./assets/tech-logos/typescript.svg" width="68" height="68" alt="TypeScript" /></a> <a href="https://react.dev/"><img src="./assets/tech-logos/react.svg" width="68" height="68" alt="React" /></a>
<br />
<a href="https://vuejs.org/"><img src="./assets/tech-logos/vue.svg" width="68" height="68" alt="Vue" /></a> <a href="https://nextjs.org/"><img src="./assets/tech-logos/nextjs.svg" width="68" height="68" alt="Next.js" /></a> <a href="https://nodejs.org/"><img src="./assets/tech-logos/nodejs.svg" width="68" height="68" alt="Node.js" /></a> <a href="https://vite.dev/"><img src="./assets/tech-logos/vite.svg" width="68" height="68" alt="Vite" /></a> <a href="https://tailwindcss.com/"><img src="./assets/tech-logos/tailwindcss.svg" width="68" height="68" alt="Tailwind CSS" /></a> <a href="https://www.postgresql.org/"><img src="./assets/tech-logos/postgresql.svg" width="68" height="68" alt="PostgreSQL" /></a>
<br />
<a href="https://www.sqlite.org/"><img src="./assets/tech-logos/sqlite.svg" width="68" height="68" alt="SQLite" /></a> <a href="https://neo4j.com/"><img src="./assets/tech-logos/neo4j.svg" width="68" height="68" alt="Neo4j" /></a> <a href="https://aws.amazon.com/"><img src="./assets/tech-logos/aws.svg" width="68" height="68" alt="AWS" /></a> <a href="https://cloud.google.com/"><img src="./assets/tech-logos/gcp.svg" width="68" height="68" alt="Google Cloud" /></a> <a href="https://kubernetes.io/"><img src="./assets/tech-logos/kubernetes.svg" width="68" height="68" alt="Kubernetes" /></a> <a href="https://www.docker.com/"><img src="./assets/tech-logos/docker.svg" width="68" height="68" alt="Docker" /></a>
<br />
<a href="https://fastapi.tiangolo.com/"><img src="./assets/tech-logos/fastapi.svg" width="68" height="68" alt="FastAPI" /></a> <a href="https://flask.palletsprojects.com/"><img src="./assets/tech-logos/flask.svg" width="68" height="68" alt="Flask" /></a> <a href="https://github.com/features/actions"><img src="./assets/tech-logos/github-actions.svg" width="68" height="68" alt="GitHub Actions" /></a> <a href="https://docs.pytest.org/"><img src="./assets/tech-logos/pytest.svg" width="68" height="68" alt="pytest" /></a> <a href="https://wandb.ai/"><img src="./assets/tech-logos/wandb.svg" width="68" height="68" alt="Weights and Biases" /></a> <a href="https://www.rust-lang.org/"><img src="./assets/tech-logos/rust.svg" width="68" height="68" alt="Rust" /></a>
</p>

</div>

<details>
<summary><b>Open the capability matrix</b></summary>

<br />

| Capability | Tools / methods | Portfolio signal |
|---|---|---|
| Machine Learning | Python, PyTorch, TensorFlow, Keras, scikit-learn, Jupyter, evaluation metrics | Classification, regression, GANs, RL, practical ML apps |
| Web + Frontend | HTML5, CSS, JavaScript, TypeScript, React, Vue, Next.js, Node.js, Vite, Tailwind CSS | Dashboards, portfolio UI, public-facing AI tools, interactive app surfaces |
| Data + Statistics | Pandas, NumPy, Matplotlib, Seaborn, statsmodels, SQL | HDB analytics, wage modelling, statistical reports, validation scripts |
| Vision + Robotics | OpenCV, ROS, sensor fusion, satellite imagery, feature engineering | ISR, CV classification, object detection, perception pipelines |
| Quantum AI | Qiskit, PennyLane, AerSimulator, parameterised quantum circuits, NISQ-aware design | HQCGAN research and arXiv preprint |
| Visual Apps + Graphs | Plotly, Dash, Tableau, Power BI, Neo4j, graph analytics | Dashboards, policy intelligence, exploratory analysis, graph-backed insights |
| Systems + Cloud | Flask, FastAPI, Docker, Kubernetes, GitHub Actions, AWS, GCP, pytest | Model serving, CI/CD, security checks, deployable apps |
| Governance + Security | threat models, audit logs, model cards, risk controls, Rust | Responsible AI docs and secure endpoint tooling |

</details>

---

## Roadmap / Build Log

<img src="./assets/timeline-roadmap.svg" alt="Animated build roadmap timeline for Goh Kun Ming" width="100%" />

<img src="./assets/roadmap-mindmap.svg" alt="Stable roadmap mindmap covering research perception systems data and governance" width="100%" />

---

## Systems Console

<img src="./assets/terminal-lab.svg" alt="Animated research terminal showing AI systems, experiments, and deployment checks" width="100%" />

---

## GitHub Telemetry

<div align="center">

<sub>Telemetry timezone: Singapore Time (SGT, UTC+08:00).</sub>
<br />
<sub>Cards are checked-in SVG snapshots for reliable GitHub rendering. Refresh with <code>python scripts/build_github_telemetry_cards.py</code>.</sub>
<br /><br />

<img width="98%" src="./assets/github-telemetry/profile-details.svg" alt="GitHub telemetry snapshot for fishman7337" />

<img width="49%" src="./assets/github-telemetry/stats.svg" alt="Repository stats for fishman7337" />
<img width="49%" src="./assets/github-telemetry/productive-time.svg" alt="Repository update time distribution for fishman7337 in Singapore time" />

<img width="49%" src="./assets/github-telemetry/repos-per-language.svg" alt="Repositories per language for fishman7337" />
<img width="49%" src="./assets/github-telemetry/language-volume.svg" alt="Top languages by code volume for fishman7337" />

<img width="98%" src="./assets/github-telemetry/activity-snapshot.svg" alt="Recent repository activity snapshot for fishman7337" />

</div>

## Contact

<div align="center">

<a href="mailto:kunmingaden@gmail.com"><img src="./assets/profile-buttons/email.svg" width="174" alt="Email" /></a>
<a href="https://www.linkedin.com/in/goh-kun-ming-58573430a/"><img src="./assets/profile-buttons/linkedin.svg" width="204" alt="LinkedIn" /></a>
<a href="https://github.com/fishman7337"><img src="./assets/profile-buttons/github.svg" width="174" alt="GitHub" /></a>
<a href="https://arxiv.org/abs/2508.09209"><img src="./assets/profile-buttons/arxiv.svg" width="174" alt="Research arXiv" /></a>

<br />
<br />

<img src="./assets/footer-wave.svg" alt="Animated footer wave with motto" width="100%" />

</div>
