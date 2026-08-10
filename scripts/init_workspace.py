#!/usr/bin/env python3
"""
ChronoPM 项目工作区初始化脚本（入口壳）

支持两种模式：
  1. 单项目模式：在指定目录下创建 ai/ 目录结构
  2. 项目集模式：在指定目录下创建 ai/portfolio/ + ai/projects/{子项目}/ 结构

用法:
    # 单项目模式
    python init_workspace.py --project-root /path/to/project --project-name "项目名"

    # 项目集模式
    python init_workspace.py --project-root /path/to/portfolio \\
        --mode portfolio \\
        --portfolio-name "江苏省市监重构项目集" \\
        --sub-projects "全链通重构,企业通重构,信用监管登记注册重构"

重构说明（CR-20260810-001）：本文件已由 1269 行单体脚本重构为入口壳，
实际逻辑拆分至 scripts/chronopm_init/ 包。CLI 参数与生成物目录结构完全不变。
"""

import argparse

from chronopm_init.file_registry import create_glossary, create_pm_profile
from chronopm_init.validators import validate_and_handle
from chronopm_init.workspace_builder import create_portfolio, create_single_project


def main():
    parser = argparse.ArgumentParser(description="ChronoPM 项目工作区初始化")
    parser.add_argument(
        "--project-root",
        required=True,
        help="项目根目录路径",
    )
    parser.add_argument(
        "--mode",
        choices=["single", "portfolio"],
        default="single",
        help="初始化模式：single=单项目，portfolio=项目集（默认: single）",
    )
    parser.add_argument(
        "--project-name",
        default="",
        help="项目名称（单项目模式）",
    )
    parser.add_argument(
        "--portfolio-name",
        default="",
        help="项目集名称（项目集模式）",
    )
    parser.add_argument(
        "--sub-projects",
        default="",
        help="子项目列表，逗号分隔（项目集模式），如：全链通重构,企业通重构,信用监管登记注册重构",
    )

    parser.add_argument(
        "--glossary",
        action="store_true",
        default=False,
        help="初始化时创建领域词库模板（内置用户已确认初始词条），不自动抽取历史术语",
    )

    parser.add_argument(
        "--profile",
        action="store_true",
        default=False,
        help="显式创建 PM 偏好档案（新工作区默认自动创建，此参数用于单独补建）",
    )

    args = parser.parse_args()

    if args.mode == "portfolio":
        sub_projects = validate_and_handle(
            args.mode, args.portfolio_name, args.sub_projects
        )
        create_portfolio(args.project_root, args.portfolio_name, sub_projects)
        if args.glossary:
            create_glossary(args.project_root, "portfolio")
        if args.profile:
            create_pm_profile(args.project_root, "portfolio")
    else:
        create_single_project(args.project_root, args.project_name)
        if args.glossary:
            create_glossary(args.project_root, "single")
        if args.profile:
            create_pm_profile(args.project_root, "single")


if __name__ == "__main__":
    main()
