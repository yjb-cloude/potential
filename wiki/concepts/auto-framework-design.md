# 自动化测试框架设计

## 分层架构

成熟的自动化测试框架采用分层设计，从底向上依次为：

```
Test Cases（测试用例层）
    ↓
Page Objects / API Wrappers（业务封装层）
    ↓
Utils / Helpers（工具层）
    ↓
Resources（资源层：配置文件、测试数据、驱动等）
```

每层只依赖下一层，上层不跨层调用，确保高内聚低耦合。

## 驱动管理

采用**单例模式**管理 WebDriver 实例，统一配置读取（config.properties / YAML）。多线程执行时结合 **ThreadLocal** 保证每个线程持有独立的 Driver 副本，避免线程安全问题。

```java
public class DriverManager {
    private static ThreadLocal<WebDriver> driver = new ThreadLocal<>();

    public static WebDriver getDriver() {
        return driver.get();
    }

    public static void setDriver(WebDriver d) {
        driver.set(d);
    }
}
```

## 配置化

- **config.properties**：基础配置（环境 URL、超时时间、浏览器类型）
- **YAML**：更复杂的多环境配置，支持结构化的环境切换
- **多环境切换**：通过 Maven Profile 或系统属性 `-Denv=staging` 动态加载

## 数据驱动

支持从多种数据源读取测试数据：
- **Excel**（Apache POI）：适合业务人员维护的表格数据
- **JSON**：接口测试的请求体模板
- **YAML**：配置类测试数据
- **Faker 库**：随机生成测试数据

## 重试机制

实现 `IRetryAnalyzer` 接口 + `@Test(retryAnalyzer = ...)` 注解，失败用例自动重试。结合 Allure 报告记录每次重试的日志和截图。

## 并发执行

通过 TestNG 的 `suite.xml` 配置 `<suite parallel="methods" thread-count="4">` 实现多线程执行。核心前提是 ThreadLocal 保证 Driver 线程安全，以及测试数据相互隔离。

## 报告集成（Allure）

```java
@Epic("用户管理")
@Feature("登录功能")
@Story("密码登录")
@Severity(SeverityLevel.BLOCKER)
@Test
void testLogin() {
    step("输入用户名");
    step("输入密码");
    step("点击登录");
}
```

Allure 支持：`@Step` 方法步骤、`@Attachment` 失败截图、各类分类注解、历史趋势聚合。

## 日志体系

**Log4j 2 / SLF4J** 统一日志管理，在关键操作（点击、输入、跳转）和断言失败时记录日志。UI 自动化在失败时自动截图并附到 Allure 报告。

## 设计模式

- **Page Object**：页面元素 + 操作封装
- **Factory**：动态代理创建页面实例
- **Builder**：构建复杂测试数据对象
- **Singleton**：DriverManager、ConfigReader
- **Strategy**：多种等待策略切换、多种定位策略切换

---

关联：[[selenium-webdriver]] | [[rest-assured-api]] | [[junit-testng]] | [[软件测试知识体系]]
