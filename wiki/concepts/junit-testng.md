# JUnit 5 与 TestNG

JUnit 和 TestNG 是 Java 生态中最主流的两个测试框架。JUnit 5 是现代 Java 项目的首选，TestNG 在复杂测试场景（数据驱动、分组、依赖）上更具优势。

## JUnit 5 核心注解

| 注解 | 说明 |
|------|------|
| `@Test` | 标记测试方法 |
| `@BeforeEach` | 每个测试方法前执行 |
| `@AfterEach` | 每个测试方法后执行 |
| `@BeforeAll` | 所有测试前执行一次（需 static） |
| `@AfterAll` | 所有测试后执行一次（需 static） |
| `@DisplayName` | 自定义测试显示名称 |
| `@Disabled` | 禁用测试 |

## TestNG 特有功能

- **`@BeforeSuite` / `@AfterSuite`**：Suite 级别前后置，适合全局初始化/清理
- **`@DataProvider`**：数据驱动测试，方法返回 `Object[][]` 或 `Iterator<Object[]>`
- **`@Test(priority = N)`**：控制测试执行顺序（数值越小越先执行）
- **`@Test(dependsOnMethods = {...})`**：指定依赖方法，被依赖方法失败则跳过

## 参数化测试对比

**JUnit 5：**
```java
@ParameterizedTest
@CsvSource({"1, 张, 三", "2, 李, 四"})
void testCreateUser(int id, String firstName, String lastName) { }

@ValueSource(strings = {"admin", "user", "guest"})
void testRole(String role) { }

@MethodSource("dataProvider")
void testWithMethodSource(String input) { }
```

**TestNG：**
```java
@Test(dataProvider = "userData")
void testCreateUser(int id, String firstName, String lastName) { }

@DataProvider(name = "userData")
Object[][] provideData() { return new Object[][]{{1, "张", "三"}, {2, "李", "四"}}; }
```

## 断言

| JUnit 5 | TestNG | 用途 |
|---------|--------|------|
| `assertEquals(expected, actual)` | `Assert.assertEquals()` | 相等断言 |
| `assertTrue(condition)` | `Assert.assertTrue()` | 条件为真 |
| `assertThrows(Exception.class, () -> {...})` | `expectedExceptions` 注解属性 | 异常断言 |
| `assertAll(() -> {...}, () -> {...})` | 无原生支持 | 组合断言（全部执行不短路） |
| `assertIterableEquals()` | 无 | 集合内容相等 |

TestNG 的 **SoftAssert** 允许断言失败后继续执行，最后统一汇总失败信息：`softAssert.assertAll()`。

## 分组执行

**JUnit 5 `@Tag`：**
```java
@Tag("smoke") @Tag("regression")
void testLogin() { }
```

**TestNG `@Test(groups = {"smoke", "regression"})`：**
```java
@Test(groups = {"smoke"})
void testLogin() { }
```

## 测试运行顺序

JUnit 5 通过 `@TestMethodOrder(MethodOrderer.OrderAnnotation.class)` + `@Order(N)` 控制顺序。TestNG 通过 `@Test(priority = N)` 实现。

---

关联：[[auto-framework-design]] | [[selenium-webdriver]] | [[rest-assured-api]]
