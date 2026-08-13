# ChronoPM v1.16.0

A Markdown-driven AI project management skill.

## Description

A project management skill for project managers (especially in To G / To B digital-transformation fields). It treats Markdown files as the source of truth, uses AI as an assistant, and keeps human confirmation as the final control point. It covers full-scope project management: requirements, task tracking, schedule control, risk & issue, milestones, cost & P&L, daily/weekly reports, meeting minutes, decision logs, retrospectives, program (portfolio) coordination, resource allocation & transfer, update-intent detection, initialization wizard, iteration management, information-completeness inspection & reminders, historical-plan import & change/delay tracking, domain glossary, PM-profile preference learning & output adaptation, and the proactive-change + human-confirmation update model.

Core principle: **fact-source files (board, register, log) are the single source of truth for project state; process records (daily reports, meeting minutes) are input and must not replace fact sources directly.**

## Working Modes

- **Single mode**: for a standalone project; all management docs live under the project root `ai/`.
- **Portfolio mode**: for a program manager coordinating multiple subprojects; layered under `portfolio/` (program level) and `projects/{subproject}/` (subproject level). Information flows bottom-up, decisions flow top-down; the program does not modify subproject fact sources directly.

## Capabilities (CAP-001 ~ CAP-026)

| Capability | Name | Note | Origin version |
|---|---|---|---|
| CAP-001 | Workspace Initialization | Init workspace; `init_workspace.py` supports single/portfolio | base |
| CAP-002 | Daily Report Management | Daily report handling with merge idempotency + personal progress | base |
| CAP-003 | Weekly Report & Portfolio Rollup | Subproject weekly + program monthly rollup | base |
| CAP-004 | PM Daily Todo (9-section panorama) | Whole-team aggregated todo view | base |
| CAP-005 | Quick Query (index-first) | Index-first lookup, no full scans by default | base |
| CAP-006 | Output Artifact Management | Batch-dir output + draft/confirm/export flow | base |
| CAP-007 | Risk & Issue Management | Risk/issue registers with multi-source cross-check | base |
| CAP-008 | Requirement Management | Requirement register + traceability matrix | base |
| CAP-009 | Change Control | Change flow + impact analysis | base |
| CAP-010 | Resource Management | Resource register; state separated from history | base |
| CAP-011 | Historical Continuity | Handover across project phases | base |
| CAP-012 | Todo Snapshot & Actuals | Snapshot freeze + plan vs actuals comparison | base |
| CAP-013 | Self-Check & Completeness | D/M/R/T layered self-check lists | base |
| CAP-014 | Excel Generation | 8 doc-sheet structures/columns/validation/formulas | base |
| CAP-015 | Version & Compatibility | Workspace health check + compatibility mode + migration | base |
| CAP-016 | Update Trigger & Intent Detection | Four-level trigger + permission tiers | base |
| CAP-017 | Skill Governance | Change tickets (CR/IA/RR) + AP review + regression guard | base |
| CAP-018 | Blueprint & External Review | Architecture decisions + capability matrix + review entry | base |
| CAP-019 | Domain Glossary | Terminology normalization + confidence + correction + confirm-learning | v1.7.0 |
| CAP-020 | Project Initialization Wizard | Six-step guided setup with progress memory & resume | v1.8.0 |
| CAP-021 | Information Completeness Inspection | 7-layer missing-info check, P0-P3 tiered reminders | v1.8.0 |
| CAP-022 | Entry Router & Knowledge Navigation | SKILL.md as entry router; rules moved to references | v1.8.0 |
| CAP-023 | PM Profile & Preference Learning | Habit learning + preference-adapted output | v1.9.0 |
| CAP-024 | Historical Plan Import & Change/Delay Track | Batch plan import + change/delay counting & tracking | v1.10.0 |
| CAP-025 | Proactive Change & Pending Window | Proactive changes + human-confirm model; pending not counted as overdue | v1.11.0 |
| CAP-026 | Change Log Tiered Archive | Active/archive tiering with auto month navigation | v1.11.0 |
| — (CAP extension) | Requirement Intelligence (RI) | Cross-source requirement extraction/merge/scope判定/three-level index retrieval; v1.16.0 extends contract scope (portfolio/requirements tiered storage + contract-register + scope_level routing + contract_refs) | v1.15.0 |

## Key Mechanisms

- **Entity Cascade Propagation** (v1.13.0): 6 entity rule files carry `§cascade rules` with AUTO / CHECK / SUGGEST actions; conflicts flagged ⚠ for PM decision.
- **Standard Workflow Data Paths** (v1.14.0): 00 §9 predefines WF-1~WF-6 high-frequency read/write file sequences; §9.1 ensures predefinition doesn't weaken judgmental reasoning. 05 §2.5 Quick Update route table mirrors Quick Query.
- **Requirement Intelligence (RI)** (v1.15.0): 07 §8 ATOM→Canonical→REQ three-layer model, dual-layer source classification (6 fixed source_category + project-extensible source_type), three-level index + graded loading + P1 semantic fallback, answers "is this requirement in contract/bidding/approval scope?" with evidence chain; PM notes project-notes dual-entry. Workspace schema 0.7.0.
- **Contract Scope & Many-to-Many Mapping** (v1.16.0): closes the "contract↔sub-project many-to-many" gap — adds portfolio-level `portfolio/requirements/` cross-source storage and `contract-register.md` (scope_level: portfolio/project/supplement, parent_contract_id, coverage, document-cluster links); ATOM/Canonical storage follows contract scope_level (supplements follow parent contract); contract-dimensional scope判定 (Canonical adds companion field contract_refs; scope_scope 5-value enum unchanged); RI four-step retrieval routing (read register → resolve contract → target-tier three-level index → output contract_refs); contract-change three-level cascade (reuses 08 scope/cost/requirement, no enum change); fixes CR-20260813-001 legacy script gaps. Workspace schema 0.8.0.
- **Update-Intent Recognition** (v1.10.0): SKILL.md as router auto-routes by intent; supports batch handling.
- **Information-Completeness Inspection** (v1.8.0): proactively scans missing info, P0-P3 tiered reminders, silent-capable.
- **PM Profile Learning** (v1.9.0): passive observe → pending → confirmed; adapts personal habits.
- **Proactive Change + Human Confirmation** (v1.11.0): low/medium-risk changes written to fact source and registered as pending-changes until confirmed; major changes trigger full regression.

## Directory Layout

```
ChronoPM Skill/
├── SKILL.md              # Core contract (entry router)
├── SKILL_BLUEPRINT.md    # Capability blueprint
├── skill.json            # Skill metadata
├── VERSION               # Version number
├── CHANGELOG.md          # Change history
├── QODER_RULES.md        # Qoder env config entry
├── assets/               # Templates & resources
├── governance/           # Governance contracts + change control (CR/IA/RR/baselines) + planning docs
├── references/           # Rule files (00~21, 22 rules)
├── scripts/              # Automation scripts (init/migrate/sync_version)
└── tests/                # Regression suite (198 cases)
```

## Version Info

| Item | Value |
|---|---|
| Skill version | 1.16.0 |
| Workspace Schema | 0.8.0 |
| Default mode | portfolio |
| Rule files | 22 (00~21) |
| Regression cases | 198 |
| Capabilities | 26 (CAP-001~026) |

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
