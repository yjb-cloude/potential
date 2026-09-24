# Day 10: 外部数据驱动 —— 从 JSON 读测试用例
# =====================================================
# 为什么要从文件读？
#   1. 加用例不改代码，测试和数据分离
#   2. 非技术人员（产品/测试主管）也能维护数据
#   3. 面试必问："你的测试数据怎么管理的？"

import json
import os
from loguru import logger


def load_json(file_name: str) -> dict:
    """加载同目录下的 JSON 文件"""
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    logger.debug(f"加载测试数据: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    logger.info(f"加载成功，共 {sum(len(v) for v in data.values())} 条用例")
    return data


def get_login_cases() -> list:
    """获取登录测试用例列表"""
    data = load_json("test_data.json")
    cases = data["login_cases"]

    # 返回 [(case_id, desc, username, password, expect_success, expect_code), ...]
    return [
        (
            c["case_id"],
            c["desc"],
            c["username"],
            c["password"],
            c["expect_success"],
            c["expect_code"],
        )
        for c in cases
    ]


def get_plan_cases() -> list:
    """获取生产计划测试用例列表"""
    data = load_json("test_data.json")
    cases = data["production_plan_cases"]

    return [
        (
            c["case_id"],
            c["desc"],
            c["plan_name"],
            c["expect_success"],
        )
        for c in cases
    ]


# ========== 测试 ==========
if __name__ == "__main__":
    print("=== 登录用例 ===")
    for case in get_login_cases():
        print(f"  {case[0]}: {case[1]}")

    print("\n=== 计划用例 ===")
    for case in get_plan_cases():
        print(f"  {case[0]}: {case[1]}")
