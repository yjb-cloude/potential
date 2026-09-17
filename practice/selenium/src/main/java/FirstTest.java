import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/**
 * 第一个 Selenium 脚本（v4）：无头模式
 * 
 * 为什么用 headless（无头）模式？
 * - 当前环境（远程桌面/虚拟机）无法正常显示 Chrome 窗口
 * - headless = 浏览器后台运行，不显示窗口
 * - CI/CD 环境（Jenkins 等）跑自动化基本都是 headless
 * 
 * 测试场景：saucedemo.com 登录
 * 1. 打开登录页
 * 2. 输入 standard_user / secret_sauce
 * 3. 点登录
 * 4. 验证跳转到商品列表页
 */
public class FirstTest {
    public static void main(String[] args) {
        // 1. 配置 Chrome 选项
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");   // 无头模式
        options.addArguments("--no-sandbox");      // 跳过沙箱检查（服务器环境需要）
        options.addArguments("--disable-gpu");     // 禁用 GPU
        options.addArguments("--window-size=1920,1080");  // 设置窗口大小

        // 2. 创建 Chrome 驱动（使用无头配置）
        WebDriver driver = new ChromeDriver(options);

        try {
            // 3. 隐式等待：全局生效，每次找元素最多等 10 秒
            driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));

            // 4. 打开 saucedemo 登录页
            System.out.println("正在打开 saucedemo.com...");
            driver.get("https://www.saucedemo.com/");

            // 5. 显式等待：等用户名输入框可交互
            WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(15));
            WebElement usernameBox = wait.until(
                ExpectedConditions.elementToBeClickable(By.id("user-name"))
            );

            // 6. 输入用户名
            System.out.println("输入用户名: standard_user");
            usernameBox.sendKeys("standard_user");

            // 7. 输入密码
            System.out.println("输入密码: secret_sauce");
            driver.findElement(By.id("password")).sendKeys("secret_sauce");

            // 8. 点击登录按钮
            System.out.println("点击登录按钮...");
            driver.findElement(By.id("login-button")).click();

            // 9. 等商品列表页标题出现
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("title")));

            // 10. 验证登录成功
            String pageTitle = driver.findElement(By.className("title")).getText();
            System.out.println("页面标题: " + pageTitle);

            if ("Products".equals(pageTitle)) {
                System.out.println("✅ 测试通过：登录成功，进入商品列表页");
            } else {
                System.out.println("❌ 测试失败：页面标题异常：" + pageTitle);
            }

        } finally {
            // 11. 关闭浏览器
            System.out.println("关闭浏览器...");
            driver.quit();
        }
    }
}
