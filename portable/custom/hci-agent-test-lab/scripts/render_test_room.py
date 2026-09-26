#!/usr/bin/env python3
"""Render a self-contained SimFrancisco-style observer room for one run."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lab_common import read_json


def safe_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def build_payload(run_dir: Path) -> dict[str, Any]:
    manifest = read_json(run_dir / "manifest.json")
    aggregate = read_json(run_dir / "aggregate.json") if (run_dir / "aggregate.json").exists() else {
        "status": "not-aggregated",
        "issues": [],
        "unknowns": [],
        "positive_signals": [],
    }

    agents: list[dict[str, Any]] = []
    station_positions = {
        "orientation": (18, 29),
        "flow": (48, 50),
        "evidence": (72, 24),
        "recovery": (76, 68),
    }
    for index, item in enumerate(manifest.get("cohort", [])):
        profile = read_json(run_dir / item["profile_path"])
        result_path = run_dir / "results" / f"{item['agent_id']}.json"
        result = read_json(result_path) if result_path.exists() else None
        station = profile.get("character", {}).get("station", "flow")
        base_x, base_y = station_positions.get(station, (45, 45))
        agents.append(
            {
                "agent_id": item["agent_id"],
                "profile_id": item["profile_id"],
                "name": profile.get("name", item["agent_id"]),
                "lens": profile.get("lens", ""),
                "questions": profile.get("mission_questions", []),
                "character": profile.get("character", {}),
                "x": base_x + (index % 2) * 6,
                "y": base_y + (index // 2) * 8,
                "status": result.get("status", "waiting") if result else "waiting",
                "task_outcome": result.get("task_outcome", {}) if result else {},
                "path": result.get("path", []) if result else [],
                "findings": result.get("findings", []) if result else [],
                "positive_signals": result.get("positive_signals", []) if result else [],
                "open_questions": result.get("open_questions", []) if result else [],
            }
        )
    return {"manifest": manifest, "aggregate": aggregate, "agents": agents}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir.expanduser().resolve()
    output = args.output.expanduser().resolve() if args.output else run_dir / "test-room.html"
    payload = build_payload(run_dir)

    page = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>HCI Agent Test Room</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #191816;
      --muted: #69645c;
      --paper: #f4efdf;
      --paper-2: #e9e1cc;
      --signal: #f5bb2d;
      --danger: #b83f43;
      --ok: #23755b;
      --line: rgba(25,24,22,.24);
      --shadow: 0 16px 44px rgba(55,45,28,.12);
    }
    * { box-sizing: border-box; }
    body { margin: 0; background: #d8cfb9; color: var(--ink); font: 15px/1.45 Inter, ui-sans-serif, system-ui, sans-serif; }
    button { font: inherit; }
    .shell { min-height: 100vh; display: grid; grid-template-rows: auto 1fr; }
    header { display: grid; grid-template-columns: 1fr auto; gap: 24px; padding: 22px 28px; background: var(--ink); color: #fff9e9; border-bottom: 5px solid var(--signal); }
    .eyebrow { margin: 0 0 5px; color: #f5c650; font: 700 11px/1.2 ui-monospace, monospace; letter-spacing: .12em; text-transform: uppercase; }
    h1 { margin: 0; max-width: 920px; font-size: clamp(22px, 3vw, 40px); line-height: 1.04; letter-spacing: -.035em; }
    .meta { align-self: center; text-align: right; color: #cec7b8; font: 12px/1.5 ui-monospace, monospace; }
    .layout { display: grid; grid-template-columns: minmax(0, 1.55fr) minmax(330px, .7fr); gap: 14px; padding: 14px; min-height: 0; }
    .room, .inspector { background: var(--paper); border: 2px solid var(--ink); box-shadow: var(--shadow); }
    .room { position: relative; min-height: 670px; overflow: hidden; background-image: linear-gradient(var(--line) 1px, transparent 1px), linear-gradient(90deg, var(--line) 1px, transparent 1px); background-size: 34px 34px; }
    .room::after { content: ""; position: absolute; inset: 0; pointer-events: none; background: radial-gradient(circle at 50% 45%, transparent 0 40%, rgba(25,24,22,.07) 100%); }
    .room-title { position: absolute; z-index: 3; left: 18px; top: 16px; max-width: 55%; padding: 11px 13px; background: var(--paper); border: 2px solid var(--ink); }
    .room-title strong { display: block; font-size: 16px; }
    .room-title span { color: var(--muted); font-size: 12px; }
    .station { position: absolute; width: 168px; min-height: 88px; padding: 10px; background: rgba(255,252,239,.82); border: 2px solid var(--ink); z-index: 1; }
    .station b { display: block; font: 700 11px/1.2 ui-monospace, monospace; text-transform: uppercase; letter-spacing: .08em; }
    .station span { color: var(--muted); font-size: 11px; }
    .s-orientation { left: 7%; top: 20%; }
    .s-flow { left: 39%; top: 43%; }
    .s-evidence { right: 7%; top: 17%; }
    .s-recovery { right: 7%; bottom: 10%; }
    .path { position: absolute; z-index: 0; background: rgba(255,255,255,.42); border: 1px dashed rgba(25,24,22,.28); }
    .path-a { left: 24%; top: 33%; width: 37%; height: 36px; transform: rotate(17deg); }
    .path-b { left: 56%; top: 39%; width: 34%; height: 36px; transform: rotate(-39deg); }
    .agent { position: absolute; z-index: 4; width: 112px; transform: translate(-50%,-50%); border: 0; background: transparent; color: var(--ink); cursor: pointer; text-align: center; }
    .agent:focus-visible { outline: 4px solid #0c6bea; outline-offset: 5px; }
    .figure { position: relative; display: inline-block; width: 42px; height: 62px; filter: drop-shadow(4px 6px 0 rgba(25,24,22,.14)); }
    .head { position: absolute; left: 10px; top: 0; width: 22px; height: 22px; background: #d99d72; border: 2px solid var(--ink); border-radius: 7px 7px 5px 5px; }
    .hair { position: absolute; left: 8px; top: -2px; width: 26px; height: 10px; background: var(--ink); border-radius: 8px 8px 2px 2px; }
    .body { position: absolute; left: 6px; top: 23px; width: 30px; height: 26px; background: var(--coat); border: 2px solid var(--ink); border-radius: 5px 5px 2px 2px; }
    .leg { position: absolute; top: 48px; width: 10px; height: 13px; background: var(--accent); border: 2px solid var(--ink); }
    .leg-a { left: 8px; } .leg-b { right: 8px; }
    .status-dot { position: absolute; right: -3px; top: 17px; width: 12px; height: 12px; border: 2px solid var(--ink); border-radius: 50%; background: #aaa; }
    .completed .status-dot { background: var(--ok); }
    .blocked .status-dot, .failed .status-dot { background: var(--danger); }
    .waiting .status-dot { background: var(--signal); }
    .agent-label { display: block; margin-top: 3px; padding: 4px 6px; background: var(--paper); border: 1px solid var(--ink); font-weight: 750; font-size: 12px; }
    .agent small { display: block; color: var(--muted); font: 10px/1.2 ui-monospace, monospace; }
    .completed .figure { animation: breathe 2.4s ease-in-out infinite; }
    .waiting .figure { animation: wait 1.2s steps(2,end) infinite; }
    @keyframes breathe { 50% { transform: translateY(-3px); } }
    @keyframes wait { 50% { transform: translateX(2px); } }
    .inspector { display: flex; flex-direction: column; min-height: 670px; }
    .panel-head { padding: 18px; border-bottom: 2px solid var(--ink); }
    .panel-head h2 { margin: 2px 0 4px; font-size: 24px; letter-spacing: -.025em; }
    .panel-head p { margin: 0; color: var(--muted); }
    .tabs { display: flex; border-bottom: 1px solid var(--line); }
    .tabs button { flex: 1; min-height: 44px; border: 0; border-right: 1px solid var(--line); background: var(--paper-2); cursor: pointer; font-weight: 700; }
    .tabs button[aria-selected="true"] { background: var(--signal); }
    .tabs button:focus-visible { outline: 3px solid #0c6bea; outline-offset: -3px; }
    .panel-body { padding: 18px; overflow: auto; }
    .kicker { color: var(--muted); font: 700 11px/1.2 ui-monospace, monospace; text-transform: uppercase; letter-spacing: .08em; }
    .metric-row { display: grid; grid-template-columns: repeat(3,1fr); border: 1px solid var(--line); margin: 14px 0; }
    .metric { padding: 10px; border-right: 1px solid var(--line); }
    .metric:last-child { border-right: 0; }
    .metric b { display: block; font-size: 20px; }
    .metric span { color: var(--muted); font-size: 11px; }
    .finding { width: 100%; margin: 0 0 9px; padding: 11px; text-align: left; background: #fffaf0; border: 1px solid var(--ink); cursor: pointer; }
    .finding:hover { background: #fff1b8; }
    .finding strong { display: block; }
    .finding span { color: var(--muted); font-size: 12px; }
    .severity { display: inline-block; margin-right: 6px; font: 700 10px/1.4 ui-monospace, monospace; text-transform: uppercase; }
    .empty { padding: 18px; border: 1px dashed var(--line); color: var(--muted); }
    .detail { margin-top: 14px; padding: 13px; background: var(--paper-2); border-left: 5px solid var(--signal); }
    .detail h3 { margin: 0 0 7px; font-size: 16px; }
    .detail p { margin: 7px 0; }
    code { font-family: ui-monospace, monospace; font-size: .9em; }
    @media (max-width: 880px) {
      header { grid-template-columns: 1fr; }
      .meta { text-align: left; }
      .layout { grid-template-columns: 1fr; }
      .room { min-height: 600px; }
      .inspector { min-height: 520px; }
    }
    @media (max-width: 520px) {
      header { padding: 18px; }
      .layout { padding: 8px; }
      .room { min-height: 520px; }
      .station { width: 124px; min-height: 74px; }
      .station span { display: none; }
      .room-title { max-width: 82%; }
      .agent { width: 84px; }
      .s-flow { left: 34%; }
    }
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation: none !important; scroll-behavior: auto !important; }
    }
  </style>
</head>
<body>
  <div class="shell">
    <header>
      <div>
        <p class="eyebrow">HCI Agent Test Lab · simulated rehearsal</p>
        <h1 id="mission"></h1>
      </div>
      <div class="meta" id="run-meta"></div>
    </header>
    <main class="layout">
      <section class="room" aria-label="Living test room">
        <div class="room-title"><strong>Living test room</strong><span>Select a character to inspect its bounded task and trace.</span></div>
        <div class="path path-a" aria-hidden="true"></div><div class="path path-b" aria-hidden="true"></div>
        <div class="station s-orientation"><b>Orientation table</b><span>What is this place and what happens next?</span></div>
        <div class="station s-flow"><b>Flow lane</b><span>Can the mission be completed safely?</span></div>
        <div class="station s-evidence"><b>Evidence desk</b><span>Why should the recommendation be trusted?</span></div>
        <div class="station s-recovery"><b>Recovery bench</b><span>Can a wrong turn be repaired?</span></div>
        <div id="agents"></div>
      </section>
      <aside class="inspector" aria-live="polite">
        <div class="panel-head"><span class="kicker" id="selected-kicker"></span><h2 id="selected-title"></h2><p id="selected-copy"></p></div>
        <div class="tabs" role="tablist">
          <button id="tab-agent" role="tab" aria-selected="true">Agent</button>
          <button id="tab-issues" role="tab" aria-selected="false">Issues</button>
          <button id="tab-boundary" role="tab" aria-selected="false">Boundary</button>
        </div>
        <div class="panel-body" id="panel-body"></div>
      </aside>
    </main>
  </div>
  <script>
    let DATA = __DATA__;
    let selectedAgent = DATA.agents[0] || null;
    let selectedTab = "agent";
    const $ = (id) => document.getElementById(id);
    const esc = (value) => String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll(String.fromCharCode(39), "&#39;");

    function renderHeader() {
      $("mission").textContent = DATA.manifest.mission;
      $("run-meta").innerHTML = `${esc(DATA.manifest.target.name)}<br>${esc(DATA.manifest.run_id)} · ${esc(DATA.aggregate.status)}`;
    }

    function renderAgents() {
      $("agents").innerHTML = DATA.agents.map(agent => `
        <button class="agent ${esc(agent.status)}" style="left:${agent.x}%;top:${agent.y}%;--coat:${esc(agent.character.color || "#555")};--accent:${esc(agent.character.accent || "#ddd")}" data-agent="${esc(agent.agent_id)}" aria-label="Inspect ${esc(agent.name)}, ${esc(agent.status)}">
          <span class="figure" aria-hidden="true"><span class="hair"></span><span class="head"></span><span class="body"></span><span class="leg leg-a"></span><span class="leg leg-b"></span><span class="status-dot"></span></span>
          <span class="agent-label">${esc(agent.name)}</span><small>${esc(agent.status)}</small>
        </button>`).join("");
      document.querySelectorAll("[data-agent]").forEach(button => button.addEventListener("click", () => {
        selectedAgent = DATA.agents.find(item => item.agent_id === button.dataset.agent);
        selectedTab = "agent";
        renderPanel();
      }));
    }

    function agentPanel(agent) {
      if (!agent) return `<div class="empty">No agents are configured.</div>`;
      const outcome = agent.task_outcome || {};
      const findings = agent.findings || [];
      return `
        <div class="metric-row">
          <div class="metric"><b>${esc(outcome.state || agent.status)}</b><span>task state</span></div>
          <div class="metric"><b>${esc(outcome.actions_used ?? "—")}</b><span>actions</span></div>
          <div class="metric"><b>${findings.length}</b><span>findings</span></div>
        </div>
        <p><span class="kicker">Lens</span><br>${esc(agent.lens)}</p>
        <p><span class="kicker">Outcome</span><br>${esc(outcome.summary || "Waiting for a tester result.")}</p>
        <h3>Questions</h3>
        <ul>${(agent.questions || []).map(item => `<li>${esc(item)}</li>`).join("")}</ul>
        <h3>Open questions</h3>
        ${(agent.open_questions || []).length ? `<ul>${agent.open_questions.map(item => `<li>${esc(item)}</li>`).join("")}</ul>` : `<div class="empty">None recorded yet.</div>`}`;
    }

    function issuesPanel() {
      const issues = DATA.aggregate.issues || [];
      if (!issues.length) return `<div class="empty">No aggregated issues yet. Waiting results remain visible rather than invented.</div>`;
      return issues.map(issue => `
        <button class="finding" data-issue="${esc(issue.id)}"><span class="severity">${esc(issue.severity)} · ${esc(issue.id)}</span><strong>${esc(issue.title)}</strong><span>${issue.agent_ids.length}/${DATA.agents.length} profiles · ${esc(issue.claim_types.join(", "))}</span></button>`).join("") +
        `<div class="detail" id="issue-detail"><h3>Select an issue</h3><p>Open one finding to inspect its evidence and human boundary.</p></div>`;
    }

    function boundaryPanel() {
      const boundary = DATA.manifest.claim_boundary;
      return `<p><span class="kicker">Authority</span><br><strong>${esc(DATA.manifest.authority.mode)}</strong></p>
        <p>${esc(DATA.manifest.authority.allowed.join("; "))}</p>
        <h3>Never infer</h3><ul>${boundary.never_infer.map(item => `<li>${esc(item)}</li>`).join("")}</ul>
        <h3>Forbidden actions</h3><ul>${DATA.manifest.authority.forbidden.map(item => `<li>${esc(item)}</li>`).join("")}</ul>
        <div class="detail"><h3>Claim boundary</h3><p>The characters visualize simulated test configurations. Trust, preference, adoption, prevalence, and lived accessibility experience still require people.</p></div>`;
    }

    function renderPanel() {
      document.querySelectorAll("[role=tab]").forEach(button => button.setAttribute("aria-selected", String(button.id === `tab-${selectedTab}`)));
      $("selected-kicker").textContent = selectedTab === "agent" ? `${selectedAgent?.profile_id || "cohort"} · ${selectedAgent?.status || "empty"}` : `run ${DATA.manifest.run_id}`;
      $("selected-title").textContent = selectedTab === "agent" ? (selectedAgent?.name || "No agent") : selectedTab === "issues" ? "Aggregated findings" : "Evidence boundary";
      $("selected-copy").textContent = selectedTab === "agent" ? (selectedAgent?.lens || "") : selectedTab === "issues" ? "Convergence, disagreement, and evidence stay inspectable." : "What this rehearsal may and may not claim.";
      $("panel-body").innerHTML = selectedTab === "agent" ? agentPanel(selectedAgent) : selectedTab === "issues" ? issuesPanel() : boundaryPanel();
      document.querySelectorAll("[data-issue]").forEach(button => button.addEventListener("click", () => {
        const issue = DATA.aggregate.issues.find(item => item.id === button.dataset.issue);
        $("issue-detail").innerHTML = `<h3>${esc(issue.id)} · ${esc(issue.title)}</h3><p>${esc(issue.observation)}</p><p><strong>Impact:</strong> ${esc(issue.impact)}</p><p><strong>Evidence:</strong> <code>${esc(issue.evidence_refs.join(", ") || "missing")}</code></p><p><strong>Human required:</strong> ${issue.human_required ? "yes" : "no"}</p>`;
      }));
    }
    ["agent","issues","boundary"].forEach(tab => $(`tab-${tab}`).addEventListener("click", () => { selectedTab = tab; renderPanel(); }));
    function renderAll() {
      renderHeader();
      renderAgents();
      renderPanel();
    }
    async function refreshLive() {
      try {
        const response = await fetch("/api/state", {cache: "no-store"});
        if (!response.ok || !response.headers.get("content-type")?.includes("application/json")) return;
        const selectedId = selectedAgent?.agent_id;
        DATA = await response.json();
        selectedAgent = DATA.agents.find(agent => agent.agent_id === selectedId) || DATA.agents[0] || null;
        renderAll();
      } catch (_) {
        // A self-contained file remains fully usable without the optional live server.
      }
    }
    renderAll();
    if (location.protocol === "http:" || location.protocol === "https:") {
      setInterval(refreshLive, 2000);
    }
  </script>
</body>
</html>
"""
    page = page.replace("__DATA__", safe_json(payload))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(page, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
