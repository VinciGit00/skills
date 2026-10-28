---
name: minimal-modular-structure
description: Design or refactor a codebase into the smallest coherent modular structure. Use when the user asks to simplify folders, remove unnecessary files, separate real architectural boundaries, or make a project modular without overengineering.
---

# Minimal Modular Structure

Create the smallest structure that keeps responsibilities clear. Modularity is
measured by cohesion and replaceable boundaries, not by the number of files or
directories.

## Method

1. Inspect the current file tree, imports, entrypoints, tests, configuration and
   documentation before moving anything.
2. Identify the few real boundaries in the system, such as protocol/core,
   server, client/node, adapters and CLI. Create a directory only when it owns a
   distinct responsibility with more than a cosmetic naming benefit.
3. Keep entrypoints thin. Put executable entrypoints in one predictable place;
   do not mix coordinator/server code into worker/client modules.
4. Merge tiny modules when they are always changed and used together. Remove
   empty packages, duplicate wrappers, obsolete compatibility files, generated
   caches and unused setup material.
5. Preserve public behavior and user-owned changes. Before deleting a file,
   verify that no source, test, command, configuration or documentation refers
   to it.
6. Update imports, commands, examples and architecture documentation to match
   the resulting tree.
7. Validate syntax, imports, focused tests and repository diff hygiene. Report
   the final tree and any intentionally retained files whose purpose is not
   obvious.

## Decision rules

- Prefer one cohesive module over several one-class or one-dataclass modules.
- Prefer explicit dependency direction; avoid circular imports and generic
  `utils`, `helpers` or `common` dumping grounds.
- Keep adapters separate only when an implementation can realistically be
  replaced without rewriting the core workflow.
- Keep tests alongside the subsystem or in one test directory; do not mirror a
  deep source hierarchy unless the suite genuinely needs it.
- Do not retain files merely because they existed previously.
- Do not compress unrelated responsibilities into a monolith solely to reduce
  file count.

The target is a structure a new contributor can understand from the tree alone,
with every remaining file having a necessary and explainable role.
