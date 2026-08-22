<div align="center">

<img src="./assets/hero-signal-garden.svg" width="100%" alt="Goh Kun Ming — Applied AI and Analytics student, introduced beside a luminous 3D signal garden" />

<br />

<a href="https://github.com/fishman7337"><img src="./assets/profile-buttons/github.svg" width="174" alt="GitHub profile" /></a>
<a href="https://www.linkedin.com/in/gohkunming/"><img src="./assets/profile-buttons/linkedin.svg" width="204" alt="LinkedIn profile" /></a>
<a href="mailto:kunmingaden@gmail.com"><img src="./assets/profile-buttons/email.svg" width="174" alt="Send email" /></a>

<br />

<a href="https://orcid.org/0009-0008-7666-781X"><img src="./assets/profile-buttons/orcid.svg" width="184" alt="ORCID researcher profile" /></a>
<a href="https://arxiv.org/abs/2508.09209"><img src="./assets/profile-buttons/arxiv.svg" width="174" alt="Read the arXiv preprint" /></a>

<br /><br />

<a href="#what-im-growing">What I’m growing</a> ·
<a href="#selected-work">Selected work</a> ·
<a href="#research-spotlight">Research</a> ·
<a href="#tool-garden">Tools</a> ·
<a href="#how-i-work">Process</a> ·
<a href="#say-hello">Contact</a>

</div>

---

## Hello

I’m Kun Ming, an Applied AI & Analytics student in Singapore. I like the whole path from an interesting question to a working artifact: understanding the data, establishing a baseline, experimenting carefully, and turning the useful parts into something other people can inspect and use.

> My favourite projects sit where rigorous experiments meet playful, approachable software.

## What I’m growing

<img src="./assets/focus-garden.svg" width="100%" alt="Explore, Model, Build, and Share — four stages for growing an idea" />

## Selected work

<img src="./assets/project-garden.svg" width="100%" alt="Animated constellation of six selected projects in quantum ML, vision, creative ML, algorithms, applied ML, and full-stack development" />

<table>
  <tr>
    <td width="50%" valign="top">
      <h3>🫧 <a href="https://github.com/fishman7337/hybrid-quantum-classical-gan-research">HQCGAN Research</a></h3>
      <p>Classical and hybrid quantum-classical GAN experiments with noisy circuit priors, FID/KID evaluation, tests, and a public preprint.</p>
      <p><code>Qiskit</code> <code>TensorFlow</code> <code>GANs</code> <code>arXiv</code></p>
    </td>
    <td width="50%" valign="top">
      <h3>🍃 <a href="https://github.com/fishman7337/leaf-object-detection">Leaf Object Detection</a></h3>
      <p>A reproducible YOLO pipeline for data preparation, annotation validation, training, ONNX export, and browser inference.</p>
      <p><code>Python</code> <code>YOLO</code> <code>ONNX</code> <code>CV</code></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🌙 <a href="https://github.com/fishman7337/sp-daaa-dsaa-ca1-haiku-generator">HaikuForge AI</a></h3>
      <p>A 5–7–5-aware haiku lab with Markov generation, poetic transformations, batch permutations, and WAV narration.</p>
      <p><code>NLP</code> <code>Markov chains</code> <code>Audio</code> <code>Python</code></p>
    </td>
    <td width="50%" valign="top">
      <h3>📰 <a href="https://github.com/fishman7337/sp-daaa-dsaa-ca2-newspaper-restoration">Newspaper Restoration</a></h3>
      <p>An explainable historical-text toolkit using prefix tries, wildcard restoration, edit-distance search, and graph visualisation.</p>
      <p><code>Tries</code> <code>Algorithms</code> <code>NetworkX</code> <code>pytest</code></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3>🚕 <a href="https://github.com/fishman7337/sp-daaa-pai-ca2-gobest-trip-safety-predictor">GoBest Trip Predictor</a></h3>
      <p>An educational offline desktop ML app with batch inference, feedback collection, lightweight drift checks, and packaged smoke tests.</p>
      <p><code>CustomTkinter</code> <code>scikit-learn</code> <code>PyInstaller</code></p>
    </td>
    <td width="50%" valign="top">
      <h3>🏃 <a href="https://github.com/fishman7337/sp-daaa-bed-ca-fitnessquest">FitnessQuest</a></h3>
      <p>A gamified fitness web app with authenticated APIs, responsive flows, security regression tests, and browser automation.</p>
      <p><code>Express</code> <code>MySQL</code> <code>JWT</code> <code>Playwright</code></p>
    </td>
  </tr>
</table>

<details>
<summary><b>Open a few more builds</b></summary>

<br />

| Project | What it explores |
| --- | --- |
| [EstateScope AI](https://github.com/fishman7337/sp-daaa-doaa-ca1-housing-price-ml-application) | Housing-value modelling across tabular, text, and image signals |
| [VeggieAI](https://github.com/fishman7337/sp-daaa-doaa-ca2-vegetable-classification-application) | Image classification, model serving, CI, Docker, and application workflows |
| [Movie Sentiment AI](https://github.com/fishman7337/sp-daaa-dele-ca1-movie-review-sentiment-analysis) | SimpleRNN, LSTM, and GRU workflows for sentiment and rating prediction |
| [Pendulum Reinforcement Learning](https://github.com/fishman7337/sp-daaa-dele-ca2-pendulum-reinforcement-learning) | Control-task experimentation with DQN-style learning |
| [HDB Price Dashboard](https://github.com/fishman7337/sp-daaa-davi-ca1-hdb-price-dashboard) | Singapore resale-price cleaning, analysis, validation, and dashboards |

</details>

## Research spotlight

<table>
  <tr>
    <td width="64%" valign="top">
      <h3>Quantum-Enhanced Generative Adversarial Networks</h3>
      <p>My public preprint compares a classical GAN with 3-, 5-, and 7-qubit hybrid variants that use parameterised quantum circuits as latent priors.</p>
      <ul>
        <li>Binary MNIST digits 0 and 1 under constrained latent dimensions.</li>
        <li>Qiskit AerSimulator with realistic noise models.</li>
        <li>FID and KID for image-quality evaluation.</li>
        <li>Reproducibility helpers, configuration, tests, and explicit limitations.</li>
      </ul>
      <p>The classical baseline led overall; the value of the study is the comparison, the reproducible trail, and a bounded look at what near-term hybrid approaches can and cannot do.</p>
    </td>
    <td width="36%" valign="middle" align="center">
      <a href="https://arxiv.org/abs/2508.09209"><img src="./assets/profile-buttons/read-preprint.svg" width="226" alt="Read the public preprint" /></a>
      <br /><br />
      <img src="./assets/profile-buttons/quantum-ml.svg" width="190" alt="Quantum machine learning" />
      <img src="./assets/profile-buttons/qiskit.svg" width="154" alt="Qiskit" />
      <img src="./assets/profile-buttons/fid-kid.svg" width="154" alt="FID and KID" />
    </td>
  </tr>
</table>

## Tool garden

<div align="center">

<p><b>AI + ML</b></p>

<a href="https://www.python.org/"><img src="./assets/tech-logos/python.svg" width="68" height="68" alt="Python" /></a>
<a href="https://pytorch.org/"><img src="./assets/tech-logos/pytorch.svg" width="68" height="68" alt="PyTorch" /></a>
<a href="https://www.tensorflow.org/"><img src="./assets/tech-logos/tensorflow.svg" width="68" height="68" alt="TensorFlow" /></a>
<a href="https://keras.io/"><img src="./assets/tech-logos/keras.svg" width="68" height="68" alt="Keras" /></a>
<a href="https://scikit-learn.org/"><img src="./assets/tech-logos/scikit-learn.svg" width="68" height="68" alt="scikit-learn" /></a>
<a href="https://qiskit.org/"><img src="./assets/tech-logos/qiskit.svg" width="68" height="68" alt="Qiskit" /></a>
<a href="https://opencv.org/"><img src="./assets/tech-logos/opencv.svg" width="68" height="68" alt="OpenCV" /></a>

<p><b>Data + product</b></p>

<a href="https://pandas.pydata.org/"><img src="./assets/tech-logos/pandas.svg" width="68" height="68" alt="Pandas" /></a>
<a href="https://numpy.org/"><img src="./assets/tech-logos/numpy.svg" width="68" height="68" alt="NumPy" /></a>
<a href="https://plotly.com/python/"><img src="./assets/tech-logos/plotly.svg" width="68" height="68" alt="Plotly" /></a>
<a href="https://flask.palletsprojects.com/"><img src="./assets/tech-logos/flask.svg" width="68" height="68" alt="Flask" /></a>
<a href="https://fastapi.tiangolo.com/"><img src="./assets/tech-logos/fastapi.svg" width="68" height="68" alt="FastAPI" /></a>
<a href="https://nodejs.org/"><img src="./assets/tech-logos/nodejs.svg" width="68" height="68" alt="Node.js" /></a>
<a href="https://react.dev/"><img src="./assets/tech-logos/react.svg" width="68" height="68" alt="React" /></a>
<a href="https://www.postgresql.org/"><img src="./assets/tech-logos/postgresql.svg" width="68" height="68" alt="PostgreSQL" /></a>

<p><b>Delivery + quality</b></p>

<a href="https://www.docker.com/"><img src="./assets/tech-logos/docker.svg" width="68" height="68" alt="Docker" /></a>
<a href="https://github.com/features/actions"><img src="./assets/tech-logos/github-actions.svg" width="68" height="68" alt="GitHub Actions" /></a>
<a href="https://docs.pytest.org/"><img src="./assets/tech-logos/pytest.svg" width="68" height="68" alt="pytest" /></a>

</div>

## How I work

<img src="./assets/research-loop.svg" width="100%" alt="Question, Baseline, Experiment, Evaluate, Share — an evidence-first research loop" />

- **Start with the question.** The model comes after the problem and the data are understood.
- **Keep a baseline nearby.** Complexity has to earn its place.
- **Make the path reproducible.** Configs, tests, seeds, and docs are part of the artifact.
- **Report limits with the result.** A useful claim includes its boundary.
- **Turn experiments into tools.** The best ideas become something inspectable and approachable.

## Contribution garden

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/fishman7337/fishman7337/output/github-contribution-grid-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/fishman7337/fishman7337/output/github-contribution-grid-snake.svg" />
  <img alt="Animated contribution trail" src="https://raw.githubusercontent.com/fishman7337/fishman7337/output/github-contribution-grid-snake.svg" width="100%" />
</picture>

<br />

<img width="49%" src="./assets/github-telemetry/stats.svg" alt="Checked-in public repository statistics snapshot" />
<img width="49%" src="./assets/github-telemetry/productive-time.svg" alt="Checked-in repository update-time distribution in Singapore time" />

<br />

<sub>Telemetry is a checked-in snapshot generated from public GitHub metadata; it is descriptive, not a measure of impact.</sub>

</div>

## Say hello

I’m always happy to talk about careful ML experiments, creative computing, reproducibility, and building better learning projects.

<div align="center">

<a href="mailto:kunmingaden@gmail.com"><img src="./assets/profile-buttons/email.svg" width="174" alt="Email Goh Kun Ming" /></a>
<a href="https://www.linkedin.com/in/gohkunming/"><img src="./assets/profile-buttons/linkedin.svg" width="204" alt="Connect on LinkedIn" /></a>
<a href="https://github.com/fishman7337"><img src="./assets/profile-buttons/github.svg" width="174" alt="Explore GitHub repositories" /></a>

<br /><br />

<img src="./assets/signal-footer.svg" width="100%" alt="Stay curious, measure honestly, and build with care" />

</div>
