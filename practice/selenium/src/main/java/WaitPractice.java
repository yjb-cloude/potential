import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import java.time.Duration;

/**
 * 等待机制对比练习（Day10）
 * 
 * 实验：用 saucedemo.com 登录，分别验证：
 * 1. 不用等待 → 可能 NoSuchElementException
 * 2. 隐式等待 → 简单全局
 * 3. 显式等待 → 精准（推荐）
 * 
 * 运行：mvn dependency:build-classpath -Dmdep.outputFile=cp.txt
 *       java -cp "target/classes;$(Get-Content cp.txt)" WaitPractice
 */
public class WaitPractice {

    static ChromeOptions getHeadlessOptions() {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-gpu");
        options.addArguments("--window-size=1920,1080");
        return options;
    }

    public static void main(String[] args) throws InterruptedException {
        // ===== 实验 1：隐式等待 =====
        System.out.println("========== 实验 1：隐式等待 ==========");
        WebDriver driver1 = new ChromeDriver(getHeadlessOptions());
        try {
            driver1.manage().timeouts().implicitlyWait(Duration.ofSeconds(10));
            driver1.get("https://www.saucedemo.com/");
            
            long start = System.currentTimeMillis();
            WebElement username = driver1.findElement(By.id("user-name"));
            long cost = System.currentTimeMillis() - start;
            System.out.println("✅ 隐式等待找到元素，耗时: " + cost + "ms");
            
            username.sendKeys("standard_user");
            driver1.findElement(By.id("password")).sendKeys("secret_sauce");
            driver1.findElement(By.id("login-button")).click();
            
            // 隐式等待的局限：页面跳转后，等标题出现还是要手动验证
            Thread.sleep(2000);
            String title = driver1.findElement(By.className("title")).getText();
            System.out.println("页面标题: " + title + (title.equals("Products") ? " ✅" : " ❌"));
        } finally {
            driver1.quit();
        }

        // ===== 实验 2：显式等待 =====
        System.out.println("\n========== 实验 2：显式等待（推荐） ==========");
        WebDriver driver2 = new ChromeDriver(getHeadlessOptions());
        try {
            driver2.get("https://www.saucedemo.com/");
            WebDriverWait wait = new WebDriverWait(driver2, Duration.ofSeconds(10));
            
            long start = System.currentTimeMillis();
            // 等用户名框可点击（精准条件）
            WebElement username = wait.until(
                ExpectedConditions.elementToBeClickable(By.id("user-name"))
            );
            long cost = System.currentTimeMillis() - start;
            System.out.println("✅ 显式等待找到元素，耗时: " + cost + "ms");
            
            username.sendKeys("standard_user");
            driver2.findElement(By.id("password")).sendKeys("secret_sauce");
            driver2.findElement(By.id("login-button")).click();
            
            // 等商品页标题可见（页面跳转的精准等待）
            wait.until(ExpectedConditions.visibilityOfElementLocated(By.className("title")));
            String title = driver2.findElement(By.className("title")).getText();
            System.out.println("页面标题: " + title + (title.equals("Products") ? " ✅" : " ❌"));
        } finally {
            driver2.quit();
        }

        System.out.println("\n🎉 两种等待对比完成！");
    }
}
