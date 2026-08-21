# ChronoPM v3.8.0

**Let AI manage your project — not just write documents for you.**

Install the skill. Feed it daily reports, minutes, contracts. Facts live in Markdown and take effect only after you confirm. People leave; the folder stays.

> **Two packs:** day-to-day entry uses **ChronoPM-Project**. Cross-project progress / risk / contracts / weekly rollup uses **ChronoPM-Portfolio** (read-only — it never writes member-project facts).

## Core ideas

These few rules are the whole model. Everything else hangs off them.

| Idea | In one sentence |
|---|---|
| Write in Project, read in Portfolio | Facts are written only in this project's `ai/`. Cross-project views aggregate; they never edit members. |
| Todos are the smallest facts | Execution state lives only in `todos/{date}/{person}.md`. Daily/weekly reports and progress are derived, not a second truth. |
| You confirm, then it counts | Done / closed / delete / cross-project writes need your nod. The AI may draft as pending; it does not rewrite live facts for you. |
| The roster is not a new file | The team list is §1 of that day's (or latest legal day's) `todos/{date}/_index.md`. Do not keep a parallel staff register. |
| A person has three layers | Role/status sit on the roster; contact lives in personal §0; join/leave history in §0.5. Cost/effort sits on the person's **latest file** §0.6: new files copy the whole table then append — never create empty historical day folders. |
| Units are project-defined | Person-days, hours, months come from `project-context` cost accounting. The skill never hard-codes one company's formula. |
| Archive ≠ backup | Archive is living history, read via indexes. `backup/` is upgrade junk and unread by default. |
| "Tomorrow" is not tomorrow's folder | "Tomorrow" in a daily report is written into **today's** todo. Do not pre-create future-dated directories. |

## Sound familiar?

| Pain | ChronoPM |
|---|---|
| Every PM runs a different standard | One rule set as the floor |
| Daily reports, risks, and todos drift apart | Todo files are the single source of truth; reports are derived |
| Handover is a zip dump nobody can navigate | Hand over `ai/`; the AI reads it and picks up |
| General AI doesn't speak your project's jargon | Glossary + project memory — more accurate over time |
| The words "there's a risk" get registered as a risk | v3.7.0 judgment card: three questions first, then write |

## Talk to it like an assistant

| You say | AI does |
|---|---|
| "Today's daily report" | Archives it, maps todos, judgment card before any risk write |
| "Kickoff notes…" | Minutes + action items onto owners' todo files |
| "Is this in the contract?" | Contract → bid → clause, with an evidence chain |
| "How's this week?" | Weekly report aggregated from todos — no invention |
| "Cross-project status" | Switch to ChronoPM-Portfolio for a read-only rollup |

**Writes go only to todo files** `todos/{date}/{person}.md`. Daily/weekly reports, progress, and backward-planning all roll up from there. Work packages `WP-NNN` group work and milestones; WP progress = live completion ratio of its todos — no stale progress file.

Terminal states (done / closed) need your confirmation. The AI does not rewrite facts on its own.

## What's new in v3.8.0

- **People live on todos:** `resource-register` / `transfer-log` retired. Roster is `_index` §1; join/leave is personal §0.5.
- **Talk to the PM in plain language:** no paths, IDs, or process names in questions. "Please confirm" means only approve-or-reject or allow-or-deny.
- **No future-dated todo folders.** Before editing one person's file, finish carry-over for everyone who should have a file today.
- **Labor-cost ledger:** §0.6 accumulates by day; if cost accounting is blank, mentions of labor cost still get recorded; reconciling with the company timesheet is the PM's job.
- **Portfolio:** V-11 shared-file split suggestions; V-12 glossary pointer index (read-only).

## Two ways to work

- **Single project:** one `ai/` folder, one project.
- **Portfolio:** ChronoPM-Portfolio rolls up many projects read-only; cross-project numbers are computed at query time and not persisted.

## Get going

1. Copy `ChronoPM-Project/` (and `ChronoPM-Portfolio/` if you need the rollup) into your AI tool's skill directory. Do not copy the whole repo root.
2. Tell the AI: "Initialize my project workspace."
3. Feed it materials the way you already work.

Pack from repo root: `python tools/pack-skill/scripts/pack.py --skill-root ChronoPM-Project`  
Before release: `python governance-shared/scripts/audit_release.py` must pass.

## What's included

| Content | Count | Description |
|---|---|---|
| Rule files | 22 | How the AI should behave in each scenario |
| Document templates | 36 | Daily/weekly reports, minutes, risk registers, WPs, source-doc split |
| Automation scripts | 5 | Init, migrate, version sync |
| Regression tests | 390 cases | Guard against breaking existing behavior |

```
ChronoPM Skill/
├── ChronoPM-Project/     # Single-project Skill package root (pack root; tests = Regression test suite (390 cases))
├── ChronoPM-Portfolio/   # Read-only portfolio companion
├── governance-shared/    # Repo-level shared (not packed): baselines / CR / IA / RR / audit
├── tools/                # pack-skill
├── README.md
├── README.en.md
└── LICENSE.txt
```

## Version info

| Item | Value |
|---|---|
| Skill version | 3.8.0 |
| Workspace schema | 0.13.0 |
| Rule files | 22 |
| Document templates | 36 |
| Regression cases | 390 |

Release zips: `ChronoPM-Project-Skill-v3.8.0.zip` + `ChronoPM-Portfolio-Skill-v3.8.0.zip`.

Changelog: [ChronoPM-Project/CHANGELOG.md](ChronoPM-Project/CHANGELOG.md)
