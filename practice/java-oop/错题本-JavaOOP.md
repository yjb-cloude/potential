# Java OOP 错题本

> Java OOP 练习踩坑 + 面试考点复习

---

## 综合练习 — Animal.java 踩坑记录

### Bug 1：`=` vs `==` 混淆

```java
if (name = null)   // ❌ 把 null 赋值给 name，结果永远是 null
if (name == null)  // ✅ 判断 name 是否为 null
```

`=` 是赋值，`==` 是比较。java 里判等用 `==`。

### Bug 2：方法写在了构造器大括号里面

```java
public Animal(String name) {
    // ...
    public String getName() {   // ❌ 方法不能嵌套
        return name;
    }
}
```

构造器和 getName 是**平级**的，要各自独立：

```java
public Animal(String name) {
    // ...
}   // 构造器结束

public String getName() {   // ✅ 独立的方法
    return name;
}
```

### Bug 3：校验完忘记赋值

```java
public Animal(String name) {
    if (name == null) {
        throw new IllegalArgumentException("...");
    }
    // ❌ 缺了 this.name = name;
}
```

校验只是检查合不合法，检查完还得用 `this.name = name` 存进去。

### Bug 4：多余的 `}` 和 缺花括号

IDE 的括号跳动能帮助发现这类问题。写完类之后肉眼检查一下：几个 `{` 就有几个 `}`。

---

## 综合练习 — 多态核心理解

### Animal → Dog / Cat 总结

```
Animal a = new Dog("旺财");
//  ↑               ↑
//  引用类型      实际对象类型
```

**一句话记住多态**：编译看左边，运行看右边。

- **编译时**：编译器看 `Animal` 有没有 `speak()` → 有，通过
- **运行时**：JVM 看实际对象是 `Dog` → 执行 Dog 的 `speak()`

**三个前提**（缺一不可）：
1. 继承关系（`Dog extends Animal`）
2. 方法重写（Dog 有 `@Override speak()`）
3. 父类引用指向子类对象（`Animal a = new Dog()`）

---

## 面试考点 ① — 数据类型 & 运算符

### `==` vs `equals`

| 比较 | 比什么 | 坑点 |
|------|--------|------|
| 基本类型 `==` | 比值 | 无 |
| Integer `==` | 比地址 | -128~127 有缓存，超出范围比地址不同 |
| 基本类型 vs 包装类 | 自动拆箱 | `int == Integer` → 拆成 int 比 |
| String `==` | 比地址 | 常量池里的相同字面量指向同一对象 |
| `equals()` | 比内容 | 引用类型必须用 equals 比内容 |

### 踩坑记忆

```
Integer x = 200; Integer y = 200;  → x == y → false（超出缓存范围）
Integer a = 100; Integer b = 100;  → a == b → true（在缓存范围）
int a = 100; Integer b = 100;     → a == b → true（自动拆箱）
"a" == "a"                        → true（常量池）
new String("a") == "a"             → false（new 强制堆分配）

---

## 第 1 题：封装是什么？为什么要封装？

**我的回答**：封装就是把属性和方法放在一起，只能内部访问和使用。为什么要使用封装：为了防止外部修改属性值，具有安全作用。

**纠错**：

1. **"把属性和方法放在一起"** — 这不叫封装，这叫**类**。封装的关键不是"放一起"，而是**"藏起来"**：字段设 `private` → 外面不能直接碰；通过 `public` 的 getter/setter → 外面能间接用，但得走你的规则。

2. **"只能内部访问"** — 不对。封装后外面**可以访问**，只是不能**直接访问字段**。必须通过你暴露的方法。

3. **"防止外部修改"** → 更准确：**控制如何修改**。setter 里加校验，不是"不让改"，而是"改之前检查一遍"。

**正确理解**：封装 = 私有字段 + 公共方法。核心是**数据安全由类自己保证，外部不用操心**。

---

## 第 2 题：访问修饰符

**我的回答**：（未作答）

**补全**：

| 修饰符 | 同类 | 同包 | 子类 | 全局 |
|--------|------|------|------|------|
| `private` | ✅ | ❌ | ❌ | ❌ |
| `default`（不写） | ✅ | ✅ | ❌ | ❌ |
| `protected` | ✅ | ✅ | ✅ | ❌ |
| `public` | ✅ | ✅ | ✅ | ✅ |

---

## 第 3 题：Getter/Setter vs public 字段

**我的回答**：方案 B 可以让外部通过 get set 方法访问和使用，如果直接使用会报错，在 setter 里面加校验能避免修改的值超出范围。

**纠错**：

1. **"如果直接使用会报错"** — `public int age` 不会编译报错。`p.age = -5` **编译通过**，只是逻辑上年龄不可能为负，属于**运行时逻辑错误**。

2. **核心区别**：方案 A 外部随便改，没人拦；方案 B 的 setter 里加 `if (age < 0)` 校验，**非法值在入口处就被拦截了**。

**正确理解**：封装的实际价值 = **数据合法性由类自己保证**。

---

## 第 4 题：this 关键字

**我的回答**：这里 name 为 null，最后会报空指针异常，this 在这里起到了区别属性名称的作用，防止属性和参数同名。

**纠错**：

1. **"会报空指针异常"** — ❌ 不会报错。`name = name;` 是把参数赋给自己，**什么也不会改**。问题是：**字段 `this.name` 永远是 null**，因为你根本没给它赋值。调用后 `s.getName()` 返回 `null`，而不是抛异常。

2. **"this 区分属性名"** — 方向对，但要更精确：`this` 不是"防止同名"，而是**当参数和字段同名时，用来指明"我要的是字段，不是参数"**。

```java
name = name;        // 参数 = 参数 → 字段没变
this.name = name;   // 字段 = 参数 → ✅ 正确
```

---

## 第 5 题：构造器 vs Setter

**我的回答**：构造器是用来构造类的，是外部访问时的一个入库，而 setter 是途径。学生应该放在 setter 里面。

**纠错**：

**结论反了** — 必填字段（如姓名）应该放**构造器**，不是 setter。

**问题在于空窗期**：

```java
Student s = new Student();   // 创建了
s.setName("张三");           // 但还没设名字！

// 这两行代码之间，s 是一个"没有名字的学生"
// setName 如果忘了调，整个对象就是坏的
```

**构造器保证：对象一旦创建，就是合法的、完整的。**

```java
public Student(String name, int age) {
    if (name == null || name.isEmpty()) {
        throw new IllegalArgumentException("姓名不能为空");
    }
    this.name = name;
    this.age = age;
}
```

`new Student()` 这行执行完，你 **100% 确定**它有名字、有年龄。

---

## 总结

| 题 | 我原来的理解 | 正确理解 |
|----|------------|---------|
| 封装 | 属性和方法放一起 | 藏数据，通过方法控制访问 |
| 修饰符 | 没答 | private < default < protected < public |
| Getter/Setter | public 字段会报错 | public 字段**编译不报错**，是**逻辑错误** |
| this | 防空指针 | 区分**字段**和**参数** |
| 构造器 vs Setter | 必填字段放 setter | 必填字段放**构造器**，保证创建即完整 |

---

## Part 2 — 继承

### 热身题：super() 传父类参数

**我的回答**：没思路。

**正确理解**：子类构造器里用 `super(参数)` 调用父类构造器，必须写在**第一行**。因为父类必须先初始化好，子类才能接着初始化——就像盖楼，先有地基再有楼层。

```java
public UITestCase(int id, String name, String priority, String browser) {
    super(id, name, priority);   // ← 第一行，调用父类构造器
    this.browser = browser;
}
```

### 继承的核心概念

| 概念 | 说明 |
|------|------|
| `extends` | 声明继承，`class UITestCase extends TestCase` |
| `super()` | 调用父类构造器（第一行） |
| `super.方法()` | 调用父类的普通方法，用于**扩展**而非替换 |
| `@Override` | 重写父类方法，编译器检查签名是否匹配 |

**重写 (Override)** vs **重载 (Overload)**：
- Override = 同名同参，子类有自己的实现（如 `execute()`）
- Overload = 同名不同参，同一个类里多个版本

**继承的访问规则**：子类能直接访问父类的 `protected` / `public` / `default(同包)`，不能访问 `private`。

**为什么 `UITestCase` 和 `APITestCase` 不用重复写 id、name、priority？**
因为继承自 `TestCase`，这些字段和方法都自动有了。新增的字段（browser、url）只在自己的类里定义。

### 练习成果

创建了 `UITestCase.java` 和 `APITestCase.java`，都继承了 `TestCase`：
- 通过 `super(id, name, priority)` 复用父类构造器
- 通过 `@Override execute()` 扩展行为：先打印自己的信息，再 `super.execute()` 执行父类逻辑
- 新增字段都有 setter 校验，和父类风格一致

---

## 面试考点 ① — 数据类型 & 运算符

### `==` vs `equals`

| 比较 | 比什么 | 坑点 |
|------|--------|------|
| 基本类型 `==` | 比值 | 无 |
| Integer `==` | 比地址 | -128~127 有缓存，超出范围比地址不同 |
| 基本类型 vs 包装类 | 自动拆箱 | `int == Integer` → 拆成 int 比 |
| String `==` | 比地址 | 常量池里的相同字面量指向同一对象 |
| `equals()` | 比内容 | 引用类型必须用 equals 比内容 |

### 踩坑记忆

```
Integer x = 200; Integer y = 200;  → x == y → false（超出缓存范围）
Integer a = 100; Integer b = 100;  → a == b → true（在缓存范围）
int a = 100; Integer b = 100;     → a == b → true（自动拆箱）
"a" == "a"                        → true（常量池）
new String("a") == "a"             → false（new 强制堆分配）
```

---

## 面试考点 ④⑤ — 集合 & 异常

### 集合遍历删除

| 方式 | 能删吗 | 原因 |
|------|--------|------|
| `for (int i = 0; ...)` | 能 | 但需要 `i--` 回退，否则漏删 |
| 增强 `for (String s : list)` | ❌ | 抛 `ConcurrentModificationException` |
| 迭代器 `iterator.remove()` | ✅ | 唯一安全姿势 |

### try-catch-finally 执行顺序

```
try { return 1; }
catch { return 2; }
finally { return 3; }
// 结果: 3    ← finally 的 return 覆盖一切
```

```
try { x = 1; return x; }
finally { x = 2; }
// 结果: 1    ← 返回值在 return 时已暂存，finally 改 x 不影响
```

- finally 一定执行（除非 System.exit 或 JVM 崩溃）
- finally 里改变量 ≠ 改返回值

---

## 2026-07-17 复习考试 — 二刷错题

### ❌ `new String("a") == "a"` 答成 true（二刷错）

错误理解："new 出来的还是指向常量池的 a"。
正确：**看见 `new` 就是堆里新对象**，绝不复用常量池 → 两个地址 → `false`。
对比：`"a" == "a"` → true（都指向常量池同一个）。

### ⚠️ 异常名记不住

增强 for 里删元素 → 抛 **`ConcurrentModificationException`**（并发修改异常）。

### ⚠️ Integer == 只答"比地址"，漏了缓存范围

必须带上 **-128~127**：范围内走缓存 → true；超出 → 新对象 → false。

### ⚠️ 访问修饰符表两次跳过

private < default < protected < public，四级表要背（第 7 题继承访问权限靠它推导）。

---

## 面试考点 ⑥ — String 不可变 & 常量池

### String 拼接创建几个对象？

```java
String s = "hello";
s = s + " world";
// 3 个对象：① "hello"（常量池） ② " world"（常量池） ③ "hello world"（堆）
```

- String 是 `final` 的，一旦创建内容不可变
- `+` 拼接底层是 `StringBuilder` → `.toString()` → `new String()`
- 循环拼接用 `StringBuilder` 手动写，避免大量中间对象

---

## 2026-07-20 Part 4 抽象类/接口/static-final

### ❌ `new String("a") == "a"` 三刷又答错（第三次了！！！）

答成 true，正确是 false。

**这次说清楚为什么记混：** 觉得 `"a"` 在常量池，`new String("a")` 构造时也传了 `"a"`，就以为指向同一个。错在**看见 `new` 就应该反应——堆上新对象**，地址不一样。

**对比记忆（不会再忘版）：**
```
"a" == "a"                     → true  同一常量池
new String("a") == "a"          → false  堆 vs 常量池
new String("a").intern() == "a" → true   intern 手动入池
```

### ❌ 接口 vs 抽象类说反了

**我说的：** "接口只能被一个类实现，抽象类能被多个类继承"
**正确：** "接口可以被多个类实现（多实现），抽象类只能被一个类继承（单继承）"

**一句话永远不忘：** 接口 = 合同（一个人签多份合同），抽象类 = 血缘（一个人只有一个亲爹）

### ❌ 场景法答成缺陷生命周期

问的是搜索功能的场景法，答了"发现bug→提bug→复现bug→解决bug"，这是缺陷生命周期，不是场景法。

**场景法速记：** 基本流 = 一路绿灯正常走完；备选流 = 走岔路了但系统有处理
- 基本流：输入关键词 → 搜索 → 展示结果列表
- 备选流：输入非法字符 → 搜索 → 提示"请输入有效关键词"
- 备选流：无搜索结果 → 显示"未找到相关商品"

### ⚠️ 前置条件"正确"太模糊

**错误写法：** "用户输入正确的注册信息"
**正确写法：** "用户名6~16位字母数字、密码≥8位、手机号11位数字"

**原则：** 前置条件不能出现"正确/正常/合适"这类主观词，要写成可验证的具体规则。

### ✅ 加深理解（这次答对了）

- static/final: final 变量 ≠ 值不能变，是引用不能变（`final StringBuilder` 内容可以改）
- 抽象类本质：不能 new，必须通过子类多态使用
- `new TestCase[3]` 是数组不是对象，抽象类不能 new 对象**但可以 new 数组容器**

### 📌 代码变动

因为 `TestCase` 改为抽象类，`LoginTestDesigner.java` 里原本 `new TestCase(...)` 的地方替换掉了。

---
