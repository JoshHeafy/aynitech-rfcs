- Feature Name: `graphify_usage_standard`
- Start Date: 2026-11-06
- RFC PR: https://github.com/JoshHeafy/aynitech-rfcs/pull/4
- Status: draft
- Origin: Observed usage in two local engineering workspaces (one single-repo project, one folder that holds several repos), graphify `0.9.38`, on 2026-11-06

# Summary

Define one shared way for Aynitech repositories to build, store, refresh and query their graphify knowledge graph, and one canonical agent instruction block that goes with it. Today teams use graphify with different rules, different hooks and no shared documentation.

# Motivation

Current state, measured on 2026-11-06 in two local workspaces:

| | Workspace A (single git repo) | Workspace B (folder with several repos, not a git repo itself) |
| --- | --- | --- |
| Version control | Git repo. `graphify-out/` is ignored in `.gitignore`. | Not a git repo. `graphify-out/` exists only on disk. |
| Latest graph | 4,024 files · 42,554 nodes · 95,118 edges · 1,777 communities | 3,625 files · 44,589 nodes · 97,009 edges · 1,934 communities |
| Snapshots kept | 6 dated folders (2026-10-13 → 2026-10-28), 454 MB | 30 dated folders (2026-08-11 → 2026-10-29), **1.5 GB** |
| Agent rules | None in `CLAUDE.md`, `AGENTS.md` or `.claude/` | `CLAUDE.md` and `AGENTS.md` have a `## graphify` section: query first, `graphify update .` after code changes |
| Hooks | No graphify hooks. Git `post-commit` and `post-checkout` are not installed. `core.hooksPath` is not set, so the repo's `.githooks/` is inactive on this clone. | `PreToolUse` hooks run `graphify hook-guard search` (Bash, Grep) and `graphify hook-guard read` (Read, Glob). An opencode plugin adds a reminder. |
| Freshness | `GRAPH_REPORT.md` was built from a commit 216 commits behind HEAD. | Not checked. |
| Ignore file | None | `.graphifyignore` with `*.sql`, `**/*.so`, `**/bin/` and the sibling repo's `graphify-out/` |

The global `~/.claude/CLAUDE.md` only contains the `/graphify` trigger. The query-first rule exists only in Workspace B, so projects that do not have it get no guidance.

Problems this causes:

- **Stale graphs.** Nothing refreshes the graph of Workspace A after commits, so agents that trust it answer from code that no longer exists.
- **No retention.** Dated snapshot folders accumulate. Workspace B holds 30 of them, 1.5 GB in total, and no written rule removes old ones.
- **Divergent rules.** Only Workspace B tells agents to query the graph first. An agent in Workspace A reads raw files unless someone reminds it.
- **Enforcement in one place.** The `hook-guard` hooks exist only in Workspace B, and their behavior is not documented in `graphify --help`.
- **No sharing.** Graphs are local, so every machine builds its own and no one can check how another one was built.

If we do nothing, each team keeps its own rules, snapshots keep growing, and agents keep working from stale or missing graphs without anyone noticing.

# Guide-level explanation

Day-to-day use, as one of the two workspaces already does it and as this RFC proposes to standardize it:

1. **Build once.** Run `/graphify <path>` in the repo root. Use `--no-viz` if only JSON and the report are needed.
2. **Ask the graph first.** For codebase questions:
   ```bash
   graphify query "how does authentication work?"
   graphify path "AuthService" "UserRepository"
   graphify explain "PaymentProcessor"
   ```
   Read `graphify-out/GRAPH_REPORT.md` only for broad architecture or when these commands do not give enough context.
3. **Refresh after code changes.** Run `graphify update .`. Per the rules in Workspace B, it re-extracts code only (AST, no LLM cost). Where the git hook is installed, see Reference-level §3.
4. **Check freshness.** Compare the `Built from commit` line in `GRAPH_REPORT.md` with `git rev-parse HEAD`. If they differ, the graph is stale for that change.
5. **Agents.** The repo's `CLAUDE.md` / `AGENTS.md` contains the canonical block (see Reference-level). Agents follow it without extra prompting.

# Reference-level explanation

## 1. Layout

- `graphify-out/` is ignored in every repo that uses graphify.
- Keep the current top-level artifacts (`graph.json`, `GRAPH_REPORT.md`, `manifest.json`, `.graphify_labels.json`, `cache/`) and the **last 3** dated snapshot folders. Delete older ones. The number 3 is a proposal; see Unresolved questions.
- Every repo's `.graphifyignore` must exclude its own `graphify-out/`, so the graph does not index itself. Baseline entries: `graphify-out/`, `*.sql`, `**/bin/`, `**/*.so`. Add repo-specific entries when needed.

## 2. Agent instructions

- One canonical block, identical in every repo, placed in `CLAUDE.md` (Claude Code) and `AGENTS.md` (other agents). The text of Workspace B's `## graphify` section is the candidate. `graphify claude install` and `graphify codex install` write a similar section, so teams can start from the tool's text, but must use the same final text everywhere.
- The block contains only: where the graph is, query-first rules, when to read `GRAPH_REPORT.md`, and the `graphify update .` rule. No per-project copy.
- Workspace B's `.claude/CLAUDE.md` points to `.claude/skills/graphify/SKILL.md`, which does not exist in that folder. The skill is installed globally in `~/.claude/skills/graphify/`. The reference should be corrected or removed when the standard is adopted.

## 3. Freshness

- **Default:** `graphify hook install` (`post-commit`, `post-checkout`) in repos where the team accepts git hooks, so the graph is refreshed on commit and checkout without a manual step. The exact command the hooks run is not verified here and must be checked before adoption.
- **Fallback:** if a repo does not install hooks, the agent block requires `graphify update .` after code changes.
- **Staleness check:** compare `Built from commit` in `GRAPH_REPORT.md` with `HEAD`. `graphify check-update <path>` reports pending re-extraction and is safe to run from cron.
- Repos that already have their own hook installer keep using it. This RFC does not change how those hooks are set up.

## 4. Enforcement hooks (optional)

`graphify claude install` adds a `PreToolUse` hook. Workspace B uses `graphify hook-guard search` on Bash and Grep, and `graphify hook-guard read` on Read and Glob. The behavior of `hook-guard` is not documented in `graphify --help`, and this RFC did not verify it. **Do not make the hooks mandatory** until someone reads the implementation or tests it in a sandbox. Once verified, the guild decides whether to adopt them.

## 5. Sharing and CI

- Graphs are per machine, and nothing is shared today.
- Options for CI: `graphify extract <path>` runs headless extraction for scripts. Its semantic pass needs an LLM backend key. The AST-only `graphify update .` does not.
- Graphs contain identifiers, file paths and community labels from the code. Treat them as internal artifacts: do not publish them outside the org.

## 6. Migration

- **Single-repo projects (like Workspace A):** add the canonical block to `CLAUDE.md` and `AGENTS.md`; add `graphify-out/` to `.graphifyignore`; decide on git hooks; delete snapshots older than the last 3.
- **Folders that hold several repos (like Workspace B):** delete snapshots older than the last 3 (the size saved is not measured here); fix the `.claude/skills/graphify` reference; keep the `.graphifyignore` entries.
- **Other repos:** a search of the local dev folder (depth 4) found no other `graphify-out/`, so no migration is needed yet beyond these two. Teams that use graphify elsewhere should add themselves to the rollout.

# Drawbacks

- Another set of rules for every repo to keep in sync, even with one canonical block.
- The graph is AST-only by default. Relations inferred from docs or semantics need an LLM run, and this RFC does not add one.
- Hooks add work to every Read, Grep and Bash call. The cost is not measured here.
- Pruning snapshots removes history that someone may want to compare. The retention rule must be explicit.

# Alternatives

- **Status quo.** Each team keeps its own rules. This is what produces the drift listed in Motivation.
- **Global graph.** `graphify global add <graph.json>` merges project graphs into `~/.graphify/global-graph.json`, so one query can span repos. It is local, so it does not solve sharing, and this RFC did not test it.
- **Shared graph service.** Out of scope for this RFC.

# Unresolved questions

- **Retention:** is "last 3 snapshots" the right rule, or should it be time-based?
- **Global rule:** should the query-first block also go into `~/.claude/CLAUDE.md`, so every project gets it, or stay per repo?
- **Git hooks:** should `post-commit` / `post-checkout` hooks be the default in every repo, given that some repos already run their own hook setup?
- **Hook-guard:** what does `graphify hook-guard` do exactly, and should it be enforced?
- **Ownership:** who maintains the canonical block (the Technical Guild, or a designated team)?
- **Out of scope:** LLM semantic extraction policy, Neo4j/FalkorDB export, Obsidian and wiki outputs, and the global cross-repo graph.
