# Day 10: 接口测试进阶 —— 日志 + 数据驱动 + 软断言 + Allure
# =====================================================
# 运行方式：
#   pytest test_api_advanced.py -v -s              （普通运行）
#   pytest test_api_advanced.py -v -s --alluredir=./allure-results  （生成 Allure 数据）
#   allure serve ./allure-results                   （打开 Allure 报告）

import pytest
import requests
from loguru import logger
from config import BASE_URL, REQUEST_TIMEOUT
from data_provider import get_login_cases


# =====================================================
# 1. 数据驱动 + 日志 —— 登录接口测试
# =====================================================
@pytest.mark.parametrize(
    "case_id,desc,username,password,expect_success,expect_code",
    get_login_cases(),
)
def test_login_data_driven(api_session, case_id, desc, username, password,
                           expect_success, expect_code):
    """
    数据驱动测试：从 JSON 文件读用例，自动展开
    面试问"怎么做数据驱动"？→ 就是这个！
    """
    url = f"{BASE_URL}/blade-auth/oauth/token"
    params = {
        "username": username,
        "password": password,
        "grant_type": "password",
    }

    logger.info(f"[{case_id}] {desc} — 开始执行")

    try:
        resp = api_session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        actual_code = resp.status_code

        logger.info(f"[{case_id}] 响应状态码: {actual_code}")

        # 断言
        assert actual_code == expect_code, (
            f"[{case_id}] {desc}: 期望 {expect_code}，实际 {actual_code}"
        )

        logger.info(f"[{case_id}] ✅ 通过")

    except Exception as e:
        logger.error(f"[{case_id}] ❌ 异常: {e}")
        raise


# =====================================================
# 2. 软断言 —— 多个断言都执行，最后一起报错
# =====================================================
# 场景：一个接口要验证 5 个字段
#   硬断言：第 1 个失败就停了，看不到后面 4 个
#   软断言：5 个都执行，最后一起告诉你哪些失败了

class TestSoftAssertion:
    """软断言示例 —— 接口返回多个字段都要验证"""

    def test_response_fields(self, api_session):
        """验证接口返回的多个字段"""
        url = f"{BASE_URL}/blade-auth/oauth/token"
        params = {"username": "admin", "password": "123456", "grant_type": "password"}

        resp = api_session.get(url, params=params, timeout=REQUEST_TIMEOUT)
        logger.info(f"响应状态码: {resp.status_code}")

        # 如果返回 JSON，逐个字段断言
        if resp.status_code == 200:
            try:
                body = resp.json()
                errors = []  # 收集所有失败的断言

                # 检查字段 1
                if "access_token" not in body:
                    errors.append("缺少 access_token 字段")

                # 检查字段 2
                if "token_type" not in body:
                    errors.append("缺少 token_type 字段")

                # 检查字段 3
                if body.get("expires_in", 0) <= 0:
                    errors.append(f"expires_in 异常: {body.get('expires_in')}")

                # 最后一次性报告所有错误
                if errors:
                    for err in errors:
                        logger.error(f"  ❌ {err}")
                    pytest.fail(f"共 {len(errors)} 个字段校验失败:\n" + "\n".join(errors))
                else:
                    logger.success("所有字段校验通过 ✅")

            except ValueError:
                pytest.fail("响应不是有效 JSON")

        logger.info("软断言测试完成")


# =====================================================
# 3. 接口链式调用 —— 生产计划完整流程
# =====================================================
class TestAPICallChain:
    """接口链式调用：新增 → 查询 → 修改 → 删除"""

    created_id = None  # 类变量，保存新增的 ID

    def test_01_create_plan(self, api_session):
        """步骤 1：新增生产计划"""
        url = f"{BASE_URL}/mes-manufact/productionPlan/addProductionPlan"
        payload = {
            "planName": "自动化测试计划",
            "planCode": "AUTO_TEST_001",
        }

        logger.info(f"POST {url}")
        resp = api_session.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        logger.info(f"响应: {resp.status_code}")

        assert resp.status_code == 200, f"新增失败: {resp.text[:200]}"

        # 保存 ID 给后续测试用
        body = resp.json()
        TestAPICallChain.created_id = body.get("data", {}).get("id")
        logger.info(f"新增成功，ID: {TestAPICallChain.created_id}")

    def test_02_query_plan(self, api_session):
        """步骤 2：查询刚才新增的计划"""
        assert TestAPICallChain.created_id, "没有可查询的 ID（test_01 可能失败了）"

        url = f"{BASE_URL}/mes-manufact/productionPlan/getInfoById"
        params = {"id": TestAPICallChain.created_id}

        logger.info(f"GET {url}?id={TestAPICallChain.created_id}")
        resp = api_session.get(url, params=params, timeout=REQUEST_TIMEOUT)

        assert resp.status_code == 200, f"查询失败: {resp.text[:200]}"
        body = resp.json()
        assert body.get("data", {}).get("planName") == "自动化测试计划"
        logger.success("查询验证通过 ✅")

    def test_03_delete_plan(self, api_session):
        """步骤 3：删除（清理测试数据）"""
        assert TestAPICallChain.created_id, "没有可删除的 ID"

        url = f"{BASE_URL}/mes-manufact/productionPlan/delete"
        params = {"id": TestAPICallChain.created_id}

        logger.info(f"DELETE {url}?id={TestAPICallChain.created_id}")
        resp = api_session.delete(url, params=params, timeout=REQUEST_TIMEOUT)

        assert resp.status_code == 200, f"删除失败: {resp.text[:200]}"
        logger.success("清理完成 ✅")


# =====================================================
# 4. Allure 报告装饰器（面试加分）
# =====================================================
# 需要安装：pip install allure-pytest
# 运行：pytest --alluredir=./allure-results
# 查看：allure serve ./allure-results
#
# from allure import severity, severity_level, feature, story, title
#
# @feature("生产计划模块")
# @story("CRUD 接口")
# @severity(severity_level.CRITICAL)
# @title("新增生产计划 - 正常流程")
# def test_create_plan(api_session):
#     ...


# =====================================================
# 面试高频总结
# =====================================================
# Q: 你的接口自动化框架怎么设计的？
# A: 分层架构：
#    config.py    → 配置层（多环境、超时、token）
#    data_provider.py → 数据层（外部 JSON 驱动）
#    conftest.py  → 基础设施层（fixture、日志、钩子）
#    test_*.py    → 用例层（数据驱动 + 断言 + 链式调用）
#
# Q: 软断言和硬断言区别？
# A: 硬断言 = 第一个失败就停
#    软断言 = 全部执行，最后一起报告
#    接口返回多个字段时，软断言效率更高
#
# Q: 测试数据怎么管理？
# A: 外部文件（JSON/YAML/Excel）+ 数据驱动函数
#    加用例不改代码，非技术人员也能维护
#
# Q: Allure 报告有什么用？
# A: 可视化测试报告：用例数、通过率、耗时、失败详情
#    给领导/客户看，比命令行输出专业 100 倍
