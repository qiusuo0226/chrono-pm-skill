#!/usr/bin/env python3
"""ChronoPM 工作区构建主流程。

职责：编排单项目 / 项目集两种模式的工作区创建流程。函数体在
CR-20260810-001 中由 scripts/init_workspace.py 原样迁移，保证行为零变化。
"""

import shutil
from pathlib import Path

from .config import (
    ALL_TEMPLATE_FILES,
    PORTFOLIO_DIRS,
    PORTFOLIO_FACT_SOURCE_FILES,
    PORTFOLIO_INDEX_TEMPLATES,
    SINGLE_FACT_SOURCE_FILES,
    SINGLE_PROJECT_DIRS,
    SUB_PROJECT_DIRS,
    SUB_PROJECT_FACT_SOURCE_FILES,
    SUB_PROJECT_INDEX_TEMPLATES,
)
from .file_registry import (
    create_ai_log,
    create_brief_file,
    create_context_file,
    create_iteration_register,
    create_lessons_file,
    create_migration_log,
    create_outputs_dir,
    create_pm_profile,
    create_project_rules,
    create_ri_skeleton,
    create_skill_version,
    generate_portfolio_readme,
    generate_single_readme,
)
from .template_renderer import (
    create_continuity_files,
    create_dirs,
    create_fact_sources,
    create_indexes,
    get_templates_dir,
)


def create_single_project(project_root: str, project_name: str = ""):
    """在项目根目录下创建 ai/ 工作区（单项目模式）"""
    ai_dir = Path(project_root) / "ai"

    if ai_dir.exists():
        print(f"警告: {ai_dir} 已存在")
        response = input("是否覆盖? (y/N): ")
        if response.lower() != 'y':
            print("取消初始化")
            return

    templates_dir = get_templates_dir()

    # 1. 创建目录结构
    print("创建目录结构...")
    create_dirs(ai_dir, SINGLE_PROJECT_DIRS)

    # 2. 复制模板文件到 templates/
    print("\n复制模板文件...")
    for template_file in ALL_TEMPLATE_FILES:
        src = templates_dir / template_file
        dst = ai_dir / "templates" / template_file
        if src.exists():
            shutil.copy2(src, dst)

    # 3. 创建事实源文件
    print("\n创建事实源文件...")
    create_fact_sources(ai_dir, SINGLE_FACT_SOURCE_FILES, templates_dir)

    # 4. 创建索引文件
    print("\n创建索引文件...")
    create_indexes(ai_dir, SUB_PROJECT_INDEX_TEMPLATES, project_name)

    # 5. 创建经验教训文件
    print("\n创建经验库...")
    create_lessons_file(ai_dir, project_name)

    # 6. 创建 AI 操作日志
    print("\n创建 AI 操作日志...")
    create_ai_log(ai_dir, project_name, "project")

    # 7. 创建项目简报文件
    print("\n创建项目简报文件...")
    create_brief_file(ai_dir, project_name, is_portfolio=False)

    # 8. 创建项目上下文文件
    print("\n创建项目上下文文件...")
    create_context_file(ai_dir, project_name, is_portfolio=False)

    # 8b. 创建迭代登记册
    print("\n创建迭代登记册...")
    create_iteration_register(ai_dir, project_name, is_portfolio=False)
    print("  create plans/iteration-register.md")

    # 8c. 创建跨源需求归集（RI）骨架（schema 0.7.0）
    print("\n创建 RI 骨架文件...")
    create_ri_skeleton(ai_dir)
    print("  create requirements/canonical + requirements/atoms (L1/L2/L3)")

    # 9. 创建项目级规则文件
    print("\n创建项目级规则文件...")
    create_project_rules(ai_dir, project_name, is_portfolio=False)

    # 9c. 创建 PM 偏好档案
    print("\n创建 PM 偏好档案...")
    create_pm_profile(project_root, "single")

    # 9b. 创建 continuity 目录
    print("\n创建阶段衔接目录...")
    create_continuity_files(ai_dir, project_name)
    print("  create continuity/project-lineage.md")
    print("  create continuity/legacy-sources.md")
    print("  create continuity/carryover-register.md")
    print("  create continuity/import-log.md")

    # 10. 创建 outputs 目录
    print("\n创建输出物目录...")
    create_outputs_dir(project_root, project_name)
    print("  create outputs/index.md")
    print("  create outputs/.templates/manifest-template.md")

    # 11. 创建版本文件
    print("\n创建版本文件...")
    create_skill_version(ai_dir, "single")
    create_migration_log(ai_dir)
    print("  create .skill-version.json")
    print("  create logs/migration-log.md")

    # 11. 创建 README.md
    print("\n创建 README.md...")
    readme_path = ai_dir / "README.md"
    readme_path.write_text(generate_single_readme(project_name), encoding="utf-8")

    # 完成
    print(f"\n{'='*60}")
    print(f"ChronoPM 单项目工作区初始化完成!")
    print(f"{'='*60}")
    print(f"项目名称: {project_name or '(未设置)'}")
    print(f"工作区路径: {ai_dir}")
    print(f"\n下一步:")
    print(f"  1. 对 AI 说：初始化项目")
    print(f"  2. AI 将引导你录入合同、项目、迭代、需求、资源和里程碑信息")
    print(f"  3. 录入完成后，AI 会自动填充 project-context、project-brief、")
    print(f"     project-index、iteration-register 等文件")
    print(f"  4. 也可手动填写 context/project-context.md、plans/budget.md、")
    print(f"     milestones/milestone-board.md、prompts/project-rules.md")


def create_portfolio(project_root: str, portfolio_name: str, sub_projects: list):
    """在项目根目录下创建 ai/portfolio/ + ai/projects/ 工作区（项目集模式）"""
    ai_dir = Path(project_root) / "ai"

    if ai_dir.exists():
        print(f"警告: {ai_dir} 已存在")
        response = input("是否覆盖? (y/N): ")
        if response.lower() != 'y':
            print("取消初始化")
            return

    templates_dir = get_templates_dir()

    # === 1. 创建项目集级目录结构 ===
    portfolio_dir = ai_dir / "portfolio"
    print("创建项目集级目录结构...")
    create_dirs(portfolio_dir, PORTFOLIO_DIRS)

    # === 2. 创建项目集级事实源文件 ===
    print("\n创建项目集级事实源文件...")
    create_fact_sources(portfolio_dir, PORTFOLIO_FACT_SOURCE_FILES, templates_dir)

    # === 2b. 创建项目集级跨源需求归集（RI）骨架（schema 0.8.0，CR-20260813-002）===
    print("\n创建项目集级 RI 骨架文件...")
    create_ri_skeleton(portfolio_dir, base="requirements")
    print("  create portfolio/requirements/canonical + atoms (L1/L2/L3)")

    # === 3. 创建项目集级索引文件 ===
    print("\n创建项目集级索引文件...")
    create_indexes(portfolio_dir, PORTFOLIO_INDEX_TEMPLATES, portfolio_name)

    # === 4. 创建项目集级简报文件 ===
    print("\n创建项目集简报文件...")
    create_brief_file(portfolio_dir, portfolio_name, is_portfolio=True, sub_projects=sub_projects)

    # === 4.5 创建项目集级上下文文件 ===
    print("\n创建项目集上下文文件...")
    create_context_file(portfolio_dir, portfolio_name, is_portfolio=True)

    # === 5. 创建项目集级规则文件 ===
    print("\n创建项目集级规则文件...")
    create_project_rules(portfolio_dir, portfolio_name, is_portfolio=True)

    # === 5b. 创建 PM 偏好档案 ===
    print("\n创建 PM 偏好档案...")
    create_pm_profile(project_root, "portfolio")

    # === 6. 创建项目集级 AI 操作日志 ===
    print("\n创建项目集级 AI 操作日志...")
    create_ai_log(portfolio_dir, portfolio_name, "portfolio")

    # === 7. 创建各子项目目录结构 ===
    print(f"\n创建 {len(sub_projects)} 个子项目目录结构...")

    for idx, sub_name in enumerate(sub_projects, 1):
        prj_id = f"PRJ-{idx:03d}"
        sub_dir = ai_dir / "projects" / sub_name

        print(f"\n  [{prj_id}] {sub_name}")

        # 7a. 创建子项目目录
        create_dirs(sub_dir, SUB_PROJECT_DIRS)

        # 7b. 创建事实源文件
        create_fact_sources(sub_dir, SUB_PROJECT_FACT_SOURCE_FILES, templates_dir)

        # 7b.1 创建跨源需求归集（RI）骨架（schema 0.7.0）
        create_ri_skeleton(sub_dir)

        # 7c. 创建索引文件
        create_indexes(sub_dir, SUB_PROJECT_INDEX_TEMPLATES, sub_name)

        # 7d. 创建经验教训文件
        create_lessons_file(sub_dir, sub_name)

        # 7e. 创建 AI 操作日志
        create_ai_log(sub_dir, sub_name, "project")

        # 7f. 创建子项目上下文文件
        create_context_file(sub_dir, sub_name, is_portfolio=False)

        # 7g. 创建子项目迭代登记册
        create_iteration_register(sub_dir, sub_name, is_portfolio=False)
        print(f"    create plans/iteration-register.md")

        # 7h. 创建子项目级规则文件
        create_project_rules(sub_dir, sub_name, is_portfolio=False)

        print(f"    完成: ai/projects/{sub_name}/")

    # === 8. 复制所有模板到 ai/templates/ ===
    print("\n复制模板文件...")
    templates_target = ai_dir / "templates"
    templates_target.mkdir(parents=True, exist_ok=True)
    for template_file in ALL_TEMPLATE_FILES:
        src = templates_dir / template_file
        dst = templates_target / template_file
        if src.exists():
            shutil.copy2(src, dst)

    # === 8b. 创建 continuity 目录 ===
    print("\n创建阶段衔接目录...")
    create_continuity_files(ai_dir, portfolio_name)
    print("  create continuity/project-lineage.md")
    print("  create continuity/legacy-sources.md")
    print("  create continuity/carryover-register.md")
    print("  create continuity/import-log.md")

    # === 9. 创建输出物目录 ===
    print("\n创建输出物目录...")
    create_outputs_dir(project_root, portfolio_name)
    print("  create outputs/index.md")
    print("  create outputs/.templates/manifest-template.md")

    # === 10. 创建版本文件 ===
    print("\n创建版本文件...")
    (ai_dir / "logs").mkdir(parents=True, exist_ok=True)
    create_skill_version(ai_dir, "portfolio")
    create_migration_log(ai_dir)
    print("  create .skill-version.json")
    print("  create logs/migration-log.md")

    # === 10. 创建 README.md ===
    print("\n创建 README.md...")
    readme_path = ai_dir / "README.md"
    readme_path.write_text(
        generate_portfolio_readme(portfolio_name, sub_projects), encoding="utf-8"
    )

    # 完成
    print(f"\n{'='*60}")
    print(f"ChronoPM 项目集工作区初始化完成!")
    print(f"{'='*60}")
    print(f"项目集名称: {portfolio_name}")
    print(f"子项目数量: {len(sub_projects)}")
    for idx, sub_name in enumerate(sub_projects, 1):
        print(f"  PRJ-{idx:03d}: {sub_name}")
    print(f"\n工作区路径: {ai_dir}")
    print(f"\n下一步:")
    print(f"  1. 对 AI 说：初始化项目")
    print(f"  2. AI 将引导你录入合同、项目、迭代、需求、资源和里程碑信息")
    print(f"  3. 录入完成后，AI 会自动填充 project-context、project-brief、")
    print(f"     project-index、iteration-register、resource-register 等文件")
    print(f"  4. 也可手动填写 portfolio/context/project-index.md、")
    print(f"     portfolio/context/project-context.md、")
    print(f"     portfolio/resources/resource-register.md")
