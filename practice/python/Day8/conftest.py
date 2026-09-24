# Day 8: pytest fixtures —— 测试前置/后置逻辑
# =====================================================
# conftest.py 是 pytest 的"自动加载"文件
# 里面的 fixture 自动对同目录下所有测试文件生效

import pytest
from mes_client import MesClient
from config import BASE_URL, BLADE_AUTH_TOKEN


@pytest.fixture(scope="session")
def mes_client():
    """
    session 级别 fixture：整个测试过程只创建一次客户端
    就像登录一次，后面所有测试复用同一个连接
    """
    client = MesClient(BASE_URL, BLADE_AUTH_TOKEN)
    yield client
    # 测试结束后可以加清理逻辑（如果需要的话）
    print("\n[fixture] 所有测试完成，MesClient 销毁")
