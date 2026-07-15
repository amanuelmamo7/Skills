# Intake Checklist — third-party skills

Run this before any skill from another repo enters this library. No exceptions, even for "official" sources.

## Checklist

1. **Read the entire SKILL.md.** Do the instructions only do what the description claims?
2. **Commands and network.** Does it tell the agent to run shell commands, fetch URLs, or send data anywhere? Each one must be justified and visible. Hidden or obfuscated instructions = reject.
3. **Scripts.** Any `scripts/` files get line-by-line review — highest risk tier. Markdown-only skills are lower risk (but prompt injection is still possible).
4. **Data sensitivity.** Does it handle credentials, personal data, or client data? For attorney-workflow skills, treat this as a confidentiality question.
5. **License.** MIT / Apache-2.0 / BSD = fine. No license = don't vendor it; link to it instead.
6. **Record it.** Copy the skill in (never link or submodule), then add a manifest.json entry:

```json
{
  "skill": "skill-folder-name",
  "source_repo": "https://github.com/author/repo",
  "pinned_commit": "full commit SHA reviewed",
  "reviewed_by": "Amanuel",
  "review_date": "YYYY-MM-DD",
  "license": "MIT",
  "risk_notes": "e.g. markdown only, no scripts, no network calls",
  "buckets": ["general"]
}
```

Getting the commit SHA of what you reviewed: on the skill's GitHub page press `y` (URL pins to the current commit), or run `git log -1 --format=%H` in a clone.

## Update flow (when the weekly audit flags upstream drift)

1. Read the diff between `pinned_commit` and upstream HEAD.
2. Re-run the checklist on the changed parts only.
3. Copy the new version in, update `pinned_commit` and `review_date`.
4. Commit with a note describing what changed upstream.
