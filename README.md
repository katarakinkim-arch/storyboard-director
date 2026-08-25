# Storyboard Director

一套面向商业 AI 短剧、AI 漫剧和 AI 视频制作的故事驱动分镜 Skill。

2.0 版的核心不是“给每句台词套一个镜头”，而是先读懂：谁想要什么、受到什么阻碍、观众在等什么、场景发生了什么变化，再选择适合这一本戏的景别、机位、构图、运镜和剪辑。

## 主要能力

- 先提炼故事引擎、戏剧节拍、观众情感站位和场景视觉引擎；
- 保留原剧情及全部台词、OS、VO，不删改、不换序；
- 一行独立台词对应一个新镜头，但动作、道具和场面调度跨镜延续；
- 防止对话退化为连续说话人正脸或机械正反打；
- 根据情感、喜剧、权力对峙、悬疑、动作和奇观分别选择镜头方法；
- 保持人物站位、180°轴线、视线、动作、伤势和道具连续；
- 将文学描写转成演员与 AI 模型可以执行的行为；
- 每个单元不超过30秒，不设最低镜头数，不设固定运动镜头比例；
- 默认正常语速5秒约18—19个中文字，并按情绪动态调整；
- 固定输出时长、画面、运镜、剪辑／动态效果和台词；
- 案例按“标杆／选择性参考／反例”分级，明确是否允许学习格式；
- 默认只使用通用导演方法，用户点名或关键高光才调用导演卡。

## 适合的任务

- 短剧、漫剧和剧情视频分镜；
- 对话、对峙、暧昧和喜剧场景；
- 悬疑调查、追逐、战斗、怪物和巨物揭示；
- 电影片头、一镜到底和材质化视觉段落。

只需修改剧本、评价剧情、写小说、总结剧情或润色台词时，不应使用本 Skill。

## 安装

向 Codex 发送：

```text
请从 https://github.com/katarakinkim-arch/storyboard-director 安装这个 Skill。
```

也可以手动克隆到个人 Skills 目录：

```bash
git clone https://github.com/katarakinkim-arch/storyboard-director.git ~/.codex/skills/storyboard-director
```

如果已有同名目录，请先备份，避免覆盖个人修改。安装或更新后，在新的 Codex 任务中调用，确保加载最新版。

## 使用

明确调用：

```text
$storyboard-director

请把下面的完整短剧脚本拆成适合 AI 视频制作的正式分镜。
重点讲清人物关系变化，保留全部台词，结尾留下自然钩子。

（粘贴剧本与参考资料）
```

也可以直接说“请把这份剧本拆成分镜”。若希望确保调用本 Skill，优先写 `$storyboard-director`。

建议一并提供：人物与场景参考图、空间布局、道具与机制设定、前后集衔接、期望画幅／模型，以及希望重点强化的角色或情绪。资料不足但不影响剧情时，Skill 会合理补足；缺失信息会实质改变剧情时才询问。

## 默认输出

先交代全场站位与轴线，再按自然戏剧阶段划分不超过30秒的单元：

```text
镜头1：
【时长：0-2秒】
画面：……
运镜：……
剪辑/动态效果：……
台词：……
```

每个单元从0秒开始，内部时间连续；后一镜起点等于前一镜终点。无台词写 `台词：无`，没有特殊效果写 `剪辑/动态效果：无`。

## 目录结构

```text
storyboard-director/
├── VERSION
├── SKILL.md
├── references/
│   ├── story-first-directing.md
│   ├── technical-continuity.md
│   ├── dialogue-visual-storytelling.md
│   ├── suspense-action-spectacle.md
│   ├── director-rules.md
│   ├── storyboard-example-library.md
│   └── storyboard-regression-library.md
├── agents/openai.yaml
├── scripts/manage_release.py
├── tests/
└── skills/storyboard-director/  # 由同步脚本生成的安装副本
```

- `SKILL.md`：故事优先工作流、硬约束、引用路由和输出契约；
- `story-first-directing.md`：故事命题、观众站位、视觉引擎、权力与镜头稳定度；
- `technical-continuity.md`：台词、计时、轴线、动作、道具和字段检查；
- `dialogue-visual-storytelling.md`：让对白发生在持续行动和多人关系中；
- `suspense-action-spectacle.md`：悬疑升级、动作因果、巨物尺度和撞击反馈；
- `director-rules.md`：开场、出场、高光、爆点、喜剧、转场、系统和钩子的按需工具箱；
- `storyboard-example-library.md`：有等级、有学习边界的收藏案例；
- `storyboard-regression-library.md`：只用于维护和测试的失败模式。

## 更新与发布

根目录中的 `SKILL.md`、`agents/` 和 `references/` 是唯一编辑源。不要直接修改 `skills/storyboard-director/`。

```bash
python scripts/manage_release.py sync
python scripts/manage_release.py check
python -m unittest discover -s tests -v
```

准备新版本：

```bash
python scripts/manage_release.py release 2.0.0
```

该命令会更新 `VERSION` 与插件清单、重新生成安装副本并检查同步状态。

## 如何继续完善

出现问题时，不要只追加一句绝对规则。先记录：失败表现、故事误读、触发条件、例外和回归检查，再决定修改核心流程、场景方法还是技术约束。

收藏新案例时应同时记录：

- 用户评价等级；
- 只学什么、不学什么；
- 是否允许学习格式；
- 哪些内容由用户人工修改；
- 适用场景与可复用方法。

私人案例迁入私有仓库不在当前版本范围内。
