# Architecture Decision Records (ADR)

ADRs document architecture decisions of high impact that have **already been made** — reserved for decisions, not open discussions (those go through the [RFC process](../PROCESS.md) first).

## Format

We use a lightweight [MADR](https://adr.github.io/madr/)-inspired format — see [`0000-template.md`](./0000-template.md) (English) and [`0000-template.es.md`](./0000-template.es.md) (Spanish). The two have identical structure, fields and rules; each project uses the language that applies (English for Kriptex, Spanish elsewhere).

## Rules

- **Immutable once merged.** Never edit the decision/content of a merged ADR.
- If a decision changes later, create a **new** ADR that supersedes the old one, and update the old one's status to `Superseded by ADR-00XX` (this status line is the only thing that may be edited after merge).
- Numbering is sequential across the whole `/adr` folder, assigned at merge time.
- Filename: `00XX-short-kebab-case-title.md`.

## How to propose one

1. Copy `0000-template.md` (English) or `0000-template.es.md` (Spanish) → `00XX-my-decision-title.md` (number `0000` until merge).
2. Open a PR tagging the Guild Leads.
3. If the decision originated from an accepted RFC, link it in the "Context" section.
4. Once merged, add it to the index below.

## Index

| # | Title | Status | Date |
|---|-------|--------|------|
| — | *(no ADRs merged yet)* | — | — |

Status values: `Proposed` · `Accepted` · `Superseded by ADR-00XX` · `Deprecated`
