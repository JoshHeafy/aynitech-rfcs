- Feature Name: `adr_governance`
- Start Date: 2026-10-07
- RFC PR: (leave empty, filled in once the PR is opened)
- Status: active (in discussion)
- Origin: Kriptex platform `CLAUDE.md` §"Architecture decisions require an ADR" and §"Sources of truth" (internal); Kriptex gitops `docs/adr/README.md` and `CLAUDE.md` (internal); Kriptex platform and gitops `ADR-000-template.md` (internal)

# Summary

Define one set of rules for every Aynitech project, for when an Architecture Decision Record (ADR) is required, who may accept it, how it is numbered, how it changes over time, where it lives (product repo vs. this guild repo), and which document wins when an ADR, a product spec and an issue disagree. The RFC also proposes a single ADR template, in English and Spanish.

# Motivation

Kriptex already runs ADRs in two repos (application platform and GitOps infrastructure) and has learned a few lessons the hard way:

- **Number collisions.** Two parallel branches each computed "the next number" and collided at merge. One ADR had to be renumbered after a merge from `dev`.
- **Unrecorded decisions cited as binding.** A data-ownership decision circulated with a citation to an ADR that never mentioned it. The decision was real but recorded nowhere, and the bad citation spread into a glossary and an issue before anyone checked.
- **Spec vs. architecture drift.** A product spec arrived fixing a formula that contradicted an Accepted ADR. Slicing that spec into issues would have reversed the decision silently.
- **Decisions in comments.** Infra decisions lived as long YAML header comments. A comment cannot record the rejected options, who accepted the decision, or when it was superseded, and nobody can find it without knowing which file to open.
- **AI agents.** Both teams use coding agents. An agent that hits an architectural fork will pick one option and keep going unless it is told to stop.

Most other Aynitech projects — AyniFX, and the projects in flight under SDF — have no formal ADR practice yet (to be confirmed with SDF). If we do nothing, each team keeps (or invents) its own rules, ADRs stop being comparable across the guild, and cross-team decisions (shared auth, API contracts consumed by the Flutter app) have no home. The cost of doing nothing is the same one Kriptex already paid: decisions cited as binding with no record, specs that silently reverse architecture, and agents choosing forks on their own.

# Guide-level explanation

## When you need an ADR

Write an ADR for anything **expensive to reverse**. The minimum list:

| Area | Examples |
| --- | --- |
| Datastores and messaging | choosing PostgreSQL vs. a document store, adding a queue or event bus |
| Backup, retention and DR | backup target, retention window, restore rehearsal policy |
| Environment promotion | how a change goes from dev to staging to prod, what syncs automatically |
| Cluster-wide components | a secrets manager, ingress controller, object storage, service mesh |
| Alerting contract | what an alert measures, its threshold semantics, who gets paged |
| API and event contracts | payload shape, versioning, breaking-change policy, shared vocabularies |
| Authentication and authorization | MFA policy, token lifetimes, how services trust identity |
| Boundaries and layering | which service owns which data, changes to the DDD layering rules |
| New framework or major dependency | a BDD runner, a state-management library for Flutter, an ORM |

If you are not sure, write the ADR. A short ADR is cheap; an unrecorded decision is not.

## Who decides

- **A human accepts an ADR.** Anyone, human or agent, may draft one.
- **AI agents never self-accept.** When an agent reaches a decision it would need to make to continue, it **stops**, presents the concrete options with pros and cons, and waits. After a human decides, the agent records the decision and follows it.
- The `Deciders` field always names people, never a tool.
- **Acceptance is auditable.** The `Proposed` → `Accepted` change is made (or explicitly approved) by the person named in `Deciders`, in the ADR's PR. An ADR whose status flips without that person acting is not accepted, no matter what the line says.

## Changing a decision

An Accepted ADR is **binding** on code, agents and reviews. To change it, write a **new** ADR that supersedes the old one and update the old one's status line to `Superseded by ADR-NNN`. Never rewrite the decision of an Accepted ADR in place. Typos and broken links may be fixed in place.

Exception: an ADR that has **not yet merged** to its project's integration branch can still be amended in its PR. The integration branch is `main` in this guild repo and each product repo's own integration branch (e.g. `dev` in Kriptex).

## Numbering

Numbering differs by location, and both rules are directory-based — never trust a remembered "next number".

**In `docs/adr/` of each product repo:** files are `ADR-NNN-<slug>.md` with three digits, computed from the directory:

```bash
ls docs/adr/ADR-*.md | sed -E 's@.*/ADR-0*([0-9]+).*@\1@' | sort -n | tail -1
```

Then add one, zero-padded to three digits. **Before committing, check the open PRs** for ADRs that already reserved that number. If two branches still collide, the one that merges second renumbers.

**In `adr/` of this guild repo:** numbering follows [`adr/README.md`](../adr/README.md) — four digits (`00XX-<slug>.md`), assigned at merge time (the file keeps `0000` until then).

Always cite an ADR by its full slug (`ADR-012-bdd-tooling`), never the bare number, and always say which repo it belongs to when citing across repos (numbers are per repo).

## Where an ADR lives

- **Product repo** (`docs/adr/` in the service repo or the infra repo): the decision affects one team's system. This is the default.
- **Guild repo** (`adr/` in `aynitech-rfcs`): the decision binds **more than one team or project**, e.g. a shared auth provider, a cross-team API contract, a common CI policy. Usually an Accepted RFC in this repo produces a guild ADR.

A product ADR may reference a guild ADR; a guild ADR should not depend on a product ADR that the other team cannot read. Describe the referenced decision in plain text instead.

## Sources of truth

Three systems hold binding content, split by the kind of claim each can settle:

| System | Owns |
| --- | --- |
| Product spec (each project's spec tool: Notion, ACTIVITIES, …) | what the thing does: invariants, edge cases, worked examples |
| ADRs in the repo | architecture and boundaries: ownership, contracts, cross-cutting patterns |
| Issue tracker (each project's tracker: Linear, ACTIVITIES, …) | acceptance criteria and issue status |

**When a product spec contradicts an Accepted ADR, the Accepted ADR stays in force until a human resolves the conflict**, by revising the spec or by accepting a superseding ADR. The ADR does not silently apply itself: whoever is slicing the spec into issues, code or `.feature` files **stops and surfaces the conflict**, and a human decides how it is resolved. Corollaries:

- A spec names the ADRs that constrain it near the top.
- A decision cited as binding must exist as an ADR, and the citation must point at the record that decides it.
- Product owns invariants; engineering owns mechanics (weights, rounding, payload shape).

# Reference-level explanation

## Proposed ADR template

This replaces the current `adr/0000-template.md` once this RFC is accepted. It ships in two files with identical structure, fields and rules: [`adr/0000-template.md`](../adr/0000-template.md) in English and [`adr/0000-template.es.md`](../adr/0000-template.es.md) in Spanish, side by side in `adr/`. English is the template for Kriptex and any English-writing project; Spanish is the template for every other project. The template merges the Kriptex platform and gitops variants; `Blast radius` ("Radio de impacto" in the Spanish version) comes from the infra variant and is optional elsewhere. On acceptance, Kriptex's `docs/adr/ADR-000-template.md` (platform and gitops) is updated to match this template, so its 170+ existing ADRs and the new ones read the same.

```markdown
# ADR-NNN: <short decision title>

- **Status:** Proposed | Accepted | Superseded by ADR-NNN-<slug> | Deprecated
- **Date:** YYYY-MM-DD (date of the last status change)
- **Deciders:** <human name(s)>   <!-- a human accepts; an agent never self-accepts -->
- **Supersedes:** <ADR-NNN-<slug>, or "none">
- **Related:** <RFC, issue key, other ADRs (with repo if cross-repo)>

## Context
What forces the decision? The problem, the constraints, and why it can't be deferred.
Link the evidence (incident, benchmark, failing pipeline) in plain text.

## Options considered

### Option A — <name>
- Pros:
- Cons:

### Option B — <name>
- Pros:
- Cons:

### Option C — Do nothing / defer
- Pros:
- Cons:

## Decision
The chosen option and why. Filled in once a human decides.

## Consequences

### Positive
- What becomes easier.

### Negative
- What becomes harder or constrained; risks and how they are mitigated.
- Follow-up work and migrations (with issue keys).

### Blast radius (optional; required for infra ADRs)
Environments, services, charts or apps touched, and what happens on rollback.

## Compliance
Once **Accepted**, this decision is binding. Code, agents and reviews must respect it.
Changing it requires a new ADR that supersedes this one, never an in-place reversal.
How compliance is checked (test, lint rule, CI gate, review checklist), if anything.
```

## Status lifecycle

```
Proposed ──(human accepts)──▶ Accepted ──(new ADR)──▶ Superseded by ADR-NNN
    │                            │
    └──(rejected: close PR)      └──(no longer relevant, no replacement)──▶ Deprecated
```

- `Proposed`: open PR, under discussion. Agents may write this status.
- `Accepted`: set by a human, in the PR that merges it or a follow-up.
- `Superseded by …`: set when the replacing ADR is accepted. Partial supersession is allowed and must say which part ("storage part superseded by ADR-NNN-…").
- `Deprecated`: the decision no longer applies and nothing replaces it. A human sets this status, and the reason must be written down — a short ADR ("ADR-NNN retires ADR-NNN without replacement, because X") records the why in the same place a supersession does. A decision that stops applying without a record is just an unrecorded decision again.

## Index

Every project that adopts this format keeps a `docs/adr/README.md` with an index table (ADR, title, status, date) and a short "decisions that still need an ADR" list so pending decisions are not lost. This is what `docs/adr/README.md` already does in Kriptex, and it is a requirement for adoption, not a suggestion.

## Enforcement

Today this is soft enforcement: instructions in `CLAUDE.md` / `AGENTS.md` for agents, and reviewer judgment for humans. A CI check could later verify that (a) new ADR numbers are unique against the base branch, and (b) a PR changing an `Accepted` ADR's Decision section also adds a superseding ADR.

## Migration

- Existing ADRs stay as they are; no renumbering.
- New ADRs use the new template from the date this RFC is accepted.
- Adoption by group:
  - **R&D teams (Kriptex and AyniFX):** from acceptance. Each project creates `docs/adr/` with an index and the template in its repos, in the template language that applies (English for Kriptex, Spanish elsewhere).
  - **Technical contracts reviewed by the guild:** from now, starting with ISC v4.
  - **SDF projects in flight:** in the methodology sessions.

# Drawbacks

- More ceremony for small decisions; the "if unsure, write it" rule will produce some trivial ADRs.
- Superseding instead of editing grows the directory and requires readers to follow chains.
- Checking open PRs for numbers is manual until a CI check exists.
- Two locations (product repo vs. guild repo) need judgment about where a decision belongs.

# Alternatives

- **Free-form decisions in issues or wiki pages.** Easy, but not versioned with the code, not reviewable in a PR, and invisible to agents working in the repo.
- **Date-based or random IDs** (`ADR-2026-10-07-slug`) to avoid collisions. Removes collisions entirely but breaks with existing Kriptex numbering and is harder to cite in conversation. Could be revisited if collisions persist.
- **Allow in-place edits with a changelog section.** Simpler directory, but the history of *why* a decision changed gets buried and old citations silently change meaning.
- **Do nothing.** Each team keeps its own rules; cross-team decisions have no home.

# Unresolved questions

- Do we want the CI uniqueness/supersession check now, or after a few months of manual practice?
- Language of ADRs: Kriptex writes in English, every other project in Spanish, with the same fields and rules; this is settled. Open: the language of **guild** ADRs, which cross projects — Spanish, as the common language of all teams?
- **Flutter / AyniFX gaps:** AyniFX has no ADR directory yet. Which repo holds decisions that span the Go backend and the Flutter app (e.g. state management, offline sync, API versioning for app store releases that can't be force-updated)? A mobile release cycle makes "expensive to reverse" broader than on the web.
- Out of scope: RFC process itself (see `rfcs/0000-template.md` and the repo README).
