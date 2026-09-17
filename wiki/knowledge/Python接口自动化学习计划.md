# Python 接口自动化学习计划

> 目标：掌握 Python 接口自动化测试，能独立编写、执行、维护接口测试脚本
> 参考：CSDN 博客《Python数据挖掘学习全攻略》结构
> 重点：只学接口自动化需要的内容，跳过数据挖掘/可视化/爬虫/机器学习

---

## 学习路线总览

```
第 1 阶段：Python 基础（补漏）（1 周）
  ├── 元组、集合
  ├── JSON 数据处理
  ├── 日期处理
  └── 文件操作（CSV/Excel）

第 2 阶段：requests 库进阶（1 周）
  ├── Session 会话管理
  ├── 文件上传
  ├── 超时处理
  └── 异常处理

第 3 阶段：pytest 测试框架（2 周）
  ├── 测试类和测试方法
  ├── 断言（assert）
  ├── 参数化测试
  ├── Fixture（前置/后置）
  └── 测试报告

第 4 阶段：接口自动化实战（2 周）
  ├── 接口关联（Token 传递）
  ├── 数据驱动（Excel/CSV）
  ├── 配置文件管理
  └── 日志记录

第 5 阶段：数据库断言（1 周）
  ├── Python 连接数据库
  ├── 数据库断言
  └── 数据清理

第 6 阶段：框架搭建 + CI/CD（1 周）
  ├── 框架设计
  ├── Jenkins/GitHub Actions 集成
  └── 测试报告优化
```

---

## 第 1 阶段：Python 基础（补漏）

### 1.1 元组和集合

**元组（tuple）**：不可变的列表

```python
# 创建元组
fruits = ("苹果", "香蕉", "橙子")

# 访问元素
print(fruits[0])  # 苹果

# 不可变，不能修改
# fruits[0] = "葡萄"  # ❌ 报错
```

**集合（set）**：无序、不重复

```python
# 创建集合
numbers = {1, 2, 3, 4, 5}

# 去重
numbers = {1, 2, 2, 3, 3, 3}
print(numbers)  # {1, 2, 3}

# 集合操作
a = {1, 2, 3}
b = {3, 4, 5}
print(a & b)  # 交集：{3}
print(a | b)  # 并集：{1, 2, 3, 4, 5}
```

**接口自动化用途**：
- 元组：存储不可变的配置（如 API 地址）
- 集合：去重、判断元素是否存在

### 1.2 JSON 数据处理

**JSON 是接口自动化的重点！**

```python
import json

# JSON 字符串 → Python 字典
json_str = '{"name": "张三", "age": 25}'
data = json.loads(json_str)
print(data["name"])  # 张三

# Python 字典 → JSON 字符串
data = {"name": "张三", "age": 25}
json_str = json.dumps(data, ensure_ascii=False)
print(json_str)  # {"name": "张三", "age": 25}

# 读取 JSON 文件
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 写入 JSON 文件
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

**接口自动化用途**：
- 解析接口响应：`response.json()`
- 构造请求体：`json=data`
- 读取测试数据：从 JSON 文件读取

### 1.3 日期处理

```python
from datetime import datetime, timedelta

# 获取当前时间
now = datetime.now()
print(now)  # 2024-01-15 10:30:00

# 格式化时间
print(now.strftime("%Y-%m-%d %H:%M:%S"))  # 2024-01-15 10:30:00
print(now.strftime("%Y%m%d"))  # 20240115

# 时间计算
tomorrow = now + timedelta(days=1)
yesterday = now - timedelta(days=1)

# 字符串 → 日期
date_str = "2024-01-15"
date = datetime.strptime(date_str, "%Y-%m-%d")
```

**接口自动化用途**：
- 生成时间戳
- 构造日期参数
- 验证响应中的时间字段

### 1.4 文件操作（CSV/Excel）

**CSV 文件**：

```python
import csv

# 读取 CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 写入 CSV
with open("data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "年龄"])
    writer.writerow(["张三", 25])
```

**Excel 文件**（需要安装 openpyxl）：

```bash
pip install openpyxl
```

```python
from openpyxl import load_workbook

# 读取 Excel
wb = load_workbook("data.xlsx")
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

**接口自动化用途**：
- 从 CSV/Excel 读取测试数据
- 把测试结果写入文件

---

## 第 2 阶段：requests 库进阶

### 2.1 Session 会话管理

**为什么需要 Session？**
- 自动管理 Cookie
- 保持登录状态
- 复用连接，提高性能

```python
import requests

# 创建 Session
session = requests.Session()

# 登录（自动保存 Cookie）
login_url = "http://192.168.9.55:5666/apis/mes-auth/token"
login_data = {
    "username": "admin",
    "password": "123456",
    "grantType": "password"
}
response = session.post(login_url, data=login_data)
print(response.json())

# 访问其他接口（自动带 Cookie）
user_url = "http://192.168.9.55:5666/apis/user/info"
response = session.get(user_url)
print(response.json())
```

### 2.2 文件上传

```python
import requests

url = "http://192.168.9.55:5666/apis/file/upload"

# 上传文件
files = {"file": open("test.txt", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

### 2.3 超时处理

```python
import requests

url = "http://192.168.9.55:5666/apis/slow-api"

# 设置超时（秒）
try:
    response = requests.get(url, timeout=5)
except requests.Timeout:
    print("请求超时")
```

### 2.4 异常处理

```python
import requests

url = "http://192.168.9.55:5666/apis/test"

try:
    response = requests.get(url)
    response.raise_for_status()  # 如果状态码不是 200，抛异常
except requests.RequestException as e:
    print(f"请求失败: {e}")
```

---

## 第 3 阶段：pytest 测试框架

### 3.1 安装

```bash
pip install pytest pytest-html
```

### 3.2 测试类和测试方法

```python
import pytest
import requests

class TestLogin:
    
    def setup_method(self):
        """每个测试方法执行前调用"""
        self.url = "http://192.168.9.55:5666/apis/mes-auth/token"
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "ClientId": "mes",
            "ClientSecret": "mes"
        }
    
    def test_login_success(self):
        """测试登录成功"""
        data = {
            "username": "admin",
            "password": "123456",
            "grantType": "password"
        }
        response = requests.post(self.url, data=data, headers=self.headers)
        
        assert response.status_code == 200
        result = response.json()
        assert result.get("code") == 200
        assert "access_token" in result.get("data", {})
    
    def test_login_wrong_password(self):
        """测试密码错误"""
        data = {
            "username": "admin",
            "password": "wrong",
            "grantType": "password"
        }
        response = requests.post(self.url, data=data, headers=self.headers)
        
        assert response.status_code == 200
        result = response.json()
        assert result.get("code") != 200
```

### 3.3 断言（assert）

```python
# 基本断言
assert 1 + 1 == 2
assert "hello" in "hello world"
assert len([1, 2, 3]) == 3

# 接口测试常用断言
assert response.status_code == 200
assert result.get("code") == 200
assert "token" in result.get("data", {})
assert result.get("data", {}).get("name") == "张三"
```

### 3.4 参数化测试

```python
import pytest
import requests

class TestLogin:
    
    @pytest.mark.parametrize("username, password, expected_code", [
        ("admin", "123456", 200),      # 正确
        ("admin", "wrong", 400),       # 密码错误
        ("", "123456", 400),           # 用户名为空
        ("admin", "", 400),            # 密码为空
    ])
    def test_login(self, username, password, expected_code):
        url = "http://192.168.9.55:5666/apis/mes-auth/token"
        data = {
            "username": username,
            "password": password,
            "grantType": "password"
        }
        response = requests.post(url, data=data)
        
        assert response.status_code == 200
        result = response.json()
        assert result.get("code") == expected_code
```

### 3.5 Fixture（前置/后置）

```python
import pytest
import requests

@pytest.fixture
def login_token():
    """前置操作：登录获取 Token"""
    url = "http://192.168.9.55:5666/apis/mes-auth/token"
    data = {
        "username": "admin",
        "password": "123456",
        "grantType": "password"
    }
    response = requests.post(url, data=data)
    token = response.json().get("data", {}).get("access_token")
    yield token  # 返回给测试用例

class TestUser:
    
    def test_get_user_info(self, login_token):
        """使用 Token 获取用户信息"""
        url = "http://192.168.9.55:5666/apis/user/info"
        headers = {"Authorization": f"Bearer {login_token}"}
        response = requests.get(url, headers=headers)
        
        assert response.status_code == 200
```

### 3.6 测试报告

```bash
# 生成 HTML 报告
pytest test_login.py --html=report.html

# 生成 Allure 报告（更美观）
pip install allure-pytest
pytest test_login.py --alluredir=./allure-results
allure serve ./allure-results
```

---

## 第 4 阶段：接口自动化实战

### 4.1 接口关联（Token 传递）

```python
import requests

class TestOrder:
    
    def setup_method(self):
        # 登录获取 Token
        login_url = "http://192.168.9.55:5666/apis/mes-auth/token"
        login_data = {
            "username": "admin",
            "password": "123456",
            "grantType": "password"
        }
        response = requests.post(login_url, data=login_data)
        self.token = response.json().get("data", {}).get("access_token")
        self.headers = {"Authorization": f"Bearer {self.token}"}
    
    def test_create_order(self):
        """创建订单"""
        url = "http://192.168.9.55:5666/apis/order/create"
        data = {"product_id": 1, "quantity": 2}
        response = requests.post(url, json=data, headers=self.headers)
        
        assert response.status_code == 200
        result = response.json()
        assert result.get("code") == 200
        
        # 保存订单 ID，给下一个接口用
        self.order_id = result.get("data", {}).get("order_id")
    
    def test_get_order(self):
        """查询订单"""
        url = f"http://192.168.9.55:5666/apis/order/{self.order_id}"
        response = requests.get(url, headers=self.headers)
        
        assert response.status_code == 200
```

### 4.2 数据驱动（Excel/CSV）

```python
import pytest
import csv
import requests

def read_csv(file_path):
    """读取 CSV 测试数据"""
    test_data = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append(row)
    return test_data

class TestLogin:
    
    @pytest.mark.parametrize("data", read_csv("test_data.csv"))
    def test_login(self, data):
        url = "http://192.168.9.55:5666/apis/mes-auth/token"
        response = requests.post(url, data=data)
        
        assert response.status_code == 200
```

**test_data.csv**：
```csv
username,password,grantType,expected_code
admin,123456,password,200
admin,wrong,password,400
,123456,password,400
admin,,password,400
```

### 4.3 配置文件管理

```python
# config.yaml
# base_url: http://192.168.9.55:5666
# username: admin
# password: 123456
# client_id: mes
# client_secret: mes

import yaml

def load_config(file_path="config.yaml"):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

config = load_config()
base_url = config["base_url"]
```

### 4.4 日志记录

```python
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("test.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# 使用日志
logger.info("开始测试登录接口")
logger.info(f"请求 URL: {url}")
logger.info(f"响应状态码: {response.status_code}")
logger.info(f"响应内容: {response.json()}")
```

---

## 第 5 阶段：数据库断言

### 5.1 Python 连接 MySQL

```bash
pip install pymysql
```

```python
import pymysql

# 连接数据库
conn = pymysql.connect(
    host="192.168.9.55",
    port=3306,
    user="root",
    password="root",
    database="mes",
    charset="utf8mb4"
)

# 创建游标
cursor = conn.cursor()

# 执行 SQL
cursor.execute("SELECT * FROM sys_user WHERE username = %s", ("admin",))
result = cursor.fetchone()
print(result)

# 关闭连接
cursor.close()
conn.close()
```

### 5.2 数据库断言

```python
import pymysql
import requests

def test_create_user():
    # 创建用户
    url = "http://192.168.9.55:5666/apis/user/create"
    data = {"username": "test_user", "password": "123456"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    
    # 数据库断言：验证用户是否创建成功
    conn = pymysql.connect(host="192.168.9.55", user="root", password="root", database="mes")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sys_user WHERE username = %s", ("test_user",))
    result = cursor.fetchone()
    assert result is not None
    cursor.close()
    conn.close()
```

---

## 第 6 阶段：框架搭建 + CI/CD

### 6.1 框架结构

```
api-auto-test/
├── config/
│   └── config.yaml          # 配置文件
├── data/
│   └── test_data.csv        # 测试数据
├── testcases/
│   ├── test_login.py        # 登录测试
│   ├── test_user.py         # 用户测试
│   └── test_order.py        # 订单测试
├── common/
│   ├── requests_util.py     # 请求工具
│   ├── db_util.py           # 数据库工具
│   └── log_util.py          # 日志工具
├── reports/
│   └── report.html          # 测试报告
├── logs/
│   └── test.log             # 日志文件
├── pytest.ini               # pytest 配置
└── requirements.txt         # 依赖
```

### 6.2 Jenkins 集成

```bash
# Jenkins 执行命令
cd api-auto-test
pip install -r requirements.txt
pytest --html=reports/report.html
```

### 6.3 GitHub Actions 集成

```yaml
# .github/workflows/test.yml
name: API Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest --html=reports/report.html
```

---

## 📚 学习检查点

| 阶段 | 检查标准 | 项目产出 |
|------|---------|---------|
| 第 1 阶段 | 能处理 JSON、CSV、Excel 文件 | 数据处理脚本 |
| 第 2 阶段 | 会用 Session、处理超时和异常 | requests 进阶脚本 |
| 第 3 阶段 | 会写 pytest 测试、参数化、Fixture | 测试用例 |
| 第 4 阶段 | 能做接口关联、数据驱动 | 完整测试脚本 |
| 第 5 阶段 | 能做数据库断言 | 数据库验证脚本 |
| 第 6 阶段 | 能搭建框架、集成 CI/CD | 完整框架 |

---

## 🎯 最终目标

学完后，你能：
1. ✅ 独立编写接口自动化测试脚本
2. ✅ 用 pytest 管理测试用例
3. ✅ 用数据驱动测试多种场景
4. ✅ 做接口关联（Token 传递）
5. ✅ 做数据库断言
6. ✅ 搭建完整的测试框架
7. ✅ 集成到 CI/CD

---

> 这个学习计划是**以接口自动化为目标**的 Python 学习路线，跳过了数据挖掘/可视化/爬虫/机器学习等不需要的内容。
