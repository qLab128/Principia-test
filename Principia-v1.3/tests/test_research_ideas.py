from __future__ import annotations

from pathlib import Path

import principia as pc
from principia.llm import LLMConfig
from principia.models import WorkItem


class LooseExtractionLLM(pc.LLMClient):
    def available(self, model: str = "auto") -> bool:
        return True

    def resolve(self, model: str = "auto") -> LLMConfig:
        return LLMConfig(provider="custom", model="loose-extraction", api_key="test", base_url="https://example.test")

    def chat_json(self, system: str, user: str, **kwargs):
        return {
            "ideas": ["Continuous process quality control for coding agents."],
            "principles": ["Risk estimates should be calibrated before they gate autonomous edits."],
            "baselines": ["Static lint-only gates"],
            "benchmarks": [{"name": "repository-scale coding benchmark"}],
            "takeaways": ["A controller should map risk into concrete actions."],
            "result_facts": ["Calibration can be measured with expected calibration error."],
        }


def static_source(query: str, limit: int, timeout: float):
    return [
        {
            "title": "Evidence Gated Multi Agent Scientific Discovery",
            "authors": ["Ada Example", "Grace Example"],
            "abstract": (
                "The paper proposes a multi-agent discovery system with benchmark evaluation, "
                "a named baseline, and evidence-gated routing under token budget constraints."
            ),
            "year": 2026,
            "venue": "MockConf",
            "source": "static",
            "url": "https://example.test/paper",
            "doi": "10.0000/principia.mock",
        },
        {
            "title": "Evidence Gated Multi Agent Scientific Discovery",
            "authors": ["Duplicate"],
            "abstract": "Duplicate should be removed by DOI.",
            "year": 2026,
            "venue": "MockConf",
            "source": "static",
            "url": "https://example.test/paper2",
            "doi": "10.0000/principia.mock",
        },
    ][:limit]


def arxiv_duplicate_source(query: str, limit: int, timeout: float):
    return [
        {
            "title": "Repository Aware Quality Control for Coding Agents",
            "abstract": "A preprint about repository-aware quality control for coding agents.",
            "year": 2026,
            "venue": "arXiv",
            "source": "arxiv",
            "url": "https://arxiv.org/abs/2601.12345",
            "arxiv_id": "2601.12345",
            "metadata": {"is_preprint": True, "is_peer_reviewed": False, "publication_type": "preprint"},
        }
    ][:limit]


def crossref_duplicate_source(query: str, limit: int, timeout: float):
    return [
        {
            "title": "Repository Aware Quality Control for Coding Agents",
            "abstract": "A peer reviewed paper about repository-aware quality control for coding agents.",
            "year": 2026,
            "venue": "International Conference on Software Engineering",
            "source": "crossref",
            "url": "https://doi.org/10.1145/principia.peer",
            "doi": "10.1145/principia.peer",
            "citation_count": 42,
            "metadata": {"is_peer_reviewed": True, "is_preprint": False, "publication_type": "proceedings-article"},
        }
    ][:limit]


def mixed_review_source(query: str, limit: int, timeout: float):
    return [
        {
            "title": "Large Scale Repository Quality Control for Coding Agents",
            "abstract": "Repository quality control for coding agents with calibrated process risk.",
            "venue": "arXiv",
            "source": "arxiv",
            "metadata": {"is_preprint": True, "is_peer_reviewed": False, "publication_type": "preprint"},
        },
        {
            "title": "Calibrated Process Risk for Coding Agents",
            "abstract": "Repository quality control for coding agents with calibrated process risk.",
            "venue": "ACM Transactions on Software Engineering and Methodology",
            "source": "crossref",
            "citation_count": 5,
            "metadata": {"is_peer_reviewed": True, "is_preprint": False, "publication_type": "journal-article"},
        },
    ][:limit]


def workspace(tmp_path: Path) -> pc.Workspace:
    return pc.Workspace(tmp_path, llm=pc.MockLLMClient(), search_sources={"static": static_source})


def test_search_dedupes_and_persists_works(tmp_path: Path) -> None:
    ws = workspace(tmp_path)

    works = ws.research.search("evidence gated multi agent discovery", target_count=5)

    assert len(works) == 1
    assert works[0].doi == "10.0000/principia.mock"
    assert ws.counts()["works"] == 1


def test_search_merges_arxiv_duplicate_into_peer_reviewed_venue(tmp_path: Path) -> None:
    ws = pc.Workspace(
        tmp_path,
        llm=pc.MockLLMClient(),
        search_sources={"arxiv": arxiv_duplicate_source, "crossref": crossref_duplicate_source},
    )

    works = ws.research.search("repository quality control coding agents", target_count=5)

    assert len(works) == 1
    assert works[0].venue == "International Conference on Software Engineering"
    assert works[0].source == "crossref"
    assert works[0].doi == "10.1145/principia.peer"
    assert works[0].arxiv_id == "2601.12345"
    assert works[0].metadata["is_peer_reviewed"] is True
    assert works[0].metadata["has_preprint"] is True
    assert "arxiv" in works[0].metadata["merged_sources"]


def test_search_ranking_prefers_peer_reviewed_metadata(tmp_path: Path) -> None:
    ws = pc.Workspace(tmp_path, llm=pc.MockLLMClient(), search_sources={"mixed": mixed_review_source})

    works = ws.research.search("repository quality control coding agents calibrated process risk", target_count=2)

    assert works[0].venue == "ACM Transactions on Software Engineering and Methodology"
    assert works[0].metadata["is_peer_reviewed"] is True
    assert works[1].venue == "arXiv"


def test_extract_cache_overwrite_and_generate_compare(tmp_path: Path) -> None:
    ws = workspace(tmp_path)
    works = ws.research.search("evidence gated multi agent discovery", target_count=5)

    first = ws.research.extract(works, model="mock")
    second = ws.research.extract(works, model="mock", overwrite=False)
    third = ws.research.extract(works, model="mock", overwrite=True)

    assert len(first) == 1
    assert first.items[0].ideas
    assert second.items[0].skipped is True
    assert third.items[0].skipped is False
    assert ws.counts()["extractions"] == 1

    idea = ws.ideas.generate(first, user_note="optimize token cost", mode="calculus", model="mock")
    comparison = ws.ideas.compare(idea, works, model="mock")

    assert idea.mode == "calculus"
    assert idea.lineage["nodes"]
    assert comparison.rows
    assert ws.counts()["ideas"] == 1
    assert ws.counts()["comparisons"] == 1


def test_workspace_run_pipeline_exports_result(tmp_path: Path) -> None:
    ws = workspace(tmp_path)

    result = ws.run(
        "evidence gated multi agent discovery",
        target_count=5,
        model="mock",
        sources=["static"],
        user_note="optimize token cost",
    )

    assert len(result.works) == 1
    assert result.features.items[0].ideas
    assert result.idea.thesis
    assert result.comparison.rows
    assert (Path(result.export_path) / "result.json").exists()
    assert (Path(result.export_path) / "works.json").exists()
    assert (Path(result.export_path) / "idea.md").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "principia_outputs" / "latest" / "idea.md").exists()


def test_workspace_staged_pipeline_can_export_result(tmp_path: Path) -> None:
    ws = workspace(tmp_path)

    works = ws.research.search("evidence gated multi agent discovery", target_count=5)
    features = ws.research.extract(works, model="mock")
    selected = pc.select_evidence(features, kinds=["ideas", "principles", "takeaways"])
    idea = ws.ideas.generate(selected, user_note="optimize token cost", mode="calculus", model="mock")
    comparison = ws.ideas.compare(idea, features, model="mock")
    export_path = ws.export(goal=works.query, works=works, features=features, idea=idea, comparison=comparison)

    assert selected.counts()["ideas"] == 1
    assert idea.methodological_details["equations"]
    assert idea.source_evidence
    assert (export_path / "result.json").exists()
    assert (export_path / "works.json").exists()
    text = (export_path / "idea.md").read_text()
    assert "## Methodological Details" in text
    assert "### Source Evidence" in text
    assert (tmp_path / "principia_outputs" / "exports" / idea.id / "idea.md").exists()
    assert (tmp_path / "principia_outputs" / "latest" / "result.json").exists()


def test_extract_normalizes_loose_provider_feature_lists(tmp_path: Path) -> None:
    ws = pc.Workspace(tmp_path, llm=LooseExtractionLLM())
    work = pc.WorkItem(
        id="Coding_Agent_Process_Control",
        title="Real-Time Process Quality Control for Autonomous Coding Agents",
        abstract="A repository-scale controller estimates calibrated risk and chooses actions.",
    )

    features = ws.research.extract([work], model="custom:loose-extraction", overwrite=True)
    item = features.items[0]

    assert item.ideas[0]["core_idea"] == "Continuous process quality control for coding agents."
    assert item.principles[0]["argument"].startswith("Risk estimates")
    assert item.baselines[0]["name"] == "Static lint-only gates"
    assert item.takeaways[0]["message"].startswith("A controller")
    assert item.result_facts[0]["fact"].startswith("Calibration")
    assert all(record["id"] for record in [*item.ideas, *item.principles, *item.baselines, *item.takeaways, *item.result_facts])


def test_feature_summary_handles_v12_style_keys() -> None:
    features = pc.ExtractedFeatures(
        model="test",
        items=[
            pc.WorkFeatures(
                work_id="W1",
                title="Agentic quality paper",
                model="test",
                ideas=[{"id": "I1", "idea_text": "Use calibrated process risk to gate autonomous edits."}],
                principles=[{"id": "P1", "abstract_signature": "Warnings must be actionable and calibrated."}],
                takeaways=[{"id": "T1", "message_text": "Quality signals should map to concrete interventions."}],
            )
        ],
    )

    markdown = pc.feature_summary_markdown(features)

    assert "calibrated process risk" in markdown
    assert "Warnings must be actionable" in markdown
    assert "concrete interventions" in markdown


def test_idea_markdown_cleans_numbered_workflow_and_wraps_latex() -> None:
    idea = pc.Idea(
        id="I1",
        title="Process Control Idea",
        thesis="Control autonomous coding-agent process quality.",
        mode="calculus",
        methodological_details={
            "summary": "A controller uses diff features.",
            "symbols": [{"symbol": "q_t", "definition": "quality state"}],
            "equations": [{"name": "Risk", "latex": "r_t = P(y_t=1 | q_t)"}],
            "workflow": [{"step": "2. Step 2", "detail": "2. Extract static features F, H, L from the patch diff."}],
            "reliability_checks": [{"check": "1. Calibration", "detail": "1. Check ECE."}],
        },
    )

    markdown = pc.idea_markdown(idea)

    assert "2. **Step 2:** 2. Extract" not in markdown
    assert "1. **Step:** Extract static features $F$, $H$, $L$ from the patch diff." in markdown
    assert "$r_t = P(y_t=1 | q_t)$" in markdown
    assert "- $q_t$: quality state" in markdown


def test_compare_requires_llm_without_mock(tmp_path: Path) -> None:
    ws = pc.Workspace(tmp_path)
    feature = pc.WorkFeatures(
        work_id="W1",
        title="Prior work",
        model="mock",
        ideas=[{"title": "Prior routed method", "core_idea": "Use routing."}],
    )
    idea = pc.Idea(
        id="I1",
        title="New routed method",
        thesis="Use routing with evidence gates.",
        mode="standard",
        mechanism_design=["Route when evidence supports it."],
    )

    try:
        ws.ideas.compare(idea, [feature], model="openai:gpt-4.1")
    except RuntimeError as exc:
        assert "requires a callable LLM" in str(exc)
    else:
        raise AssertionError("compare should not silently fallback without a callable LLM")


def test_public_types_are_importable() -> None:
    assert pc.Workspace
    assert pc.WorkItem is WorkItem
    assert pc.WorkList
    assert pc.ExtractedFeatures
    assert pc.EvidencePacket
    assert pc.Idea
    assert pc.IdeaComparison
    assert pc.RunHandle
    assert pc.RunStatus
    assert pc.CancelToken
    assert pc.LLMConfig
    assert pc.select_evidence
    assert "methodological_details" in pc.schema_markdown(pc.Idea)
