# Day 9: AI 回答质量评估测试
# =====================================================
# 运行方式：pytest test_ai_quality.py -v -s
# 测试点：API可用性 + 回答质量 + 响应时间 + 异常处理

import pytest
from ai_client import ask_deepseek


# =====================================================
# 1. 基础可用性测试
# =====================================================
class TestAIBasic:
    """AI 接口基础测试 —— 能不能正常工作"""

    def test_ask_success(self):
        """测试：调用 API 应该返回成功"""
        result = ask_deepseek("你好")
        assert result["success"] is True, f"调用失败: {result['error']}"

    def test_answer_not_empty(self):
        """测试：回答不应该为空"""
        result = ask_deepseek("你好")
        assert result["success"] is True
        assert len(result["answer"]) > 0, "回答内容为空"

    def test_time_cost_positive(self):
        """测试：耗时应该大于 0"""
        result = ask_deepseek("你好")
        assert result["time_cost"] > 0, "耗时异常"


# =====================================================
# 2. 回答质量测试 —— 数据驱动
# =====================================================
# 面试高频：用 parametrize 做数据驱动测试！
QUESTIONS = [
    # (问题, 期望包含的关键词, 最少字数)
    ("什么是软件测试", "测试", 10),
    ("Python 的列表和元组有什么区别", "列表", 20),
    ("HTTP 和 HTTPS 的区别", "加密", 10),
    ("什么是接口测试", "接口", 10),
]


class TestAIQuality:
    """AI 回答质量测试 —— 关键词 + 最小长度"""

    @pytest.mark.parametrize("question,min_keyword,min_length", QUESTIONS)
    def test_answer_contains_keyword(self, question, min_keyword, min_length):
        """测试：回答应包含相关关键词且长度达标"""
        result = ask_deepseek(question)

        # 断言 1：调用成功
        assert result["success"], f"调用失败: {result['error']}"

        # 断言 2：回答长度达标
        answer = result["answer"]
        assert len(answer) >= min_length, (
            f"回答太短({len(answer)}字): {answer[:50]}"
        )

        # 断言 3：包含关键词（不区分大小写）
        assert min_keyword.lower() in answer.lower(), (
            f"回答未包含关键词 '{min_keyword}': {answer[:100]}"
        )

        print(f"\n  Q: {question}")
        print(f"  A: {answer[:80]}...")
        print(f"  耗时: {result['time_cost']}s")


# =====================================================
# 3. 响应时间测试 —— 性能断言
# =====================================================
class TestAIPerformance:
    """AI 响应时间测试 —— 性能基线"""

    def test_response_within_30s(self):
        """测试：单次请求应在 30 秒内返回"""
        result = ask_deepseek("用一句话解释回归测试")
        assert result["success"], f"调用失败: {result['error']}"
        assert result["time_cost"] < 30, (
            f"响应太慢: {result['time_cost']}s（阈值 30s）"
        )
        print(f"\n  响应时间: {result['time_cost']}s")

    @pytest.mark.parametrize("question", [
        "什么是单元测试",
        "什么是集成测试",
        "什么是系统测试",
    ])
    def test_batch_response_time(self, question):
        """测试：连续 3 个请求，每个都应在 30s 内"""
        result = ask_deepseek(question)
        assert result["success"], f"调用失败: {result['error']}"
        assert result["time_cost"] < 30, f"{question} 响应超时"


# =====================================================
# 4. 边界 / 异常测试
# =====================================================
class TestAIEdgeCases:
    """边界和异常场景测试"""

    def test_empty_question(self):
        """测试：空问题不应该崩溃"""
        result = ask_deepseek("")
        # 不管回答啥，至少不能报错崩溃
        assert "error" in result  # 结构完整

    def test_very_long_question(self):
        """测试：超长问题（500字）不应崩溃"""
        long_question = "测试" * 250  # 500 字
        result = ask_deepseek(long_question)
        assert "error" in result  # 结构完整，没有抛异常

    def test_special_characters(self):
        """测试：特殊字符不应导致崩溃"""
        result = ask_deepseek("SELECT * FROM users WHERE id=1; DROP TABLE--")
        assert "error" in result  # 结构完整


# =====================================================
# 面试高频问题总结
# =====================================================
# Q: AI 测试怎么测？
# A: 4 个维度：
#    1. 可用性：API 能不能调通
#    2. 质量：回答是否包含关键词、长度是否达标
#    3. 性能：响应时间是否在阈值内
#    4. 健壮性：空输入/超长输入/特殊字符不崩溃
#
# Q: 什么是数据驱动测试？
# A: 把测试数据和测试逻辑分离，用 @pytest.mark.parametrize
#    一份代码跑多组数据，加数据不改代码
#
# Q: 断言写在哪？
# A: 每个 test 方法里，assert 条件 + 失败信息
#    assert result["success"], f"调用失败: {result['error']}"
