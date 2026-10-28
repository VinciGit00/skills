---
name: restart-p2p-dashboard
description: Restart and verify the GrabCAD P2P coordinator dashboard when the user asks to restart it or apply dashboard changes that require a service restart. Automatically complete the restart and readiness checks within the authorized task; do not restart scraper workers.
---

# Restart the P2P dashboard

The dashboard is served by the P2P coordinator, which owns the only authoritative
SQLite database. Restart its existing service on the configured host; never
start a replacement coordinator from a worker checkout.

## Locate the running deployment

- Start from the current GrabCAD checkout, normally
  `/Users/marcovinciguerra/github/grabcad`. Read its `p2p_scraping/config.json`
  privately for `coordinator_url` and node inventory. Do not print API tokens.
- Resolve the coordinator host using the configured endpoint and available SSH
  aliases. Inspect the target service and absolute repository path rather than
  assuming the current Mac is the coordinator. A local `worker_bootstrap` or
  `retired_coordinator` configuration must not be used to start a coordinator.
- Use passwordless SSH with `BatchMode=yes` and a bounded connection timeout.
  If Tailscale is unavailable, use an existing verified LAN alias if present;
  do not change network routes, tokens, or endpoint configuration to restart.
- On macOS, inspect the matching LaunchAgent's label and ProgramArguments.
  The existing deployment has used `com.interpretai.cad-p2p-coordinator`, but
  confirm its command targets `p2p_scraping/coordinator.py` and the authoritative
  configuration. On Linux, inspect the existing systemd unit. For a container,
  identify and restart only the already configured coordinator service.

## Apply and restart

A user's restart request already authorizes the service restart; do not ask
again. When applying authorized dashboard changes, restart automatically if
Python server/config-renderer changes require it. HTML and YAML are normally
read on each request, so a reload is sufficient unless a restart was requested.

Before restarting after changes, compile changed Python modules and render the
page with the **active** presentation configuration. The deployment may use
`.grabcad/p2p/dashboard-imports/presentation.yaml` instead of the tracked
`dashboard/config.yaml`. Keep imported presentation files compatible with new
labels; preserve their custom values. Do not overwrite unrelated remote edits.

For a verified macOS user LaunchAgent, run on that host:

```bash
launchctl kickstart -k "gui/$(id -u)/<verified-coordinator-label>"
```

Do not kill processes by broad patterns, restart worker services, clear
cooldowns, replace credentials, modify the authoritative database, or start
another coordinator. A dashboard restart does not change scraper accounts.

## Verify recovery

- Poll for up to 90 seconds with short waits, allowing startup time. Require
  successful JSON from `/api/status?source=<configured-source>` and HTTP 200
  with the actual dashboard markup from `/network?source=<configured-source>`.
  Confirm the response is not a dashboard configuration error page.
- Verify locally on the coordinator and through the user's reachable endpoint.
  A successful SSH command or listening port alone does not prove readiness.
- For UI changes, open the dashboard, confirm the changed content in the browser,
  and inspect a screenshot at the relevant section. Check advancing worker
  heartbeats without treating a cooldown as a dead worker.
- If the one restart fails, inspect its service status and configured stderr
  log, redact secrets, and diagnose before trying again. Do not loop restarts.
  Repair an identified issue within the authorized change or report the exact
  blocker. Preserve workers and runtime data throughout.

Report the dashboard URL, whether restart and HTTP/UI checks succeeded, and any
remaining issue. Keep the distinction between coordinator health and actual
scraper download progress explicit.

## Dynamic network and account cleanup

Build checks from the current configuration and live status response, not a
fixed host list. The dashboard shows workers with running/idle/ready/joining
status and heartbeats no older than 30 seconds. Offline hosts disappear and
return when their heartbeats resume; preserve historical manifest totals.
After restarting, compare two samples and check that each intended live worker
advances its heartbeat. Check the worker count requested by the user per device
and ensure shard totals exclude disabled historical definitions; synchronize
affected private inventories before an authorized worker restart. Do not claim an account exists merely because a random
email was generated: distinguish pending registration from verified login.

When the user also requests removing old saved accounts during a transition to
`create` mode, retire the old coordinator pool and the selected workers' legacy
credential/profile paths into a private runtime backup outside the active lookup
paths. Derive the selected workers and hosts from the user's scope and effective
configuration. Preserve generated-account files, registration-attempt state,
cooldowns, task directories, CAD downloads and the authoritative database.
Never retire accounts belonging to unrelated running deployments. A dashboard
restart by itself does not authorize account cleanup or worker restarts.
