# Day 8: pytest 测试 —— 带断言的接口自动化
# =====================================================
# 运行方式：pytest test_kafka_flow.py -v
# 加 -s 可以看到 print 输出

import pytest
from config import (
    WORK_ORDER_CODE,
    OPERATOR_ID,
    RESULT,
    FLOW_CODE_LIST,
    PROCESS_CODE_LIST,
    PROCESS_WAIT_SECONDS,
)


class TestSingleFlow:
    """单个流转码测试 —— 用第一个码"""

    def test_one_flow_code_all_processes(self, mes_client):
        """测试：一个流转码跑完全部工序，应该全部成功"""
        flow_code = FLOW_CODE_LIST[0]  # FLOW202609200011

        result = mes_client.batch_run_processes(
            work_order_code=WORK_ORDER_CODE,
            flow_code=flow_code,
            process_codes=PROCESS_CODE_LIST,
            operator_id=OPERATOR_ID,
            result=RESULT,
            wait_seconds=PROCESS_WAIT_SECONDS,
        )

        # 核心断言：失败数必须为 0
        assert result["fail"] == 0, (
            f"流转码 {flow_code} 有 {result['fail']} 道工序失败！"
        )
        assert result["success"] == result["total"]


class TestBatchFlow:
    """批量流转码测试 —— 用第二个码（避免和上面冲突）"""

    @pytest.mark.parametrize("flow_code", FLOW_CODE_LIST[1:])
    def test_each_flow_code(self, mes_client, flow_code):
        """数据驱动：每个流转码都跑完全工序"""
        result = mes_client.batch_run_processes(
            work_order_code=WORK_ORDER_CODE,
            flow_code=flow_code,
            process_codes=PROCESS_CODE_LIST,
            operator_id=OPERATOR_ID,
            result=RESULT,
            wait_seconds=PROCESS_WAIT_SECONDS,
        )

        assert result["fail"] == 0, f"流转码 {flow_code} 存在失败工序"
        assert result["success"] == len(PROCESS_CODE_LIST)


# =====================================================
# 面试加分点：parametrize 数据驱动
# =====================================================
# TestBatchFlow 用 @pytest.mark.parametrize 自动展开测试
# FLOW_CODE_LIST 有几个码，就自动生成几个测试用例
# 这就是「数据驱动测试」，面试高频考点！
