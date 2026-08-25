# Storyboard Director 2.0：故事优先升级实施计划

**目标：** 将 Skill 从“按镜头规则生成”升级为“先理解故事、再选择镜头方法”，同时保留台词、时长、连续性与输出格式等生产硬约束。

**单一源：** 只编辑仓库根目录的 `SKILL.md`、`agents/`、`references/`；通过 `scripts/manage_release.py` 自动同步 `skills/storyboard-director/`。

## 任务一：建立故事优先核心

- 重写 `SKILL.md`，把故事理解、戏剧变化、观众情感站位和场景视觉引擎放在镜头技法之前。
- 将台词、时间、轴线、连续性、AI 可执行性保留为硬约束。
- 将导演卡、比例、机位建议降为按需工具，不作为创意生成器。

## 任务二：拆分按需参考模块

- 新建 `references/story-first-directing.md`：故事引擎、节拍、可选分析工具、关键镜头择优。
- 新建 `references/dialogue-visual-storytelling.md`：对话中的持续动作、道具、空间关系和多人调度。
- 新建 `references/suspense-action-spectacle.md`：悬疑递进、动作因果链、巨物揭示和撞击反馈。
- 新建 `references/technical-continuity.md`：时长、台词、轴线、动作、道具和输出契约。
- 精简 `references/director-rules.md` 为特殊场景工具箱。

## 任务三：案例分级与回归约束

- 为案例库建立“标杆／选择性参考／反例”分级，并记录“只学分镜／可学格式”等边界。
- 明确用户人工改动不归因于 AI，也不自动升级为全局规则。
- 新建 `references/storyboard-regression-library.md`，保存宫门对话和洞府后半段创意塌缩等失败模式。

## 任务四：文档、测试与版本

- 更新 `README.md` 与 `agents/openai.yaml`。
- 增加契约测试，防止重新出现固定运动比例、全量规则强制加载、案例格式误学等问题。
- 发布 `2.0.0`，同步插件副本。

## 任务五：验证与发布

- 运行单元测试、Skill 校验、插件校验、同步检查与文本差异检查。
- 提交并推送 GitHub `main`。
- 备份旧本地安装，重新安装 GitHub 版本，核对版本和文件清单。
