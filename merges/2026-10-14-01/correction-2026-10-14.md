# Correction — status classification in the 2026-10-14 merge

## What was wrong

Commit `af3dd15` correctly recorded seven Grok Bot closure observations in `state/observations.csv` and in the run's closure section, but it also presented the same URLs as opportunities. Three closed-only URLs were counted under new findings and four previously known closed URLs were counted under rechecked findings.

The reported Netherlands vacancy, **Uitvoerder Rope Access Drachten**, was one of the affected records. Grok Bot had placed it under `Closed since last run` and reported HTTP 404; it did not report the vacancy as active.

## Root cause

The merge classified every newly observed URL as new or rechecked before applying the observation's status. Closures were then added to a separate section without being removed from the opportunity sections. The rechecked bullets also omitted current status, hiding the contradiction.

This was a merge-classification and presentation error. It was not caused by source timing: all three available agent updates used by the run were published before the scheduled 01:00 Europe/Amsterdam merge time.

## Correction applied

- The seven closure URLs now appear only under `Source-reported closures`.
- Corrected new non-closed findings: **19**, formerly 22.
- Corrected rechecks without a status transition: **4**, formerly 9.
- The one reopening appears only under `Source-reported reopenings`.
- Rechecked bullets now state their current source status.
- `latest.md`, the run README, and the repository navigation use the corrected counts.

The cumulative observation history and vacancy status claims were already accurate and remain intact. Source repositories and saved source checkpoints were not changed.

## Prevention added

`MERGE.md` now requires status resolution before new/rechecked classification and defines mutually exclusive closure, reopening, and opportunity categories. `scripts/validate_merge_status.py` blocks publication when a normalized URL appears in both an opportunity section and closures, when closure wording appears in an opportunity bullet, when rechecked status is omitted, or when section counts do not match their bullets.
