# Selenium 自动化练习

> 目标：掌握 Selenium WebDriver 自动化测试
> 环境：Java 11 + Maven 3.9.15 + Chrome 137 + Selenium 4.21

---

## 📁 项目结构

```
practice/selenium/
├── pom.xml                    # Maven 配置（Selenium 依赖）
├── src/main/java/
│   └── FirstTest.java         # 第一个脚本：saucedemo 登录自动化
└── cp.txt                     # classpath（mvn dependency:build-classpath 生成）
```

## 🚀 运行方式

```bash
# 编译
mvn compile

# 方式 1：exec 插件（stdout 可能被吞，不推荐）
mvn exec:java -Dexec.mainClass=FirstTest

# 方式 2：直接 java 运行（推荐，输出正常）
mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
java -cp "target/classes;$(Get-Content cp.txt)" FirstTest
```

## ✅ 已完成

### FirstTest.java（2026-08-27 跑通）
- 打开 saucedemo.com 登录页
- 输入 standard_user / secret_sauce
- 点击登录
- 验证跳转到商品列表页（标题 = Products）

## 📚 学到的知识点

### 1. 等待机制（面试必问）
| 类型 | 说明 | 用法 |
|------|------|------|
| **隐式等待** | 全局生效，找元素前等 N 秒 | `driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10))` |
| **显式等待** | 等特定条件满足（推荐） | `WebDriverWait(driver, Duration.ofSeconds(10)).until(ExpectedConditions.elementToBeClickable(...))` |

**为什么不用 Thread.sleep？**
- sleep 固定等待，即使元素已就绪也要傻等
- 等待机制是"等到条件满足就继续"，更智能更高效

### 2. 无头模式（headless）
- 浏览器后台运行，不显示窗口
- CI/CD 环境（Jenkins）跑自动化必用
- 配置：`options.addArguments("--headless=new")`

### 3. 元素定位
- `By.id("user-name")` — ID 定位（最快）
- `By.className("title")` — 类名定位
- 后续要学：Name / CSS Selector / XPath

### 4. 常用操作
- `sendKeys("文本")` — 输入文本
- `.click()` — 点击
- `.getText()` — 读取文本
- `.quit()` — 关闭浏览器

## ⚠️ 踩坑记录

1. **阿里云镜像失效**：`maven.aliyun.com/repository/public` 返回 404 → 改用中央仓库 `repo.maven.apache.org`
2. **element not interactable**：页面没加载完就操作 → 加等待机制
3. **窗口自动关闭**：远程/虚拟环境无法显示窗口 → 用 headless 模式
4. **百度会拦截自动化**：触发安全验证 → 换测试专用网站 saucedemo.com

## 📝 面试话术

> "我用 Selenium WebDriver 做了 UI 自动化测试，熟悉元素定位（ID/Class/CSS/XPath）、显式等待机制、Page Object 模式，能在 CI 环境用无头模式跑自动化。"

## 🎯 下一步

- [ ] 元素定位深入学习（CSS Selector / XPath）
- [ ] 8 种定位方式
- [ ] Page Object 设计模式
- [ ] TestNG 集成（@Test 注解管理用例）
- [ ] 自动化测试框架搭建
