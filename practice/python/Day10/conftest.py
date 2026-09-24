# Day 10: conftest.py —— 全局 fixture + 日志集成
# =====================================================
# conftest.py 的规则：
#   1. 放在测试目录下，pytest 自动加载，不需要 import
#   2. fixture 名字 = 参数名，自动注入
#   3. scope 控制生命周期（function/class/module/session）

import pytest
import time
import requests
from loguru import logger
from config import BASE_URL, TOKEN, REQUEST_TIMEOUT


# =====================================================
# Fixture 1: API Session（整个测试会话只创建一次）
# =====================================================
@pytest.fixture(scope="session")
def api_session():
    """创建全局 requests.Session，整个测试只初始化一次"""
    session = requests.Session()
    session.headers.update({
        "Content-Type": "application/json",
        "blade-auth": TOKEN,
    })
    logger.info(f"[fixture] API Session 创建完成，目标: {BASE_URL}")
    yield session  # yield 后面是清理代码
    session.close()
    logger.info("[fixture] API Session 已关闭")


# =====================================================
# Fixture 2: 测试计时（每个测试自动记录耗时）
# =====================================================
@pytest.fixture(autouse=True)
def timer(request):
    """自动给每个测试计时，打印到日志"""
    start = time.time()
    yield
    elapsed = round(time.time() - start, 2)
    logger.info(f"[{request.node.name}] 耗时: {elapsed}s")


# =====================================================
# Fixture 3: 测试失败自动截图 / 记录（面试加分）
# =====================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    pytest 钩子：测试失败时自动记录到日志
    面试问"怎么处理测试失败"？→ 用 hook 自动捕获
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        logger.error(f"[FAIL] {item.node.name}")
        logger.error(f"  错误信息: {report.longrepr}")


# =====================================================
# 常见面试题
# =====================================================
# Q: conftest.py 放在哪？
# A: 放在测试目录下，pytest 自动发现，不需要 import
#
# Q: fixture 的 scope 有哪些？
# A: function（每个测试）、class（每个类）、module（每个文件）、session（整个会话）
#
# Q: yield 和 return 的区别？
# A: yield 前面是 setup，后面是 teardown
#    fixture 用 yield，测试用完后会自动执行清理代码
#
# Q: autouse=True 是什么？
# A: 不用显式引用，每个测试自动执行（如计时、日志）
