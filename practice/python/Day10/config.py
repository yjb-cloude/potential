# Day 10: 多环境配置 —— 面试加分点
# =====================================================
# 切换环境只改 ENV 变量，其他全部自动切换
# 面试问"怎么做多环境管理"？→ 就是这个！

ENV = "test"  # "test" / "pre" / "prod"

# ========== 环境配置表 ==========
ENV_CONFIG = {
    "test": {
        "base_url": "http://your-test-server:80",
        "token": "bearer YOUR_TOKEN_HERE",  # ⚠️ 真实 token 不要提交到 git
    },
    "pre": {
        "base_url": "http://pre.mes.example.com:80",
        "token": "bearer pre_xxxx",
    },
    "prod": {
        "base_url": "http://mes.example.com:80",
        "token": "bearer prod_xxxx",
    },
}

# ========== 获取当前环境配置 ==========
config = ENV_CONFIG[ENV]
BASE_URL = config["base_url"]
TOKEN = config["token"]

# ========== 业务参数 ==========
WORK_ORDER_CODE = "PORE202609200003"
OPERATOR_ID = "1636547239557992450"

# ========== 超时配置（秒） ==========
REQUEST_TIMEOUT = 10
AI_TIMEOUT = 30
