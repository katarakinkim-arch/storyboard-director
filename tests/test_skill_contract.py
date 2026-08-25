from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SkillContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        cls.examples = (ROOT / "references/storyboard-example-library.md").read_text(
            encoding="utf-8"
        )
        cls.regressions = (ROOT / "references/storyboard-regression-library.md").read_text(
            encoding="utf-8"
        )

    def test_story_first_is_the_creative_core(self) -> None:
        self.assertIn("故事是核心，镜头是讲故事的方法", self.skill)
        self.assertIn("找到故事引擎", self.skill)
        self.assertIn("视觉引擎", self.skill)
        self.assertIn("每个镜头至少推进", self.skill)

    def test_required_reference_modules_exist(self) -> None:
        required = {
            "story-first-directing.md",
            "technical-continuity.md",
            "dialogue-visual-storytelling.md",
            "suspense-action-spectacle.md",
            "director-rules.md",
            "storyboard-example-library.md",
            "storyboard-regression-library.md",
        }
        for filename in required:
            self.assertTrue((ROOT / "references" / filename).is_file(), filename)

    def test_only_core_references_are_always_required(self) -> None:
        mandatory = self.skill.split("正式生成前必须完整读取：", 1)[1].split(
            "根据场景按需读取：", 1
        )[0]
        self.assertIn("story-first-directing.md", mandatory)
        self.assertIn("technical-continuity.md", mandatory)
        self.assertNotIn("director-rules.md", mandatory)
        self.assertNotIn("storyboard-example-library.md", mandatory)

    def test_timing_and_dialogue_contract(self) -> None:
        self.assertIn("5 秒约 18—19 个中文字", self.skill)
        self.assertIn("不设最低镜头数", self.skill)
        self.assertIn("不设固定百分比", self.skill)
        self.assertIn("同一行台词拆到多个编号镜头", self.skill)
        self.assertIn("每个分镜单元总长不超过 30 秒", self.skill)

    def test_no_fixed_movement_target_returns(self) -> None:
        forbidden = (
            "运动镜头占总量 62%",
            "运动镜头比例：62%",
            "运动镜头比例：60%",
            "OTS使用强度：60%",
        )
        for phrase in forbidden:
            self.assertNotIn(phrase, self.skill)

    def test_example_grades_and_format_boundaries(self) -> None:
        self.assertIn("标杆／非常好", self.examples)
        self.assertGreaterEqual(self.examples.count("不错／选择性参考"), 3)
        self.assertIn("仅学习分镜设计，不学习整体输出格式", self.examples)
        self.assertIn("不得继承", self.examples)

    def test_manual_edits_are_not_attributed_to_ai(self) -> None:
        expected = "脚从大腿滑到胸口\u201d和\u201c扣住脚踝\u201d是用户人工添加"
        self.assertIn(expected, self.examples)
        self.assertIn(expected, self.regressions)
        self.assertIn("不得把人工改动归因于 AI", self.skill)

    def test_regressions_cover_known_failures(self) -> None:
        for phrase in (
            "宫门旧人拦路",
            "强开场之后创意塌缩",
            "把“不错”当成“最高标准”",
            "丹药",
            "秦昭禾",
        ):
            self.assertIn(phrase, self.regressions)

    def test_output_fields_are_complete(self) -> None:
        for field in ("【时长：x-y秒】", "画面：", "运镜：", "剪辑/动态效果：", "台词："):
            self.assertIn(field, self.skill)
        self.assertRegex(self.skill, re.compile(r"单元标注总时长必须与最后一镜结束时间一致"))


if __name__ == "__main__":
    unittest.main()
