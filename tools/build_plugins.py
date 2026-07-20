#!/usr/bin/env python3
"""Generate bucket-level plugins from index.json.

index.json is the source of truth. This script:
  1. Reads every skill node and its buckets.
  2. Rebuilds plugins/<bucket>/ from scratch: a .claude-plugin/plugin.json
     plus a skills/ directory containing a copy of each member skill.
  3. Rewrites .claude-plugin/marketplace.json listing the full library
     plugin plus one plugin per non-empty bucket.

Run from the repo root:  python3 tools/build_plugins.py
Re-run whenever a skill is added, removed, or re-bucketed.
Generated plugins/ content is committed so marketplace installs work.
"""

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "0.2.0"

BUCKET_DESCRIPTIONS = {
    "general": "Research, writing, and thinking utilities: deep research, research briefs, note synthesis, proofreading.",
    "web-application": "Web app development: React, Next.js, Tailwind, shadcn/ui, frontend design, form CRO, SEO audits.",
    "attorney-workflow": "Legal practice workflows and legal-AI research.",
    "market-analysis": "Market and equity analysis: pre/post-market briefs, macro readthroughs, deep dives, theses.",
    "personal-assistant": "Executive-assistant capabilities: briefs, comms, transcription, time tracking, redaction, reminders.",
    "agent-infrastructure": "Building and running agents: design patterns, orchestration, scheduling, memory.",
    "dev-operations": "Running software responsibly: house rules, audits, incidents, rotations, costs, CI gates.",
    "software-architecture": "Design patterns for software: DDD, CQRS, event sourcing, sagas, dbt modeling.",
}

OWNER = {"name": "Amanuel Mamo", "email": "amanuelmamo7@gmail.com"}


def main() -> None:
    index = json.loads((ROOT / "index.json").read_text())
    skills = [n for n in index["nodes"] if n["type"] == "skill"]

    buckets: dict[str, list[str]] = {}
    for s in skills:
        for b in s.get("buckets", []):
            buckets.setdefault(b, []).append(s["id"])

    plugins_dir = ROOT / "plugins"
    if plugins_dir.exists():
        shutil.rmtree(plugins_dir)

    plugin_entries = [
        {
            "name": "skills-library",
            "source": "./",
            "description": f"The full curated library ({len(skills)} skills across {len(buckets)} buckets).",
        }
    ]

    # Stable order: as declared in index.json's buckets array.
    for bucket in [b for b in index.get("buckets", []) if b in buckets]:
        members = sorted(buckets[bucket])
        bucket_dir = plugins_dir / bucket
        (bucket_dir / ".claude-plugin").mkdir(parents=True)
        (bucket_dir / ".claude-plugin" / "plugin.json").write_text(
            json.dumps(
                {
                    "name": bucket,
                    "version": VERSION,
                    "description": BUCKET_DESCRIPTIONS.get(
                        bucket, f"Skills in the {bucket} bucket."
                    )
                    + f" ({len(members)} skill{'s' if len(members) != 1 else ''} — generated from index.json, do not edit by hand.)",
                    "author": OWNER,
                },
                indent=2,
            )
            + "\n"
        )
        for skill_id in members:
            src = ROOT / "skills" / skill_id
            if not src.is_dir():
                raise SystemExit(f"index.json lists '{skill_id}' but skills/{skill_id} is missing")
            shutil.copytree(src, bucket_dir / "skills" / skill_id)
        plugin_entries.append(
            {
                "name": bucket,
                "source": f"./plugins/{bucket}",
                "description": BUCKET_DESCRIPTIONS.get(bucket, f"{bucket} bucket")
                + f" ({len(members)} skill{'s' if len(members) != 1 else ''})",
            }
        )
        print(f"plugins/{bucket}: {len(members)} skills")

    marketplace = {
        "name": "amanuel-skills",
        "owner": OWNER,
        "metadata": {
            "description": "Amanuel's curated skills library — reviewed, pinned, and indexed. index.json is the knowledge graph; manifest.json is third-party provenance.",
            "version": VERSION,
        },
        "plugins": plugin_entries,
    }
    mp_dir = ROOT / ".claude-plugin"
    mp_dir.mkdir(exist_ok=True)
    (mp_dir / "marketplace.json").write_text(json.dumps(marketplace, indent=2) + "\n")
    print(f"marketplace.json: {len(plugin_entries)} plugins, version {VERSION}")


if __name__ == "__main__":
    main()
