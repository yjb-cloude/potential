# Day 8: 配置分离 —— 所有可变参数集中在这里
# =====================================================
# 切换环境/项目时，只改这个文件，其他代码不用动

# ========== 服务器地址 ==========
BASE_URL = "http://your-test-server:80"

# ========== 认证 Token ==========
# Token 过期后只改这里
# ⚠️ 真实 token 不要提交到 git，此处仅占位；本地使用时替换
BLADE_AUTH_TOKEN = "bearer YOUR_TOKEN_HERE"

# ========== 业务参数 ==========
WORK_ORDER_CODE = "PORE202609200003"
OPERATOR_ID = "1636547239557992450"
RESULT = "OK"  # OK=触发工单；NG=触发不良记录（NG 需同时传 flowDefectRecordVOList）

# ========== 流转码列表 ==========
# 当前：生成 FLOW202609040046 一个码，改 range 可批量生成
FLOW_CODE_LIST = [f"FLOW20260920001{i:01d}" for i in range(1, 3)]

# ========== 工序列表（顺序不能乱！） ==========
# 工艺顺序：A1 → A2 → ... → A10
# 如果报"前置工序未完成"，检查这里是否反了
PROCESS_CODE_LIST = [f"A{i}" for i in range(1, 11)]

# ========== 工序间等待秒数 ==========
# 过完一道工序后等待，让状态生效再进入下一道
PROCESS_WAIT_SECONDS = 1
