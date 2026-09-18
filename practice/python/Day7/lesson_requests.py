# Day 7: requests 库 — Python 接口自动化核心
# ============================================
# 这个文件是「理论笔记 + 可运行示例」，边读边跑
# 依赖：pip install requests

import requests
import json

# ============================================================
# 一、requests 最核心的 5 个方法
# ============================================================
# 对应 HTTP 的 5 种请求方式：
#   GET    — 查（获取数据）
#   POST   — 增（创建数据）
#   PUT    — 改（全量更新）
#   PATCH  — 改（部分更新）
#   DELETE — 删
#
# 记忆口诀：增删改查 → POST DELETE PUT/patch GET
# ============================================================

# --- 1. GET 请求：获取数据 ---
print("=" * 50)
print("一、GET 请求")
print("=" * 50)

# 用 httpbin.org 做测试（一个专门用来测试 HTTP 的公共网站）
resp = requests.get("https://httpbin.org/get")

# resp 的四大属性（和 Postman 里看到的一样！）
print(f"状态码: {resp.status_code}")        # 200
print(f"响应头 Content-Type: {resp.headers['Content-Type']}")
print(f"响应体类型: {type(resp.text)}")       # str（原始文本）
print(f"响应体 JSON 类型: {type(resp.json())}")  # dict（已解析）

# 带参数的 GET（相当于 Postman 里加 Params）
# ?name=tom&age=25
resp = requests.get(
    "https://httpbin.org/get",
    params={"name": "tom", "age": 25}   # requests 自动拼 URL
)
data = resp.json()
print(f"\n携带参数: {data['args']}")   # {'name': 'tom', 'age': '25'}


# --- 2. POST 请求：提交数据 ---
print("\n" + "=" * 50)
print("二、POST 请求")
print("=" * 50)

# JSON 格式提交（最常用！相当于 Postman Body -> raw -> JSON）
resp = requests.post(
    "https://httpbin.org/post",
    json={"username": "admin", "password": "123456"}
)
print(f"POST 响应: {resp.json()['json']}")  # {'username': 'admin', 'password': '123456'}

# 表单格式提交（相当于 Postman Body -> form-urlencoded）
resp = requests.post(
    "https://httpbin.org/post",
    data={"key1": "value1", "key2": "value2"}
)
print(f"表单响应: {resp.json()['form']}")  # {'key1': 'value1', 'key2': 'value2'}


# --- 3. 带 Headers 的请求 ---
print("\n" + "=" * 50)
print("三、自定义 Headers（模拟登录态）")
print("=" * 50)

headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.test",
    "X-Custom-Header": "my-value"
}
resp = requests.get(
    "https://httpbin.org/headers",
    headers=headers
)
print(f"服务端看到的 Headers:\n{json.dumps(resp.json()['headers'], indent=2)}")


# ============================================================
# 二、Response 对象速查表
# ============================================================
# resp.status_code   → int     状态码（200/404/500...）
# resp.headers       → dict    响应头
# resp.text          → str     响应体（文本）
# resp.json()        → dict    响应体（解析JSON，失败抛异常）
# resp.content       → bytes   响应体（二进制，用于下载文件）
# resp.url           → str     最终请求的 URL（含重定向）
# resp.ok            → bool    状态码 < 400 → True
# resp.elapsed       → timedelta 请求耗时
# ============================================================

print("\n" + "=" * 50)
print("四、Response 常用属性")
print("=" * 50)

resp = requests.get("https://httpbin.org/get")
print(f"resp.ok      = {resp.ok}")           # True
print(f"resp.url     = {resp.url}")
print(f"resp.elapsed = {resp.elapsed}")


# ============================================================
# 三、实战模式：封装一个 API 客户端类
# ============================================================
# 企业里不会每个请求都写 requests.get/post
# 而是封装一个类，统一管理 base_url、headers、日志
# ============================================================

print("\n" + "=" * 50)
print("五、封装 API 客户端（企业级写法）")
print("=" * 50)


class ApiClient:
    """接口测试客户端 — 封装常用请求方法"""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()  # Session 自动管理 Cookie

    def set_token(self, token: str):
        """设置登录 token"""
        self.session.headers["Authorization"] = f"Bearer {token}"

    def get(self, path: str, params: dict = None) -> dict:
        """GET 请求"""
        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = self.session.get(url, params=params)
        return self._handle_response(resp)

    def post(self, path: str, json_data: dict = None) -> dict:
        """POST 请求"""
        url = f"{self.base_url}/{path.lstrip('/')}"
        resp = self.session.post(url, json=json_data)
        return self._handle_response(resp)

    def _handle_response(self, resp: requests.Response) -> dict:
        """统一处理响应：检查状态码 + 解析 JSON"""
        print(f"  [{resp.status_code}] {resp.request.method} {resp.url}")
        if not resp.ok:
            raise Exception(f"请求失败: {resp.status_code} - {resp.text[:200]}")
        return resp.json()


# 使用示例
client = ApiClient("https://httpbin.org")
data = client.get("/get", params={"page": 1, "size": 10})
print(f"分页参数: {data['args']}")

data = client.post("/post", json_data={"name": "测试订单", "qty": 100})
print(f"创建结果: {data['json']}")


# ============================================================
# 四、异常处理（对接口场景）
# ============================================================
print("\n" + "=" * 50)
print("六、接口测试异常处理")
print("=" * 50)


def safe_get(url: str, timeout: int = 5) -> tuple:
    """安全的 GET 请求，返回 (成功?, 结果/错误信息)"""
    try:
        resp = requests.get(url, timeout=timeout)  # timeout 防卡死！
        resp.raise_for_status()  # 4xx/5xx 直接抛异常
        return (True, resp.json())
    except requests.exceptions.ConnectionError:
        return (False, "连接失败 — 服务器宕了或 URL 写错了")
    except requests.exceptions.Timeout:
        return (False, f"请求超时（{timeout}s）")
    except requests.exceptions.HTTPError as e:
        return (False, f"HTTP 错误: {e.response.status_code}")
    except json.JSONDecodeError:
        return (False, "响应不是 JSON 格式")


# 正常 URL
ok, result = safe_get("https://httpbin.org/get")
print(f"正常请求: 成功={ok}")

# 故意超时
ok, result = safe_get("https://httpbin.org/delay/10", timeout=2)
print(f"超时请求: 成功={ok}, 原因={result}")


# ============================================================
# 五、和 Postman 的对应关系
# ============================================================
#
#  Postman 操作              Python 代码
#  ────────────────────────  ──────────────────────────
#  新建请求 + 选 GET/POST   requests.get() / .post()
#  Params 标签页             params={"key": "val"}
#  Headers 标签页            headers={"Auth": "Bearer xxx"}
#  Body → raw → JSON         json={"key": "val"}
#  Body → form-urlencoded    data={"key": "val"}
#  Tests 标签页（断言）       assert resp.status_code == 200
#  Collection Runner         pytest + parametrize
#  环境变量                  变量 / config 文件
#  Pre-request Script        fixture（登录拿 token）
#
# ============================================================
print("\n✅ Day 7 理论部分完成！接下来做练习题 → practice.py")