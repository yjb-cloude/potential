# Java OOP 代码练习 — 测试场景版

> 关联知识：[[wiki/concepts/junit-testng]] | [[wiki/concepts/test-case-design]]
> 目标：通过动手写代码，巩固封装、继承、多态、抽象类/接口四大 OOP 核心概念

---

## Part 1 — 封装 (Encapsulation)

**场景**：写一个 `TestCase` 类，表示一条测试用例。

要求：
- 私有字段：`id` (int)、`name` (String)、`priority` (String: "P0"/"P1"/"P2"/"P3")、`status` (String: "PASS"/"FAIL"/"SKIP"/"PENDING")
- 提供 getter/setter，在 setter 中做参数校验：
  - `priority` 只接受 "P0"、"P1"、"P2"、"P3"，否则抛 `IllegalArgumentException`
  - `status` 只接受 "PASS"、"FAIL"、"SKIP"、"PENDING"，否则抛异常
- 提供 `execute()` 方法，把 `status` 改成 "PASS" 并打印执行日志
- 重写 `toString()` 返回格式：`[P0] 用例名称 —— PASS`

**创建文件**: `TestCase.java`

完成后运行测试验证。

---

## Part 2 — 继承 (Inheritance)

**场景**：不同类型的测试用例有不同执行方式。

创建两个子类继承 `TestCase`：

**`UITestCase`**：
- 新增字段：`browser` (String: "Chrome"/"Firefox"/"Edge")
- 重写 `execute()`：打印 "在 [browser] 上打开页面..." 再执行父类逻辑
- 使用 `super` 调用父类构造器

**`APITestCase`**：
- 新增字段：`url` (String)、`httpMethod` (String: "GET"/"POST"/"PUT"/"DELETE")
- 重写 `execute()`：打印 "发送 [GET] 请求到 [url]..." 再执行父类逻辑

**创建文件**: `UITestCase.java`、`APITestCase.java`

---

## Part 3 — 多态 (Polymorphism)

**场景**：写一个 `TestRunner`，能批量执行不同类型的测试用例。

- 定义一个 `runTest(TestCase tc)` 静态方法：调用 `tc.execute()`
- 定义一个 `runAll(TestCase[] tests)` 静态方法：遍历数组逐个执行
- 在 `main` 中创建一个包含 `TestCase`、`UITestCase`、`APITestCase` 的数组，传给 `runAll()` 验证多态行为

**创建文件**: `TestRunner.java`

---

## Part 4 — 抽象类 / 接口 (Abstract & Interface)

**场景**：让设计更规范。

1. 把 `TestCase` **改为抽象类**，`execute()` 改为抽象方法
2. 创建一个 **`Reportable` 接口**，包含：
   - `String toReport()` —— 生成测试报告文本
   - `default void printReport()` —— 默认实现打印报告
3. 让 `UITestCase` 和 `APITestCase` 实现 `Reportable` 接口
4. 在 `TestRunner` 中增加 `generateReport(Reportable[] items)` 方法

**修改文件**: `TestCase.java`（改为抽象类）、新建 `Reportable.java`、修改子类和 `TestRunner`
