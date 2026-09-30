#!/usr/bin/env python3
"""
ChronoPM 项目工作区初始化脚本（入口壳）

v3.0.0：init 仅单项目模式。集工作区不由 init 创建，跨项目归集由本包 portfolio-skill/ 承载。

用法:
    python init_workspace.py --project-root /path/to/project --project-name "项目名"

--mode portfolio 将被拒绝。集工作区不由 init 创建，跨项目归集由本包 portfolio-skill/ 承载。

重构说明（CR-20260810-001）：本文件已由 1269 行单体脚本重构为入口壳，
实际逻辑拆分至 scripts/chronopm_init/ 包。
"""

import argparse
import sys

from chronopm_init.file_registry import create_glossary, create_pm_profile
from chronopm_init.workspace_builder import create_single_project


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
        help="初始化模式：仅 single。portfolio 已移除。跨项目归集由本包 portfolio-skill/ 承载，init 不建集工作区",
    )
    parser.add_argument(
        "--project-name",
        default="",
        help="项目名称（单项目模式）",
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
        print("错误: 集工作区不由 init 创建。跨项目归集由本包 portfolio-skill/ 承载，init 仅 single")
        sys.exit(1)

    create_single_project(args.project_root, args.project_name)
    if args.glossary:
        create_glossary(args.project_root)
    if args.profile:
        create_pm_profile(args.project_root)


if __name__ == "__main__":
    main()
