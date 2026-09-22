# AyniTech RFCs & ADRs

This repository is the home for **RFCs** (Requests for Comments) and **ADRs** (Architecture Decision Records) for the AyniTech R&D department, maintained by the [Technical Guild](https://github.com/aynitech).

## What goes where

| | RFC | ADR |
|---|---|---|
| Purpose | Propose and **discuss** a change (standard, tool, dependency, methodology) | **Record** an architecture decision that has already been made |
| State | Mutable while in discussion, frozen once accepted/rejected | Immutable once merged |
| Lives in | [`/rfcs`](./rfcs) | [`/adr`](./adr) |
| Process | See [`PROCESS.md`](./PROCESS.md) | See [`/adr/README.md`](./adr/README.md) |

If you're unsure which one applies: if it needs debate/consensus first → RFC. If a decision is already final and you just need to document *why* → ADR (an RFC can also result in an ADR once accepted).

## How to propose an RFC

1. Copy [`rfcs/0000-template.md`](./rfcs/0000-template.md) to a new file `rfcs/0000-my-feature-name.md` (leave the number as `0000` — it gets assigned on merge).
2. Fill it in following the template.
3. Open a Pull Request. This automatically opens the discussion window.
4. Discuss in the PR / linked GitHub Issue for **5 business days** (see [`PROCESS.md`](./PROCESS.md)).
5. Guild Leads consolidate consensus and merge (accepted) or close (rejected) the PR.
6. On merge, the RFC is assigned the next sequential number and added to the index below.

## RFC Index

| # | Title | Status | Owner |
|---|-------|--------|-------|
| — | *(no RFCs merged yet)* | — | — |

Status values: `draft` · `active` (in discussion) · `accepted` · `rejected` · `superseded`

## ADR Index

See [`/adr/README.md`](./adr/README.md) for the full list of architecture decisions.

## Herramientas

- [`tools/guild_post.py`](./tools/guild_post.py): CLI para armar un "Tech Share" (recurso técnico + TL;DR + por qué importa) listo para publicar en `#guild-engineering`, en modo interactivo o no interactivo (invocable desde un agente). No requiere dependencias externas. Ver [`tools/README.md`](./tools/README.md) para el formato del mensaje y ejemplos de uso.

## Guild Leads

- [@Ausubel](https://github.com/Ausubel)
- [@Joshar](https://github.com/Joshar)
