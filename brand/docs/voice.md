# Voice

**Chamuka Labs is an applied AI lab: we ship AI-native products, put research into practice, and build tools for AI agents.**

Voice is founder-led, short, specific, slightly dry: a tinkerer speaking for the lab.

## Positioning (do not invent past this)

Use this one-liner verbatim when you need a sentence for the lab (docs, about copy, README). Do **not** put it under a lockup; templates still end on chamuka.ai with no slogan.

> Chamuka Labs is an applied AI lab: we ship AI-native products, put research into practice, and build tools for AI agents.

Social / profile bio, verbatim:

> Applied AI lab. We ship products, put research to work, and build tools for agents. Flagship: DrawIt, a canvas you and the model both edit.

What that means:

1. **Ship AI-native products and tools.** AI is in the artefact itself, not just a chat window.
2. **Put research into practice.** “Research” means applied engineering only. Do not claim papers, benchmarks, evaluation work, or research results.
3. **Build tools for AI agents.** Examples: DrawIt’s MCP server and CLI, Vmette, Conduit.

## Hierarchy

Lead with the lab, then name the outputs.

- **DrawIt** is the flagship.
- **FormIt, Play, Waypoint, Vmette** and others are experiments or infrastructure, not launched products.
- **Daybreak** is brand infrastructure, not a product.

## Visuals

- Lab / org surfaces: the master lockup.
- Flagship surfaces: Chamuka + DrawIt, ember `#E24E1B`.

## Do not claim

- Hype words (“groundbreaking”, “empowering creators worldwide”).
- Invented customers, logos, testimonials, or metrics (no “60fps”, no “90% faster”).
- That every experiment is a launched product.
- That other chamuka-inc repos or products are already open source. This repository being Apache 2.0 is fine to state.
- **“From thoughts to form”** anywhere but DrawIt. Never as a line for Chamuka Labs, Daybreak, FormIt, or org chrome.
- Other taglines for the lab or for Daybreak.

## Principles

1. **Plain first.** Say what the thing is in one sentence. The first line of a README should be able to replace the GitHub description without a rewrite.
2. **Short, specific, slightly dry.** No trailing exclamation marks, no emoji in org listings, no “best”, no marketing puff.
3. **Named, not nicknamed.** Surfaces say Chamuka Labs (org) or Chamuka + product name (DrawIt on flagship surfaces). Do not drop “Chamuka” from a product lockup.
4. **Placeholders until confirmed.** Do not invent social handles. `name@chamuka.ai` is a stand-in for a person’s address on business cards and email signatures. Conduct and security reports go to `security@chamuka.ai`.

## Repo names and descriptions

- Public name: Chamuka Labs. GitHub owner: `chamuka-inc`.
- User-facing products: `chamuka-<name>` in lowercase kebab-case (`chamuka-drawit`). No camelCase in the repo name.
- Shared libraries: `@chamuka/<package>` on the registry, `chamuka-<package>` on GitHub.
- Descriptions: one sentence, what it is, no trailing `!`, no emoji. Do not use DrawIt’s line on a lab or design-system repo.

Visual do / don’t examples: [`templates/github-repo-naming.svg`](../../templates/github-repo-naming.svg).

## UI copy

- Buttons are verbs: *Save*, *Send invite*, *Create form* — not *Submit* unless the legal meaning is submit.
- Empty states explain the next step, not the absence.
- Errors name the problem and a way forward. Do not blame the person.
- Loading copy is quiet (*Loading forms…*) — no jokes that stall a retry.
- Help text is optional and short. If it restates the label, delete it.

## Words we avoid in chrome

“Simply”, “just”, “awesome”, “unlock”, “magic”, “groundbreaking”, “empowering”. Prefer the concrete: *Draw together. Shape a form. Run a session.*
