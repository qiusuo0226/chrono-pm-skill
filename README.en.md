# ChronoPM v3.19.0 — An AI Sidekick That Actually Manages Projects

**You make the calls. It remembers, computes, and watches. Every project fact lives in Markdown — and stays with the project.**

ChronoPM is a project-management methodology packaged as an AI skill: talk the way you already do — paste a daily report, share meeting minutes, ask about progress — and it files the facts into a clean set of Markdown files. Anything that matters takes effect only after you nod. People leave, AI tools change; the project's memory stays in the folder.

> **Two packs:** day-to-day entry with **ChronoPM-Project** (single project — every write happens here); cross-project progress / risk / contract / weekly rollups with **ChronoPM-Portfolio** (read-only — it never writes member projects).
>
> **Python:** init / migrate / verify scripts need Python **≥3.9** (3.10+ recommended). Daily todos and queries do not.

## Why you need it

A PM's project facts scatter everywhere: daily reports in chat threads, minutes in inboxes, risks in someone's head, progress in a stale deck. Trying to confirm "how was this requirement decided?" turns into an afternoon of archaeology.

Generic AI doesn't fix that. Its context resets, it forgets your project, and it will enthusiastically log an offhand "seems risky" as a formal risk entry. Numbers without provenance you can't trust — and shouldn't.

Handover is worse: zip ten folders, hit send, and the next PM starts from zero against a structure they've never seen.

ChronoPM solves all three at once: **facts live in files, the AI guards the files, you gate the changes.**

## Three commitments

The whole system rests on three commitments; everything else follows from them:

1. **One truth per fact.** Todos, risks, issues, decisions, requirements, and contracts each have a single source-of-truth file. Daily and weekly reports, progress, and backward plans are all derived live from those facts. No second truth exists — so nothing can "drift apart."
2. **The AI drafts; you approve.** Mention a new requirement, a risk, or a staffing change, and the AI catches it and files it. But operations that change the record — marking done, closing, deleting — take effect only after your confirmation, with every change logged.
3. **Handover is a folder.** All management activity lives inside the project's own `ai/` directory and never touches your deliverables. Hand that folder to the AI, and the next PM picks up right where you left off.

## How the pieces connect

Module flow diagrams (person → AI → which file → whether you decide): [ChronoPM-Project/SKILL_MODULE_MAP.md](ChronoPM-Project/SKILL_MODULE_MAP.md)

## See a real conversation

Conversation walkthroughs (names and numbers are fake; the way you talk is real). Written in Chinese, covering init, feeding contracts, daily reports, meetings, backward plans, portfolio, and change:

Index: [examples/](examples/) (20 pieces; follow the reading order there)

## Just talk to it

| You say | It does |
|---|---|
| "Here's today's report…" | Archives it, updates owners' todos, shows a judgment card before any risk gets registered |
| "Kickoff notes…" | Structures the minutes and drops action items onto each owner's todo file |
| "Is this requirement backed by the contract?" | Walks contract → bid → clause and answers with an evidence chain |
| "How did this week go?" | Aggregates the weekly report from live todos — every number traceable |
| "We launch next month — plan backwards" | Derives the plan from milestones, flagging the critical path and resource conflicts |
| "How's the whole portfolio?" | Switch to ChronoPM-Portfolio for a read-only rollup across projects |
| "Who is still unassigned on this plan?" | Opens the plan's node sub-rows; empty slots show as unassigned |
| "Roll up each project's plan before 7 Oct" | Matches by date window, not plan name |
| "The skill can't do this — file it as an upgrade need" | Writes a skill-gap note under `ai/outputs/`, not the requirement register |

The full surface of day-to-day management is covered: requirements and change tracking, todos and work packages, plans and backward scheduling, milestones, risks and issues, decision records, meetings and reviews, daily and weekly reports, labor-cost ledgers, lessons learned — plus a glossary that grows with your project, so the AI gets better at your jargon over time.

## Getting started

1. Copy `ChronoPM-Project/` (and `ChronoPM-Portfolio/` if you need cross-project rollups) into your AI tool's skill directory. Do not copy the whole repo root.
2. Tell the AI: "Initialize my project workspace."
3. From then on, feed it materials the way you already work.

Pack from the source repo: `python tools/pack-skill/scripts/pack.py --skill-root ChronoPM-Project`  
Before release: `python governance-shared/scripts/audit_release.py` must pass.

## Repository layout

```
ChronoPM Skill/
├── ChronoPM-Project/     # Single-project skill pack (rules, templates, scripts, regression suite)
├── ChronoPM-Portfolio/   # Read-only portfolio companion
├── examples/             # Conversation walkthroughs (init through portfolio, 20 pieces)
├── governance-shared/    # Repo-level governance: baselines / CR / impact analysis / release audit (not packed)
├── tools/                # Packing tools
├── README.md
├── README.en.md
└── LICENSE.txt
```

## Engineering quality

- **729 regression cases** guarding every update against breaking existing behavior;
- **Two-layer versioning:** the skill version and the workspace schema evolve independently, with compatibility checks and migration guidance on upgrade;
- **Governance built in:** change requests, impact analysis, and release audits are formal flows in the repo, not verbal agreements.

## Version info

| Item | Value |
|---|---|
| Skill version | 3.19.0 |
| Workspace schema | 0.16.0 |
| Rule files | 23 |
| Document templates | 36 |
| Regression cases | 729 |

Release artifacts: `ChronoPM-Project-Skill-v3.18.0.zip` + `ChronoPM-Portfolio-Skill-v3.18.0.zip`.

Regression tests | 729 cases. Regression test suite (729 cases).

Changelog: [ChronoPM-Project/CHANGELOG.md](ChronoPM-Project/CHANGELOG.md)

## License

[MIT](LICENSE.txt)
