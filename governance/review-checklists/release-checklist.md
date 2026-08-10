# Release Checklist

发布前必须确认所有检查项：

## Change Control

- [ ] 是否有 Change Request？
- [ ] 是否有明确可验证目标？
- [ ] 是否没有混入无关改动？
- [ ] 是否有 Impact Analysis？
- [ ] 是否已获得用户确认？

## Compatibility

- [ ] 是否影响核心契约？
- [ ] 是否影响 workspace schema？
- [ ] 是否需要迁移脚本？
- [ ] 是否影响旧工作区？

## Regression

- [ ] 是否运行正向用例？
- [ ] 是否运行反向用例？
- [ ] 是否运行旧功能回归用例？
- [ ] 是否没有失败用例？

## Documentation

- [ ] 是否更新 VERSION？
- [ ] 是否更新 skill.json？
- [ ] 是否更新 CHANGELOG.md？
- [ ] 是否更新 SKILL.md？
- [ ] 是否生成 regression report？
- [ ] SKILL_BLUEPRINT.md 是否已按版本级别更新（必更/应更/免更）？
- [ ] skill.json blueprint.lastVersion 是否与 VERSION 一致？
- [ ] CHANGELOG 是否标注 Blueprint Impact？

## Baseline

- [ ] 是否创建新版本基线？
- [ ] 是否保留上一版本回滚路径？

## Copy

- [ ] 是否复制到灵犀安装目录？
