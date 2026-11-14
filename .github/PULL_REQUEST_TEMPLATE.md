## Summary

<!-- What changed, and why. -->

## Checklist

- [ ] `pnpm build`, `pnpm lint`, `pnpm typecheck`, and `pnpm test` pass locally
- [ ] `pnpm generate:agent` is a no-op (`git diff --exit-code` after it)
- [ ] Storybook covers new or restyled UI
- [ ] Changeset added if `@chamuka/tokens`, `@chamuka/ui`, or `@chamuka/icons` should bump
- [ ] Public component props stay Chamuka-shaped (no leaked UI SDK types)
- [ ] Copy follows `brand/docs/voice.md` (“From thoughts to form” is DrawIt only)
