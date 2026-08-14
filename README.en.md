# ChronoPM v1.18.0

**Let AI manage your project — not just write documents for you.**

## What is this?

ChronoPM is an AI skill for project managers. Once installed, your AI assistant understands your project and helps with daily management — writing daily reports, organizing meeting minutes, tracking tasks and risks, managing requirement changes, and generating weekly/monthly reports.

It's not another project management app. It works directly in your existing folders. All project data is plain Markdown — no database, no cloud service, no vendor lock-in.

**In short: it's an AI assistant that understands your project better and better over time, turning scattered project information into structured knowledge assets.**

## Sound familiar?

If you've managed projects, you've probably been through some of these:

**1. Inconsistent management standards**
Different project managers have different habits and methods. Put a new person on the same project, and the granularity of cost control, risk identification, and stakeholder management changes completely. It's not a competence problem — it's the lack of a unified framework as a safety net. Project quality depends too much on individual experience.

**2. Information gaps from daily grind**
Even when a PM has set up a solid management system and file structure, the daily flood of tasks means associated files don't always get updated in sync. Seems minor — but broken information chains accumulate into real project risk.

**3. Uncontrollable handover quality**
Project managers move around, and handovers are often inadequate. The old approach was to dump a project documentation package — but with dozens or hundreds of files, the newcomer has no idea where to start or what's critical. Hidden risks get buried in the handover, and by the time they surface, it's too late.

**4. Too much time on document wrangling**
Weekly reports, daily reports, meeting minutes, risk registers, change requests… PMs spend so much time organizing documents that it squeezes out the time they should spend on actual communication and coordination. The priorities are backwards.

**5. Acceptance reports lack systematic backing**
The final project acceptance report draws from materials generated during daily management. But those materials are scattered across files and systems. Even if you want to use AI to help compile them, starting from scratch takes enormous effort — and without a proper feeding standard, the results are usually poor.

**6. General AI tools don't speak "project"**
Projects have their own jargon, abbreviations, and internal codenames. With general-purpose AI, you're constantly re-explaining the context. It burns resources, delivers poor results, and people end up thinking "might as well do it myself."

**7. No global view for multi-project coordination**
Senior managers juggle multiple projects and need to coordinate resources across them, understand how schedules interrelate. But there's no tool that connects the dots and gives you a unified picture.

## How ChronoPM addresses this

ChronoPM is positioned as an **intelligent project management knowledge assistant**. PMs continuously "feed" it project materials — meeting minutes, requirement documents, risk registers, weekly/daily reports, communication records, and so on. It automatically understands the project's unique context, generating structured knowledge indexes across dimensions like cost, resources, stakeholders, risks, issues, and schedule. The result: a **readable, transferable, reusable project knowledge package**.

## What value does it deliver?

**Level the management baseline — a "virtual PMO" for every PM**
Regardless of experience level, the tool ensures information is completed from a unified dimensional framework. No critical dimension gets missed just because of personal habit. Management quality gets a floor.

**Handover changes from "knowledge walks out the door" to "knowledge walks with the project"**
At handover, just transfer the structured index folder. The newcomer lets the AI read it and quickly grasps the full picture — how much has been spent, which risks are still open, what stakeholders care about, what issues remain. No more digging through files one by one. Handover quality no longer depends on someone's ability to explain things.

**Daily materials auto-accumulate, freeing PM time**
Weekly reports, daily reports, meeting minutes — feed them in and the tool auto-structures and archives them. PMs stop spending so much time on document wrangling and redirect that energy to communication and coordination. Meanwhile, this daily accumulation directly supports the final acceptance report — acceptance becomes "the natural outcome" instead of "last-minute scrambling."

**Understands your project's language, gets more accurate over time**
Continuous feeding builds a project-specific knowledge index. Jargon, internal codenames, historical context — all accurately understood without re-explaining every time. This completely solves the "general AI doesn't get our project" problem.

**Multi-project coordination with a global view**
Senior managers can link multiple project knowledge packages to coordinate resources across projects, compare progress, and identify resource conflicts — supporting better decisions.

**Zero additional learning cost**
It's not a new system or platform. It doesn't require changing how you work. PMs just feed it materials as they normally would, and it handles the structured organization automatically.

## How to use it?

**Step 1: Install the Skill**

Copy this directory into your AI tool's (e.g., Qoder) Skill directory.

**Step 2: Initialize your workspace**

Tell the AI: "Initialize my project workspace." It will guide you through setup — project name, team members, current phase, and which mode to use.

**Step 3: Use it daily**

Talk to the AI like you would to an assistant:

| You say | AI does |
|---|---|
| "Today's daily report" | Summarizes all updates, generates the report, and syncs personal progress |
| "We had a kickoff meeting, here are the notes…" | Organizes minutes, extracts action items, assigns owners |
| "The client wants to add feature XX" | Registers the requirement, assesses impact, updates the traceability matrix |
| "How's this week going?" | Pulls from all files and generates a weekly summary |
| "Overall program status" | Aggregates all subproject statuses into a program-level monthly report |
| "Check if anything's missing" | Scans all management files, lists gaps with priority levels |
| "Is this requirement within contract scope?" | Traces from contract → bidding → specific requirements with an evidence chain |

## Two working modes

- **Single project mode**: One `ai/` folder manages one project. Good for standalone projects.
- **Portfolio mode**: One program manager coordinates multiple subprojects. Information flows bottom-up, decisions flow top-down.

## Key features

**Markdown files are your database**
All project info lives in `.md` files. No software, database, or cloud service required. You can open them with any text editor — and still read them ten years from now.

**AI reads first, writes only with your approval**
The AI reads existing files to understand context before every operation. It asks for your confirmation before writing important data — it won't change things behind your back.

**Every change is traceable**
Requirement registration, change control, impact analysis — every step is recorded. Who requested it, when, and what it affects, all traceable.

**Project knowledge survives personnel changes**
All project knowledge lives in files. When someone new joins, the AI reads the files and gets up to speed. When someone leaves, the project history stays.

**End-to-end reporting**
Daily reports, weekly reports, monthly reports, meeting minutes, decision logs, retrospectives — all have standard templates. The AI fills them in and rolls them up automatically.

**Requirement scope is traceable**
From contracts to bidding documents to specific requirements — a three-layer model helps you answer "is this requirement within the contract scope?"

**Reasoning Baseline — smarter status derivation**
A built-in lifecycle derivation chain derives the actual completion status of modules/tasks from milestone terminal events such as "rehearsal passed," "review passed," and "acceptance passed," then cross-checks it against the task board. Combined with an entity registry and cross-source contradiction handling, weekly reports and queries no longer rely on a single board status — fewer missed counts and fewer misjudgments.

## Capabilities at a glance (CAP-001 ~ CAP-031)

| Capability | Name | Description |
|---|---|---|
| CAP-001 | Workspace Initialization | One-click project workspace setup, single/portfolio modes |
| CAP-002 | Daily Report Management | Report processing, merge idempotency, personal progress sync |
| CAP-003 | Weekly Report & Portfolio Rollup | Subproject weekly + program monthly auto-rollup |
| CAP-004 | PM Daily Todo | Whole-team aggregated todo view, 9-section panorama |
| CAP-005 | Quick Query | Index-first lookup, no full scans by default |
| CAP-006 | Output Artifact Management | Batch-dir output + draft/confirm/export flow |
| CAP-007 | Risk & Issue Management | Risk/issue registers with multi-source cross-check |
| CAP-008 | Requirement Management | Requirement register + traceability matrix |
| CAP-009 | Change Control | Change flow + impact analysis |
| CAP-010 | Resource Management | Resource register; state separated from history |
| CAP-011 | Historical Continuity | Phase handover, legacy import |
| CAP-012 | Todo Snapshot & Actuals | Snapshot freeze + plan vs actuals comparison |
| CAP-013 | Self-Check & Completeness | D/M/R/T layered self-check lists |
| CAP-014 | Excel Generation | 8 doc-sheet structures/columns/validation/formulas |
| CAP-015 | Version & Compatibility | Workspace health check + compatibility mode + migration |
| CAP-016 | Update Trigger & Intent Detection | Four-level trigger + permission tiers |
| CAP-017 | Skill Governance | Change tickets (CR/IA/RR) + regression guard |
| CAP-018 | Blueprint & External Review | Architecture decisions + capability matrix |
| CAP-019 | Domain Glossary | Terminology normalization + confidence + correction + confirm-learning |
| CAP-020 | Initialization Wizard | Six-step guided setup with progress memory & resume |
| CAP-021 | Information Completeness Inspection | 7-layer missing-info check, P0-P3 tiered reminders |
| CAP-022 | Entry Router | SKILL.md as entry router, rule navigation |
| CAP-023 | PM Profile & Preference Learning | Habit learning + preference-adapted output |
| CAP-024 | Historical Plan Import | Batch plan import + change/delay tracking |
| CAP-025 | Proactive Change | Proactive changes + human-confirm update model |
| CAP-026 | Change Log Tiered Archive | Active/archive tiering with auto month navigation |
| RI | Requirement Intelligence | Cross-source requirement merge/scope judgment/three-level index; contract scope many-to-many mapping |
| CAP-027 | Daily Report Integrated Review & Proactive Querying | After report processing, compare plan-vs-done, risk/issue changes, and task progress deviations; proactively ask about blockers/risks/omissions/feasibility |
| CAP-028 | Delegation Tracking Cascade | Auto-generate a follow-up todo for the delegator on task delegation; validate related requirement status consistency on task status change |
| CAP-029 | Closure Confirmation with Evidence | Risk/issue closure suggestions must list ID + evidence + related impact; no unsupported closure |
| CAP-030 | Communication Quality Rules | Numbered pending items + mandatory live file reading (no cache); traceable, accurate output |
| CAP-031 | Query Default Filtering | Task/todo queries default to incomplete items only; explicit "all" shows everything |
| — (extension) | Reasoning Baseline | Lifecycle derivation chain + cross-source contradiction handling + entity registry + task-set association; derives actual completion status from milestone events |

## What's included

| Content | Count | Description |
|---|---|---|
| Rule files | 22 | Define how the AI should behave in various scenarios |
| Document templates | 49 | Daily reports, weekly reports, meeting minutes, risk registers, and more |
| Automation scripts | 5 | Workspace initialization, version migration, version sync, etc. |
| Regression tests | 225 cases | Ensure every update doesn't break existing functionality |

## Directory layout

```
ChronoPM Skill/
├── SKILL.md              # AI entry file. The AI reads this first when loading the Skill
│                          # to understand its capabilities, routing rules, and behavior.
│                          # Think of it as the AI's "job description."
├── skill.json            # Skill metadata. Version, capability declarations, upgrade history —
│                          # used by AI tool platforms to identify and manage this Skill.
├── VERSION               # Current version number (plain text), for quick reference.
├── CHANGELOG.md          # Change history. What changed in each version, release date, impact scope.
│
├── references/           # 📖 Rule files (22 files, numbered 00~21)
│   │                      # The AI's "code of conduct" — defines what to do in each scenario.
│   ├── 00-pm-main-rules.md        # PM master rules: core workflows, permission model, safety baseline
│   ├── 01-daily-report-rules.md   # Daily report handling: merge, idempotency, personal progress sync
│   ├── 02-meeting-rules.md        # Meeting minutes: structured recording, action item extraction, decision archiving
│   ├── 03-task-board-rules.md     # Task board: task registration, status transitions, cascade propagation
│   ├── 04-risk-issue-rules.md     # Risk & issue: registration, assessment, multi-source cross-check
│   ├── 05-query-rules.md          # Query rules: index-first, no full scans
│   ├── 06-file-rules.md           # File rules: naming conventions, archive paths, read/write constraints
│   ├── 07-requirement-rules.md    # Requirement management: registration, traceability, RI three-layer model
│   ├── 08-change-control-rules.md # Change control: flow, impact analysis, cascade rules
│   ├── 09-portfolio-rules.md      # Portfolio coordination: multi-subproject coordination, resource transfer
│   ├── 10~21                      # Other rules (update triggers, output artifacts, Excel generation,
│   │                              # compatibility, self-check, snapshots, glossary, init wizard,
│   │                              # completeness inspection, version rules, PM profile, etc.)
│   └── ...
│
├── assets/               # 📦 Resource files
│   └── templates/        # Document templates (49). The AI fills these when generating files,
│                          # ensuring consistent formatting. Covers daily reports, weekly reports,
│                          # meeting minutes, risk registers, decision logs, retrospectives, etc.
│                          # Note: the workspace ai/ directory tree is created programmatically by
│                          # the init script; it does not rely on a separate directory template.
│
├── scripts/              # ⚙️ Automation scripts
│   ├── init_workspace.py      # Workspace initialization: creates directory structure in single/portfolio mode
│   ├── migrate_workspace.py   # Workspace migration: automatically upgrades old workspaces to latest structure
│   ├── sync_version.py        # Version sync: propagates version from single source of truth to all touchpoint files
│   ├── _version.py            # Single source of truth for versions: SKILL_VERSION + WORKSPACE_SCHEMA_VERSION
│   └── chronopm_init/         # Initialization engine: config, template rendering, validation, directory building
│
├── governance/           # 🛡️ Governance contracts (for developers)
│   ├── contracts/             # Core contract: defines protection levels and release rules for Skill changes
│   ├── baselines/             # Version baseline snapshots: complete file copies per version, for rollback/audit
│   ├── change-requests/       # Change requests (CR): formal records of every Skill self-modification
│   ├── impact-analysis/       # Impact analysis (IA): pre-change impact scope assessment
│   ├── regression-reports/    # Regression reports (RR): full test results for each release
│   ├── review-checklists/     # Release checklists: ensures no release step is skipped
│   └── planning/              # Design documents: design docs for major features
│
└── tests/                # 🧪 Regression test suite (225 cases)
                              # Run after every Skill update to ensure nothing breaks.
```

## Version info

| Item | Value |
|---|---|
| Skill version | 1.18.0 |
| Workspace schema | 0.8.0 |
| Rule files | 22 |
| Document templates | 49 |
| Regression cases | 225 |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
