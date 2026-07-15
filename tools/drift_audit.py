#!/usr/bin/env python3
"""Drift audit: has any vendored third-party skill changed upstream?

Reads manifest.json, and for every third-party skill asks the GitHub API:
"what is the latest commit touching this skill's source_path on the
upstream default branch, and what was it as of our pinned commit?"
If those differ, the skill has drifted and needs a diff-review
(see docs/INTAKE.md, Update flow).

Nothing is updated automatically — this script only reports.

Usage (from repo root):
  python3 tools/drift_audit.py

Optional: set GITHUB_TOKEN in the environment to raise API rate limits
(the weekly GitHub Action does this automatically).

Exit codes: 0 = everything current, 1 = drift found, 2 = audit error.
"""

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
API = "https://api.github.com"


def gh_get(url: str):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json",
                                               "User-Agent": "skills-drift-audit"})
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def latest_commit_for_path(owner: str, repo: str, path: str, ref: str):
    """Newest commit sha touching `path` as of `ref` (or None if none found)."""
    data = gh_get(f"{API}/repos/{owner}/{repo}/commits?path={path}&sha={ref}&per_page=1")
    if not data:
        return None, None, None
    c = data[0]
    return c["sha"], c["commit"]["committer"]["date"][:10], c["commit"]["message"].splitlines()[0][:80]


def main() -> None:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    entries = manifest.get("third_party_skills", [])
    if not entries:
        print("No third-party skills in manifest — nothing to audit.")
        sys.exit(0)

    drifted, current, errors = [], [], []

    # Group by (repo, pinned_commit) so repo-level info prints once.
    for e in entries:
        repo_url = e["source_repo"].rstrip("/")
        owner, repo = repo_url.split("github.com/")[1].split("/")[:2]
        skill, path, pinned = e["skill"], e["source_path"], e["pinned_commit"]
        try:
            head_sha, head_date, head_msg = latest_commit_for_path(owner, repo, path, "HEAD")
            pin_sha, _, _ = latest_commit_for_path(owner, repo, path, pinned)
            if head_sha is None:
                errors.append(f"{skill}: path no longer exists upstream ({path}) — upstream may have moved or deleted it")
            elif head_sha == pin_sha:
                current.append(skill)
            else:
                drifted.append(
                    f"{skill}: CHANGED upstream\n"
                    f"    reviewed as of: {pinned[:9]}\n"
                    f"    newest touching commit: {head_sha[:9]} ({head_date}) {head_msg}\n"
                    f"    diff to review: {repo_url}/compare/{pinned[:12]}...{head_sha[:12]}"
                )
        except Exception as exc:  # rate limits, network, renamed repos
            errors.append(f"{skill}: audit failed ({exc})")

    print(f"DRIFT AUDIT — {len(entries)} third-party skills")
    print(f"current: {len(current)} | drifted: {len(drifted)} | errors: {len(errors)}")
    if drifted:
        print("\n== DRIFTED (needs diff-review per docs/INTAKE.md) ==")
        print("\n".join(drifted))
    if errors:
        print("\n== ERRORS ==")
        print("\n".join(f"  {x}" for x in errors))
    if current:
        print("\n== CURRENT ==\n  " + ", ".join(current))

    sys.exit(1 if drifted else (2 if errors else 0))


if __name__ == "__main__":
    main()
