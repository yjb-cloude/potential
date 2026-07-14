# Selenium WebDriver

## 架构

Selenium 采用经典的 C/S 架构，自底向上分为四层：

- **浏览器**：Chrome、Firefox、Edge 等真实浏览器
- **Browser Drivers**：各浏览器厂商提供的驱动（chromedriver、geckodriver），负责将 WebDriver 指令翻译为浏览器原生操作
- **WebDriver API**（W3C 标准协议）：客户端与驱动之间的 JSON Wire Protocol 通信
- **Client Libraries**：Java、Python、C#、Ruby、JavaScript 等多语言绑定

## 元素定位（8 种）

Selenium 提供 8 种定位方式，按推荐程度排序：

| 定位策略 | 方法 | 适用场景 |
|---------|------|---------|
| ID | `findElement(By.id())` | 元素有唯一 ID（最快） |
| Name | `findElement(By.name())` | 表单字段 |
| ClassName | `findElement(By.className())` | 样式类定位 |
| TagName | `findElement(By.tagName())` | 批量获取同类标签 |
| LinkText | `findElement(By.linkText())` | 精确匹配超链接文本 |
| PartialLinkText | `findElement(By.partialLinkText())` | 模糊匹配超链接文本 |
| XPath | `findElement(By.xpath())` | 万能定位，支持复杂 DOM 路径 |
| CssSelector | `findElement(By.cssSelector())` | 比 XPath 性能更好，支持 `#id` `.class` `[attr]` |

## XPath 常用语法

- `//` — 从任意位置选取节点
- `/` — 从根节点选取直接子节点
- `@` — 选取属性，如 `//input[@id='username']`
- `[]` — 条件过滤，如 `//div[@class='container']`
- `text()` — 匹配文本，如 `//button[text()='提交']`
- `contains()` — 模糊匹配，如 `//button[contains(text(),'提交')]`
- 轴：`following-sibling::`、`ancestor::`、`parent::`

## 三种等待机制

1. **ImplicitlyWait**：全局隐式等待，在 `findElement` 时轮询 DOM，直到元素出现或超时
2. **WebDriverWait + ExpectedConditions**：显示等待，针对特定条件，如 `visibilityOfElementLocated`、`elementToBeClickable`、`presenceOfElementLocated`
3. **FluentWait**：最灵活的等待，可自定义轮询间隔和忽略异常类型

## Page Object 设计模式

```
BasePage（通用方法：find/sendKeys/click/wait）
  └── LoginPage（登录相关元素 + 操作）
  └── HomePage（首页相关元素 + 操作）
  └── SearchPage（搜索相关元素 + 操作）
```

每个 Page 类封装页面元素定义 + 操作方法，测试用例只调用业务方法，不接触底层定位。

## 特殊元素处理

- **iframe**：`driver.switchTo().frame()` 进入，操作完 `switchTo().defaultContent()` 退出
- **Alert**：`driver.switchTo().alert()` → `accept()` / `dismiss()` / `getText()` / `sendKeys()`
- **下拉框（Select）**：实例化 `new Select(element)`，支持 `selectByIndex` / `selectByValue` / `selectByVisibleText`
- **多窗口**：`getWindowHandles()` 获取所有句柄，`switchTo().window(handle)` 切换

## 浏览器配置

```java
ChromeOptions options = new ChromeOptions();
options.addArguments("--headless");   // 无头模式
options.addArguments("--disable-gpu");
options.addArguments("--window-size=1920,1080");
WebDriver driver = new ChromeDriver(options);
```

## 驱动管理

使用 **WebDriverManager**（Boni Garcia）自动匹配浏览器版本下载驱动，无需手动维护 `webdriver.chrome.driver` 系统属性。

---

关联：[[auto-framework-design]] | [[junit-testng]] | [[软件测试知识体系]]
