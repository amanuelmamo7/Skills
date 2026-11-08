# Deferred Work Register

Consciously postponed work: what / why not now / what would trigger doing it. Per the `deferred-work-register` skill — an omission recorded here is a decision, not a gap.

| What | Why not now | Trigger to do it |
|---|---|---|
| `persuasive-drafting` skill (objective→persuasive transition: theme development, persuasive rule framing and case illustrations, persuasion through placement, headings, paragraph and sentence structure) | Furthest from current transactional practice; attorney-workflow v1 prioritizes analysis and client-communication skills | First real brief-writing or demand-letter matter; or litigation-posture skills seeing regular use |
| External delegates for `model-delegation` (Hermes/GPT via OpenClaw, local Ollama) — register non-Claude models in the delegate registry via MCP-wrapped invocation (reference shape: MCP tool exposing an OpenAI-compatible endpoint) | RAM cannot host GPT + Claude + Ollama concurrently; Claude-only registry captures the bulk of savings without new wiring | Hardware upgrade; or OpenClaw gains a Hermes endpoint; or monthly model spend makes free-local delegation material |
| Trim `tax-analysis` description (1198 chars) to ≤ 1024 | Works in Claude Code today; only strict tools reject it | Before adding evals to `tax-analysis`, or any tool/marketplace rejects the skill |
| Verify PR #8 tightening (contract-table quotes, explicit "because", term-of-art at first use) | Small, hard-line-neutral changes; a dedicated rerun isn't worth the cost | Next batch eval run that includes any of the three legal skills |
| Evals for remaining high-stakes skills (`contract-dispute-analysis`, `regulatory-change-analysis`, `litigation-hold-and-triage`, `authority-synthesis`, `tax-analysis`) | Pilot (4 skills) proved the method; each spec costs authoring time + a run | Next substantive edit to that skill, or before relying on it for real client work |
| Place the two private skills' evals (kept outside this repo) beside their private sources | Those skills live outside this public repo | First time either private skill is edited or tested |
| Run Hedera skill evals with `--baseline` (agent-kit-plugin, hedera-consensus-service, hedera-token-service; 8 cases, ~$1–1.50) | Not building on Hedera yet; no decision hinges on it; upstream checks are mostly string-match `contains`, a weaker signal than our rubric checks | Start of a real Hedera build — the run decides which Hedera skills to keep |
