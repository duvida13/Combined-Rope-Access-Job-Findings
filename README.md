# Combined rope-access job links

This repository collects **position titles and vacancy links** reported by four independent job-search agents. It does not contain their full research notes, a CV, application history, contact details, or outreach records.

## Open the findings

- [Latest merge](latest.md) — 26 new non-closed jobs in the 2026-10-23 run.
- [All findings by country](all-findings.md) — the full historical vacancy list in a browsable Markdown format, with position, source agents, and last reported date.
- [Merge runs](merges/README.md) — one folder per requested merge, with only jobs first reported since the previous run clearly separated from rechecks.
- [Vacancy links (CSV)](vacancies.csv) — 3,744 distinct individual or shortened job URLs from the published history. Sort by `latest_source_date` before opening. Historical entries are **not automatically current vacancies**.
- [Links needing review](review-links.csv) — 180 search or general careers pages kept separately because they do not identify one posting reliably.
- [Source differences](conflicts.md) — same-link wording, country, or status differences that warrant human review. All source claims are retained.

## How this snapshot was made

The initial manual merge read these repositories on 29 September 2026:

| Agent | Source repository | Published material used |
|---|---|---|
| ChatGPT | [ChatGPT-Daily-Job-Search-Rope-Access-](https://github.com/duvida13/ChatGPT-Daily-Job-Search-Rope-Access-) | cumulative public job index |
| Claude | [rope-access-job-search](https://github.com/duvida13/rope-access-job-search) | dated digests; rejected/search-hit state excluded |
| Grok Search | [GROK-Rope-Access-Job-Search](https://github.com/duvida13/GROK-Rope-Access-Job-Search) | dated findings |
| Grok Bot | [GROK-BOT](https://github.com/duvida13/GROK-BOT) | dated findings |

URLs were grouped only when their normalized URL matched (protocol, `www`, trailing slash, and common tracking parameters ignored). Matching URLs combine their reporting agents and status claims. Different URLs remain separate even when the titles look similar. No agent's status overrides another's. General careers/search pages are separated for review; shortened job links still require a click to confirm their destination. `latest_source_date` is the date of the most recent published source observation, not a fresh application-page check. The CSV is a link collection, not a list of confirmed open jobs.

## Updating

An external scheduled task requests an incremental merge daily at 01:00 Europe/Amsterdam; the repository itself has no GitHub Actions workflow. [The merge procedure](MERGE.md) uses saved source commit IDs and observation records to process only work published after the previous merge. Each run gets a new folder in [merges/](merges/README.md), while the cumulative CSV and country page preserve the full history.

The 14 October run received a [status-classification correction](merges/2026-10-14-01/correction-2026-10-14.md): source-reported closures must be recorded only as closures, never presented or counted as current new/rechecked opportunities.
