# Domain Docs

This repository uses a single-context domain-documentation layout.

## Before exploring

Read the following when they exist:

- `CONTEXT.md` at the repository root
- ADRs under `docs/adr/`

If these files do not exist, proceed silently. The domain-modeling workflow creates them when terminology or durable decisions are resolved.

## File structure

```text
/
├── CONTEXT.md
├── docs/
│   └── adr/
└── src/
```

## Use the glossary vocabulary

When naming a domain concept in an issue, proposal, test, or implementation, use the term defined in `CONTEXT.md`.

Do not drift toward synonyms that the glossary explicitly rejects. If a required concept is absent, reconsider whether new terminology is actually needed or record the gap for domain modeling.

## Flag ADR conflicts

If proposed work contradicts an existing ADR, surface the conflict rather than silently overriding the decision.
