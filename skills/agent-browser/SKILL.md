---
name: agent-browser
description: Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality.
---

# agent-browser

Use the installed `agent-browser` CLI for browser automation. Before the first command, load the matching runtime instructions with `agent-browser skills get core`; load a specialized CLI skill when the task needs one.

## Execution host

Prefer the user's Mac mini for browser and computer UI automation. From another machine, make one bounded availability check through the configured `macmini` SSH alias and use `/opt/homebrew/bin/agent-browser` there.

If the Mac mini cannot complete the task—including SSH failure, no usable graphical session, an unresponsive browser, or failed screen capture—fall back automatically to `cua_repl` against the current Mac's existing browser or native-app session. Inspect existing tabs first, do not export cookies or credentials, and report which host was used. Do not require a separate user confirmation merely to switch execution hosts; confirmations for consequential UI actions still apply normally.

For authenticated websites, reuse an existing authenticated browser session. Prefer Safari on the Mac mini. On the fallback host, use the browser or native-app session already available through `cua_repl`; never copy cookies or credentials between hosts.

Keep a task on one host after selecting it unless that host becomes unusable. A frontend running on another machine is not reachable through the selected host's `localhost`; use the project's existing remote exposure capability or an SSH tunnel.

## Workflow

Use accessibility snapshots and stable element references before coordinate actions. Re-read the current UI state after each interaction, verify the requested result visibly, and stop once the result is present. Preserve all normal confirmation requirements for uploads, messages, deletions, purchases, account changes, and other consequential actions.
