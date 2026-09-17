# 进度快照

> 用于跨设备同步学习进度。每次会话结束时更新，新设备读这个文件恢复上下文。
> 📚 首页：[[learning-roadmap]]

## 当前进度
- **阶段**：测试学习 + 面试准备（8 周计划第 5 周左右，目标 9 月中旬可面试）
- **最近学习**：Selenium 自动化入门——第一个脚本跑通（saucedemo 登录）+ 8 种元素定位练习（LocatorPractice.java + 本地练习页）
- **最后更新**：2026-09-20

## 已完成
### Java OOP 全部 4 部分
- ✅ Part 1 封装：`TestCase.java`（getter/setter + 参数校验）
- ✅ Part 2 继承：`UITestCase.java` + `APITestCase.java`（继承 TestCase）
- ✅ Part 3 多态：`Animal/Dog/Cat/Zoo.java`（独立写+数组遍历多态）
- ✅ Part 4 抽象/接口：`Reportable.java` + TestCase 改为抽象类
- ✅ OOP 代码练习共 9 个 Java 文件

### Java 核心进阶
- ✅ Lambda 语法（参数省略、单行省略、表达式 vs 语句）
- ✅ Stream 中间操作 vs 终端操作（惰性求值）
- ✅ Stream filter / map / sorted / collect / count / anyMatch
- ✅ 泛型（类/方法/通配符/类型擦除）
- ✅ Optional（orElse / orElseThrow / map 链式）
- ✅ 异常体系（运行时 vs 受检、try-with-resources）
- ✅ IO 流（字节流/字符流、BufferedReader/Writer、序列化）

### 测试基础
- ✅ saucedemo.com 手工测试
- ✅ 等价类/边界值用例设计（LoginTestDesigner.java）
- ✅ 测试用例结果记录（测试用例结果.md）
- ✅ 错题本已建立（错题本.md，模拟面试已进行 4 轮）
- ✅ API测试入门（MES项目+Postman链式请求）
- ✅ 测试理论体系（[[软件测试知识体系]]）

### SQL（2026-08-11 开始，测试岗面试必考）
- ✅ 电商订单系统练习库：`practice/sql/init.sql`（users/products/orders 三表）
- ✅ 第一关：基础查询（排序/IN/OR/BETWEEN/LIKE/LIMIT）
- ✅ 第二关：聚合统计（COUNT/AVG/MAX/GROUP BY/HAVING 前菜）
- ✅ 第三关：JOIN 多表全通关（三表 JOIN / DISTINCT / LEFT JOIN+IS NULL / IFNULL 补零）
- ✅ 第四关：子查询 + NULL 处理（18-20 题完成，21 题待补）
- ✅ 第五关：测试视角综合题（22-25 题完成，超卖检查是面试案例）

### Selenium 自动化（2026-08 开始）
- ✅ 环境搭建：Maven 项目 + Selenium 4.21 + headless Chrome（远程桌面环境）
- ✅ 第一个脚本：`FirstTest.java` — saucedemo 登录 + 断言进入商品页
- ✅ Day9 元素定位：8 种定位全通关（`LocatorPractice.java` + 本地练习页 `testpages/login.html`）
- ✅ 定位速查笔记：`practice/selenium/定位方式速查.md`（xpath/css 语法 + 踩坑记录）
- ✅ 等待机制概念：Thread.sleep（不用）/ 隐式等待 / 显式等待（`WaitPractice.java` 实验通过）

## 面试题进展
- ✅ `==` vs `equals` / Integer 缓存 / String 常量池
- ✅ 集合遍历删除 / try-catch-finally / String 不可变性
- ✅ 模拟面试 4 轮：测试基础 / 登录场景 / 购物车 / 搜索 / Bug生命周期 / Severity vs Priority
- ✅ SQL 面试模拟 5 题全部完成（JOIN 区别 / WHERE vs HAVING / COUNT 三兄弟 / IS NULL 主键 / 慢查询优化）

### Python 自动化测试（2026-09-20 开始）
- ✅ JSON 数据处理：loads/dumps、嵌套取值、列表推导式过滤、安全取值
- ✅ 文件读写：JSON 文件（load/dump）+ CSV 文件（DictReader/writer）
- ✅ 异常处理：try/except/else/finally、safe_request 封装
- ✅ pytest 入门：assert 断言、@pytest.mark.parametrize 数据驱动
- ✅ conftest.py + fixture（scope="session"）
- ✅ 完整项目结构：conftest.py + test_login.py（参数化）

## 待完成
- [ ] 🔵 SQL 第四关第 21 题：NOT IN vs NOT EXISTS 对比
- [ ] 🔵 Selenium Page Object 模式（LoginPage 类 + 测试类）
- [ ] 🔵 Selenium Page Object 模式（LoginPage 类 + 测试类）
- [ ] 🔵 Rest Assured API 自动化（有 Postman 基础，升级代码自动化）
- [ ] 🟣 AI 测试用例生成器（第五周计划）
- [ ] 🟢 Python 基础学习（已建立知识体系）

## 下次学习建议
1. Python：完善 Day6 pytest 项目，把 test_login.py 跑通
2. Python：接入真实 MES 接口，练习 token 管理 + 断言
3. Selenium：继续 Page Object 模式（LoginPage 类 + 测试类）

```bash
cd D:/personal-wiki
git pull
# 然后说："继续 SQL 练习" 或 "继续面试模拟"
```
