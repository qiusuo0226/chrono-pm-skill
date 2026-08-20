# ChronoPM v3.0.0

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

## Todos & Work Packages: the core of project execution (v2.0.0 / v2.1.0 enhanced)

v2.0.0 converges the entire execution system into two layers: **todo files** manage every concrete task, and **work packages (WP)** manage grouping and milestones. Understand these two concepts and you understand ChronoPM's entire data flow.

### Todos: one file per person per day

Each executor gets one todo file per day: `todos/{date}/{executor}.md`. It is the **single source of truth** for task execution status — daily reports, weekly reports, progress, and the backward-planning matrix are all aggregated from it in real time. No separate boards or indexes are maintained.

- **Globally unique IDs**: every todo gets a `TD-{name-initials}-{date}-{seq}` ID, traceable across days and projects.
- **Handover changes the ID, not the work**: when a task changes owner, a new ID is created with a traceability chain — it's always clear who did what.
- **Built-in work log**: daily report content no longer lives in separate files; it goes straight into the todo file's work-log section (done today / in progress / blockers / risks / hours).
- **Identity snapshot (v2.1.0)**: each daily todo file carries a §0 identity block (role / name / contact / responsible module / start date / expected end date), auto-copied via T+1 carryover; conflicts with resource-register are resolved in favor of the register.
- **Progress column (v2.1.0)**: the core execution table adds a "Progress" column (0%-100%), updated from daily-report mapping; two-track arbitration with status — status=completed forces progress to 100%, progress=100% without completed status does NOT auto-promote (terminal state needs PM confirmation).
- **Two-step daily-report flow (v2.1.0)**: the daily report's original text is first archived verbatim into the todo file's §2 archive section (no summarizing), then mapped into the §3 work-log section and todo fields, fully traceable.
- **Todo carryover (v2.1.0)**: before creating/updating todos, the AI mandatorily scans the previous day's all-person unresolved todos and carries them over to today (Step 0, hard block — no new todos before it completes); same-person carryover keeps the same ID across days.

### Work packages (WP): the planning unit

Plan files (`plans/PLAN-xxx.md`) organize work with work packages (numbered `WP-NNN`):

- **Todos must belong to a work package**: formal todos carry a WP reference, so plan adjustments cascade precisely down to every todo.
- **Milestone = milestone work package**: rehearsal, go-live and other milestones no longer get their own files — they are simply work packages flagged as milestones.
- **Progress is never stored separately**: WP progress = real-time aggregation of its todos' completion ratio. Always consistent with actual execution — no stale progress numbers.

### The full data flow

```
[Input entries]  Daily reports / meeting minutes / verbal assignments /
                 requirement breakdown / approved changes / backward planning
                          │
                          ▼  AI parses, extracts, unified ownership routing
[Single source]  todos/{date}/{executor}.md todo files
                          │
          ┌───────────────┼───────────────────┐
          ▼               ▼                   ▼
  Aggregate by WP ref   Slice by due date   Work-log section
          │               │                   │
          ▼               ▼                   ▼
[Plan view]            [Time view]          [Reporting view]
WP progress /           "What's on today" /  daily → weekly →
backward countdown      "this week's plan"   monthly reports
```

Key point: **todo files are the only write target; everything else is a derived view**. Daily/weekly reports are outputs, not data sources — reports can never drift out of sync with reality.

### Five task-creation entry points

No matter where a task comes in, it goes through the same ownership routing — nothing lost, nothing duplicated, nothing scattered:

| Entry point | Example scenario |
|---|---|
| Verbal assignment | "Add a todo for Wang: finish the API doc by Friday" |
| Daily report extraction | "Tomorrow's plan" in a member's report auto-becomes a todo |
| Meeting action items | Action items extracted from minutes land as todos |
| Requirement breakdown | Confirmed requirements split into work packages and todos |
| Approved changes | Follow-up tasks added/adjusted after a change is approved |

Every new task lands in one of three places: **inside a work package** (high-confidence match) / **standalone todo** (has owner + deadline + deliverable) / **one-time reminder** (doesn't occupy a todo file, reminds once). When unsure, the AI asks — it never decides silently.

### Status system (fully Chinese in the workspace)

| Entity | Status flow |
|---|---|
| Todo | pending → in progress → awaiting review → completed (can become blocked / cancelled / transferred out) |
| Work package | planned → in progress → completed |
| Requirement | proposed → confirmed → in progress → delivered → accepted (can become changed / cancelled) |
| Risk | open → monitoring → mitigated → closed (can become escalated-to-issue) |
| Issue | open → in progress → resolved → closed (can become blocked) |
| Change | submitted → assessing → approved / rejected → implemented (can become cancelled) |

**How status updates take effect**: say "Wang's API doc is done," and the AI finds the matching todo, proposes marking it completed, and auto-runs cascade checks (WP progress, related risks/issues, requirement status). Process-level updates are written as "pending confirmation" first; terminal changes (completed/cancelled) only take effect after your approval — no missed updates, no unsolicited overwrites.

**Close gate (v2.1.0, DF-002)**: closing (completed/cancelled/transferred-out) requires the four elements "ID + evidence + related impact + PM confirmation"; after daily/weekly-report flows the AI proactively lists close candidates for your confirmation.

## Two working modes

- **Single project mode**: One `ai/` folder manages one project. Good for standalone projects.
- **Portfolio mode**: One program manager coordinates multiple subprojects. Information flows bottom-up, decisions flow top-down. Portfolio-level availability/schedule aggregations are dynamic views (v2.1.0 hard constraint) — personnel availability, schedule conflicts, staffing rates, milestone/gate attainment are all aggregated in real time from each subproject at query time and never persisted to any index file, so aggregated data never goes stale.

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

**Dual-view requirements: business ⇄ implementation**
The same requirement looks like "what to build" to the client (business view) and "how to build it" to developers (implementation view). Dev-side docs (PRD/design/API specs/prototypes) are ingested into the requirement library, with each register entry carrying an "implementation view" and "prototype/doc links." When processing developers' daily reports, the AI can match against the business context — so it truly understands what a report is about.

**Reasoning Baseline — smarter status derivation**
A built-in lifecycle derivation chain derives the actual completion status of modules/tasks from milestone terminal events such as "rehearsal passed," "review passed," and "acceptance passed," then cross-checks it against todo files. Combined with an entity registry and cross-source contradiction handling, weekly reports and queries no longer rely on a single todo-file status — fewer missed counts and fewer misjudgments.

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
| RI | Requirement Intelligence | Cross-source requirement merge/scope judgment/three-level index; contract scope many-to-many mapping; business⇄implementation dual-view (implementation view / prototype links) |
| CAP-027 | Daily Report Integrated Review & Proactive Querying | After report processing, compare plan-vs-done, risk/issue changes, and task progress deviations; proactively ask about blockers/risks/omissions/feasibility |
| CAP-028 | Delegation Tracking Cascade | Auto-generate a follow-up todo for the delegator on task delegation; validate related requirement status consistency on task status change |
| CAP-029 | Closure Confirmation with Evidence | Risk/issue closure suggestions must list ID + evidence + related impact; no unsupported closure |
| CAP-030 | Communication Quality Rules | Numbered pending items + mandatory live file reading (no cache); traceable, accurate output |
| CAP-031 | Query Default Filtering | Task/todo queries default to incomplete items only; explicit "all" shows everything |
| — (extension) | Backward Planning & WP Work Packages | Reverse-plan plan work packages around a target deadline (WF-7: backward planning = a way to arrange plans, not a separate system); unified ownership routing for all five task-creation entry points (WF-8: three-way split into WP / standalone todo / one-time reminder, formal todos must land on todo files); PLAN-file WP rough-planning table + backward-planning metadata; WP hierarchical query & backward-planning countdown; **Backward Daily Matrix** (person × date, authoritative source = todo files, supports portfolio multi-sub-project todo traversal and legacy degradation) |
| — (extension) | Reasoning Baseline | Lifecycle derivation chain + cross-source contradiction handling + entity registry + task-set association; derives actual completion status from milestone events |

## What's included

| Content | Count | Description |
|---|---|---|
| Rule files | 22 | Define how the AI should behave in various scenarios |
| Document templates | 33 | Daily reports, weekly reports, meeting minutes, risk registers, and more |
| Automation scripts | 5 | Workspace initialization, version migration, version sync, etc. |
| Regression tests | 299 cases | Ensure every update doesn't break existing functionality |

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
├── references/           # 📖 Rule files (22 files, numbered 00~22; No.03 merged into No.00 since v2.0.0)
│   │                      # The AI's "code of conduct" — defines what to do in each scenario.
│   ├── 00-pm-main-rules.md        # PM master rules: core workflows, permission model, safety baseline
│   ├── 01-daily-report-rules.md   # Daily report handling: merge, idempotency, work-log integration
│   ├── 02-meeting-rules.md        # Meeting minutes: structured recording, action item extraction, decision archiving
│   ├── 04-risk-issue-rules.md     # Risk & issue: registration, assessment, multi-source cross-check
│   ├── 05-query-rules.md          # Query rules: index-first, no full scans
│   ├── 06-file-rules.md           # File rules: naming conventions, archive paths, read/write constraints
│   ├── 07-requirement-rules.md    # Requirement management: registration, traceability, RI three-layer model, business⇄implementation dual-view
│   ├── 08-change-control-rules.md # Change control: flow, impact analysis, cascade rules
│   ├── 09-portfolio-rules.md      # Portfolio coordination: multi-subproject coordination, resource transfer
│   ├── 10~22                      # Other rules (update triggers, output artifacts, Excel generation,
│   │                              # compatibility, self-check, snapshots, glossary, init wizard,
│   │                              # completeness inspection, version rules, PM profile, personal todo, etc.)
│   └── ...
│
├── assets/               # 📦 Resource files
│   └── templates/        # Document templates (36). The AI fills these when generating files,
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
│   ├── migrations/            # Upgrade files: authoritative execution source of the version chain (upgrade-to-{version}.md)
│   ├── impact-analysis/       # Impact analysis (IA): pre-change impact scope assessment
│   ├── regression-reports/    # Regression reports (RR): full test results for each release
│   ├── review-checklists/     # Release checklists: ensures no release step is skipped
│   └── planning/              # Design documents: design docs for major features
│
└── tests/                # 🧪 Regression test suite (299 cases)
                              # Run after every Skill update to ensure nothing breaks.
```

## Version info

| Item | Value |
|---|---|
| Skill version | 3.0.0 |
| Workspace schema | 0.9.0 |
| Rule files | 22 |
| Document templates | 33 |
| Regression cases | 299 |

## Distribution package naming

Release artifacts follow `{BrandName}-Skill-v{version}.zip`. Since v3.0.0 one release produces two packages (G-3):

- `ChronoPM-Project-Skill-v3.0.0.zip` (main package, single-project management)
- `ChronoPM-Portfolio-Skill-v3.0.0.zip` (read-only aggregation companion package)

- **BrandName**: brand prefix of `displayName` in each package's `skill.json` (before `—` or `(`)
- **version**: semantic version with `v` prefix (both packages share one version line)

On this machine, packaging uses the Python entry `tools/pack-skill/scripts/pack.py` (when PowerShell execution policy is restricted); its exclusion model reads `pack.ps1` as the **single source of truth**, while `pack.ps1` serves as the cross-platform reference implementation. Running `pack.py` at the repo root auto-detects the `ChronoPM-Portfolio/` companion and emits both zips; the Project package excludes `ChronoPM-Portfolio/` (exclusion model in `pack.ps1`). Before release, `governance/scripts/audit_release.py` must pass, including a “naming drift guard” assertion that rejects legacy `{name}-{version}.zip` artifacts.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
