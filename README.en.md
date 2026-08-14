# ChronoPM v1.16.2

**Let AI manage your project — not just write documents for you.**

## What is this?

ChronoPM is an AI skill for project managers. Once installed, your AI assistant understands your project and helps with daily management — writing daily reports, organizing meeting minutes, tracking tasks and risks, managing requirement changes, and generating weekly/monthly reports.

It's not another project management app. It works directly in your existing folders. All project data is plain Markdown — no database, no cloud service, no vendor lock-in.

## What problem does it solve?

If you've managed a project, you've probably been through this:

- **Information is scattered everywhere** — daily reports in chat groups, tasks in Excel, requirements in Word, decisions in someone's head. Finding anything takes forever.
- **AI doesn't understand your project** — you ask AI to help write a report, but the output has nothing to do with your actual project because it doesn't know your team, your progress, or your context.
- **Changes are out of control** — the client says "change this," and suddenly nobody remembers what was changed, what it affects, or who approved it.
- **Knowledge walks out the door** — when someone leaves, the project history goes with them.

ChronoPM organizes all project information in a set of Markdown files. Once the AI reads these files, it understands your project and can actually help.

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
