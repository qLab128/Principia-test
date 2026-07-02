from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .features import idea_markdown
from .ideas import IdeaService
from .llm import LLMClient, LLMConfig
from .models import CancelToken, ExtractedFeatures, Idea, IdeaComparison, PipelineResult, WorkList
from .research import ResearchService, SearchSource
from .run import ProgressCallback
from .storage import WorkspaceStorage


class Workspace:
    """Top-level local-first Principia workspace."""

    def __init__(
        self,
        root: str | Path = ".",
        *,
        llm: LLMClient | None = None,
        llm_config: LLMConfig | None = None,
        search_sources: dict[str, SearchSource] | None = None,
    ) -> None:
        self.root = Path(root).expanduser().resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.storage = WorkspaceStorage(self.root)
        self._ensure_visible_workspace()
        self.llm = llm or LLMClient(llm_config)
        self.research = ResearchService(self.storage, self.llm, search_sources=search_sources)
        self.ideas = IdeaService(self.storage, self.llm)

    @property
    def path(self) -> Path:
        return self.root

    @property
    def db_path(self) -> Path:
        return self.storage.db_path

    @property
    def artifacts_dir(self) -> Path:
        return self.storage.artifacts_dir

    @property
    def outputs_dir(self) -> Path:
        return self.root / "principia_outputs"

    def counts(self) -> dict[str, int]:
        return self.storage.counts()

    def run_events(self, run_id: str) -> list[dict[str, Any]]:
        return self.storage.list_run_events(run_id)

    def run(
        self,
        goal: str,
        *,
        target_count: int = 20,
        model: str = "auto",
        idea_model: str | None = None,
        compare_model: str | None = None,
        mode: str = "calculus",
        user_note: str = "",
        sources: list[str] | None = None,
        overwrite: bool = False,
        extract_count: int | None = None,
        show_progress: bool = False,
        callback: ProgressCallback | None = None,
        cancel_token: CancelToken | None = None,
    ) -> PipelineResult:
        works = self.research.search(
            goal,
            target_count=target_count,
            sources=sources,
            show_progress=show_progress,
            callback=callback,
            cancel_token=cancel_token,
        )
        extraction_input = works
        if extract_count is not None:
            extraction_input = WorkList(
                query=works.query,
                items=works.items[: max(1, min(int(extract_count), len(works.items)))],
                target_count=extract_count,
                mode=works.mode,
                sources=works.sources,
                run_id=works.run_id,
            )
        features = self.research.extract(
            extraction_input,
            model=model,
            overwrite=overwrite,
            show_progress=show_progress,
            callback=callback,
            cancel_token=cancel_token,
        )
        idea = self.ideas.generate(
            features,
            user_note=user_note or goal,
            mode=mode,
            model=idea_model or model,
            overwrite=overwrite,
            show_progress=show_progress,
            callback=callback,
            cancel_token=cancel_token,
        )
        comparison = self.ideas.compare(
            idea,
            features,
            model=compare_model or idea_model or model,
            show_progress=show_progress,
            callback=callback,
            cancel_token=cancel_token,
        )
        result = PipelineResult(
            goal=goal,
            works=works,
            features=features,
            idea=idea,
            comparison=comparison,
            workspace_path=str(self.path),
        )
        export_path = self.export_result(result)
        return result.model_copy(update={"export_path": str(export_path)})

    def export_result(self, result: PipelineResult) -> Path:
        export_dir = self.artifacts_dir / "exports" / result.idea.id
        export_dir.mkdir(parents=True, exist_ok=True)
        payload = result.model_dump()
        (export_dir / "result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        (export_dir / "works.json").write_text(json.dumps(result.works.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
        (export_dir / "idea.md").write_text(format_idea_markdown(result), encoding="utf-8")
        self._write_visible_export(result, export_dir)
        return export_dir

    def export(
        self,
        *,
        goal: str,
        works: WorkList,
        features: ExtractedFeatures,
        idea: Idea,
        comparison: IdeaComparison,
    ) -> Path:
        result = PipelineResult(
            goal=goal,
            works=works,
            features=features,
            idea=idea,
            comparison=comparison,
            workspace_path=str(self.path),
        )
        return self.export_result(result)

    def _ensure_visible_workspace(self) -> None:
        self.outputs_dir.mkdir(parents=True, exist_ok=True)
        readme = self.root / "README.md"
        if not readme.exists():
            readme.write_text(
                "\n".join(
                    [
                        "# Principia Workspace",
                        "",
                        "Visible files are written to `principia_outputs/`.",
                        "Internal SQLite state and caches are stored in the hidden `.principia/` folder.",
                        "",
                        "Typical files after export:",
                        "",
                        "- `principia_outputs/latest/idea.md`",
                        "- `principia_outputs/latest/result.json`",
                        "- `principia_outputs/latest/works.json`",
                        "- `principia_outputs/exports/<idea_id>/...`",
                        "",
                    ]
                ),
                encoding="utf-8",
            )
        index = self.outputs_dir / "README.md"
        if not index.exists():
            index.write_text(
                "\n".join(
                    [
                        "# Principia Outputs",
                        "",
                        "This visible folder mirrors the main exported artifacts from `.principia/artifacts/exports/`.",
                        "",
                        "- `latest/` contains the latest exported workflow result.",
                        "- `exports/` contains timestamp-free idea-ID folders for previous exports.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )

    def _write_visible_export(self, result: PipelineResult, hidden_export_dir: Path) -> None:
        export_dir = self.outputs_dir / "exports" / result.idea.id
        latest_dir = self.outputs_dir / "latest"
        for target in (export_dir, latest_dir):
            target.mkdir(parents=True, exist_ok=True)
            payload = result.model_dump()
            (target / "result.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            (target / "works.json").write_text(json.dumps(result.works.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8")
            (target / "idea.md").write_text(format_idea_markdown(result), encoding="utf-8")
            (target / "README.md").write_text(
                "\n".join(
                    [
                        f"# {result.idea.title}",
                        "",
                        f"Hidden canonical export: `{hidden_export_dir}`",
                        "",
                        "- `idea.md`: readable Idea Card.",
                        "- `result.json`: complete structured workflow result.",
                        "- `works.json`: retrieved work list.",
                        "",
                    ]
                ),
                encoding="utf-8",
            )


def format_idea_markdown(result: PipelineResult) -> str:
    idea = result.idea
    lines = [f"# {idea.title}", "", f"Goal: {result.goal}", "", idea_markdown(idea).strip(), ""]
    if result.comparison.rows:
        lines.extend(
            [
                "## Comparison Highlights",
                *[
                    f"- {row.get('title', 'Prior idea')}: {row.get('essential_difference') or row.get('mechanistic_similarity')}"
                    for row in result.comparison.rows[:8]
                ],
            ]
        )
    return "\n".join(lines).strip() + "\n"
