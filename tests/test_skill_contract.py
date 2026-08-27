from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")
REFS = ROOT / "references"


class StoryboardSkillContractTests(unittest.TestCase):
    def test_single_priority_system_and_conflict_resolver(self) -> None:
        self.assertEqual(SKILL.count("## 冲突裁决顺序"), 1)
        self.assertIn("其他参考文件不得另设优先级", SKILL)
        self.assertIn("与剧情准确、表演所有权、空间连续或 AI 可执行性冲突时，前者必须让步", SKILL)

    def test_only_two_normative_reference_sources(self) -> None:
        self.assertIn("硬约束，仅来自本文件和 `references/core-story-performance.md`、`references/continuity-timing-output.md`", SKILL)
        core = (REFS / "core-story-performance.md").read_text(encoding="utf-8")
        technical = (REFS / "continuity-timing-output.md").read_text(encoding="utf-8")
        self.assertIn("唯一规范来源", core)
        self.assertIn("唯一技术规范来源", technical)

    def test_legacy_files_are_redirects_not_duplicate_rulebooks(self) -> None:
        mapping = {
            "story-first-directing.md": "core-story-performance.md",
            "technical-continuity.md": "continuity-timing-output.md",
            "storyboard-quality-gate.md": "quality-check.md",
        }
        for name, target in mapping.items():
            text = (REFS / name).read_text(encoding="utf-8")
            self.assertIn("不再维护独立", text)
            self.assertIn(target, text)
            self.assertLess(len(text), 500)

    def test_method_and_case_libraries_are_non_normative(self) -> None:
        files = (
            "dialogue-visual-storytelling.md", "suspense-action-spectacle.md",
            "transitions-dynamics-depth.md", "director-rules.md",
            "anime-action-language.md", "pixar-story-rhythm-comedy.md",
            "director-camera-language-library.md", "user-curated-camera-moves.md",
            "user-curated-visual-sequences.md", "user-curated-comedic-expressions.md",
            "storyboard-example-library.md", "storyboard-regression-library.md",
        )
        for name in files:
            text = (REFS / name).read_text(encoding="utf-8")[:500]
            self.assertRegex(text, r"不是(?:硬约束|规范|默认画风|创作方法库|输出模板|默认配额)")

    def test_story_core_resolves_known_conflicts(self) -> None:
        core = (REFS / "core-story-performance.md").read_text(encoding="utf-8")
        for phrase in (
            "表演所有权", "不得仅为景别丰富切到无关局部", "一行台词与视觉切点",
            "稳定不等于固定", "视觉丰富度是结果，不是目标", "只把“蜷缩”换成“轻点”",
        ):
            self.assertIn(phrase, core)

    def test_technical_core_resolves_known_continuity_failures(self) -> None:
        technical = (REFS / "continuity-timing-output.md").read_text(encoding="utf-8")
        for phrase in (
            "5 秒约 18—19 个中文字", "总长不超过 30 秒", "不设最低镜头数",
            "完整 360°不能以风格为由覆盖轴线", "遮挡只能隐藏本来合理发生的移动",
            "章节计时归零不代表故事状态归零", "前景遮挡可制造纵深",
            "连续三个固定镜头时复核", "未经剧本或既有设定建立",
        ):
            self.assertIn(phrase, technical)

    def test_quality_check_diagnoses_without_second_rulebook(self) -> None:
        quality = (REFS / "quality-check.md").read_text(encoding="utf-8")
        self.assertIn("只负责发现失败，不重新定义创作规则", quality)
        self.assertIn("六遍检查", quality)
        self.assertLess(len(quality), 3000)

    def test_output_contract_and_chapter_wording(self) -> None:
        contract = (REFS / "continuity-timing-output.md").read_text(encoding="utf-8")
        for field in ("【时长：x-y秒】", "画面：", "运镜：", "剪辑/动态效果：", "台词："):
            self.assertIn(field, contract)
        self.assertIn("第一章｜章节标题", SKILL)
        self.assertNotIn("单元一｜单元标题", SKILL)

    def test_reference_routes_exist(self) -> None:
        for reference in set(re.findall(r"`(references/[^`]+\.md)`", SKILL)):
            self.assertTrue((ROOT / reference).is_file(), reference)

    def test_curated_knowledge_is_preserved(self) -> None:
        joined = "\n".join(path.read_text(encoding="utf-8") for path in REFS.glob("*.md"))
        for phrase in ("Michael Bay", "动画动作分镜语言库", "3D动画的故事节奏", "VIS-002", "案例008", "夸张喜剧表情词库", "回归007"):
            self.assertIn(phrase, joined)

    def test_shot_family_planning_precedes_shot_writing(self) -> None:
        core = (REFS / "core-story-performance.md").read_text(encoding="utf-8")
        for phrase in (
            "镜头家族预排", "空间关系位", "表演位", "结果位", "主观信息位",
            "动作路径位", "因果细节位", "环境后果位",
            "不得边写台词边临时选择“近景／固定”",
            "角度必须来自人物与空间",
        ):
            self.assertIn(phrase, core)
        self.assertIn("镜头家族表", SKILL)

    def test_camera_motion_uses_triggers_not_quota(self) -> None:
        technical = (REFS / "continuity-timing-output.md").read_text(encoding="utf-8")
        for phrase in (
            "运动触发表", "人物从一个位置移动到另一个位置", "权力由一方转移到另一方",
            "起幅看什么", "最后落在什么新信息或结果上",
            "无明确落幅的缓推仍按固定镜头处理",
            "这是诊断阈值，不是强制配额",
        ):
            self.assertIn(phrase, technical)
        self.assertIn("不得以“近景／中近景＋固定”为默认起点", SKILL)

    def test_regression_covers_static_closeup_collapse(self) -> None:
        regressions = (REFS / "storyboard-regression-library.md").read_text(encoding="utf-8")
        for phrase in (
            "回归008｜近景固定退化", "没有先为戏剧节拍分配观察任务",
            "镜头家族表和运动触发表", "只添加“微”字",
        ):
            self.assertIn(phrase, regressions)

    def test_scale_angle_and_physical_camera_positions_are_separate(self) -> None:
        core = (REFS / "core-story-performance.md").read_text(encoding="utf-8")
        for phrase in (
            "景别与角度分开规划", "景别回答“观众离信息多近”",
            "角度回答“观众从什么关系位置观看”", "三种功能景别",
            "三个真实观察位", "相邻三镜不得同时保持",
        ):
            self.assertIn(phrase, core)
        self.assertIn("物理机位与前景图", SKILL)

    def test_foreground_has_inventory_geometry_and_function(self) -> None:
        technical = (REFS / "continuity-timing-output.md").read_text(encoding="utf-8")
        for phrase in (
            "前景清单", "至少使用一个前景构图", "建立纵深和人物距离",
            "默认让前景停留在画面边缘或一侧", "普通关系镜只使用一个主要前景层",
            "不能为了得到 OTS 让人物换边或瞬移",
        ):
            self.assertIn(phrase, technical)

    def test_motion_has_minimum_trigger_conversion_and_single_path(self) -> None:
        technical = (REFS / "continuity-timing-output.md").read_text(encoding="utf-8")
        for phrase in (
            "至少选择两个最重要的触发点转化为运动镜头",
            "每镜只设一条主要摄影机路径", "不得把“下降＋前推＋环绕＋拉焦”",
            "运动镜头的落幅必须与起幅不同",
        ):
            self.assertIn(phrase, technical)

    def test_dialogue_subtext_is_evidence_based_and_non_inventive(self) -> None:
        core = (REFS / "core-story-performance.md").read_text(encoding="utf-8")
        for phrase in (
            "对白潜台词转为可见表演", "称呼是否从身份、昵称、尊称变成全名",
            "高可信潜台词", "中可信潜台词", "低可信推测",
            "台词证据 → 当前意图／防御 → 可观察行为",
            "不能因此直接新增摔杯、拥抱、下跪、攻击、哭泣或离场",
            "潜台词推导只负责把已有关系拍出来，不创造新事实",
        ):
            self.assertIn(phrase, core)

    def test_case_009_preserves_subtext_methods_without_globalizing_preferences(self) -> None:
        examples = (REFS / "storyboard-example-library.md").read_text(encoding="utf-8")
        for phrase in (
            "案例009｜重生夜暧昧试探与喜剧抽身", "【不错的分镜／选择性参考】",
            "从对白提取关系动作", "让视觉母题形成状态链", "保持连续场面动作",
            "用期待落差完成喜剧", "不能作为景别角度标杆",
            "不继承脚部镜头数量", "不学习案例的自检结论和旧版排版",
        ):
            self.assertIn(phrase, examples)


if __name__ == "__main__":
    unittest.main()
