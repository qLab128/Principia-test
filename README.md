<div align="center">

# Principia

### Principle-First Automatic Idea Discovery System

**Ideas from principles. Evidence before hype. Validation before papers.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](#quick-start)
[![Local First](https://img.shields.io/badge/local--first-research_workspace-0ea5e9)](#local-first-by-design)
[![SQLite](https://img.shields.io/badge/storage-SQLite-003B57?logo=sqlite&logoColor=white)](#architecture)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#contributing)

<a href="#why-principia">Why Principia</a> ·
<a href="#quick-start">Quick Start</a> ·
<a href="#what-you-can-do-today">Current Demo</a> ·
<a href="#architecture">Architecture</a> ·
<a href="#roadmap">Roadmap</a>

</div>

---

## Why Principia

Most AI research ideation tools can produce a fluent paragraph. Principia is built around a harder question:

> **Where did this idea come from, what principle makes it plausible, and how can we test it?**

Principia turns a rough research goal or idea draft into a structured local research workspace. It searches public scholarly metadata, extracts reusable field knowledge, organizes that knowledge into a growing principle library, and helps researchers generate new ideas whose evidence, assumptions, baselines, risks, and validation paths are visible.

The name is deliberate. **Principia** is not just an idea generator. It is a principle-oriented research instrument: a place to turn literature into reusable principles, turn principles into traceable ideas, and turn feedback from experiments back into better research memory.

## Core Thesis

```text
Research idea = Goal
              + Evidence
              + Principle lineage
              + Idea operator
              + Novelty contrast
              + Validation plan
              + Feedback loop
```

Principia is designed for researchers who do not merely want *more* ideas. They want ideas with visible origin, explicit assumptions, comparable prior work, and a path toward validation.

## What You Can Do Today

This repository is a local demo of the Principia workflow.

| Capability | What it does |
| --- | --- |
| **Project workspace** | Create project-scoped research spaces instead of losing ideas in chat history. |
| **Hybrid source discovery** | Searches free public metadata sources including arXiv, OpenAlex, and Crossref, then ranks and deduplicates relevant works. |
| **Evidence library** | Structures a project into Existed Ideas, Principles, Takeaway Messages, Benchmarks, Baselines, and My Ideas. |
| **Principle mining** | Extracts reusable mechanisms, assumptions, tradeoffs, failure modes, and transfer hooks from prior work. |
| **Principle-first idea generation** | Generates new ideas from selected existed ideas, principles, takeaway messages, and the user's own hunch. |
| **Idea detail page** | Shows novelty claim, mechanistic design, why it might work, validation protocol, metrics, risks, related existed ideas, principle map, and source evidence. |
| **Research memory** | Uses a local SQLite-backed object store so the product can act as an information-management library for research ideas and reasoning traces. |
| **CLI + local web UI** | Run the web app locally or use CLI commands for ingestion, generation, principle search, graph output, and reset. |

## Not Just an Idea Generator

Principia also acts as a **research idea and thought-management library**.

Instead of treating every session as a disposable LLM conversation, Principia keeps durable objects:

- **Source Works**: papers, reports, and technical sources behind a project.
- **Existed Ideas**: concise records of what prior works actually contributed.
- **Principle Cards**: reusable mechanisms, assumptions, constraints, tradeoffs, invariants, failure modes, evidence spans, and confidence scores.
- **Takeaway Messages**: nontrivial empirical lessons that can guide new work.
- **Benchmarks, Baselines, and Results**: structured experimental context for fair comparison.
- **My Ideas**: generated or user-authored idea records with versions, regeneration, editing, related-work comparison, principle maps, and source evidence.

The long-term goal is a living **Principle Pool**: not a vector database of paper chunks, but a structured knowledge base of reusable research mechanisms.

## The Principle-First Loop

```mermaid
flowchart LR
    A[Research Goal or Idea Draft] --> B[Hybrid Corpus Builder]
    B --> C[Structured Evidence Library]
    C --> D[Principle Pool]
    D --> E[Idea Operators]
    E --> F[Traceable Idea Card]
    F --> G[Validation Plan]
    G --> H[Feedback and Run Notes]
    H -. updates .-> D
```

Principia's idea operators are designed to make ideation inspectable rather than magical:

| Operator | Question it asks |
| --- | --- |
| **Principle transfer** | Can a mechanism from another domain solve the same abstract pressure here? |
| **Assumption inversion** | What happens if we deliberately violate a hidden assumption? |
| **Contradiction resolution** | Can a known principle resolve a tension such as quality vs. cost or novelty vs. feasibility? |
| **Mechanism composition** | Which compatible mechanisms become stronger together? |
| **Failure-mode transplant** | What known failures in one domain should stress-test another? |
| **Evaluator binding** | What is the cheapest falsification path before we over-invest? |

## How Principia Is Different

| Compared with... | Typical focus | Principia's focus |
| --- | --- | --- |
| **Chatbot brainstorming** | Persuasive idea lists. | Structured Idea Cards with evidence, principle lineage, novelty contrast, validation path, and risks. |
| **RAG-only ideation** | Retrieve papers, summarize, then brainstorm. | Convert papers into reusable principles before generating new ideas. |
| **Survey/report tools** such as STORM or AutoSurvey | Knowledge curation and long-form reports. | Use literature synthesis as a launchpad for testable, principle-grounded hypotheses. |
| **Idea-discovery agents** such as ResearchAgent or SciAgents | Agentic literature-based hypothesis generation. | Local editable research memory: principles, existed ideas, baselines, benchmarks, user notes, and generated ideas in one workspace. |
| **AI Scientist-style systems** | End-to-end automation toward experiments and papers. | A human-in-the-loop principle, evidence, and validation layer; the north-star metric is idea survival, not automatic paper production. |
| **Evaluator/code-search agents** such as AlphaEvolve-like systems | Search code or algorithm variants under evaluators. | Search the *idea space* first, then prepare validation artifacts for implementation. |

Principia is best understood as the missing connective layer between literature review, idea generation, experiment planning, and research memory.

## Quick Start

```bash
git clone https://github.com/pzqpzq/Principia.git
cd Principia
python3 principia.py serve
```

Open the local app:

```text
http://127.0.0.1:8790/
```

On first launch, Principia creates a local database:

```text
data/principia.sqlite
```

Then create a project, paste a research goal or idea draft, choose an LLM, set a target work count, and click **Research**.

## API Keys

Principia ships without secrets. Add keys in the app through **API Keys**, or create `.env` manually:

```bash
cp .env.example .env
```

Then edit:

```text
SILICONFLOW_API_KEY=your_siliconflow_key_here
OPENAI_API_KEY=your_openai_key_here
```

At least one callable LLM provider is required for LLM extraction and idea generation.

Useful options:

```text
PRINCIPIA_REQUEST_TIMEOUT=180
PRINCIPIA_COST_LIMIT_CNY=1000
PRINCIPIA_SSL_VERIFY=1
```

Run on another port if needed:

```bash
python3 principia.py serve --host 127.0.0.1 --port 8791
```

## CLI Examples

Mine principles from related works:

```bash
python3 principia.py ingest "long-context reasoning efficiency in LLM agents" --max-works 8
```

Generate traceable idea cards:

```bash
python3 principia.py generate "new idea for reliable and efficient LLM research agents" --ideas 4
```

Search the local principle pool:

```bash
python3 principia.py principles "adaptive compute routing under uncertainty" --top-k 8
```

Print a compact lineage graph:

```bash
python3 principia.py graph --query "agent memory and long-context reasoning"
```

Reset local data:

```bash
python3 principia.py reset --yes
```

## Workflow

1. **Create a project** for a research direction.
2. **Enter a research goal or idea draft.**
3. **Run Research** to collect and structure related field knowledge.
4. **Inspect the evidence library**: Existed Ideas, Benchmarks, Baselines, Principles, and Takeaway Messages.
5. **Generate Idea** from selected evidence and your own note.
6. **Review the Idea Detail page**: novelty, mechanism, risks, validation protocol, related prior ideas, principle map, and source evidence.
7. **Edit, regenerate, or preserve versions** as your research thinking evolves.

## Architecture

```text
Principia
├── principia.py                 # CLI entry point
├── principia_demo/
│   ├── cli.py                   # ingest/generate/principles/graph/state/reset/serve
│   ├── server.py                # local HTTP API and static file server
│   ├── engine.py                # goal formalization, retrieval, curation, principle mining, idea generation
│   ├── research_sources.py      # arXiv + OpenAlex + Crossref hybrid discovery
│   ├── arxiv.py                 # arXiv search and fallback seed works
│   ├── llm_client.py            # SiliconFlow/OpenAI-compatible LLM calls and cost guard
│   ├── storage.py               # SQLite-backed local object store
│   ├── models.py                # typed research objects
│   ├── config.py                # local settings and environment handling
│   └── utils.py                 # scoring, IDs, text utilities
├── static/
│   ├── index.html / app.js      # project workspace UI
│   ├── idea.html / idea.js      # generated idea detail page
│   ├── item.html / item.js      # record detail page
│   └── styles.css               # local UI styling
├── tests/                       # offline regression tests
└── data/                        # local data directory; not for committed user data
```

### Core Objects

```text
ResearchGoal
  -> SourceWork
  -> WorkFact
  -> PrincipleCard
  -> PrincipleRelation
  -> IdeaCard
  -> ResultEstimate
  -> PromptPlan
  -> FeedbackEvent
```

These typed objects are the foundation for making research ideation traceable, editable, and reusable.

## Local-First by Design

Principia is intentionally local-first:

- Project data lives in `data/principia.sqlite`.
- API keys are saved locally in `.env`.
- The frontend is static HTML/CSS/JS served by a lightweight Python backend.
- The demo does not ship with private project data.
- Tests use fake or no-op LLM clients and do not spend API credits.

Do not commit or share:

```text
.env
data/*.sqlite
data/*.sqlite-*
__pycache__/
*.pyc
.DS_Store
```

## Quality and Research Integrity

Principia is designed to avoid misleading demo behavior:

- It should warn when an LLM provider cannot be called instead of silently falling back to fake generated content.
- It keeps baseline and benchmark context visible so generated ideas can be compared fairly.
- It treats generated ideas as hypotheses, not facts.
- It favors provenance, editability, and validation over paper-mill automation.
- It keeps the human in the loop for research judgment, interpretation, and dissemination.

## Roadmap

Current local demo:

- [x] Local project workspace
- [x] SQLite-backed research object store
- [x] Hybrid public metadata retrieval through arXiv, OpenAlex, and Crossref
- [x] Existed Ideas, Principles, Takeaway Messages, Benchmarks, Baselines, and My Ideas tabs
- [x] LLM-assisted extraction and idea generation
- [x] Idea detail pages with versioning, editing, regeneration, related-work comparison, principle map, and source evidence
- [x] CLI for ingestion, generation, principle search, graph output, serving, and reset
- [x] Local API-key management through `.env`

Near-term extensions:

- [ ] Stronger Principle Card verification and evidence-span inspection
- [ ] More explicit Idea Card exports: `IDEA_CARD.md`, `PRINCIPLE_TRACE.json`, and `VALIDATION_PLAN.md`
- [ ] Codex-ready prompt plan export for repo orientation, experiment contract, baseline, candidate method, evaluation, ablations, result analysis, and feedback packaging
- [ ] Calibrated result estimator with predicted vs. actual outcome tracking
- [ ] Feedback ingestion from run logs, reviewer comments, user notes, and experiment metrics
- [ ] MCP or assistant integration so other agents can call Principia as the principle and validation layer
- [ ] Public or team-level Principle Graph with moderation and opt-in sharing

## Why Star This Repo

Star Principia if you care about any of these problems:

- AI-assisted research should be **traceable**, not just fluent.
- Literature review should become reusable **research memory**, not a one-off summary.
- Idea generation should expose **principles, assumptions, baselines, metrics, and failure modes**.
- Research agents should optimize for **ideas that survive implementation**, not just ideas that sound novel.
- Local-first tools should let researchers keep unpublished ideas and private notes under their control.

## Running Tests

Install optional test dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Run:

```bash
python3 -m unittest discover -s tests -p 'test*.py'
```

## Contributing

Useful contribution areas include:

- Better principle extraction and verification prompts.
- Richer evidence-span UI.
- Better graph visualization for principle lineage.
- New source connectors for scholarly metadata.
- Codex prompt-plan exporters.
- Evaluation benchmarks comparing direct LLM ideation, RAG ideation, and principle-first ideation.
- Documentation, screenshots, and example research projects.

## Related Systems and Positioning

Principia is informed by work on literature-grounded ideation, graph-based scientific agents, automated survey generation, AI-scientist systems, and evaluator-guided code search. It is not trying to replace those systems. It is trying to provide the principle, evidence, and validation layer that connects them.

Representative systems worth reading:

- [ResearchAgent](https://arxiv.org/abs/2404.07738): iterative research idea generation over scientific literature.
- [SciAgents](https://arxiv.org/abs/2409.05556): multi-agent graph reasoning for scientific hypothesis generation.
- [STORM](https://github.com/stanford-oval/storm): retrieval and multi-perspective question asking for grounded report generation.
- [The AI Scientist](https://sakana.ai/ai-scientist/): end-to-end automated scientific discovery pipeline.
- [AlphaEvolve](https://deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/): evaluator-guided algorithm discovery through evolutionary code search.

## Status

Principia is an actively evolving research demo for local experimentation, product validation, and high-fidelity research-workflow prototyping. It is not yet a production multi-user deployment.

## License

License is not specified yet. Add a `LICENSE` file before broad external redistribution.
