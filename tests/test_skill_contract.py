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
        cls.technical = (ROOT / "references/technical-continuity.md").read_text(
            encoding="utf-8"
        )
        cls.director = (ROOT / "references/director-rules.md").read_text(encoding="utf-8")
        cls.camera_moves = (ROOT / "references/user-curated-camera-moves.md").read_text(
            encoding="utf-8"
        )
        cls.story_first = (ROOT / "references/story-first-directing.md").read_text(
            encoding="utf-8"
        )
        cls.dialogue = (ROOT / "references/dialogue-visual-storytelling.md").read_text(
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
            "user-curated-camera-moves.md",
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

    def test_shot_duration_uses_content_load_not_uniform_length(self) -> None:
        for phrase in (
            "识别主体所需时间 ＋ 动作／台词／信息变化所需时间 ＋ 结果停留与情绪落地时间",
            "以下只用于估时和发现异常，不是必须达到的配额",
            "平均镜头时长（ASL）只用于发现节奏倾向，不作为目标",
            "连续5镜以上都落在相近的1—1.5秒",
        ):
            self.assertIn(phrase, self.technical)
        self.assertIn("观众识别主体＋看懂动作／台词变化＋感受结果", self.skill)

    def test_key_moments_and_character_entrances_avoid_rendering_inflation(self) -> None:
        for phrase in (
            "出场的四个功能阶段",
            "定义性行动",
            "关键时刻的渲染",
            "主要时刻",
            "铺垫／蓄力",
            "对比优于堆叠",
            "若删去特效和运镜后事件本身不再重要",
        ):
            self.assertIn(phrase, self.director)
        for phrase in ("等时碎切与渲染通胀", "不统一套出场模板", "高光结果必须延续"):
            self.assertIn(phrase, self.regressions)

    def test_repeated_visual_motifs_require_state_progression(self) -> None:
        for phrase in (
            "视觉母题的状态阶梯",
            "位置",
            "接触与受力",
            "主动权",
            "视觉增量测试",
            "程度升级只有越过明确阈值时才成立",
        ):
            self.assertIn(phrase, self.story_first)
        for phrase in (
            "身体细节与道具必须形成状态推进",
            "同义重复",
            "退路消失",
            "没有新状态时不要为了维持母题强行插镜",
        ):
            self.assertIn(phrase, self.dialogue)

    def test_foot_comparison_is_scoped_to_the_user_feedback(self) -> None:
        for phrase in (
            "回归005｜视觉母题原地踏步",
            "镜头1、3、4",
            "只认可其脚部母题具有较明显的阶段推进",
            "32.5秒",
            "位置—阻断—接触—阈值—僵住—余震",
            "认可仅限脚部变化",
        ):
            self.assertIn(phrase, self.regressions)
        self.assertIn("同一视觉母题反复出现时", self.skill)

    def test_stealth_attack_regression_preserves_failure_scope(self) -> None:
        for phrase in (
            "回归006｜洞府暗算：毒火效果升级替代行动意义",
            "把“特效状态”误当成“故事状态”",
            "太便宜他了",
            "镜头3与镜头6",
            "镜头4与镜头5",
            "紫色→蓝色",
            "观察目标 → 原计划或初始冲动 → 新证据／判断 → 手段改变 → 执行 → 可见后果",
            "不得自行选择其中一种后果",
            "固定摄影机、近景和特写不是天然错误",
            "颜色变化可以承担信息",
        ):
            self.assertIn(phrase, self.regressions)

    def test_example_grades_and_format_boundaries(self) -> None:
        self.assertIn("标杆／非常好", self.examples)
        self.assertGreaterEqual(self.examples.count("不错／选择性参考"), 4)
        self.assertIn("仅学习分镜设计，不学习整体输出格式", self.examples)
        self.assertIn("不得继承", self.examples)

    def test_orca_rescue_case_preserves_only_reusable_design(self) -> None:
        for phrase in (
            "案例004｜受伤虎鲸救援与深海巨物苏醒",
            "威胁变受害者",
            "用平行误判制造戏剧性反讽",
            "仅学习故事递进与分镜设计，不学习整体输出格式",
            "不得无过渡改成头顶出现",
            "不得拆成四个编号镜头",
        ):
            self.assertIn(phrase, self.examples)

    def test_benchmark_ensemble_entrance_preserves_hierarchy_and_ai_fallback(self) -> None:
        for phrase in (
            "案例005｜九龙封宫与屋檐群像接力登场",
            "【标杆／非常好】",
            "秦然不参与众统领的从天而降",
            "统领强势降临，秦然早已在场且姿态散漫",
            "群像焦点接力",
            "七人大全景",
            "图片文件未收录进Skill仓库",
            "复杂AI视频不必强求整段12—16秒真正一次生成",
        ):
            self.assertIn(phrase, self.examples)

        for phrase in (
            "CAM-008｜群像接力式 Bay 环绕——前景拉焦与领袖遮挡揭示",
            "统领2从前景盲区猛然转入",
            "身体擦镜",
            "下属共同完成的强势降落",
            "将长运动拆为三段",
            "领袖稳定揭示",
        ):
            self.assertIn(phrase, self.camera_moves)

        for phrase in (
            "势力群像与领袖压轴",
            "共同力量先落地",
            "个体差异再成立",
            "领袖用反差定级",
            "关系全景作确认",
        ):
            self.assertIn(phrase, self.director)

    def test_physical_comedy_case_is_selective_and_angle_aware(self) -> None:
        for phrase in (
            "案例006｜洞府中招与满屋失控",
            "【整体挺好／不错／选择性参考】",
            "角度太像，基本上都是平视",
            "身体—判断—语言—空间—落空—后果",
            "建立四个机位锚点",
            "窗边或人物正侧方近距离机位",
            "洞府高角度三分之四主镜头",
            "家具旁低机位",
            "门外反拍机位",
            "摄影机固定不是缺点",
            "不因为案例整体不错就学习其全部字段",
        ):
            self.assertIn(phrase, self.examples)

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
