# Day 10: 日志模块 —— 测试必备
# =====================================================
# 为什么需要日志？
#   print() 只能看当前，日志可以写文件、带时间、分级别
#   接口测试出 bug 时，日志是唯一的证据
#
# 面试问"你怎么做日志管理"？→ loguru 一行搞定

import sys
from loguru import logger

# ========== 移除默认 handler ==========
logger.remove()

# ========== 控制台输出（彩色） ==========
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | {message}",
    level="INFO",
    colorize=True,
)

# ========== 文件输出（按天轮转） ==========
logger.add(
    "logs/test_{time:YYYY-MM-DD}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {message}",
    level="DEBUG",
    rotation="1 day",     # 每天一个文件
    retention="7 days",   # 只保留 7 天
    encoding="utf-8",
)

# ========== 使用示例 ==========
if __name__ == "__main__":
    logger.debug("这是调试信息，只在文件里")
    logger.info("这是普通信息")
    logger.warning("这是警告")
    logger.error("这是错误")
    logger.success("这是成功！")

    # 接口测试中常用格式
    logger.info(f"POST /api/login → 200 OK (0.35s)")
    logger.error(f"POST /api/login → 500 Internal Server Error")
