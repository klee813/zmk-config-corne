# Issue tracker: GitHub

Issues and specifications for this repository live as GitHub issues. Use the `gh` CLI for all operations.

Repository: `leungkcofficial/zmk-config-corne-default`

## Conventions

- Create: `gh issue create --title "..." --body "..."`
- Read: `gh issue view <number> --comments`
- List: `gh issue list --state open`
- Comment: `gh issue comment <number> --body "..."`
- Add a label: `gh issue edit <number> --add-label "..."`
- Remove a label: `gh issue edit <number> --remove-label "..."`
- Close: `gh issue close <number> --comment "..."`

Run commands inside this repository so `gh` can infer the repository from its Git remote.

## Pull requests as a triage surface

**PRs as a request surface: no.**

GitHub shares one numbering sequence across issues and pull requests. Resolve an ambiguous reference such as `#42` with `gh pr view 42`, falling back to `gh issue view 42`.

## Skill conventions

When a skill says “publish to the issue tracker,” create a GitHub issue.

When a skill says “fetch the relevant ticket,” run:

`gh issue view <number> --comments`
