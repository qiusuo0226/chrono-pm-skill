#!/usr/bin/env python3
"""ChronoPM 模板渲染与基础文件辅助函数。

职责：模板目录定位、文件复制、目录创建、事实源与索引文件生成、
continuity 阶段衔接文件生成。函数体在 CR-20260810-001 中由
scripts/init_workspace.py 原样迁移，保证行为零变化。
"""

import shutil
from pathlib import Path

from .config import ALL_TEMPLATE_FILES  # noqa: F401  （供外部按需引用）


def get_templates_dir():
    """获取 Skill 包中的模板目录"""
    skill_root = Path(__file__).parent.parent.parent
    return skill_root / "assets" / "templates"


def copy_template(src_dir: Path, target_path: Path, template_name: str):
    """从模板目录复制文件到目标路径"""
    src = src_dir / template_name
    if src.exists() and not target_path.exists():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target_path)
        return True
    return False


def create_dirs(base_dir: Path, dirs: list):
    """创建目录结构"""
    for dir_path in dirs:
        full_path = base_dir / dir_path
        full_path.mkdir(parents=True, exist_ok=True)


def create_fact_sources(base_dir: Path, fact_files: dict, templates_dir: Path):
    """创建事实源文件"""
    for target_path, template_name in fact_files.items():
        dst = base_dir / target_path
        copy_template(templates_dir, dst, template_name)


def create_indexes(base_dir: Path, index_templates: dict, name: str):
    """创建索引文件"""
    for index_path, content_template in index_templates.items():
        dst = base_dir / index_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        content = content_template.format(name=name)
        dst.write_text(content, encoding="utf-8")


def create_continuity_files(ai_dir: Path, project_name: str):
    """在 ai/continuity/ 下创建阶段衔接文件"""
    continuity_dir = ai_dir / "continuity"
    continuity_dir.mkdir(parents=True, exist_ok=True)

    templates_dir = get_templates_dir()

    # 创建阶段谱系
    lineage_path = continuity_dir / "project-lineage.md"
    if not lineage_path.exists():
        copy_template(templates_dir, lineage_path, "project-lineage-template.md")

    # 创建历史来源登记
    legacy_path = continuity_dir / "legacy-sources.md"
    if not legacy_path.exists():
        copy_template(templates_dir, legacy_path, "legacy-sources-template.md")

    # 创建结转事项登记册
    carryover_path = continuity_dir / "carryover-register.md"
    if not carryover_path.exists():
        copy_template(templates_dir, carryover_path, "carryover-register-template.md")

    # 创建导入日志
    import_log_path = continuity_dir / "import-log.md"
    if not import_log_path.exists():
        copy_template(templates_dir, import_log_path, "import-log-template.md")
