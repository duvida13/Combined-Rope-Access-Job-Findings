# Incremental merge procedure

Use this procedure whenever the user asks for combined findings again. **Do not repeat the initial historical extraction.** The initial snapshot covered the four sources through 29 September 2026.

1. Read [`state/source-checkpoints.json`](state/source-checkpoints.json). The four commit SHAs are the last successfully merged source revisions. Read the existing [`state/observations.csv`](state/observations.csv), [`vacancies.csv`](vacancies.csv), and [`review-links.csv`](review-links.csv) as the cumulative baseline.
2. Fetch the current default branch of each source repository. For each, compare its saved SHA to current HEAD with `git diff --name-status OLD_SHA..NEW_SHA`. Inspect **only added or modified published job files**: `digests/` and `seen-jobs.md` for ChatGPT (the repository changed from its former `daily/` and `data/job-index.md` layout in October 2026); `digests/` for Claude; `finds/` for the two Grok repositories. Ignore candidate notes, private context, migration-only copies of already-merged dated files, and Claude's `state/seen_jobs.json` (it includes rejected hits). If a source SHA is unchanged, skip that source entirely.
3. Extract only position title, country when present, vacancy URL, source agent/file, source status, and source date. Preserve the meaning of source headings and fields: a job under `Closed`, `Removed`, `Expired`, or equivalent is a status event, **not an active finding**. For a changed cumulative ChatGPT index, compare `seen-jobs.md` rows against the index at the saved checkpoint and process only new or materially changed rows. For a changed dated file, compare each observation with its prior row signature; do not replay unchanged rows. Do not copy résumé information, contact details, full notes, or application history.
4. Normalize URLs consistently: lower-case the host, remove a leading `www`, use HTTPS, drop a trailing slash and common tracking parameters. Treat an exact normalized URL as one vacancy with **all** reporting agents and claims. Keep different URLs separate unless a human has verified that they are the same posting. Keep general careers pages marked as uncertain.
5. Resolve the current-run status for every normalized URL **before** classifying it:
   - `closed`, `expired`, `withdrawn`, `removed`, `invalid`, HTTP 404, and HTTP 410 are closure states;
   - `reopened` is a reopening state and must be labeled explicitly;
   - `live` is an active source claim;
   - `unverified` or `needs-revalidation` may be retained, but must never be described as verified live.
   If observations conflict, use the later timestamp when one is available. If same-date ordering is unknown, put the URL in the disagreement/review section and do not present it as active.
6. Compare each normalized individual vacancy URL with the cumulative `vacancies.csv` **before** adding it. The run's primary classifications are mutually exclusive:
   - `New findings`: URLs absent from the prior cumulative snapshot whose current-run status is not a closure state;
   - `Previously listed — rechecked or changed`: existing URLs re-observed without a closure or reopening transition; show the current status in every bullet;
   - `Source-reported closures`: all closure transitions, including URLs first observed already closed; never count or repeat these as new/rechecked opportunities;
   - `Source-reported reopenings`: reopening transitions, listed here rather than repeated under rechecked findings;
   - `Conflicts/review`: unresolved contradictory status claims.
   Never present unchanged historical rows as new.
7. Create a **new folder for every run** at `merges/YYYY-MM-DD-NN/`, where `NN` is 01, 02, etc. for multiple runs on the same Amsterdam calendar date. Its `findings.md` holds that run's new findings, rechecks, status transitions, and disagreements, each labeled and grouped by country where applicable. Its `README.md` records the run date, source commit range for each of the four repositories, counts, and any unavailable sources. Add the run to `merges/README.md`; set `latest.md` to the same run's findings. A zero-new-jobs run still gets a folder and states zero. Do not silently reuse a folder.
8. Append the new source observations to `state/observations.csv`; update `vacancies.csv` without deleting historical links, then regenerate `all-findings.md` from the cumulative CSV grouped by country. Keep search and general careers pages in `review-links.csv`. Update `conflicts.md` with substantive disagreements, retaining both claims and links to source findings. The old `updates/2026-09-29.md` remains as a historical baseline; new runs use `merges/`.
9. Before publication, run `python3 scripts/validate_merge_status.py merges/YYYY-MM-DD-NN/findings.md`. Publication is blocked unless all of these invariants pass:
   - no normalized URL appears in both a new/rechecked opportunity section and the closures section;
   - no closure wording or status appears in an opportunity bullet;
   - each rechecked bullet states its current status;
   - heading counts equal the number of vacancy bullets in their sections.
   Also compare the rendered `latest.md` with the run's `findings.md` and verify the summary counts in both README files.
10. Only after the new files are prepared and validation passes, replace the four SHAs in `state/source-checkpoints.json` with the source HEADs and set `merged_at` to the run date. If a source is unavailable, leave its SHA unchanged and state clearly that it was not merged. Commit the validated run and checkpoint update together. This makes retries safe.

The date in a source file is not proof that a vacancy remains open. No fresh vacancy research is required for this merge. The external scheduler may request the run, but it does not relax any inspection, status, validation, or source-read-only rule above.
