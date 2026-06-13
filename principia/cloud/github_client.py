from __future__ import annotations

import shutil
import subprocess
import tempfile
from typing import Any
from pathlib import Path


def pr_export_instructions(contribution_path: str) -> dict[str, Any]:
    return {
        "mode": "pr_export",
        "contribution_path": contribution_path,
        "safe_default": True,
        "instructions": [
            "Create a branch in the GitHub repository.",
            "Add the contribution file under cloud/contributions/ or attach it to the maintainer workflow.",
            "Open a pull request against main.",
            "Wait for principia-cloud-validate to pass before merge.",
        ],
    }


def maintainer_direct_push(
    contribution_path: str,
    repo_root: Path,
    *,
    branch: str = "",
    remote: str = "origin",
    base_branch: str = "main",
    push: bool = True,
) -> dict[str, Any]:
    source = _resolve_contribution_path(contribution_path, repo_root)
    if not source.exists():
        return {"ok": False, "mode": "maintainer_direct_push", "error": f"Contribution file not found: {source}"}
    if source.suffix.lower() != ".json":
        return {"ok": False, "mode": "maintainer_direct_push", "error": "Contribution file must be a JSON file."}

    branch = branch.strip() or f"codex/cloud-contribution-{_safe_branch_part(source.stem)}"
    worktree_root = Path(tempfile.mkdtemp(prefix="principia-cloud-push-"))
    worktree_path = worktree_root / _safe_branch_part(branch)
    target_rel = Path("cloud") / "contributions" / source.name
    commands: list[dict[str, Any]] = []

    def git(cwd: Path, args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            ["git", *args],
            cwd=str(cwd),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        commands.append(
            {
                "cwd": str(cwd),
                "args": ["git", *args],
                "returncode": completed.returncode,
                "stdout": completed.stdout[-2000:],
                "stderr": completed.stderr[-2000:],
            }
        )
        if check and completed.returncode != 0:
            raise RuntimeError((completed.stderr or completed.stdout or "git command failed").strip())
        return completed

    try:
        git(repo_root, ["fetch", remote, base_branch], check=False)
        if worktree_path.exists():
            shutil.rmtree(worktree_path)
        base_ref = f"{remote}/{base_branch}"
        add = git(repo_root, ["worktree", "add", "--detach", str(worktree_path), base_ref], check=False)
        if add.returncode != 0:
            git(repo_root, ["worktree", "add", "--detach", str(worktree_path), base_branch])
        git(worktree_path, ["checkout", "-B", branch])
        target = worktree_path / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        git(worktree_path, ["add", str(target_rel)])
        status = git(worktree_path, ["status", "--porcelain", "--", str(target_rel)]).stdout.strip()
        if not status:
            return {
                "ok": True,
                "mode": "maintainer_direct_push",
                "branch": branch,
                "pushed": False,
                "message": "Contribution already exists with identical content.",
                "commands": commands,
            }
        git(worktree_path, ["commit", "-m", f"Add Principia cloud contribution {source.stem}"])
        commit = git(worktree_path, ["rev-parse", "HEAD"]).stdout.strip()
        if push:
            git(worktree_path, ["push", "-u", remote, f"HEAD:{branch}"])
        return {
            "ok": True,
            "mode": "maintainer_direct_push",
            "branch": branch,
            "remote": remote,
            "base_branch": base_branch,
            "pushed": bool(push),
            "commit": commit,
            "target_path": str(target_rel),
            "commands": commands,
        }
    except Exception as exc:
        return {
            "ok": False,
            "mode": "maintainer_direct_push",
            "branch": branch,
            "remote": remote,
            "base_branch": base_branch,
            "pushed": False,
            "error": str(exc),
            "commands": commands,
        }
    finally:
        if worktree_path.exists():
            git(repo_root, ["worktree", "remove", "--force", str(worktree_path)], check=False)
        if worktree_root.exists():
            shutil.rmtree(worktree_root, ignore_errors=True)


def _resolve_contribution_path(value: str, repo_root: Path) -> Path:
    path = Path(str(value or "")).expanduser()
    return path if path.is_absolute() else repo_root / path


def _safe_branch_part(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_", "."} else "-" for ch in str(value or "").strip())
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    return (cleaned or "contribution")[:80]
