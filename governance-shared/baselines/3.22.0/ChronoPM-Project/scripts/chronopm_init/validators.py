#!/usr/bin/env python3
"""ChronoPM 命令行参数校验。

职责：校验 init_workspace.py 的 CLI 参数。函数体在 CR-20260810-001 中
由 scripts/init_workspace.py 主入口的校验逻辑原样迁移，保证行为零变化
（包括错误提示顺序与 exit 行为）。
"""

import sys


def parse_sub_projects(sub_projects_str: str) -> list:
    """将逗号分隔的子项目字符串解析为列表"""
    return [s.strip() for s in sub_projects_str.split(",") if s.strip()]


def validate_and_handle(mode: str, portfolio_name: str, sub_projects: str):
    """校验参数；不合法时打印对应错误并退出。

    与原 init_workspace.py 主入口逻辑一致：
    - portfolio 模式缺 --portfolio-name 时打印错误并 exit(1)
    - portfolio 模式缺 --sub-projects 时打印错误并 exit(1)
    返回解析后的 sub_projects 列表（仅当校验通过时）。
    """
    if mode == "portfolio":
        if not portfolio_name:
            print("错误: 项目集模式需要 --portfolio-name 参数")
            sys.exit(1)
        if not sub_projects:
            print("错误: 项目集模式需要 --sub-projects 参数")
            sys.exit(1)
        return parse_sub_projects(sub_projects)
    return []
