# ChronoPM v1.16.2

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

## What's included

| Content | Count | Description |
|---|---|---|
| Rule files | 22 | Define how the AI should behave in various scenarios |
| Document templates | 48 | Daily reports, weekly reports, meeting minutes, risk registers, and more |
| Automation scripts | 5 | Workspace initialization, version migration, version sync, etc. |
| Regression tests | 185 cases | Ensure every update doesn't break existing functionality |

## Directory layout

```
ChronoPM Skill/
├── SKILL.md           # AI entry point — the AI reads this to know how to help you
├── skill.json         # Version and metadata
├── VERSION            # Current version number
├── CHANGELOG.md       # Change history
├── references/        # 22 rule files (the AI's code of conduct)
├── assets/templates/  # 48 document templates
├── scripts/           # Automation scripts
├── governance/        # Governance contracts and change management (for developers)
└── tests/             # Regression test suite
```

## Version info

| Item | Value |
|---|---|
| Skill version | 1.16.2 |
| Workspace schema | 0.8.0 |
| Rule files | 22 |
| Document templates | 48 |
| Regression cases | 185 |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
