---
name: autonomous-site-rebuilder
description: Run, diagnose, or extend the autonomous Python workflow that crawls a website through ScrapeGraphAI, builds a local multi-page mock, audits every route and visible child link with agent-browser, recrawls missing content, and repairs the result with Codex CLI. Use for autonomous site reconstruction, missing-image or missing-page repair, dashboard progress, and workflow architecture changes in the interpret project.
---

# Autonomous Site Rebuilder

Operate from the project root and keep the process autonomous and resumable.

1. Read `README.md`, `.env.example`, and existing workflow state before changing or running the pipeline.
2. Keep `scripts/agentic_workflow.py` limited to orchestration and state transitions.
3. Put one responsibility per file under `scripts/agents/`. Put ScrapeGraphAI transport and crawl logic under `scripts/scraping/`.
4. Preserve enums, the maximum-step guard, targeted recrawls, browser checks for every route and visible child link, the live dashboard, and persistent logging.
5. Use real downloaded image assets. Never use screenshots as editorial images.
6. Read `SGAI_API_KEY` only from the environment. Never store or print secrets.
7. Run `python3 -m compileall scripts site` and focused smoke tests after edits. Start paid crawls only when the user explicitly requests execution.
8. After a run, report the dashboard URL, state path, log path, latest audit report, and terminal status.
