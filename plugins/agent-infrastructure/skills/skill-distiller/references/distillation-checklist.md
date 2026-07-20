# Distillation Checklist

Run this before calling any skill done. Each item exists because its absence has a known failure mode (noted in parentheses).

## Evidence

- [ ] The provenance line names a real incident, correction, or workflow — not a hypothetical (speculative skills encode guesses, not lessons)
- [ ] Nothing in the body re-teaches what the model already knows (context bloat buries the actual lesson)
- [ ] The lesson would recur without this skill (one-off capabilities don't earn their maintenance cost)

## Boundaries

- [ ] Hard lines are stated as design rules with reasons, once, structurally (disclaimers get ignored; understood constraints get followed)
- [ ] Every time-critical or consistency-critical step is in code, not prose (a prompt cannot promise "exactly once")
- [ ] Proactive behavior has a rule-based interrupt bar and state-file dedup (vibe-based interruption trains the user to ignore the skill)
- [ ] Instruction strictness matches step fragility (exact steps where wrong moves are costly; heuristics where many paths are valid)
- [ ] Every failure-capable step documents what failure looks like and what happens next (happy-path skills break silently in production)
- [ ] Steps only a human can perform are halt-for-user gates with the exact command printed (an agent that pretends success is worse than one that stops)
- [ ] The staleness falsifier section exists and is specific (skills that can't name their expiry conditions misfire quietly instead of getting fixed)

## Body

- [ ] Required output elements have template slots, not prose requests (prose skips the unfun parts; templates can't)
- [ ] Each step that matters names the artifact proving it ran (presence of instructions is not evidence of execution)
- [ ] Destructive writes go through the proposed-diff gate (reversible until the moment of commit)
- [ ] Setup is state-checked before use (assuming setup is the most common first-run failure)
- [ ] Repeated-run skills have an append-only run log read at start (without run memory, the skill repeats itself)
- [ ] Every constraint carries its reason (future maintainers must distinguish load-bearing rules from incidental ones)
- [ ] Facts about live systems are marked verify-before-trust, not baked in as truth (notes decay; reality is the source of truth)
- [ ] No absolute paths, no time-sensitive facts, no bundled library source (portability, rot, and bloat respectively)

## Routing and library fit

- [ ] Description = what + when + differentiator, with realistic trigger phrases (the description routes; if the skill doesn't fire, the description is wrong)
- [ ] Description never summarizes the workflow (agents follow the summary and skip the body)
- [ ] Overlaps with existing skills are named and disambiguated in writing (silent overlap causes silent misrouting)
- [ ] Dependencies (CLIs, endpoints, credentials, other skills) are declared (undeclared dependencies fail as mysteries)
- [ ] Command execution, unattended operation, or delegated trust is prominently labeled (risk that isn't surfaced can't be consented to)

## Verification

- [ ] Trigger test passed: the skill fires on a natural description of the task, unnamed (routing is half the skill)
- [ ] Execution test passed on the original motivating case (a skill that can't beat baseline on its own lesson isn't carrying it)
- [ ] Adversarial pass done; real gaps patched, hypothetical ones resisted (bloat is also a failure mode)
- [ ] Trigger confidence and output confidence reported separately, with what would raise the lower one (they are independent quantities)
- [ ] v1 shipped; deferred improvements logged as what / why-not-now / trigger-condition (speculative polish delays real feedback)
