# Java OOP 代码练习 — 测试场景版

> 关联知识：[[wiki/concepts/junit-testng]] | [[wiki/concepts/test-case-design]]
> 目标：通过动手写代码，巩固封装、继承、多态、抽象类/接口四大 OOP 核心概念

---

## 📚 基础知识速查

### 什么是 OOP？

OOP = **面向对象编程**。把现实世界中的事物抽象成"对象"，每个对象有**属性**（数据）和**行为**（方法）。
Java 是纯 OOP 语言——一切代码都要写在 class 里。

### 类 vs 对象

| 概念 | 类比 | 代码 |
|------|------|------|
| **类 (Class)** | 图纸、模板 | `class TestCase { ... }` |
| **对象 (Object)** | 用图纸盖出来的房子 | `new TestCase(1, "登录", "P0")` |

一个类可以创建无数个对象，就像一张图纸可以盖无数栋房子。

### OOP 四大支柱

```
┌─────────────────────────────────────────────┐
│              OOP 四大支柱                     │
│                                             │
│  ① 封装 Encapsulation   → 藏数据，暴露行为    │
│  ② 继承 Inheritance     → 子类复用父类代码     │
│  ③ 多态 Polymorphism    → 同一方法，不同表现   │
│  ④ 抽象 Abstraction     → 抓本质，忽略细节    │
└─────────────────────────────────────────────┘
```

#### ① 封装 — 把数据藏起来，通过方法访问

**核心思想**：字段设为 `private`，不让外部直接碰；提供 `public` 的 getter/setter 控制访问。

```java
// ❌ 不封装：谁都能改，改错了没人管
public int age;

// ✅ 封装：外部只能通过 setter 改，setter 里可以做校验
private int age;
public void setAge(int age) {
    if (age < 0 || age > 150) throw new IllegalArgumentException();
    this.age = age;
}
```

**为什么要封装？**
- **数据安全**：防止外部设出非法值（比如年龄 -5）
- **隐藏实现**：内部怎么存，外部不需要知道
- **可控修改**：setter 里加日志、触发事件等

#### ② 继承 — 子类自动拥有父类的字段和方法

```java
class Animal {           // 父类
    void eat() { ... }
}
class Dog extends Animal {  // 子类
    void bark() { ... }
}
```

Dog 对象既能 `eat()` 也能 `bark()`，因为继承了 Animal。

**关键字**：`extends`（继承）、`super`（调用父类）、`@Override`（重写父类方法）

#### ③ 多态 — 同一引用类型，实际指向不同子类对象

```java
TestCase tc = new UITestCase(...);  // 左边是父类类型，右边是子类对象
tc.execute();  // 实际执行的是 UITestCase 的 execute()
```

**好处**：写代码时面向父类/接口，运行时自动适配具体子类。`runAll(TestCase[] tests)` 可以混放各种子类。

#### ④ 抽象 — 只定义"有什么"，不定义"怎么做"

- **抽象类** (`abstract class`)：可以有抽象方法（没 body）和普通方法；不能被实例化，只能被继承
- **接口** (`interface`)：全是契约（方法签名），实现类必须实现所有方法；Java 8 起可以有 `default` 方法

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
