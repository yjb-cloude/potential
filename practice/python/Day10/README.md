# Day 10: 接口测试进阶

## 📁 文件结构
```
Day10/
├── config.py           # 多环境配置（test/pre/prod 切换）
├── logger.py           # 日志模块（loguru，控制台+文件）
├── data_provider.py    # 外部数据驱动（从 JSON 读用例）
├── test_data.json      # 测试数据文件（产品/非技术人员可维护）
├── conftest.py         # 全局 fixture + 测试计时 + 失败自动记录
├── test_api_advanced.py # 4 大测试模式演示
└── README.md           # 本文件
```

## 🎯 今天学了什么

### 1. 多环境配置（config.py）
```python
ENV = "test"  # 改这一行切换环境
config = ENV_CONFIG[ENV]  # 自动加载对应配置
```
**面试话术：** "我用字典管理多环境配置，切环境只改一个变量，其他全自动化"

### 2. 日志管理（logger.py + loguru）
```python
from loguru import logger
logger.info("POST /api/login → 200 OK (0.35s)")
logger.error("POST /api/login → 500 Error")
```
**为什么不用 print？**
- print 只能看当前，日志可以写文件、带时间戳、分级别
- 接口出 bug 时，日志是唯一证据

### 3. 外部数据驱动（data_provider.py + test_data.json）
```python
@pytest.mark.parametrize("case_id,desc,username,password,...", get_login_cases())
def test_login(case_id, desc, ...):
    ...
```
**好处：**
- 加用例只改 JSON，不改代码
- 测试和数据分离，非技术人员也能维护
- 面试必问！

### 4. 软断言（收集所有错误，最后一起报）
```python
errors = []
if "access_token" not in body:
    errors.append("缺少 access_token")
if body.get("expires_in", 0) <= 0:
    errors.append("expires_in 异常")
if errors:
    pytest.fail(f"共 {len(errors)} 个失败:\n" + "\n".join(errors))
```
**硬断言 vs 软断言：**
- 硬断言：第 1 个失败就停
- 软断言：全部执行，最后一起报告（适合多字段验证）

### 5. 链式接口测试（新增 → 查询 → 删除）
```python
def test_01_create():  ...  # 创建，保存 ID
def test_02_query():   ...  # 用 ID 查询验证
def test_03_delete():  ...  # 用 ID 删除清理
```
**关键：** pytest 按方法名排序执行（test_01, test_02, test_03）
**用类变量传数据：** TestAPICallChain.created_id

### 6. conftest.py 进阶
- `scope="session"` → 整个测试只创建一次
- `autouse=True` → 每个测试自动执行（计时、日志）
- `@pytest.hookimpl` → 测试失败自动捕获记录

## 🏗️ 接口自动化框架分层
```
┌─────────────────────────────────────┐
│  用例层（test_*.py）                 │  ← 数据驱动 + 断言 + 链式调用
├─────────────────────────────────────┤
│  数据层（data_provider.py + JSON）   │  ← 外部文件驱动，不改代码
├─────────────────────────────────────┤
│  基础设施层（conftest.py + logger）  │  ← fixture、日志、钩子
├─────────────────────────────────────┤
│  配置层（config.py）                 │  ← 多环境、超时、token
└─────────────────────────────────────┘
```

## 💡 面试高频题

### Q1: 你的接口自动化框架怎么设计的？
**A:** 分四层——配置层（多环境切换）、数据层（JSON 驱动）、基础设施层（fixture+日志）、用例层（数据驱动+断言）

### Q2: 测试数据怎么管理？
**A:** 外部 JSON 文件 + 数据驱动函数。加用例改 JSON，不改代码。好处是维护方便、非技术人员也能改。

### Q3: conftest.py 有什么用？
**A:** 三个作用——
1. 定义公共 fixture（session、token、数据库连接）
2. 自动执行的 fixture（autouse=True，如计时、日志）
3. pytest 钩子（测试失败自动记录）

### Q4: 接口之间有依赖怎么办？
**A:** 用链式调用——第一个接口的返回值存到类变量，后续接口用这个变量。用 test_01/02/03 控制顺序。

### Q5: 怎么生成测试报告？
**A:** Allure——运行 pytest --alluredir=./allure-results，然后 allure serve 打开可视化报告，包含用例数、通过率、耗时、失败详情。

## 🚀 下一步
- 安装 loguru：`pip install loguru`
- 安装 allure：`pip install allure-pytest`
- 运行测试：`pytest Day10/test_api_advanced.py -v -s`
- 生成报告：`pytest Day10/ --alluredir=./allure-results`
