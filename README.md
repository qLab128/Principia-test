<h1 align="center">Principia</h1>

<p align="center">
  <b>Ideas from principles, validated by evidence.</b>
</p>

<p align="center">
  Principia is a local-first research workbench that turns papers into reusable principles,
  composes those principles into traceable research ideas, and helps researchers inspect
  why an idea may be worth testing.
</p>

<p align="center">
  <a href="https://github.com/pzqpzq/Principia"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-pzqpzq%2FPrincipia-181717?logo=github"></a>
  <img alt="Version" src="https://img.shields.io/badge/version-v1.1-0f766e">
  <img alt="Paper" src="https://img.shields.io/badge/ICML-2026-2563eb">
  <img alt="Mode" src="https://img.shields.io/badge/mode-local--first-7c3aed">
  <img alt="Cloud" src="https://img.shields.io/badge/cloud-GitHub--native-0366d6">
  <img alt="Python" src="https://img.shields.io/badge/python-3.9%2B-blue">
</p>

<p align="center">
  <a href="#research-highlight">Research Highlight</a> ·
  <a href="#why-principia">Why Principia</a> ·
  <a href="#product-tour">Product Tour</a> ·
  <a href="#v11-highlights">V1.1 Highlights</a> ·
  <a href="#quick-start">Quick Start</a> ·
  <a href="#contact">Contact</a>
</p>

---

## Research Highlight

Principia is connected to our ICML research on symbolic communication among LLM agents:

> **[When LLMs Develop Languages: Symbolic Communication for Efficient Multi-Agent Reasoning](https://icml.cc/virtual/2026/poster/61557)**  
> ICML 2026

The paper introduces **Communicative Language Symbolism Routing (CLSR)**, a test-time framework where multiple LLM agents autonomously invent, evolve, share, and route compact **Language Symbolism Frameworks (LSFs)** to improve the accuracy-token trade-off.

**Principia Calculus** brings this idea into research ideation: instead of asking an LLM to directly write a proposal, Principia lets the model build intermediate symbolic handles, compose them, verify derivation steps, and expose the lineage behind the final Idea Card.

---

<p align="center">
  <img src="docs/screenshots/main_operation.png" width="80%" alt="Principia research workspace">
</p>

<p align="center">
  <i>From a rough research goal to a structured, lineage-backed idea workspace.</i>
</p>

---

## Why Principia

Most AI brainstorming tools produce fluent text. Principia is designed for a higher standard: **a good research idea should show where it came from, what it assumes, what evidence supports it, and how it can be tested.**

Principia turns ideation into a visible workflow:

```text
research goal
  → relevant works
  → existed ideas
  → principles
  → takeaway messages
  → evidence composition
  → symbolic derivation
  → Idea Card
  → comparison, validation, and export
```

### What makes it different

| Instead of... | Principia gives you... |
|---|---|
| Black-box brainstorming | Idea Cards with source evidence, assumptions, risks, and derivation traces |
| Paper summaries only | Reusable principles, benchmarks, baselines, takeaways, and existed ideas |
| RAG over whole papers | Concept-level retrieval: select only the specific evidence that matters |
| One-shot idea generation | Standard generation plus deeper **Principia Calculus** symbolic derivation |
| Local notes that stay isolated | A local research memory plus an optional GitHub-native Cloud Library |

Principia is not trying to be another chatbot. It is the **principle, evidence, and validation layer** for research ideation.

---

## Product Tour

### 1. Build a research workspace

Create a project, describe your research target, choose a model, set the number of works to research, and let Principia organize the run.

<table>
<tr>
<td width="50%"><img src="docs/screenshots/main_existedIdeas.png" alt="Existed Ideas"></td>
<td width="50%"><img src="docs/screenshots/main_principles.png" alt="Principles tab"></td>
</tr>
<tr>
<td align="center"><b>Existed works & ideas</b></td>
<td align="center"><b>Principles library</b></td>
</tr>
</table>

### 2. Convert literature into reusable research objects

Principia extracts more than summaries. Each work can become a set of structured records: prior ideas, principles, takeaways, benchmarks, baselines, and evidence links.

<table>
<tr>
<td width="41%"><img src="docs/screenshots/principle_card.png" alt="Principle card"></td>
<td width="59%"><img src="docs/screenshots/generate_idea.png" alt="Generate new Ideas"></td>
</tr>
<tr>
<td align="center"><b>Principle details</b></td>
<td align="center"><b>Evidence composer</b></td>
</tr>
</table>

### 3. Generate an Idea Card from selected evidence

You decide which evidence the model should use. Principia then generates a structured Idea Card with the thesis, mechanism, novelty claim, method variants, validation protocol, metrics, risks, and related prior work.

<table>
<tr>
<td width="50%"><img src="docs/screenshots/idea_summary.png" alt="Generated idea overview"></td>
<td width="50%"><img src="docs/screenshots/idea_summary2.png" alt="Generated idea details"></td>
</tr>
<tr>
<td align="center"><b>Idea overview</b></td>
<td align="center"><b>Validation-ready details</b></td>
</tr>
</table>

### 4. Inspect the reasoning path

Principia Calculus reveals the symbolic construction process behind an idea. The final output is not only a paragraph; it is a lineage graph that shows how concepts were transformed and composed.

<table>
<tr>
<td width="50%"><img src="docs/screenshots/idea_calculus.png" alt="Principia Calculus lineage graph"></td>
<td width="50%"><img src="docs/screenshots/idea_principleMap.png" alt="Principle map"></td>
</tr>
<tr>
<td align="center"><b>Symbolic lineage</b></td>
<td align="center"><b>Principle map</b></td>
</tr>
</table>

### 5. Compare against related ideas

Principia helps you reason about novelty by comparing a generated idea with nearby existed ideas, highlighting similarities, differences, and potential advantages.

<p align="center">
  <img src="docs/screenshots/idea_comparison.png" width="75%" alt="Related ideas comparison">
</p>

---

## V1.1 Highlights

### Principia Calculus, upgraded

V1.1 deepens the symbolic idea-discovery mode. Principia can now build intermediate symbolic structures, connect them through derivation steps, and show how the generated idea emerged from selected principles and evidence.

```text
selected evidence
  → compact symbolic handles
  → derivation patches
  → verifier checks
  → speculative L0 nodes
  → lineage graph
  → final Idea Card
```

This makes ideation more inspectable: you can see not only **what** the model proposed, but **how** it got there.

### Cloud Library

V1.1 introduces a GitHub-native Cloud Library for shared research memory. The local app remains the main workspace, but it can read released public records from the cloud before spending new LLM calls.

In practice, this means Principia can:

- search cloud records by title, venue, year, author, model, concept type, benchmark, or baseline;
- reuse existing paper extractions when the cloud already has the latest version;
- store multiple LLM-specific versions for the same work;
- sync selected local research outputs to the cloud with admin authorization;
- crawl candidate papers from top AI venues and queue them for research;
- keep paper full text out of the public cloud memory by storing structured Principia records instead.

Open the Cloud Library UI after starting the app:

```text
http://127.0.0.1:8795/cloud
```

### Local-first by default

Principia is designed for serious research workflows where privacy matters. Your project state, local database, selected evidence, generated ideas, and unpublished notes stay on your machine unless you explicitly sync selected records.

### Evidence-aware idea generation

Before producing an idea, Principia lets you choose the exact ingredients: works, existed ideas, principles, takeaway messages, benchmarks, and baselines. This makes the generation process easier to audit and easier to reproduce.

### Research memory that compounds

A Principia workspace improves as it accumulates literature, extracted concepts, symbolic derivations, and user feedback. The long-term artifact is not a chat transcript; it is a reusable principle memory.

---

## Who Is Principia For?

Principia is built for:

- AI researchers who want stronger idea provenance;
- PhD students building literature-grounded research directions;
- research engineers turning ideas into validation plans;
- lab teams collecting reusable principles across papers;
- independent researchers who want a local-first research workbench;
- builders who want to connect ideation with Codex-style implementation workflows.

---

## Quick Start

Principia requires **Python 3.9+**. Python **3.12** is recommended.

```bash
git clone https://github.com/pzqpzq/Principia.git
cd Principia

python3.12 -m pip install -r requirements.txt
cp .env.example .env

python3.12 principia.py serve --host 127.0.0.1 --port 8795
```

Open the local app:

```text
http://127.0.0.1:8795/
```

The repository includes a compact release database so that you can explore the interface immediately.

### Configure LLM providers

Add your own keys to `.env`. Do not commit `.env`.

```text
SILICONFLOW_API_KEY=your_siliconflow_key_here
OPENAI_API_KEY=your_openai_key_here

PRINCIPIA_LLM_BASE_URL=https://api.siliconflow.cn/v1
PRINCIPIA_OPENAI_BASE_URL=https://api.openai.com/v1
```

Principia surfaces failed online model calls instead of silently replacing them with template content. Completed extraction batches are preserved even if a later stage fails.

---

## Basic Workflow

1. **Create or open a project.**  
   Keep independent goals, selected materials, research runs, and generated ideas in one workspace.

2. **Run research.**  
   Principia retrieves relevant works and extracts structured records: works, existed ideas, principles, takeaways, benchmarks, baselines, and result facts.

3. **Compose evidence.**  
   Select exactly which records should influence the next generated idea.

4. **Generate with Standard mode or Principia Calculus.**  
   Standard mode is faster. Principia Calculus is deeper and more inspectable.

5. **Inspect, compare, and export.**  
   Review the Idea Card, principle map, symbolic lineage, related idea comparison, validation protocol, and Markdown export.

---

## Principia Cloud Library

The V1.1 Cloud Library is designed to make repeated research cheaper and faster while keeping the product local-first.

When Principia sees a candidate paper during research, it can check whether the cloud already contains a compatible extraction for the selected LLM and paper version. If yes, the app can hydrate the local workspace from the cloud record instead of calling the model again. If not, Principia can research the paper locally and optionally prepare a contribution for cloud sync.

Cloud Library modes:

| Mode | What it is for |
|---|---|
| **Search** | Find released works, principles, benchmarks, baselines, and takeaways |
| **Hydrate** | Pull selected cloud records into your local workspace |
| **Sync** | Upload selected local research outputs after admin authorization |
| **Crawl** | Discover papers from AI venues and queue them for research |
| **Admin** | Edit, delete, merge, or export cloud operations with audit notes |

The cloud design is intentionally GitHub-native: it can be hosted through repository files, release assets, contribution packs, and GitHub workflows rather than a separately deployed database server.

---

## Principia Calculus

Principia Calculus is the signature generation mode in V1.1.

A normal LLM prompt often hides its reasoning inside a single answer. Principia Calculus instead creates a symbolic workspace where evidence-backed concepts can be compressed, composed, checked, and expanded again.

Example:

```text
P.ATCU  = Adaptive token/compute routing under uncertainty
P.EFB   = Evaluator-first binding
TM.ROH  = Routing overhead can erase gains

D.EVR   = compose(P.ATCU, P.EFB)
D.COST  = stress_test(D.EVR, TM.ROH)
I.EVRA  = specialize(D.COST, research-agent ideation)
```

The goal is not to make the model sound more mathematical. The goal is to make the idea-generation process **inspectable, editable, and reusable**.

---

## Research Integrity and Privacy

Principia is built around provenance and user control.

- Generated ideas should trace back to selected evidence.
- Benchmarks and baselines should be official or source-grounded.
- Speculative symbolic nodes are marked separately from evidence-backed records.
- Full paper text may be used transiently for extraction, but it is not retained as public cloud memory.
- Private projects stay local unless you explicitly sync selected records.
- Cloud write operations require admin authorization.
- Failed model calls are surfaced rather than hidden behind fake fallback content.

---

## For Developers

The main app is intentionally simple to run: a local Python service, a browser UI, and local SQLite-backed research memory.

<details>
<summary>Useful commands</summary>

```bash
# Start the local app
python3.12 principia.py serve --host 127.0.0.1 --port 8795

# Inspect local research memory
python3.12 principia.py state --v1

# Run a research task
python3.12 principia.py research "efficient LLM research agents" --target-works 50

# Retrieve selected concept types
python3.12 principia.py retrieve "adaptive compute routing" --types principle,takeaway_message

# Generate through Principia Calculus
python3.12 principia.py generate "new idea for agent memory" --mode principia-calculus

# Open cloud commands
python3.12 principia.py cloud --help
```

</details>

<details>
<summary>Repository orientation</summary>

```text
principia/        core Python package
static/           local browser UI
cloud/            Cloud Library schemas, manifests, and examples
docs/screenshots/ README screenshots
data/             compact release database and local artifacts
tests/            regression tests
legacy/           archived earlier versions
principia.py      CLI entrypoint
```

</details>

The older V1.0 implementation can be kept under `legacy/` for reference while V1.1 becomes the main product surface.

---

## Roadmap

Principia V1.1 establishes the local-first workbench plus GitHub-native Cloud Library. Next directions include:

- richer public Principle Graph browsing;
- stronger concept deduplication and merge review;
- better cloud search and semantic retrieval;
- Codex prompt-pack export for validation workflows;
- feedback ingestion from experiments and reviews;
- calibration of predicted versus observed idea outcomes;
- shareable Idea Cards and community validation packs.

---

## Star the Project

If Principia resonates with your research workflow, please consider giving the repository a star. It helps us grow the public principle-memory ecosystem and makes the project easier for researchers and builders to discover.

---

## Contact

**Academic collaboration**  
In collaboration with the **[Institute of Computing Technology, Chinese Academy of Sciences](https://english.ict.cas.cn/)**.  
Contact: [peizhengqi22@mails.ucas.ac.cn](mailto:peizhengqi22@mails.ucas.ac.cn)

**Business collaboration**  
In collaboration with **Beijing Chipflow Technology Co., Ltd.**. 
Contact: [peizhengqi@chipflow.net](mailto:peizhengqi@chipflow.net)

---

<p align="center">
  <b>Principia: ideas from principles, validated by evidence.</b>
</p>
