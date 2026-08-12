# veraidyn.github.io

The public Veraidyn website, served by GitHub Pages from the `main` branch.

**This repository is public. Everything committed here is world-readable, permanently, including anything later deleted.** Nothing about engagements, clients, strategy or the decision log belongs in it. Those live in the M365 tenant and in the private `veraidyn/veraidyn` repository.

---

## Status: scaffold, not launched

`index.html` is structure with **marked placeholders**. Every `class="todo"` block must be replaced before this is published, and there is a `<meta name="robots" content="noindex">` in the head that must be removed at the same time.

The copy was deliberately not drafted by an agent. It is outward-facing positioning for a jointly-owned company, so it is a decision for both principals — and the overclaim risk is high enough right now to be worth stating: Veraidyn has one delivered engagement, it was unpaid and scope-reduced, and it was performed as "Phil Stafford, d/b/a Singularity Systems" rather than as Veraidyn.

**House rule, from `CLAUDE.md` in the private repo:** never describe Veraidyn's output as *certified*, *audited*, *attested*, *compliant* or *safe*. The product is independent evidence plus an explicit residual-risk statement.

## Before publishing

1. Replace every `.todo` block.
2. Remove the `noindex` meta tag.
3. Run the drafted copy through the review pipeline: `fact-checker-external` and `fact-checker-internal` in parallel, then `style-editor-phil`, then `chief-editor`.
4. Confirm the registered corporate name and whether "PBC" forms part of it.

## Local preview

No build step, no dependencies — it is one static file.

```bash
python3 -m http.server 8080
# then open http://localhost:8080
```

## Deployment

Every push to `main` publishes. There is no staging branch; if one is wanted, set Pages to build from a `gh-pages` branch instead and treat `main` as the draft.

## Custom domain

Set it in **Settings → Pages → Custom domain**, not by hand-editing a `CNAME` file — GitHub writes that file itself and the two will conflict. DNS records are listed in `docs/github-setup-2026-08-11.md` in the private repository.
