# RFC Process

This document formalizes the process agreed in the "Technical Guild (R&D)" proposal.

## 1. Before writing

Check the RFC Index in [`README.md`](./README.md) and open PRs to avoid duplicating an in-progress discussion. If a similar topic exists, comment there instead.

## 2. Draft

- Copy `rfcs/0000-template.md` → `rfcs/0000-short-descriptive-name.md`.
- Keep the filename in `kebab-case`, in English.
- The number stays `0000` until merge — **do not** self-assign a number.

## 3. Open a Pull Request

- PR title: `RFC: <short title>`.
- The PR description should link to (or embed) the motivation summary.
- Tag the Guild Leads (`@Ausubel`, `@Joshar`) as reviewers.

## 4. Discussion window — 5 business days

- Discussion happens asynchronously in the PR comments (or a linked GitHub Issue if the thread gets long).
- Anyone in R&D can comment, propose alternatives, or raise concerns.
- The 5-business-day clock starts when the PR is opened, not when it's first reviewed.
- Guild Leads may extend the window once if the discussion is still active and productive.

## 5. Resolution

At the end of the window, Guild Leads:

- **Consolidate consensus** if one emerged, or
- **Make the final call** if no consensus was reached, documenting the reasoning in the PR before merging/closing.

Outcomes:

- **Accepted** → PR is merged, RFC gets the next sequential number, status set to `accepted`, index updated.
- **Rejected** → PR is closed (not merged), reasoning left in the PR thread for future reference.
- **Needs an ADR** → if the accepted RFC implies a concrete architecture decision, open a companion ADR in `/adr` referencing the RFC.

## 6. Numbering

- Numbers are sequential and assigned **only at merge time**, based on the highest existing number in `/rfcs`.
- Never reuse a number, even for a rejected RFC.

## 7. Changing an accepted RFC

Accepted RFCs are not edited in place. To change or replace one:

1. Open a new RFC.
2. Reference the old one and mark it as superseding it.
3. Once the new one is accepted, update the old RFC's status to `superseded` and link to the new one.
