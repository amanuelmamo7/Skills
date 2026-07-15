#!/opt/homebrew/bin/python3.13
"""
Claude analysis layer.

Fixes vs v1:
  - Calls the methods that actually exist (vpip()/pfr(), not *_pct()).
  - None-safe formatting: a fresh session can never crash the prompt build.
  - Uses the Anthropic Python SDK (streaming, ~sub-second first token)
    when `anthropic` is installed AND ANTHROPIC_API_KEY is set;
    otherwise falls back to the authenticated `claude` CLI.
  - analyze() never raises — it returns an error string instead, so the
    HUD input thread can never be killed by an advice query again.
"""

import os
import subprocess
import logging

from parser import GameState, state_summary
from stats import SessionTracker

log = logging.getLogger("hud.advisor")

CLAUDE_BIN = "/opt/homebrew/bin/claude"
MODEL      = "claude-haiku-4-5-20251001"   # fast — mid-hand latency budget
CLI_TIMEOUT = 25


def _fmt(v, spec=".0f", suffix=""):
    return f"{v:{spec}}{suffix}" if v is not None else "—"


def _player_line(p):
    return (f"{p.hands}h | VPIP {_fmt(p.vpip(), '.0f', '%')} "
            f"PFR {_fmt(p.pfr(), '.0f', '%')} "
            f"3B {_fmt(p.threeb(), '.0f', '%')} "
            f"AF {_fmt(p.af(), '.1f')} "
            f"CB {_fmt(p.cb(), '.0f', '%')} "
            f"FCB {_fmt(p.fcb(), '.0f', '%')} "
            f"WTSD {_fmt(p.wtsd(), '.0f', '%')}")


def build_prompt(state: GameState, tracker: SessionTracker, question: str = "") -> str:
    # The frame at query time often lacks cards (sidebar refresh, partial
    # OCR) — fall back to what the tracker remembered for this hand.
    hand = getattr(tracker, "hand", None)
    if hand is not None:
        if not state.hero_cards and hand.hero_cards:
            state.hero_cards = list(hand.hero_cards)
        if not state.board and hand.board:
            state.board = list(hand.board)
    villain_lines = []
    for seat, v in sorted(tracker.villains.items(), key=lambda x: -x[1].hands):
        if v.hands >= 3:
            villain_lines.append(f"  #{seat}: {_player_line(v)}")
    villain_block = ("\n".join(villain_lines)
                     if villain_lines else "  (insufficient sample — <3 hands)")
    hero_block = "  " + _player_line(tracker.hero)

    spr_line = ""
    stacks = dict(state.villain_stacks)
    if state.hero_stack_bb is not None:
        stacks["HERO"] = state.hero_stack_bb
    if state.pot_bb and stacks:
        eff = min(stacks.values())
        spr_line = f"SPR: {eff / state.pot_bb:.1f} | "

    bounty_line = ""
    if state.game_type == "tournament" and state.bounties:
        b = "  ".join(f"#{k}=${v:.2f}" for k, v in state.bounties.items())
        bounty_line = f"Bounties (PKO): {b}\n"

    q = question.strip() or "What is the best action and why? 3-4 sentences max."

    return f"""You are a poker coach giving real-time decision support. Be direct and concise — the player needs to act fast.

=== CURRENT HAND ===
{state_summary(state)}
{spr_line}Hand #{tracker.hand_count} ({state.game_type})
{bounty_line}
=== HERO STATS (this session) ===
{hero_block}

=== VILLAIN STATS (this session, by seat number) ===
{villain_block}

=== QUESTION ===
{q}

Answer in plain text. Lead with the recommended action, then the reason. Max 4 sentences. No markdown headers."""


# ─── Backends ─────────────────────────────────────────────────────────────────

_sdk_client = None

def _try_sdk():
    """Persistent Anthropic SDK client if installed + key present."""
    global _sdk_client
    if _sdk_client is not None:
        return _sdk_client
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return None
    try:
        import anthropic
        _sdk_client = anthropic.Anthropic()
        return _sdk_client
    except Exception:
        return None


def _query_sdk(client, prompt, stream_print=True):
    out = []
    with client.messages.stream(
        model=MODEL, max_tokens=300,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            out.append(text)
            if stream_print:
                print(text, end="", flush=True)
    if stream_print:
        print()
    return "".join(out)


def _query_cli(prompt):
    result = subprocess.run(
        [CLAUDE_BIN, "-p", prompt, "--model", MODEL],
        capture_output=True, text=True, timeout=CLI_TIMEOUT,
    )
    output = result.stdout.strip()
    if not output and result.stderr:
        return f"[Claude error: {result.stderr.strip()[:200]}]"
    return output or "[No response from Claude]"


def analyze(state: GameState, tracker: SessionTracker, question: str = "",
            stream_print=True) -> str:
    """Build prompt + query Claude. NEVER raises."""
    try:
        prompt = build_prompt(state, tracker, question)
    except Exception as e:
        log.exception("prompt build failed")
        return f"[Prompt build failed: {e!r} — see logs]"
    try:
        client = _try_sdk()
        if client is not None:
            return _query_sdk(client, prompt, stream_print=stream_print)
        return _query_cli(prompt)
    except subprocess.TimeoutExpired:
        return "[Claude timed out — decide on your reads]"
    except Exception as e:
        log.exception("claude query failed")
        return f"[Analysis unavailable: {e!r}]"
