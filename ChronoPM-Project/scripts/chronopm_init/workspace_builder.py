#!/usr/bin/env python3
"""ChronoPM 工作区构建主流程。

职责：编排单项目工作区创建流程。函数体在
CR-20260810-001 中由 scripts/init_workspace.py 原样迁移，保证行为零变化。
v3.0.0（P-14）：create_portfolio 项目集初始化分支已删除，init 仅产
单项目工作区；集工作区归 ChronoPM-Portfolio 伴生包（无 init 脚本）。
存量 portfolio 工作区的读取/迁移仍由 scripts/migrate_workspace.py 承载。
"""

import shutil
from pathlib import Path

from .config import (
    ALL_TEMPLATE_FILES,
    SINGLE_FACT_SOURCE_FILES,
    SINGLE_PROJECT_DIRS,
    SINGLE_PROJECT_INDEX_TEMPLATES,
    resolve_template_path,
)
from .file_registry import (
    create_ai_log,
    create_brief_file,
    create_context_file,
    create_lessons_file,
    create_migration_log,
    create_outputs_dir,
    create_pm_profile,
    create_project_rules,
    create_ri_skeleton,
    create_skill_version,
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
    # 四份 source-* 走 resolve_template_path（能力目录）；其余仍在 Project templates。
    # 不预建 pm-decisions.md / logs/ops 实例。
    print("\n复制模板文件...")
    for template_file in ALL_TEMPLATE_FILES:
        src = resolve_template_path(template_file)
        dst = ai_dir / "templates" / template_file
        if src.exists():
            shutil.copy2(src, dst)
        else:
            print(f"  ⚠️ 模板不存在，跳过: {template_file} ({src})")

    # 3. 创建事实源文件
    print("\n创建事实源文件...")
    create_fact_sources(ai_dir, SINGLE_FACT_SOURCE_FILES, templates_dir)

    # 4. 创建索引文件
    print("\n创建索引文件...")
    create_indexes(ai_dir, SINGLE_PROJECT_INDEX_TEMPLATES, project_name)

    # 5. 创建经验教训文件
    print("\n创建经验库...")
    create_lessons_file(ai_dir, project_name)

    # 6. 创建 AI 操作日志
    print("\n创建 AI 操作日志...")
    create_ai_log(ai_dir, project_name, "project")

    # 7. 创建项目简报文件
    print("\n创建项目简报文件...")
    create_brief_file(ai_dir, project_name)

    # 8. 创建项目上下文文件
    print("\n创建项目上下文文件...")
    create_context_file(ai_dir, project_name)

    # 8b. 创建跨源需求归集（RI）骨架（schema 0.7.0）
    # v2.0.0：迭代登记册已删除，PLAN 计划文件由 AI 按需创建
    print("\n创建 RI 骨架文件...")
    create_ri_skeleton(ai_dir)
    print("  create requirements/canonical + requirements/atoms (L1/L2/L3)")

    # 9. 创建项目级规则文件
    print("\n创建项目级规则文件...")
    create_project_rules(ai_dir, project_name)

    # 9c. 创建 PM 偏好档案
    print("\n创建 PM 偏好档案...")
    create_pm_profile(project_root)

    # 9b. 创建 continuity 目录
    print("\n创建阶段衔接目录...")
    create_continuity_files(ai_dir, project_name)
    print("  create context/project-lineage.md")
    print("  create context/legacy-sources.md")
    print("  create context/import-log.md")

    # 10. 创建 outputs 目录（v2.1.0：位于 ai/outputs/）
    print("\n创建输出物目录...")
    create_outputs_dir(project_root, project_name)
    print("  create ai/outputs/index.md")
    print("  create ai/outputs/.templates/manifest-template.md")

    # 11. 创建版本文件
    print("\n创建版本文件...")
    create_skill_version(ai_dir, "single")
    create_migration_log(ai_dir)
    print("  create .skill-version.json")
    print("  create logs/migration-log.md")

    # 11. 创建 README.md
    print("\n创建 README.md...")
    readme_path = ai_dir / "README.md"
    if readme_path.exists():
        print("  README.md 已存在，跳过（不覆盖）")
    else:
        readme_path.write_text(generate_single_readme(project_name), encoding="utf-8")

    # 完成
    print(f"\n{'='*60}")
    print(f"ChronoPM 单项目工作区初始化完成!")
    print(f"{'='*60}")
    print(f"项目名称: {project_name or '(未设置)'}")
    print(f"工作区路径: {ai_dir}")
    print(f"\n下一步:")
    print(f"  1. 对 AI 说：初始化项目")
    print(f"  2. AI 将引导你录入合同、项目、计划、需求、资源信息")
    print(f"  3. 录入完成后，AI 会自动填充 project-context、project-brief、")
    print(f"     project-index、PLAN 计划文件等")
    print(f"  4. 也可手动填写 context/project-context.md、project-info/budget.md、")
    print(f"     prompts/project-rules.md")
