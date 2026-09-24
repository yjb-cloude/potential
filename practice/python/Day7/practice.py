# Day 7 练习：requests 库 + 接口自动化
# =======================================
# 每个 TODO 都有提示，做完运行看看结果
# 测试网站：https://httpbin.org（公共免费，随便测）

import requests
import json


# ============================================================
# TODO 1：基础 GET 请求
# ============================================================
# 用 requests.get 请求 https://httpbin.org/get
# 打印状态码和响应体（用 .json() 解析）
# 提示：resp = requests.get(url)
try:
    resp = requests.get("https://httpbin.org/get", timeout=5)
    print(f"TODO1 状态码: {resp.status_code}")
    print(f"TODO1 响应体: {resp.json()}")
except Exception as e:
    print(f"TODO1 请求失败: {e}")


# ============================================================
# TODO 2：带参数的 GET 请求
# ============================================================
# 请求 https://httpbin.org/get
# 携带参数：keyword=python, page=1, size=10
# 打印服务端收到的参数（resp.json()['args']）
# 提示：params={"keyword": "python", ...}
try:
    resp = requests.get("https://httpbin.org/get", params={"keyword": "python", "page": 1, "size": 10}, timeout=5)
    print(f"TODO2 参数: {resp.json()['args']}")
except Exception as e:
    print(f"TODO2 请求失败: {e}")


# ============================================================
# TODO 3：POST 提交 JSON 数据
# ============================================================
# POST 到 https://httpbin.org/post
# 提交 JSON：{"name": "张三", "age": 25, "skills": ["Python", "SQL"]}
# 打印服务端收到的 JSON（resp.json()['json']）
# 提示：json={"name": "张三", ...}
try:
    resp = requests.post("https://httpbin.org/post", json={"name": "张三", "age": 25, "skills": ["Python", "SQL"]}, timeout=5)
    print(f"TODO3 收到的数据: {resp.json()['json']}")
except Exception as e:
    print(f"TODO3 请求失败: {e}")


# ============================================================
# TODO 4：自定义 Headers
# ============================================================
# GET 请求 https://httpbin.org/headers
# 设置 Headers:
#   Authorization: Bearer my-token-123
#   Content-Type: application/json
# 打印服务端看到的所有 headers（resp.json()['headers']）
# 提示：headers={...}
try:
    resp = requests.get("https://httpbin.org/headers", headers={"Authorization": "Bearer my-token-123", "Content-Type": "application/json"}, timeout=5)
    print(f"TODO4 headers: {resp.json()['headers']}")
except Exception as e:
    print(f"TODO4 请求失败: {e}")


# ============================================================
# TODO 5：状态码断言
# ============================================================
# 分别请求以下 3 个 URL，打印状态码并判断是否成功（200）
#   https://httpbin.org/get
#   https://httpbin.org/status/404
#   https://httpbin.org/status/500
# 提示：resp.status_code == 200 判断成功
urls = [
    "https://httpbin.org/get",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
]
# 用 for 循环遍历 urls，每个打印 "URL → 状态码 → 成功/失败"
for url in urls:
    try:
        resp = requests.get(url, timeout=5)
        status = "[OK] 成功" if resp.status_code == 200 else "[FAIL] 失败"
        print(f"{url} → {resp.status_code} → {status}")
    except Exception as e:
        print(f"{url} → 请求失败: {e}")


# ============================================================
# TODO 6：封装 get_user_info 函数
# ============================================================
# 写一个函数 get_user_info(user_id: int) -> dict
#   - GET 请求 https://httpbin.org/get?user_id={user_id}
#   - 成功返回 {"success": True, "data": resp.json()}
#   - 异常返回 {"success": False, "error": "错误信息"}
#   - 设定 timeout=3 秒
#
# 调用测试：
#   get_user_info(1)  → 应该成功
#   get_user_info("abc")  → 观察结果
# 提示：参考 lesson_requests.py 里的 safe_get

def get_user_info(user_id: int) -> dict:
    try:
        resp = requests.get(
            "https://httpbin.org/get",
            params={"user_id": user_id},
            timeout=3,
        )
        resp.raise_for_status()   # 4xx/5xx 抛异常
        return {"success": True, "data": resp.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}

# 测试
result1 = get_user_info(1)
print(f"\nTODO6 查询用户1: {result1}")


# ============================================================
# TODO 7：封装 MiniApiClient 类（综合练习）
# ============================================================
# 完成下面的类，实现：
#   - __init__(self, base_url)  —— 保存 base_url
#   - get(self, path, params=None)  —— GET 请求
#   - post(self, path, data=None)  —— POST 请求
#   - _check(self, resp)  —— 检查状态码，非200打印警告
#
# 要求：所有方法返回 resp.json()
#
# 测试代码已经在下面写好了，你只需要补全类的实现

class MiniApiClient:
    """迷你 API 客户端"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def _check(self, resp) -> dict:
        if resp.status_code != 200:
            print(f"警告: 状态码 {resp.status_code}")
        return resp.json()

    def get(self, path: str, params: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        resp = requests.get(url, params=params, timeout=5)
        return self._check(resp)

    def post(self, path: str, data: dict = None) -> dict:
        url = f"{self.base_url}{path}"
        resp = requests.post(url, json=data, timeout=5)
        return self._check(resp)


# --- 测试 ---
api = MiniApiClient("https://httpbin.org")

result = api.get("/get", params={"test": "hello"})
print(f"TODO7 GET: {result['args']}")

result = api.post("/post", data={"msg": "from MiniApiClient"})
print(f"TODO7 POST: {result['json']}")


# ============================================================
# TODO 8（挑战题）：模拟登录流程
# ============================================================
# 很多接口需要先登录拿到 token，再带着 token 访问
# 用 requests.Session 模拟这个流程：
#
# 步骤 1：POST 登录 → https://httpbin.org/post
#         提交 {"username": "admin", "password": "123456"}
#         模拟拿到 token = "fake-token-from-server"
#
# 步骤 2：用同一个 session，GET 带 token 访问
#         https://httpbin.org/headers
#         Headers: Authorization: Bearer {token}
#
# 步骤 3：打印服务端看到的 Authorization 头
#
# 提示：
#   session = requests.Session()
#   session.headers["Authorization"] = f"Bearer {token}"

# 步骤 1：模拟登录，拿 token
session = requests.Session()
try:
    resp = session.post(
        "https://httpbin.org/post",
        json={"username": "admin", "password": "123456"},
        timeout=5,
    )
    print(f"TODO8 登录响应: {resp.json()['json']}")
    token = "fake-token-from-server"
except Exception as e:
    print(f"TODO8 登录失败: {e}")
    token = None

# 步骤 2：设置 token 到 session 的 headers
if token:
    session.headers["Authorization"] = f"Bearer {token}"

    # 步骤 3：用 session 访问，token 自动带上
    try:
        resp = session.get("https://httpbin.org/headers", timeout=5)
        auth = resp.json()["headers"].get("Authorization", "没有 Authorization 头")
        print(f"TODO8 服务端看到的 Authorization: {auth}")
    except Exception as e:
        print(f"TODO8 请求失败: {e}")


print("\n" + "=" * 50)
print("Day 7 练习完成！运行方式：python practice.py")
print("=" * 50)