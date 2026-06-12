# Principia v1.0

Principia is a local-first research ideation system for building high-quality, evidence-grounded ideas from papers, benchmarks, baselines, principles, and generated symbolic derivations.

Version 1.0 upgrades the earlier Principia 0.x demo into a product-oriented codebase with normalized research memory, live research workflows, concept-level retrieval, traceable idea generation, and an MVP of **Principia Calculus**, a symbolic mode for deriving new ideas through verified lineage graphs instead of opaque one-shot text generation.

Business collaboration: [peizhengqi@chipflow.net](mailto:peizhengqi@chipflow.net)  
Academic collaboration: [peizhengqi22@mails.ucas.ac.cn](mailto:peizhengqi22@mails.ucas.ac.cn)

## Screenshots

| Research workspace | Works library |
| --- | --- |
| ![Research goal and project workspace](docs/screenshots/main_goal.png) | ![Works tab with research records](docs/screenshots/main_works.png) |

| Evidence composition | Generated idea |
| --- | --- |
| ![Compose from research evidence](docs/screenshots/add_evidence.png) | ![Generated idea overview](docs/screenshots/new_idea_intro.png) |

| Principia Calculus lineage | Principle map |
| --- | --- |
| ![Symbolic lineage graph](docs/screenshots/calculus_graph.png) | ![Principle map](docs/screenshots/principle_map.png) |

| Principles | Related idea comparison |
| --- | --- |
| ![Principles tab](docs/screenshots/main_principles.png) | ![Related idea comparison](docs/screenshots/compare_ideas.png) |

## What Principia Does

Principia helps a researcher move from a broad goal to a traceable Idea Card:

1. Search and ingest relevant works.
2. Extract high-quality existed ideas, principles, takeaway messages, benchmarks, and baselines from paper evidence.
3. Store records in local SQLite with versioning, source links, evidence links, and full-text search.
4. Select research materials into an evidence composer.
5. Generate new ideas in standard mode or Principia Calculus mode.
6. Inspect symbolic lineage, principle relationships, related idea comparisons, and source evidence.
7. Export generated ideas as Markdown for external agents, experiments, method writing, or follow-up research.

The system is designed around content quality and provenance. Failed online LLM calls are not silently replaced by templated filler.

## Key v1.0 Features

- Local-first SQLite product codebase.
- Project sidebar with independent workspace scrolling.
- Research workflow with cancellable LLM stages and partial persistence.
- Works tab with show-more pagination and per-work extraction.
- Normalized global memory layer:
  `global_work`, `work_version`, `extraction_run`, `concept_card`, `concept_version`, `evidence_link`, `symbol_registry`, `derivation_run`, `derivation_node`, `derivation_edge`, `project_record_membership`, `run_event`, `embedding_index`, and `migration_status`.
- Compatibility adapter for the older record buckets:
  Source Works, Existed Ideas, Principles, Takeaway Messages, Benchmarks, Baselines, Results, and My Ideas.
- Concept-level retrieval instead of retrieving a work and blindly showing all child records.
- SQLite FTS5 search for works and concepts.
- Optional embedding table with no mandatory vector dependency.
- API key modal with masked status.
- Detail pages, item editing, version selectors, refresh with LLM, and exports.
- Standard idea generation and Principia Calculus generation.
- Symbol table, verified derivation patches, speculative L0 nodes, lineage graph, principle map, and related-ideas comparison.
- Markdown export for generated ideas.
- Regression tests for schema, migration, extraction quality gates, cancellation, symbolic verification, no-template fallback, and UI-compatible routes.

## Included Data

This repository includes the current v1.0 local SQLite database at:

```text
data/principia.sqlite
```

It preserves the two current projects from the release workspace:

- `SciDia-MAS`
- `LLM+logics`

The database has been compacted with `VACUUM INTO` and checked with `PRAGMA integrity_check`. Runtime WAL/SHM files, logs, caches, PDFs, API keys, and private `.env` files are excluded.

## Repository Layout

```text
.
├── principia/                  # v1 Python package
├── static/                     # browser UI
├── tests/                      # v1 regression tests
├── data/
│   ├── principia.sqlite        # included v1 demo/release database
│   └── artifacts/              # local artifact folders, gitkept empty
├── docs/screenshots/           # README screenshots
├── legacy/v0-demo-jun8-v2/     # archived 0.x demo source
├── principia.py                # CLI entrypoint
├── requirements.txt
└── principia_v1_design_proposal.md
```

The `legacy/v0-demo-jun8-v2/` folder keeps the old demo source for reference. It intentionally excludes old private databases and `.env` files.

## Quick Start

Principia v1.0 requires Python 3.9 or newer. Python 3.12 is recommended and was used for the release validation.

```bash
git clone https://github.com/pzqpzq/Principia.git
cd Principia
python3.12 -m pip install -r requirements.txt
cp .env.example .env
python3.12 principia.py serve --host 127.0.0.1 --port 8792
```

Open:

```text
http://127.0.0.1:8792/
```

The included database should show the two preserved projects immediately. If you want a clean local workspace instead, run:

```bash
python3.12 principia.py reset --yes
```

## LLM Configuration

Principia works best with SiliconFlow models for day-to-day research and can optionally use OpenAI-compatible models. Put private keys only in `.env`, never in committed files:

```text
SILICONFLOW_API_KEY=your_siliconflow_key_here
OPENAI_API_KEY=your_openai_key_here
PRINCIPIA_LLM_BASE_URL=https://api.siliconflow.cn/v1
PRINCIPIA_OPENAI_BASE_URL=https://api.openai.com/v1
PRINCIPIA_REQUEST_TIMEOUT=180
PRINCIPIA_SLOW_REQUEST_TIMEOUT=420
```

Large models can require long timeouts. If an online LLM call fails, Principia surfaces the failure and preserves completed batches instead of inventing replacement content.

## Workflow

### 1. Create or open a project

Each project stores its own goal, selected works, memberships, generated ideas, and run status. Multiple projects can be managed independently.

### 2. Run Research

Research retrieves relevant works, stores paper metadata, then extracts structured information from selected works:

- Existed Ideas
- Principles
- Takeaway Messages
- Benchmarks
- Baselines
- Result facts and evidence links

Extraction is designed to prefer objective, complete, source-grounded arguments over author-voice quotes or loose summaries.

### 3. Compose From Research Evidence

Use the evidence composer to select works, ideas, principles, benchmarks, baselines, or takeaways. The selected evidence is project-scoped and can be inspected before generation.

### 4. Generate Ideas

Two generation modes are available:

- **Standard mode**: synthesizes a full Idea Card directly from selected evidence and the project goal.
- **Principia Calculus mode**: builds symbols, derives compact structured patches, verifies references/support, stores lineage nodes and edges, then synthesizes a final Idea Card.

### 5. Inspect and Export

Generated idea pages include:

- Novelty claim
- Mechanistic design
- Method variants
- Derived principles
- Validation protocol
- Relevant baselines and metrics
- Source evidence
- Related idea comparison
- Principle map
- Symbolic lineage graph
- Markdown export

## CLI

```bash
python3.12 principia.py serve --host 127.0.0.1 --port 8792
python3.12 principia.py state --v1
python3.12 principia.py research "efficient LLM research agents" --target-works 100
python3.12 principia.py retrieve "adaptive compute routing" --types principle,takeaway_message
python3.12 principia.py generate "new idea for agent memory" --mode principia-calculus
python3.12 principia.py symbols --namespace default
python3.12 principia.py lineage MI-...
python3.12 principia.py export MI-...
python3.12 principia.py migrate
python3.12 principia.py reset --yes
```

Legacy-compatible commands remain available for old workflows:

```bash
python3.12 principia.py ingest "long-context reasoning efficiency"
python3.12 principia.py principles "adaptive budget allocation"
python3.12 principia.py graph --query "agent memory"
```

## API Surface

Stable v1 endpoints include:

```text
POST /api/v1/research/start
GET  /api/v1/research/status
POST /api/v1/research/cancel
GET  /api/v1/projects
GET  /api/v1/project/tab
GET  /api/v1/item/detail
POST /api/v1/item/update
POST /api/v1/item/refresh/start
POST /api/v1/retrieve-concepts
POST /api/v1/ideas/standard-generate
POST /api/v1/ideas/symbolic-generate
GET  /api/v1/ideas/{idea_id}/lineage
GET  /api/v1/symbols/table
GET  /api/v1/symbols/expand
POST /api/v1/feedback/ingest
```

Temporary `/api/v2/*` aliases remain for compatibility while older detail and assembler flows are fully migrated.

## Quality and Safety Rules

Principia v1.0 is strict about generated content:

- No silent template fallback for failed online LLM calls.
- Offline/demo fallback content must be explicit and labeled.
- Completed extraction batches are persisted before later-stage failures.
- Cancellation is run-level: late responses are not saved after cancellation.
- Benchmarks and baselines should be official and source-grounded, not invented.
- Ideas, principles, and takeaways should be objective, complete, independent arguments rather than paper quotes or author-voice claims.
- Full paper text can be used transiently for extraction, but full text is not retained in local storage.

## Tests

```bash
python3.12 -m unittest discover -s tests -v
```

Current local validation for this release:

```text
106 tests OK
```

The tests cover schema creation, migration, work identity and versioning, extraction cache behavior, quality gates, FTS search, symbol collision handling, derivation verification, symbolic generation, cancellation, related comparisons, markdown export, and no-template-fallback regressions.

## Notes for Developers

- Keep private data in `.env` and local-only artifact folders.
- Do not commit WAL/SHM files, logs, cached PDFs, or API keys.
- `data/principia.sqlite` is intentionally included for the v1.0 release snapshot.
- Run tests before publishing changes.
- Use the v1 API paths for new frontend work; keep `/api/v2/*` only for temporary compatibility.
