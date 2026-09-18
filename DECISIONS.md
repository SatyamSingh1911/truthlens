# TruthLens Decision Points

## DP1 — Feed order

**Choice: Risk first, then recency.**

The feed puts High Risk claims first because the product is a triage tool: reviewers and citizens should be able to notice claims with multiple automatic warning signals quickly. Within each risk group, newer submissions appear first so the feed still feels current. Risk is only a triage signal, not a truth judgment.

## DP2 — Visibility

**Choice: Unverified claims remain publicly visible.**

Keeping unverified claims visible makes the workflow transparent and lets users see what is awaiting review. The UI clearly labels these claims as **Unverified**, so publication is not presented as confirmation. This also lets a reviewer demonstrate the full lifecycle from submission to review.

## DP3 — Editing

**Choice: Claims cannot be edited after submission.**

The original submission is treated as an auditable record: changing its text could silently change the basis for the original automatic flags. Instead, reviewers can add a status and note, preserving the submitted claim and its triage result. If a materially different claim is discovered, it should be submitted as a new claim.
