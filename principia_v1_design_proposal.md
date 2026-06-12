# Principia Next-Generation Design Proposal

**Working title:** Principia Global Principle Memory + Symbolic Lineage Generation  
**Target version:** Principia v3 / Next Generation  
**Date:** June 2026  
**Prepared for:** Principia demo evolution planning  
**Core definition:** A principle-first automatic idea discovery system that turns research works into a shared, versioned, symbolically addressable research memory, then uses that memory to generate traceable, validation-aware ideas.

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Design Thesis](#2-design-thesis)
3. [Current Version Baseline](#3-current-version-baseline)
4. [Requirement-to-Architecture Mapping](#4-requirement-to-architecture-mapping)
5. [Target Architecture](#5-target-architecture)
6. [Global Information Library](#6-global-information-library)
7. [Storage and Indexing Strategy](#7-storage-and-indexing-strategy)
8. [Work Ingestion, Update, and Versioning Logic](#8-work-ingestion-update-and-versioning-logic)
9. [Concept Extraction and Upsert Logic](#9-concept-extraction-and-upsert-logic)
10. [Independent Retrieval of Ideas, Principles, and Takeaway Messages](#10-independent-retrieval-of-ideas-principles-and-takeaway-messages)
11. [New Generation Mode: Principia Calculus](#11-new-generation-mode-principia-calculus)
12. [Symbol Registry and Token-Efficient Reasoning](#12-symbol-registry-and-token-efficient-reasoning)
13. [Derivation Graph, Verification, and Promotion Rules](#13-derivation-graph-verification-and-promotion-rules)
14. [Idea Detail Page and Lineage Visualization](#14-idea-detail-page-and-lineage-visualization)
15. [API and Module Refactor](#15-api-and-module-refactor)
16. [Migration Plan from Current Demo](#16-migration-plan-from-current-demo)
17. [Quality Metrics and Diagnostics](#17-quality-metrics-and-diagnostics)
18. [Security, Privacy, and Research Integrity](#18-security-privacy-and-research-integrity)
19. [Implementation Roadmap](#19-implementation-roadmap)
20. [Example End-to-End Run](#20-example-end-to-end-run)
21. [Key Design Decisions for Review](#21-key-design-decisions-for-review)
22. [Appendix A: Proposed SQL-Like Schema](#22-appendix-a-proposed-sql-like-schema)
23. [Appendix B: Symbolic Patch Schema](#23-appendix-b-symbolic-patch-schema)
24. [Appendix C: Source-Backed Technical References](#24-appendix-c-source-backed-technical-references)

---

## 1. Executive Summary

The next generation of Principia should evolve from a local demo research workspace into a **shared, versioned, principle-first research memory system**.

The current version already has the right foundation:

- project workspaces;
- source work discovery;
- extraction of existed ideas, principles, takeaway messages, benchmarks, and baselines;
- a local SQLite-backed store;
- project membership records;
- LLM-based extraction and item refresh;
- generated idea pages with related existed ideas, principle maps, and source evidence.

The next version should formalize those capabilities into a robust architecture:

```text
Every research run contributes reusable global knowledge.
Every work is canonicalized and versioned.
Every LLM extraction is cached by work version, model, prompt, and schema.
Every idea, principle, and takeaway is independently retrievable at card level.
Every generated idea is traceable through a derivation graph.
Every speculative intermediate concept is saved but clearly marked as unverified.
```

The most important upgrade is to make the **global information library** the system's core asset. This library should not be a loose vector database of chunks. It should be a typed, versioned, evidence-linked memory of works, extracted concepts, symbolic names, derivation graphs, validation feedback, and project-level views.

The second major upgrade is a new generation mode, recommended name: **Principia Calculus**. In this mode, Principia assigns compact symbolic handles to existing ideas, principles, and takeaway messages, then lets an LLM construct new concepts, arguments, hypotheses, deductions, and final ideas through structured symbolic derivation patches. These intermediate objects can be recursively reused, but they are stored as **speculative L0 derivations**, not as evidence-backed literature facts.

The expected result is a system that:

- avoids duplicate search and duplicate LLM extraction;
- improves global memory over time;
- reduces output-token cost during deep idea generation;
- produces more explainable and more structured research ideas;
- shows users how a new idea was derived layer by layer;
- distinguishes evidence-backed concepts from speculative reasoning artifacts.

---

## 2. Design Thesis

Principia should be designed around this principle:

> **Research ideation should be a traceable operation over reusable principles, not a black-box chat response.**

The core product object is not a paragraph. It is a **lineage-backed Idea Card**:

```text
Idea = Goal
     + Retrieved evidence
     + Existed ideas
     + Principles
     + Takeaway messages
     + Symbolic derivation graph
     + Novelty contrast
     + Feasibility/risk analysis
     + Validation plan
     + Feedback loop
```

This creates a clear distinction from ordinary idea-generation products and AI-scientist-style pipelines:

| Product category | Typical behavior | Principia next-gen behavior |
|---|---|---|
| Chatbot brainstorming | Generates plausible ideas in prose | Generates structured idea objects with source lineage |
| RAG idea tools | Retrieves papers and asks LLM to brainstorm | Extracts independent reusable concepts, then reasons over them |
| AI Scientist systems | Often target end-to-end paper or experiment automation | Focuses on principle-grounded ideation, validation planning, and research memory |
| Paper survey tools | Summarize literature | Converts literature into reusable principles, takeaways, baselines, and idea seeds |
| Knowledge bases | Store notes/chunks | Store canonical works, concept versions, evidence links, symbols, and derivation graphs |

The next-generation product identity should be:

> **Principia is the principle, evidence, and validation layer for AI research ideation.**

---

## 3. Current Version Baseline

The uploaded codebase already contains several assets that should be preserved and refactored rather than discarded.

### 3.1 Existing strengths

Current capabilities visible in the codebase include:

```text
Project workspace
  - active project sidebar
  - project creation/edit/delete/reorder
  - project-level tab views

Research pipeline
  - research goal / idea draft input
  - target LLM selector
  - target works selector
  - research run status and cancellation

Global-ish record buckets
  - source_works
  - existed_ideas
  - principles
  - takeaway_messages
  - benchmark_records
  - baseline_records
  - result_records
  - my_ideas
  - evidence_links
  - research_runs
  - project_memberships

Storage
  - SQLite-backed generic object store
  - JSON payloads
  - bucket counts
  - item search
  - usage tracking

Source discovery
  - arXiv
  - OpenAlex
  - Crossref
  - deduplication by title
  - ranking by lexical relevance, year, and URL availability

LLM support
  - SiliconFlow-compatible chat completions
  - OpenAI-compatible responses/chat endpoint handling
  - model aliases
  - request timeout and cost guard

Idea detail page
  - related existed ideas
  - principle map
  - source evidence
  - edit/regenerate/delete idea
  - version selector
```

### 3.2 Current limitations

The current version uses a flexible but demo-oriented storage model. It is good for rapid iteration, but not enough for a long-lived multi-user or multi-project global library.

Main limitations:

```text
1. Work identity is not strong enough.
   Works should be canonicalized through DOI/arXiv/OpenAlex/Crossref IDs, title hashes, abstract hashes, and fuzzy resolution.

2. Work metadata and extraction outputs are not separated enough.
   A source work should have multiple source metadata versions and multiple extraction runs.

3. Concept-level versioning needs to become first-class.
   Same work + same concept + different LLM should become a concept version, not a duplicate concept.

4. Retrieval should be card-level rather than work-level.
   A work's principle may be relevant while its existed idea is not.

5. Symbolic reasoning is not yet represented as a persistent graph.
   Current principle maps should evolve into derivation DAGs with typed nodes and edges.

6. Speculative derived concepts need a separate lifecycle.
   LLM-derived intermediate objects must be reusable but not confused with extracted literature facts.
```

---

## 4. Requirement-to-Architecture Mapping

### Requirement 1: Share all research-run work information globally

Design response:

```text
Introduce a Global Research Memory layer with canonical works, work versions, extraction runs, concept cards, concept versions, evidence links, and project memberships.
```

Each project should point to global records rather than duplicating them.

### Requirement 2: Efficient storage, retrieval efficiency, and retrieval precision

Design response:

```text
Use normalized relational tables for identity and metadata.
Use JSON payloads for flexible LLM outputs.
Use FTS for exact lexical retrieval.
Use embeddings for semantic retrieval.
Use graph relations for lineage and expansion.
Use structured filters for validation level, model, scope, concept type, and project.
```

### Requirement 3: Efficient information insertion and update logic

Design response:

```text
Use deterministic-first work identity resolution.
Use source-modified timestamps and content hashes to detect updates.
Use extraction cache keys: work_version × model × prompt_version × schema_version.
Use concept-level deduplication and versioning.
Use LLM only for ambiguous identity or semantic merge cases.
```

### Requirement 4: Retrieve related ideas, principles, and takeaways independently

Design response:

```text
Use independent retrieval pipelines per concept type.
Do not retrieve whole works and blindly show all child concepts.
Run separate hybrid retrieval jobs for existed ideas, principles, takeaway messages, benchmarks, baselines, and feedback lessons.
```

### Requirement 5: Add symbolic recursive reasoning mode for idea generation

Design response:

```text
Create Principia Calculus:
- persistent symbol registry;
- compact symbolic prompts;
- iterative derivation patches;
- speculative intermediate concept storage;
- derivation verifier;
- lineage graph visualization;
- promotion/rejection workflow.
```

---

## 5. Target Architecture

Recommended architecture:

```text
┌─────────────────────────────────────────────────────────┐
│                    Product Surface                       │
│  Project Workspace | Research Atlas | Idea Workbench     │
│  Symbolic Lineage Viewer | Feedback Inbox | API Keys      │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                  Reasoning Services                      │
│  Goal Formalizer                                         │
│  Global Work Resolver                                    │
│  Work Version Comparator                                 │
│  Concept Extractor                                       │
│  Concept Canonicalizer                                   │
│  Independent Concept Retriever                           │
│  Symbol Registry                                         │
│  Principia Calculus Ideator                              │
│  Derivation Verifier                                     │
│  Novelty / Feasibility / Risk Critic                     │
│  Feedback Assimilator                                    │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                 Global Knowledge Store                   │
│  Works | Work Versions | Extraction Runs                 │
│  Concept Cards | Concept Versions | Evidence Links       │
│  Symbols | Derivation Nodes | Derivation Edges           │
│  Embeddings | FTS Indexes | Project Memberships          │
└─────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────┐
│                   External Sources                       │
│  arXiv | OpenAlex | Crossref | Semantic Scholar          │
│  PDFs | GitHub | Local Notes | Experiment Feedback       │
└─────────────────────────────────────────────────────────┘
```

### 5.1 Core architectural rule

Every record should answer four questions:

```text
What is this object?
Where did it come from?
Which version/model produced it?
How confident or validated is it?
```

### 5.2 Project views vs global records

Projects should not own duplicated copies of works and concepts. Instead:

```text
Global library:
  canonical work/concept records

Project membership:
  which global records are visible/relevant to this project

Project-private annotations:
  user's comments, selections, manual edits, and speculative notes
```

This creates the desired sharing behavior while preserving privacy boundaries.

---

## 6. Global Information Library

The global library should be built from seven object families.

### 6.1 Work identity layer

Purpose: one canonical row per real-world work.

Examples:

```text
paper
arXiv preprint
conference paper
GitHub repository
benchmark suite
technical report
documentation page
deployment note
```

Key design:

```text
global_work = stable identity
work_version = metadata/content snapshot
```

### 6.2 Extraction layer

Purpose: track every LLM extraction run.

Key design:

```text
extraction_run = work_version + LLM + prompt_version + schema_version
```

This prevents repeated LLM calls for unchanged works.

### 6.3 Concept layer

Purpose: store independently retrievable research objects.

Concept types:

```text
existed_idea
principle
takeaway_message
benchmark
baseline
result_fact
gap
failure_mode
assumption
user_note
derived_concept
argument
hypothesis
deduction
idea_seed
generated_idea
```

The important design move is that **existed ideas, principles, and takeaway messages all become concept cards**, but their `concept_type` differs.

### 6.4 Concept version layer

Purpose: store multiple LLM/human versions of the same concept.

A concept can have versions from:

```text
same work, different LLM
same work, different prompt version
same work, updated schema
manual user edit
post-feedback revision
```

### 6.5 Evidence layer

Purpose: connect concepts to source evidence.

Examples:

```text
work title
abstract span
paper section
table result
benchmark result
repo README
user feedback
experiment log
reviewer comment
```

No extracted concept should be treated as evidence-backed unless it has evidence links.

### 6.6 Symbol layer

Purpose: give each reusable concept a compact symbolic handle.

Examples:

```text
P.ATCU   = Adaptive Token/Compute Routing under Uncertainty
P.EFB    = Evaluator-First Binding
TM.ROH   = Routing Overhead Harm
XI.RAGD  = RAG-only Ideation Drift
H.EVR    = Evidence-Value Routing Hypothesis
D.COST   = Cost-Gated Derivation
```

### 6.7 Derivation layer

Purpose: store generated intermediate concepts and final ideas as graph nodes and edges.

Examples:

```text
P.ATCU + P.EFB -> D.EVR
D.EVR + TM.ROH -> D.COST
D.COST + XI.RAGD -> I.EVRA
```

---

## 7. Storage and Indexing Strategy

The storage strategy should support two deployment modes.

### 7.1 Local mode

Recommended stack:

```text
SQLite
+ normalized tables
+ JSON payload columns
+ FTS5 lexical index
+ sqlite-vec or embedding table for local vector search
+ local artifact directory for raw source JSON, logs, PDFs, and prompt packs
```

Local directory layout:

```text
data/
  principia.sqlite
  artifacts/
    sources/
    pdfs/
    prompt_packs/
    run_logs/
  cache/
    embeddings/
    source_json/
```

Use local mode for:

```text
private project data
private ideas
private PDFs
private user notes
offline or low-friction demos
single-user research workbench
```

### 7.2 Hosted / multi-user mode

Recommended stack:

```text
Postgres
+ pgvector
+ Postgres full-text search
+ object storage
+ optional graph sidecar later
+ queue/orchestrator for extraction jobs
```

Use hosted mode for:

```text
multi-user global library
team workspaces
public Principle Pool
large-scale retrieval
collaboration
analytics and calibration
```

### 7.3 Index types

Use multiple index families because no single retrieval method is enough.

| Index | Purpose | Example query |
|---|---|---|
| B-tree / unique indexes | identity, IDs, timestamps | find work by DOI or arXiv ID |
| FTS | exact terms, benchmark names, method names | `routing overhead`, `MMLU`, `few-view` |
| Vector | semantic similarity | similar principle mechanisms |
| Graph | lineage and relational search | principles that resolve a tradeoff |
| Structured filters | precision and permissions | validation >= L2, concept_type = principle |

### 7.4 Recommended retrieval fields

Do not embed entire JSON payloads only. Store multiple embedding views:

```text
work_title_abstract_embedding
concept_summary_embedding
concept_mechanism_embedding
concept_failure_modes_embedding
concept_assumptions_embedding
idea_thesis_embedding
derived_node_expression_embedding
```

This allows retrieval to match the user's query at the right semantic level.

### 7.5 Space-efficiency rules

```text
1. Store one canonical work per identity cluster.
2. Store new work_version only when meaningful content changes.
3. Store extraction output once per work_version × model × prompt_version × schema_version.
4. Store concept versions instead of duplicating concept cards.
5. Store compact active payloads, but archive raw extraction logs separately.
6. Store embeddings per useful retrieval field, not every text field.
7. Use half-precision vectors where supported.
8. Keep symbolic derivation patches compact: symbols + short summaries + edges.
9. Compress raw source JSON, logs, and PDFs outside hot relational tables.
```

### 7.6 Retrieval quality principle

The global library should use **hybrid retrieval**:

```text
Hybrid score = vector relevance
             + lexical relevance
             + graph proximity
             + validation prior
             + project/user context boost
             - duplicate/near-duplicate penalty
```

Reason: scientific retrieval often depends on exact names, acronyms, benchmark names, and subtle semantic similarity at the same time.

---

## 8. Work Ingestion, Update, and Versioning Logic

The user's proposed update logic is strong. I recommend refining it into a deterministic-first pipeline with LLM fallback only for ambiguous cases.

### 8.1 Ingestion pipeline

```text
1. Formalize query.
2. Search global library first.
3. Estimate coverage gaps.
4. Search external sources only for missing coverage.
5. Normalize each retrieved work.
6. Resolve identity against global_work.
7. Compare content hashes and source modified timestamps.
8. Decide skip / metadata update / new work_version / new extraction_run.
9. Extract missing concept versions.
10. Re-index concepts and embeddings.
11. Attach relevant objects to the current project.
```

### 8.2 Work identity resolution

For each retrieved work, compute identity signals:

```text
external_id_score:
  DOI exact match
  arXiv ID exact match
  OpenAlex ID exact match
  Crossref ID exact match
  Semantic Scholar ID exact match

title_score:
  normalized title hash
  fuzzy title similarity
  title embedding similarity

metadata_score:
  author overlap
  year match
  venue/source match
  URL/domain match

abstract_score:
  abstract hash
  abstract similarity
```

Decision rule:

```text
identity_confidence >= 0.95:
  same work

0.80 <= identity_confidence < 0.95:
  ambiguous; use LLM resolver or queue manual review

identity_confidence < 0.80:
  new work
```

### 8.3 Work update decision matrix

| Case | Condition | Action |
|---|---|---|
| Existing unchanged work | same identity, same title hash, same abstract hash, same source modified time | do not update, do not call LLM |
| Existing work with metadata-only change | citation count, source URL, venue, community signals changed; abstract unchanged | update global_work metadata, skip extraction |
| Existing work with content update | title or abstract hash changed, or source modified time newer | create new work_version; enqueue extraction |
| Existing work with same content and same target extraction | work_version × model × prompt × schema exists | reuse extraction |
| Existing work with same content but different LLM | target model extraction missing | create new extraction_run and concept versions |
| Existing work with same content but new prompt/schema | prompt_version or schema_version changed | create new extraction_run |
| New work | no strong identity match | create global_work, work_version, extraction_run |
| Ambiguous identity | medium confidence | create review task; do not merge automatically |

### 8.4 Extraction cache key

```text
extraction_cache_key = hash(
  work_version_id,
  llm_provider,
  llm_model,
  prompt_version,
  schema_version,
  extraction_task_type
)
```

If this key already exists with `status = complete`, skip LLM extraction.

### 8.5 Why this matters

This prevents:

```text
same paper being extracted repeatedly across projects;
same paper being extracted repeatedly for the same model;
new LLM outputs overwriting old outputs;
source metadata updates triggering unnecessary extraction;
ambiguous duplicate papers polluting the library;
private project copies diverging from global canonical records.
```

---

## 9. Concept Extraction and Upsert Logic

After work-level ingestion, the system needs concept-level canonicalization.

### 9.1 Extracted objects

For each work version, extraction should produce independent lists:

```text
existed_ideas[]
principles[]
takeaway_messages[]
benchmarks[]
baselines[]
result_facts[]
assumptions[]
failure_modes[]
```

Do not require a one-to-one mapping between these lists.

### 9.2 Concept canonicalization

For each extracted object:

```text
1. Normalize text.
2. Compute canonical key.
3. Retrieve similar concepts of the same type.
4. Compare source evidence.
5. Decide create new concept, add new version, or link to related concept.
```

### 9.3 Upsert decision matrix

| Case | Condition | Action |
|---|---|---|
| Same work, same evidence, same semantic claim | existing concept found | add concept_version |
| Same work, same evidence, different extraction wording | existing concept found | add concept_version; keep active highest quality |
| Different work, same general principle | semantically equivalent but different evidence | add support edge or candidate merge |
| Different work, similar but not identical mechanism | close semantic neighbor | create new concept; add relation edge |
| LLM-derived speculative concept | no source evidence | create concept with `source_origin = llm_derived`, `validation_level = L0` |
| User manual edit | user edits active payload | create manual concept_version |

### 9.4 Concept version scoring

Each version can receive a quality score:

```text
quality_score =
  0.30 * evidence_support
+ 0.20 * specificity
+ 0.15 * faithfulness
+ 0.15 * non-genericness
+ 0.10 * retrieval_usefulness
+ 0.10 * schema_completeness
```

The active version should normally be:

```text
highest quality version
unless user manually pins a version
or organization policy prefers a specific model
```

### 9.5 Evidence requirements by concept type

| Concept type | Minimum evidence |
|---|---|
| existed_idea | title/abstract or method/contribution span |
| principle | mechanism span + problem pressure or assumption span |
| takeaway_message | empirical result, observation, limitation, or comparison span |
| benchmark | dataset/task/metric source |
| baseline | baseline name + evidence of comparison or standard usage |
| derived_concept | support symbols, not necessarily literature evidence |
| final_idea | derivation graph + selected source evidence |

---

## 10. Independent Retrieval of Ideas, Principles, and Takeaway Messages

The retrieval system must operate at concept-card level.

A work may contain:

```text
Relevant principle: yes
Relevant takeaway: yes
Relevant existed idea: no
Relevant benchmark: maybe
Relevant baseline: no
```

Therefore, Principia should not retrieve a work and blindly display all extracted child objects.

### 10.1 Query profile

Before retrieval, create a structured query profile:

```json
{
  "target_domain": "LLM research agents",
  "target_problem": "API-cost-efficient idea discovery",
  "desired_contribution": ["method", "system", "evaluation"],
  "mechanism_interests": [
    "principle-grounded ideation",
    "evidence retrieval",
    "symbolic reasoning",
    "feedback loops",
    "output-token reduction"
  ],
  "constraints": {
    "compute": "API-cost sensitive",
    "output_token_budget": "low",
    "input_token_budget": "moderate"
  },
  "risk_preference": "balanced"
}
```

### 10.2 Retrieval jobs

Run separate retrieval jobs:

```text
retrieve_existed_ideas(query_profile)
retrieve_principles(query_profile)
retrieve_takeaway_messages(query_profile)
retrieve_benchmarks(query_profile)
retrieve_baselines(query_profile)
retrieve_feedback_lessons(query_profile)
retrieve_speculative_candidates(query_profile)
```

### 10.3 Candidate generation

Each retrieval job should combine:

```text
1. FTS candidates
   exact acronyms, benchmark names, method names, failure phrases

2. Vector candidates
   semantic similarity over concept summaries and mechanisms

3. Graph candidates
   neighbors of highly relevant works/concepts

4. Project-local candidates
   items already selected, highlighted, validated, or edited by the user

5. High-validation global candidates
   high-confidence cards from peer-reviewed or widely adopted works
```

### 10.4 Fusion and reranking

Recommended retrieval stack:

```text
candidate_generation:
  top_k_fts = 80
  top_k_vector = 80
  top_k_graph = 40
  top_k_project = 40

fusion:
  reciprocal_rank_fusion or weighted rank fusion

reranking:
  cheap LLM / cross-encoder rerank top 30 only

diversification:
  cap by work cluster, method family, and repeated mechanism

final:
  return top 8-20 per concept type
```

### 10.5 Retrieval explanation

Each retrieved card should include a compact reason:

```json
{
  "concept_id": "P-ATCU",
  "why_retrieved": [
    "matched mechanism: adaptive resource allocation",
    "matched constraint: output-token cost",
    "linked failure mode: routing overhead",
    "validation_level: L3"
  ]
}
```

This helps users trust why an item was included.

---

## 11. New Generation Mode: Principia Calculus

I recommend naming the new mode:

> **Principia Calculus**

Internal name:

```text
symbolic_lineage_mode
```

Alternative names:

```text
Symbolic Lineage Mode
Idea Algebra Mode
Principle Calculus
Deep Lineage Mode
Recursive Principle Mode
```

I prefer **Principia Calculus** because it fits the product's identity and communicates structured operations over principle objects rather than free-form brainstorming.

### 11.1 Core idea

Principia first converts retrieved objects into a compact symbol table:

```text
P.ATCU  = Adaptive Token/Compute Routing under Uncertainty
P.EFB   = Evaluator-First Binding
P.CSR   = Compression as Sufficient Representation
TM.ROH  = Routing Overhead Harm
XI.RAGD = RAG-only Ideation Drift
```

Then the LLM reasons over symbols and emits compact derivation patches:

```text
D.EVR  = compose(P.ATCU, P.EFB)
D.COST = stress_test(D.EVR, TM.ROH)
D.NOV  = contrast(D.COST, XI.RAGD)
I.EVRA = specialize(D.NOV, "research agents")
```

### 11.2 Allowed generated object types

During symbolic generation, the LLM may create:

```text
derived_concept
argument
hypothesis
deduction
constraint
failure_mode
idea_seed
final_idea
```

But newly derived objects must initially be labeled:

```text
source_origin = llm_derived
validation_level = L0
verification_status = speculative_unverified
```

They must not be mixed with evidence-backed extracted concepts.

### 11.3 Generation loop

```text
Round 0. Build query profile and symbol table.
Round 1. Generate first-layer derived concepts from retrieved evidence.
Round 2. Apply idea operators: transfer, inversion, composition, contradiction resolution.
Round 3. Stress-test with failure modes and takeaway messages.
Round 4. Create candidate idea seeds.
Round 5. Rank by novelty, feasibility, validation path, and lineage quality.
Round 6. Generate final Idea Card from the verified derivation graph.
```

### 11.4 Pseudo-code

```python
def principia_calculus_generate(query, project_id, budget):
    profile = formalize_query(query)

    evidence = retrieve_independent_concepts(
        profile,
        types=[
            "existed_idea",
            "principle",
            "takeaway_message",
            "benchmark",
            "baseline",
            "feedback_lesson",
        ],
    )

    symbol_table = ensure_symbols(evidence)
    derivation = DerivationGraph()
    frontier = seed_frontier(symbol_table)

    for depth in range(budget.max_depth):
        prompt_pack = compress_frontier(
            symbol_table=symbol_table,
            frontier=frontier,
            derivation=derivation,
        )

        patch = llm_generate_derivation_patch(
            query_profile=profile,
            symbols=symbol_table,
            frontier=frontier,
            allowed_ops=[
                "principle_transfer",
                "assumption_inversion",
                "contradiction_resolution",
                "mechanism_composition",
                "failure_mode_transplant",
                "evaluator_binding",
            ],
            output_schema="DerivationPatch",
        )

        verified_patch = verify_derivation_patch(patch, symbol_table)
        derivation.apply(verified_patch)

        new_nodes = store_speculative_nodes(verified_patch)
        symbol_table.extend(assign_symbols(new_nodes))

        frontier = select_next_frontier(
            derivation,
            criteria=[
                "novelty",
                "support",
                "testability",
                "uncertainty_reduction",
            ],
        )

        if stop_condition_met(derivation, budget):
            break

    idea = synthesize_final_idea(derivation, profile)
    idea = novelty_and_feasibility_check(idea)
    return idea, derivation
```

### 11.5 Cost strategy

The key cost principle:

```text
Allow moderate input tokens.
Minimize intermediate output tokens.
Generate full natural-language expansion only once at the end.
```

Practical controls:

```text
1. Use compact symbols in intermediate rounds.
2. Require JSON derivation patches, not long prose.
3. Use an efficient model for symbol naming and retrieval labels.
4. Use a stronger model only for selected synthesis rounds.
5. Reuse symbol tables across projects.
6. Cache derivation patches by evidence symbol set and query profile.
7. Expand full explanation lazily in UI when a user clicks a node.
```

---

## 12. Symbol Registry and Token-Efficient Reasoning

### 12.1 Symbol design

Symbols should be short, stable, and human-readable.

Recommended prefix system:

| Prefix | Meaning |
|---|---|
| `W.` | Work |
| `XI.` | Existed idea |
| `P.` | Principle |
| `TM.` | Takeaway message |
| `B.` | Benchmark |
| `BL.` | Baseline |
| `A.` | Assumption |
| `F.` | Failure mode |
| `D.` | Derived concept / deduction |
| `H.` | Hypothesis |
| `ARG.` | Argument |
| `I.` | Final/generated idea |

Examples:

```text
P.ATCU   Adaptive Token/Compute Routing under Uncertainty
P.EFB    Evaluator-First Binding
TM.ROH   Routing Overhead Harm
XI.LGID  Literature-Grounded Ideation Drift
D.EVR    Evidence-Value Routing
H.CGR    Cost-Gated Retrieval Hypothesis
I.EVRA   Evidence-Value Routed Research Agents
```

### 12.2 Symbol naming policy

Symbols can be created by:

```text
deterministic abbreviation
LLM suggested name
human edit
organization policy
```

Recommended default:

```text
1. Generate deterministic candidate from title/key phrase.
2. Ask LLM to propose short memorable alternatives.
3. Check namespace collision.
4. Store active symbol.
5. Allow user rename with redirect/deprecation history.
```

### 12.3 Symbol lifecycle

```text
active:
  usable in prompts and UI

deprecated:
  old symbol redirects to new symbol

collision_review:
  ambiguous or duplicated symbol

private:
  project/user/org scoped symbol

scratch:
  temporary symbol from a derivation run
```

### 12.4 Symbol expansion contract

Every symbol must expand to:

```json
{
  "symbol": "P.ATCU",
  "concept_id": "P-...",
  "concept_type": "principle",
  "short_label": "Adaptive Token/Compute Routing",
  "gloss": "Allocate scarce inference budget according to uncertainty and expected marginal value.",
  "validation_level": "L2",
  "source_origin": "literature_extracted",
  "evidence_links": ["E-..."]
}
```

This ensures symbols are compression devices, not hidden or unverifiable claims.

---

## 13. Derivation Graph, Verification, and Promotion Rules

### 13.1 Derivation graph model

A derivation graph is a DAG:

```text
Evidence-backed concepts -> speculative derived nodes -> candidate idea seeds -> final idea
```

Node types:

```text
evidence_card
existed_idea
principle
takeaway_message
benchmark
baseline
derived_concept
argument
hypothesis
deduction
idea_seed
final_idea
```

Edge types:

```text
supports
composes
transfers_to
abstracts
specializes
contradicts
warns_against
resolves_tradeoff
assumes
falsifies
validates
leads_to
```

### 13.2 Verification checks

Every symbolic patch should pass a verifier before being stored.

Verifier checks:

```text
Reference check:
  every cited symbol exists in the current symbol table

Type check:
  a derived node cannot claim to be literature_extracted

Support check:
  evidence_backed status requires evidence-backed source nodes

Speculation check:
  combinations without direct source evidence are marked speculative_unverified

Contradiction check:
  search for opposing concepts and attach risk edges

Novelty check:
  retrieve closest prior existed ideas and mark overlap risk

Falsifiability check:
  every final idea must have a cheapest falsification path

Token economy check:
  reject verbose intermediate patches that do not use symbols
```

### 13.3 Validation statuses

Use a clear status system:

```text
extracted_unverified:
  extracted from source but not human/validator reviewed

evidence_supported:
  has source evidence and passes verifier

speculative_unverified:
  derived by LLM reasoning, no direct literature evidence

user_validated:
  user approved or edited

experiment_supported:
  validated by run feedback

contradicted:
  evidence or feedback contradicts it

deprecated:
  superseded by better version
```

### 13.4 Promotion rules

LLM-derived concepts should enter a staging namespace first.

```text
symbolic_scratch:
  created during a derivation run
  project-visible
  L0
  not globally trusted

global_candidate:
  useful speculative concept
  shareable but clearly marked as speculative

global_verified:
  promoted after evidence, experiment feedback, or expert review
```

Promotion path:

```text
scratch -> project_saved -> global_candidate -> global_verified
```

Demotion path:

```text
active -> contradicted -> deprecated
```

### 13.5 Why this matters

This preserves creativity without contaminating the global evidence pool. A speculative insight can be reused, but it cannot be mistaken for a principle extracted from a validated paper.

---

## 14. Idea Detail Page and Lineage Visualization

The current idea detail page should evolve into a full **Symbolic Lineage Viewer**.

### 14.1 Recommended page layout

```text
Idea Detail Page
├── Idea Summary
│   ├── title
│   ├── one-sentence thesis
│   ├── novelty claim
│   └── validation status
│
├── Generation Metadata
│   ├── model
│   ├── mode: Standard / Principia Calculus
│   ├── source evidence count
│   └── derivation depth
│
├── Symbolic Lineage Graph
│   ├── Layer 0: retrieved works/evidence
│   ├── Layer 1: existed ideas/principles/takeaways
│   ├── Layer 2: derived concepts
│   ├── Layer 3: hypotheses/arguments/deductions
│   └── Layer 4: final idea
│
├── Risk and Contradiction Map
├── Source Evidence
├── Related Prior Art
├── Validation Protocol
├── User Feedback / Experiment Feedback
└── Export Panel
```

### 14.2 Node styling

```text
Solid border:
  evidence-backed extracted concept

Dashed border:
  speculative LLM-derived concept

Green:
  validated or supported

Red:
  contradicted or high-risk

Blue:
  user-provided note or assumption

Gray:
  deprecated or low-confidence

Gold:
  final generated idea
```

### 14.3 Edge interactions

Clicking an edge should show:

```text
relation_type
source node
target node
rationale
support strength
model/version that created it
validator status
```

### 14.4 Node interactions

Clicking a node should show:

```text
symbol
full expansion
concept type
source origin
validation status
evidence links
related works
versions
promotion/rejection actions
```

### 14.5 User actions

```text
Promote node:
  save useful speculative concept to project or global candidate pool

Reject node:
  mark derivation as bad; avoid similar future derivations

Regenerate from selected nodes:
  run Principia Calculus with approved subset

Expand natural language:
  ask LLM to expand a compact symbolic derivation into a readable explanation

Export lineage:
  DERIVATION_GRAPH.json
  PRINCIPLE_TRACE.json
  IDEA_CARD.md
```

### 14.6 Visualization libraries

For local static UI:

```text
SVG + vanilla JS for simple graphs
D3.js for custom layout
```

For richer hosted/product UI:

```text
React Flow
Cytoscape.js
Sigma.js
```

---

## 15. API and Module Refactor

### 15.1 New modules

Recommended module layout:

```text
principia/
  schema_v3.py
  global_store.py
  identity_resolver.py
  work_versioning.py
  extraction_scheduler.py
  concept_extractor.py
  concept_canonicalizer.py
  concept_indexer.py
  hybrid_retriever.py
  symbol_registry.py
  symbolic_ideator.py
  derivation_verifier.py
  lineage_graph.py
  migration_v2_to_v3.py
```

### 15.2 Service responsibilities

| Module | Responsibility |
|---|---|
| `global_store.py` | normalized tables, transactions, migrations |
| `identity_resolver.py` | match incoming works to canonical global works |
| `work_versioning.py` | content hashes, source timestamps, version decisions |
| `extraction_scheduler.py` | decide which LLM extractions are required |
| `concept_canonicalizer.py` | dedupe/merge/version concept cards |
| `concept_indexer.py` | maintain FTS/vector/graph indexes |
| `hybrid_retriever.py` | independent retrieval by concept type |
| `symbol_registry.py` | symbol creation, collision handling, expansion |
| `symbolic_ideator.py` | Principia Calculus loop |
| `derivation_verifier.py` | patch validation and status assignment |
| `lineage_graph.py` | DAG construction and UI payloads |
| `migration_v2_to_v3.py` | convert current buckets into new schema |

### 15.3 New API endpoints

```text
POST /api/v3/research/start
GET  /api/v3/research/status

POST /api/v3/global/works/resolve
POST /api/v3/global/works/upsert
POST /api/v3/global/extractions/ensure

GET  /api/v3/global/search
POST /api/v3/global/retrieve-concepts

POST /api/v3/symbols/ensure
GET  /api/v3/symbols/table
GET  /api/v3/symbols/expand

POST /api/v3/ideas/standard-generate
POST /api/v3/ideas/symbolic-generate
GET  /api/v3/ideas/{idea_id}/lineage

POST /api/v3/derivations/{derivation_id}/verify
POST /api/v3/derivations/{derivation_id}/promote-node
POST /api/v3/derivations/{derivation_id}/reject-node

POST /api/v3/feedback/ingest
```

### 15.4 Compatibility layer

To avoid rewriting everything immediately, add a compatibility adapter:

```python
class CompatStore:
    def list_items(self, bucket, query="", limit=100):
        return GlobalStore.query_bucket_compatible(bucket, query, limit)

    def get_item(self, bucket, item_id):
        return GlobalStore.get_compatible_record(bucket, item_id)
```

This lets the existing UI tabs continue working while the backend schema evolves.

---

## 16. Migration Plan from Current Demo

### 16.1 Bucket mapping

| Current bucket | New representation |
|---|---|
| `source_works` | `global_work` + `work_version` |
| `existed_ideas` | `concept_card(type=existed_idea)` + `concept_version` |
| `principles` | `concept_card(type=principle)` + `concept_version` |
| `takeaway_messages` | `concept_card(type=takeaway_message)` + `concept_version` |
| `benchmark_records` | `concept_card(type=benchmark)` or normalized benchmark table |
| `baseline_records` | `concept_card(type=baseline)` or normalized baseline table |
| `result_records` | `concept_card(type=result_fact)` or normalized result table |
| `ideas` / `my_ideas` | `concept_card(type=generated_idea)` + derivation graph |
| `evidence_links` | `evidence_link` |
| `project_memberships` | project-to-work/concept membership tables |
| `research_runs` | `research_run` + `extraction_run` + `derivation_run` |

### 16.2 Migration steps

```text
Step 1. Add v3 tables alongside current records table.
Step 2. Backfill global_work from source_works.
Step 3. Create work_version rows from current work payloads.
Step 4. Backfill concept_card and concept_version from existed_ideas, principles, and takeaway_messages.
Step 5. Backfill project memberships.
Step 6. Generate initial symbols for existing concept cards.
Step 7. Create FTS index over concepts and works.
Step 8. Add optional embedding generation job.
Step 9. Add compatibility read APIs.
Step 10. Gradually move UI endpoints to v3 retrieval.
```

### 16.3 Migration safety

```text
Do not delete current records table immediately.
Keep v2 data immutable during initial migration.
Write v3 records in parallel for one release.
Add a `migration_status` table.
Add rollback export to JSON.
Run tests against v2 compatibility APIs.
```

---

## 17. Quality Metrics and Diagnostics

### 17.1 Global library efficiency

```text
work_cache_hit_rate:
  retrieved works already present in global_work

llm_extraction_avoidance_rate:
  works that did not require new extraction

duplicate_work_rate:
  works later merged as duplicates

duplicate_concept_rate:
  concepts later merged

stale_extraction_rate:
  extractions invalidated by work_version or schema changes
```

### 17.2 Retrieval quality

```text
precision_at_k_existed_ideas
precision_at_k_principles
precision_at_k_takeaway_messages
independent_retrieval_diversity
work_cluster_diversity
validation_level_distribution
human_acceptance_rate
```

### 17.3 Principia Calculus quality

```text
output_token_cost_per_idea
derivation_depth
verified_node_ratio
unsupported_node_rejection_rate
speculative_node_reuse_rate
final_idea_novelty_score
final_idea_feasibility_score
user_selected_idea_rate
```

### 17.4 Research survival metrics

```text
time_to_first_validation_plan
time_to_first_runnable_experiment
post_execution_score_drop
idea_survival_after_implementation
prediction_vs_actual_calibration
feedback_ingestion_rate
```

### 17.5 Product quality dashboard

Add a developer dashboard showing:

```text
Global library size
Works by source provider
Concepts by type
Concepts by validation level
Extraction runs by model
Cache hit rate
LLM cost saved by reuse
Most reused symbols
Most rejected speculative nodes
Top failure modes
```

---

## 18. Security, Privacy, and Research Integrity

### 18.1 Scope and sharing policy

Each object should have a scope:

```text
global_public:
  visible to all users

org_shared:
  visible inside a team/workspace

project_private:
  visible only in one project

user_private:
  visible only to one user

symbolic_scratch:
  temporary or derivation-run-local
```

Default policy:

```text
Private user notes, unpublished ideas, private papers, and local code artifacts should never enter the global public library automatically.
```

### 18.2 Research integrity rules

```text
No concept without provenance.
No evidence-backed claim without evidence links.
No speculative node promoted as literature fact.
No hidden failed validations.
No fabricated citations.
No automatic public sharing of private records.
No automatic paper submission.
```

### 18.3 LLM-derived content guardrails

```text
LLM-derived intermediate objects must be labeled L0.
LLM-derived concepts require promotion before global reuse as serious evidence.
Contradicted concepts remain searchable but are marked contradicted/deprecated.
Users can inspect source evidence for all evidence-backed concepts.
```

### 18.4 Cost guardrails

```text
Extraction cache must be checked before every LLM call.
Intermediate symbolic generation should have strict output-token caps.
Long natural-language explanations should be generated lazily.
Project-level and user-level cost budgets should be enforced.
```

---

## 19. Implementation Roadmap

### Phase 1: Global library normalization

Estimated effort: 1-2 weeks.

Deliverables:

```text
global_work
work_version
extraction_run
concept_card
concept_version
evidence_link
project membership migration
compatibility adapter
```

Success criteria:

```text
Same work is not duplicated across projects.
Same extraction is not repeated for unchanged work/model/prompt/schema.
Existing UI tabs still work through compatibility adapter.
```

### Phase 2: Hybrid search index

Estimated effort: 1-2 weeks.

Deliverables:

```text
FTS index for works and concepts
embedding table or sqlite-vec integration
hybrid retriever
RRF or weighted fusion
independent retrieval by concept type
retrieval explanation payload
```

Success criteria:

```text
Principles, existed ideas, and takeaway messages can be searched independently.
Top retrieved cards are visibly more relevant than work-level retrieval.
```

### Phase 3: Work update and extraction cache

Estimated effort: 1-2 weeks.

Deliverables:

```text
identity resolver
work content hasher
source timestamp comparator
extraction cache key
LLM extraction scheduler
concept canonicalizer
```

Success criteria:

```text
Unchanged works skip extraction.
Changed works create new work_version.
Different LLMs create concept versions.
Ambiguous identity cases are flagged, not blindly merged.
```

### Phase 4: Symbol registry

Estimated effort: 1 week.

Deliverables:

```text
symbol_registry table
symbol generator
collision detector
symbol expansion API
symbol display UI
```

Success criteria:

```text
Every concept has a stable compact symbol.
Symbols are unique within namespace.
Symbols expand to full provenance and payload.
```

### Phase 5: Principia Calculus

Estimated effort: 2-3 weeks.

Deliverables:

```text
symbolic_ideator.py
derivation tables
derivation patch schema
derivation verifier
iterative symbolic generation loop
final idea synthesis from derivation graph
```

Success criteria:

```text
New mode can generate an idea from a symbolic derivation graph.
Intermediate derived nodes are stored as speculative L0 objects.
Output-token usage is lower than verbose chain generation.
```

### Phase 6: Lineage visualization

Estimated effort: 1-2 weeks.

Deliverables:

```text
Symbolic Lineage section on idea page
layered graph layout
node expansion
edge inspector
promote/reject/regenerate controls
DERIVATION_GRAPH.json export
```

Success criteria:

```text
User can see how final idea was formed from prior concepts.
User can inspect every source and intermediate node.
User can reject bad speculative derivations.
```

---

## 20. Example End-to-End Run

### 20.1 User query

```text
Generate a new idea for reducing API cost in LLM research agents while keeping idea quality high.
```

### 20.2 Independent retrieval result

```text
Relevant existed ideas:
  XI.RAGD  RAG-only ideation drift
  XI.EVAL  Evaluator-first agent loops

Relevant principles:
  P.ATCU   Adaptive token/compute routing under uncertainty
  P.EFB    Evaluator-first binding
  P.CSR    Compression as sufficient representation

Relevant takeaway messages:
  TM.ROH   Routing overhead can erase adaptive-compute gains
  TM.BSF   Baseline strength often determines whether gains are meaningful

Relevant benchmarks:
  B.AGENT  Agent task benchmark family
  B.SCI    Scientific ideation evaluation suite
```

### 20.3 Principia Calculus derivation

```text
D.EVR = compose(P.ATCU, P.EFB)
      = route research actions by expected evidence value before spending retrieval/coding budget

D.COST = stress_test(D.EVR, TM.ROH)
       = routing must be cheap and triggered only under high uncertainty

D.NOV = contrast(D.COST, XI.RAGD)
      = retrieval should not be always-on; it should fire when it reduces uncertainty

I.EVRA = specialize(D.NOV, "LLM research agents")
       = Evidence-Value Routed Research Agents
```

### 20.4 Final idea

```text
Title:
  Evidence-Value Routed Research Agents

Thesis:
  A research agent should allocate retrieval, critique, coding, and ablation effort according to expected evidence value, rather than following a fixed pipeline or always-on RAG loop.

Core mechanism:
  At each step, estimate which action most reduces uncertainty about whether the idea will survive implementation, then route budget there.

Novelty claim:
  Existing research agents often separate ideation, retrieval, coding, and validation into fixed stages. This idea makes evidence-value estimation the controller for the entire research workflow.

Cheapest falsification:
  Compare a fixed-stage research agent against an evidence-routed agent on small research tasks, measuring supported-idea rate per API dollar.

Key risk:
  The evidence-value estimator may be too expensive or miscalibrated, causing routing overhead to cancel benefits.
```

### 20.5 Visible lineage graph

```text
P.ATCU ─┐
        ├─ compose ─> D.EVR ─┐
P.EFB  ─┘                    ├─ stress_test + gate ─> D.COST ─┐
TM.ROH ───── warns_against ──┘                                ├─ contrast ─> D.NOV ─> I.EVRA
XI.RAGD ───── prior_art_contrast ─────────────────────────────┘
```

---

## 21. Key Design Decisions for Review

### Decision 1: Use one unified concept table

Recommended:

```text
concept_card + concept_type
```

Rather than separate unrelated tables for existed ideas, principles, takeaway messages, etc.

Reason:

```text
shared versioning, retrieval, symbols, evidence links, and derivation graph logic
```

### Decision 2: Treat LLM differences as concept versions

Recommended:

```text
same concept_id
different concept_version_id
different extraction_run_id
```

Reason:

```text
avoid duplicates while preserving model-specific outputs
```

### Decision 3: Store speculative derivations globally but separately

Recommended:

```text
store derived concepts as L0/speculative_unverified
place them in symbolic_scratch or global_candidate scope
```

Reason:

```text
allows recursive reuse without polluting evidence-backed literature memory
```

### Decision 4: Use structured derivation graph, not raw hidden reasoning transcript

Recommended:

```text
store symbols, operators, nodes, edges, short rationales, and verification status
```

Reason:

```text
gives explainability and UI traceability while keeping generation compact and auditable
```

### Decision 5: Use hybrid retrieval for every important concept search

Recommended:

```text
FTS + vector + graph + structured filters + rerank
```

Reason:

```text
scientific retrieval needs exact terms and semantic similarity at the same time
```

### Decision 6: Use local-first storage for demo, Postgres/pgvector for hosted product

Recommended:

```text
local: SQLite + FTS5 + sqlite-vec/embedding table
hosted: Postgres + pgvector + full-text search + object storage
```

Reason:

```text
minimal local complexity; scalable hosted architecture later
```

---

## 22. Appendix A: Proposed SQL-Like Schema

This schema is intentionally SQL-like rather than final migration code.

### 22.1 Global work

```sql
CREATE TABLE global_work (
  work_id TEXT PRIMARY KEY,
  canonical_title TEXT NOT NULL,
  title_norm TEXT NOT NULL,
  title_hash TEXT NOT NULL,
  doi TEXT,
  arxiv_id TEXT,
  openalex_id TEXT,
  crossref_id TEXT,
  semantic_scholar_id TEXT,
  year INTEGER,
  venue_or_source TEXT,
  source_type TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL,
  identity_confidence REAL,
  identity_status TEXT
);

CREATE UNIQUE INDEX idx_work_doi ON global_work(doi) WHERE doi IS NOT NULL AND doi != '';
CREATE UNIQUE INDEX idx_work_arxiv ON global_work(arxiv_id) WHERE arxiv_id IS NOT NULL AND arxiv_id != '';
CREATE INDEX idx_work_title_hash ON global_work(title_hash);
```

### 22.2 Work version

```sql
CREATE TABLE work_version (
  work_version_id TEXT PRIMARY KEY,
  work_id TEXT NOT NULL,
  source_provider TEXT,
  source_record_id TEXT,
  title TEXT,
  abstract TEXT,
  title_hash TEXT,
  abstract_hash TEXT,
  source_modified_at TEXT,
  source_updated_at TEXT,
  metadata_json TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(work_id) REFERENCES global_work(work_id)
);

CREATE INDEX idx_work_version_work ON work_version(work_id);
CREATE INDEX idx_work_version_hash ON work_version(work_id, title_hash, abstract_hash);
```

### 22.3 Extraction run

```sql
CREATE TABLE extraction_run (
  extraction_run_id TEXT PRIMARY KEY,
  work_id TEXT NOT NULL,
  work_version_id TEXT NOT NULL,
  llm_provider TEXT,
  llm_model TEXT,
  model_mode TEXT,
  prompt_version TEXT,
  schema_version TEXT,
  extraction_task_type TEXT,
  extraction_status TEXT,
  input_token_estimate INTEGER,
  output_token_estimate INTEGER,
  cost_estimate REAL,
  error_message TEXT,
  created_at TEXT NOT NULL,
  completed_at TEXT,
  FOREIGN KEY(work_id) REFERENCES global_work(work_id),
  FOREIGN KEY(work_version_id) REFERENCES work_version(work_version_id)
);

CREATE UNIQUE INDEX idx_extraction_cache
ON extraction_run(
  work_version_id,
  llm_provider,
  llm_model,
  prompt_version,
  schema_version,
  extraction_task_type
);
```

### 22.4 Concept card

```sql
CREATE TABLE concept_card (
  concept_id TEXT PRIMARY KEY,
  concept_type TEXT NOT NULL,
  canonical_key TEXT NOT NULL,
  canonical_label TEXT,
  source_origin TEXT NOT NULL,
  validation_level TEXT,
  verification_status TEXT,
  confidence_score REAL,
  public_scope TEXT,
  created_by_user_id TEXT,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX idx_concept_type ON concept_card(concept_type);
CREATE INDEX idx_concept_validation ON concept_card(validation_level);
CREATE INDEX idx_concept_scope ON concept_card(public_scope);
```

### 22.5 Concept version

```sql
CREATE TABLE concept_version (
  concept_version_id TEXT PRIMARY KEY,
  concept_id TEXT NOT NULL,
  extraction_run_id TEXT,
  llm_provider TEXT,
  llm_model TEXT,
  prompt_version TEXT,
  schema_version TEXT,
  payload_json TEXT NOT NULL,
  summary_text TEXT,
  text_hash TEXT,
  quality_score REAL,
  is_active BOOLEAN,
  is_manual_edit BOOLEAN,
  created_at TEXT NOT NULL,
  FOREIGN KEY(concept_id) REFERENCES concept_card(concept_id),
  FOREIGN KEY(extraction_run_id) REFERENCES extraction_run(extraction_run_id)
);

CREATE INDEX idx_concept_version_concept ON concept_version(concept_id);
CREATE INDEX idx_concept_version_active ON concept_version(concept_id, is_active);
```

### 22.6 Evidence link

```sql
CREATE TABLE evidence_link (
  evidence_id TEXT PRIMARY KEY,
  concept_id TEXT NOT NULL,
  concept_version_id TEXT,
  work_id TEXT,
  work_version_id TEXT,
  evidence_type TEXT,
  evidence_span TEXT,
  source_url TEXT,
  confidence REAL,
  created_at TEXT NOT NULL,
  FOREIGN KEY(concept_id) REFERENCES concept_card(concept_id),
  FOREIGN KEY(concept_version_id) REFERENCES concept_version(concept_version_id),
  FOREIGN KEY(work_id) REFERENCES global_work(work_id),
  FOREIGN KEY(work_version_id) REFERENCES work_version(work_version_id)
);
```

### 22.7 Symbol registry

```sql
CREATE TABLE symbol_registry (
  symbol_id TEXT PRIMARY KEY,
  concept_id TEXT NOT NULL,
  namespace TEXT NOT NULL,
  short_code TEXT NOT NULL,
  label TEXT NOT NULL,
  gloss TEXT,
  symbol_source TEXT,
  llm_provider TEXT,
  llm_model TEXT,
  status TEXT,
  created_at TEXT NOT NULL,
  UNIQUE(namespace, short_code),
  FOREIGN KEY(concept_id) REFERENCES concept_card(concept_id)
);
```

### 22.8 Derivation graph

```sql
CREATE TABLE derivation_run (
  derivation_id TEXT PRIMARY KEY,
  project_id TEXT,
  query TEXT,
  generation_mode TEXT,
  llm_provider TEXT,
  llm_model TEXT,
  prompt_version TEXT,
  created_at TEXT NOT NULL,
  completed_at TEXT,
  status TEXT
);

CREATE TABLE derivation_node (
  node_id TEXT PRIMARY KEY,
  derivation_id TEXT NOT NULL,
  concept_id TEXT,
  node_type TEXT,
  symbol_code TEXT,
  expression TEXT,
  natural_language_summary TEXT,
  validation_status TEXT,
  speculation_depth INTEGER,
  confidence REAL,
  verifier_status TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(derivation_id) REFERENCES derivation_run(derivation_id),
  FOREIGN KEY(concept_id) REFERENCES concept_card(concept_id)
);

CREATE TABLE derivation_edge (
  edge_id TEXT PRIMARY KEY,
  derivation_id TEXT NOT NULL,
  source_node_id TEXT NOT NULL,
  target_node_id TEXT NOT NULL,
  relation_type TEXT,
  rationale TEXT,
  created_at TEXT NOT NULL,
  FOREIGN KEY(derivation_id) REFERENCES derivation_run(derivation_id),
  FOREIGN KEY(source_node_id) REFERENCES derivation_node(node_id),
  FOREIGN KEY(target_node_id) REFERENCES derivation_node(node_id)
);
```

### 22.9 Project memberships

```sql
CREATE TABLE project_record_membership (
  membership_id TEXT PRIMARY KEY,
  project_id TEXT NOT NULL,
  record_type TEXT NOT NULL,
  record_id TEXT NOT NULL,
  source TEXT,
  display_order INTEGER,
  hidden BOOLEAN,
  created_at TEXT NOT NULL,
  updated_at TEXT NOT NULL
);

CREATE INDEX idx_project_membership_project
ON project_record_membership(project_id, record_type, display_order);
```

---

## 23. Appendix B: Symbolic Patch Schema

Intermediate LLM outputs in Principia Calculus should use a compact JSON patch.

```json
{
  "new_nodes": [
    {
      "symbol": "D.EVR",
      "node_type": "derived_concept",
      "expression": "compose(P.ATCU, P.EFB)",
      "summary": "Rank research actions by expected evidence value before spending retrieval or coding budget.",
      "support_symbols": ["P.ATCU", "P.EFB"],
      "risk_symbols": ["TM.ROH"],
      "validation_status": "speculative_unverified",
      "confidence": 0.54,
      "cheapest_falsification": "Compare fixed-stage research agent vs evidence-routed agent on small idea-validation tasks."
    }
  ],
  "new_edges": [
    {
      "source": "P.ATCU",
      "target": "D.EVR",
      "relation": "composes",
      "rationale": "Both concern allocating scarce reasoning or compute budget under uncertainty."
    },
    {
      "source": "P.EFB",
      "target": "D.EVR",
      "relation": "composes",
      "rationale": "Evaluator-first binding gives the routing objective."
    },
    {
      "source": "TM.ROH",
      "target": "D.EVR",
      "relation": "warns_against",
      "rationale": "Adaptive routing only helps if routing overhead is lower than saved compute."
    }
  ],
  "candidate_ideas": [
    {
      "symbol": "I.EVRA",
      "title": "Evidence-Value Routed Research Agents",
      "derived_from": ["D.EVR"],
      "one_sentence_thesis": "Research agents should route retrieval, critique, coding, and ablation budget toward the action with highest expected evidence value."
    }
  ]
}
```

### 23.1 Patch validation rules

```text
1. All support_symbols and risk_symbols must exist.
2. All new symbols must be unique in the derivation namespace.
3. All new nodes are L0 unless explicitly verified by evidence links.
4. A final idea must include at least one evidence-backed upstream path.
5. A final idea must include at least one risk or falsification node.
6. Natural-language summaries should be short.
7. Expressions should use allowed operators only.
```

---

## 24. Appendix C: Source-Backed Technical References

These references support the storage and retrieval architecture recommended in this proposal.

1. **SQLite FTS5** — official SQLite documentation describes FTS5 as a virtual table module for efficient full-text search over large document collections and supports `MATCH`, relevance ranking, phrase search, prefix search, NEAR queries, column filters, and boolean operators.  
   URL: https://www.sqlite.org/fts5.html

2. **sqlite-vec** — a local SQLite vector search extension that can run on laptops, servers, mobile devices, browsers via WASM, and other environments, with pure SQL create/insert/select usage.  
   URL: https://alexgarcia.xyz/sqlite-vec/

3. **pgvector** — Postgres vector similarity search extension supporting exact nearest-neighbor search, approximate indexes such as HNSW and IVFFlat, hybrid search with Postgres full-text search, half-precision vectors, binary vectors, and sparse vectors.  
   URL: https://github.com/pgvector/pgvector

4. **OpenAlex Developers** — OpenAlex documentation describes OpenAlex as a fully open catalog of the global research system, with hundreds of millions of scholarly works, authors, institutions, and more; it offers API access and data snapshots.  
   URL: https://developers.openalex.org/

5. **Principia original proposal** — defines the product as a principle-first automatic idea discovery system that converts literature into a living Principle Pool, generates traceable ideas, estimates outcomes, exports validation prompts, and ingests feedback.

---

## Final Recommendation

The next generation of Principia should be built around one core transformation:

```text
From project-local extraction demo
    to shared versioned global principle memory
    to symbolic lineage-based idea generation.
```

The new system should make three things first-class:

```text
1. Global memory:
   works, versions, extraction runs, concepts, evidence, symbols.

2. Independent retrieval:
   ideas, principles, takeaways, benchmarks, baselines, and feedback lessons retrieved separately.

3. Symbolic derivation:
   compact symbols, recursive derived concepts, verifier, and visible lineage graph.
```

If implemented carefully, Principia will be clearly differentiated from generic idea-generation systems. It will not merely produce more ideas. It will produce ideas whose origin, assumptions, risks, evidence, speculative reasoning path, and validation plan are visible and reusable.

