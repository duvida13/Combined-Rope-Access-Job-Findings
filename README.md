# Combined rope-access job links

This repository collects **position titles and vacancy links** reported by four independent job-search agents. It does not contain their full research notes, a CV, application history, contact details, or outreach records.

## Open the findings

- [Latest manual merge](latest.md) — 50 individual links reported or revalidated on 29 September 2026 in this first snapshot.
- [Dated merge history](updates/2026-09-29.md) — each future requested merge gets its own dated delta; older results stay available.
- [All collected links (CSV)](vacancies.csv) — 2,830 distinct URLs from the published history. Sort by `latest_source_date` and check `link_type` before opening. Historical entries are **not automatically current vacancies**.
- [Source differences](conflicts.md) — same-link wording, country, or status differences that warrant human review. All source claims are retained.

## How this snapshot was made

The initial manual merge read these repositories on 29 September 2026:

| Agent | Source repository | Published material used |
|---|---|---|
| ChatGPT | [ChatGPT-Daily-Job-Search-Rope-Access-](https://github.com/duvida13/ChatGPT-Daily-Job-Search-Rope-Access-) | cumulative public job index |
| Claude | [rope-access-job-search](https://github.com/duvida13/rope-access-job-search) | dated digests; rejected/search-hit state excluded |
| Grok Search | [GROK-Rope-Access-Job-Search](https://github.com/duvida13/GROK-Rope-Access-Job-Search) | dated findings |
| Grok Bot | [GROK-BOT](https://github.com/duvida13/GROK-BOT) | dated findings |

URLs were grouped only when their normalized URL matched (protocol, `www`, trailing slash, and common tracking parameters ignored). Matching URLs combine their reporting agents and status claims. Different URLs remain separate even when the titles look similar. No agent's status overrides another's. General careers pages and short links are marked in `link_type`; they may require further navigation or be stale. `latest_source_date` is the date of the most recent published source observation, not a fresh application-page check. The CSV is a link collection, not a list of confirmed open jobs.

## Updating

Updates happen **only when requested**. [The merge procedure](MERGE.md) uses saved source commit IDs and observation records to process only work published after the previous merge. It appends a dated delta, updates the cumulative CSV, and preserves conflicting claims. There is no scheduled workflow or automatic sync in this repository.
