# PR Description Generator

You will review the Git diff between the **current branch (HEAD)** and **develop**, then generate a PR description using the template below.

## Instructions

- Base every section **only on the diff**. Do not invent functionality.
- Write like a senior engineer dropping a Slack message — short sentences, zero filler, no AI hedging.
- The reviewer should feel like he is reading a twitter feed not a paragraph or essay.
- Each section should be skimmable in seconds: one sharp sentence beats three vague ones.
- Sound like a human who knows the codebase, not a model summarizing a diff.
- No corporate fluff ("leverages", "facilitates", "ensures"), no passive voice, no throat-clearing.
- Group related changes instead of listing every modified line.
- Mention implementation details only if they help reviewers understand the _why_, not the _what_.
- If a section is not applicable, state `None`.
- Output **only Markdown** matching the template below.
- Do **not** wrap the output in code fences.
- Leave the **Pre-review checklist** exactly as shown with all checkboxes unchecked.
- Also focus on no-goal so that it ensures the reviewer doesnot go out of scope.
- You can access linear ticket for further details if you wish to know the context, usually the branch name has the ticket number like arindam/ae-1234-your-fixes
- The **Summary & Changes** section must be 280 characters or fewer — if it doesn't fit in a tweet, trim it.

---

## Summary & Changes

<Briefly explain the problem solved, why it mattered, and the overall implementation approach in 2–5 sentences.>

<details>
<summary><h2>Screenshots</h2></summary>
<!-- Add screenshots or screen recordings here -->
### Stubs
<!-- Add screenshots of stubbed UI components here, labelled by stub name -->
</details>

<details>
<summary><h2>Scope</h2></summary>

[Generate a file tree of every file touched, with a short `←` annotation per file explaining what changed. Group by directory.]

</details>

[One sentence summarising which layers were touched (e.g. API layer, component tree, state, utils).]

## Handled

- <Implemented change #1>
- <Implemented change #2>
- <Implemented change #3>
- <Implemented change #4>

## Non-goals

- Does not <excluded change #1>
- Does not <excluded change #2>
- Does not <excluded change #3>

## Testing

- Manual validation: <scenario #1>
- Manual validation: <scenario #2>
- Manual validation: <scenario #3>

## Pre-review checklist

- [ ] Extracted constants for repeated strings
- [ ] Ensured naming consistency with existing file patterns
- [ ] Ran linter/formatter
- [ ] Removed debug code
- [ ] Reviewed full diff for style consistency
- [ ] Kept behind a feature flag if it is a feature change
- [ ] Added links (Linear/GitHub code references) if applicable — <ticket/link>

**Important:** Give output in markdown format.
