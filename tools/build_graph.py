#!/usr/bin/env python3
"""Generate graph.html — an interactive view of the knowledge graph.

Embeds index.json into a self-contained HTML page (vis-network via CDN).
Open graph.html in any browser. Node colors: skills by bucket, sources
gray, human gold. Edge labels show relationship types.

Run from the repo root:  python3 tools/build_graph.py
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BUCKET_COLORS = {
    "market-analysis": "#4e79a7",
    "personal-assistant": "#59a14f",
    "web-application": "#f28e2b",
    "agent-infrastructure": "#b07aa1",
    "general": "#76b7b2",
    "attorney-workflow": "#e15759",
    "projects": "#edc948",
}

TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Skills Knowledge Graph</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
  body { margin:0; font-family:-apple-system,sans-serif; }
  #graph { width:100vw; height:92vh; }
  #legend { padding:8px 16px; font-size:13px; color:#333; border-bottom:1px solid #ddd; }
  .chip { display:inline-block; margin-right:12px; }
  .dot { display:inline-block; width:10px; height:10px; border-radius:50%; margin-right:4px; }
</style>
</head>
<body>
<div id="legend">__LEGEND__ &nbsp;|&nbsp; ◆ source &nbsp; ★ reviewer &nbsp;|&nbsp; hover a node for details, drag to explore</div>
<div id="graph"></div>
<script>
const data = __DATA__;
const bucketColors = __COLORS__;
const nodes = data.nodes.map(n => {
  if (n.type === "human") return { id:n.id, label:n.name, shape:"star", size:28, color:"#f1c40f", title:n.role };
  if (n.type === "source") return { id:n.id, label:n.name, shape:"diamond", size:18, color:"#95a5a6", title:n.location||"" };
  const b = (n.buckets||[])[0];
  return { id:n.id, label:n.id, shape:"dot", size:12,
           color: bucketColors[b] || "#7f8c8d",
           title: n.id + "\\n" + (n.description||"") + "\\nrisk: " + (n.risk||"") };
});
const edges = data.edges.map(e => ({
  from:e.from, to:e.to,
  label: (e.type==="copied-from"||e.type==="reviewed-by") ? "" : e.type,
  font:{size:9, color:"#888"},
  color: e.type==="reviewed-by" ? "#f1c40f" : (e.type==="copied-from" ? "#ccc" : "#e15759"),
  arrows:"to", width: e.type==="use-instead"||e.type==="use-with" ? 2 : 0.6
}));
new vis.Network(document.getElementById("graph"), {nodes, edges}, {
  physics:{ solver:"forceAtlas2Based", forceAtlas2Based:{ gravitationalConstant:-40, springLength:90 }, stabilization:{iterations:150} },
  interaction:{ hover:true, tooltipDelay:100 }
});
</script>
</body>
</html>
"""


def main() -> None:
    index = json.loads((ROOT / "index.json").read_text())
    legend = "".join(
        f'<span class="chip"><span class="dot" style="background:{c}"></span>{b}</span>'
        for b, c in BUCKET_COLORS.items()
    )
    html = (
        TEMPLATE.replace("__DATA__", json.dumps(index))
        .replace("__COLORS__", json.dumps(BUCKET_COLORS))
        .replace("__LEGEND__", legend)
    )
    (ROOT / "graph.html").write_text(html)
    n = len(index["nodes"])
    e = len(index["edges"])
    print(f"graph.html: {n} nodes, {e} edges")


if __name__ == "__main__":
    main()
