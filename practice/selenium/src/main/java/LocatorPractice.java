import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.chrome.ChromeOptions;

/**
 * Day9 练习：8 种元素定位方式
 *
 * 练习页面：testpages/login.html（本地文件，file:// 协议打开）
 *
 * 定位方式一览：
 *  1. By.id()               id 属性，页面必须唯一，最优先用
 *  2. By.name()             表单 name 属性
 *  3. By.className()        class 属性（注意：只能传一个类名）
 *  4. By.tagName()          标签名（input / button / a ...）
 *  5. By.linkText()         链接的完整文本
 *  6. By.partialLinkText()  链接文本的模糊匹配
 *  7. By.xpath()            XML 路径语法，最强大也最啰嗦
 *  8. By.cssSelector()      CSS 选择器语法，简洁
 *
 * 面试高频：这 8 种里你最常用哪几种？为什么？
 * 答案参考：id > cssSelector > xpath。id 唯一稳定；css 简洁；xpath 用于复杂场景
 * （如按文本找元素、层级很深、动态属性时用相对路径 + contains）。
 */
public class LocatorPractice {

    public static void main(String[] args) {
        ChromeOptions options = new ChromeOptions();
        options.addArguments("--headless=new");
        options.addArguments("--no-sandbox");
        options.addArguments("--disable-gpu");
        options.addArguments("--window-size=1920,1080");

        WebDriver driver = new ChromeDriver(options);

        try {
            // 本地页面用 file:// 协议打开（路径换成你自己机器上的）
            String page = "file:///D:/personal-wiki/practice/selenium/testpages/login.html";
            driver.get(page);

            System.out.println("======== 1. By.id：找用户名输入框 ========");
            WebElement username = driver.findElement(By.id("username"));
            print(username, "定位到");

            System.out.println("======== 2. By.name：找密码输入框 ========");
            WebElement password = driver.findElement(By.name("password"));
            print(password, "定位到");

            System.out.println("======== 3. By.className：找登录按钮 ========");
            // 注意：按钮 class 是 "btn btn-primary" 两个类名，只能传其中一个
            WebElement loginBtn = driver.findElement(By.className("btn-primary"));
            print(loginBtn, "定位到");

            System.out.println("======== 4. By.tagName：找页面上第一个按钮 ========");
            // tagName 会返回第一个匹配的，通常用于"页面只有一个某标签"时
            WebElement firstBtn = driver.findElement(By.tagName("button"));
            print(firstBtn, "定位到");

            System.out.println("======== 5. By.linkText：链接完整文本 ========");
            WebElement aboutLink = driver.findElement(By.linkText("关于我们"));
            print(aboutLink, "定位到");

            System.out.println("======== 6. By.partialLinkText：链接模糊文本 ========");
            // 只写"联系"两个字也能命中"联系我们"
            WebElement contactLink = driver.findElement(By.partialLinkText("联系"));
            print(contactLink, "定位到");

            System.out.println("======== 7. By.xpath：三种常用写法 ========");
            // 7.1 属性定位（最常用）
            WebElement byAttr = driver.findElement(By.xpath("//input[@placeholder='请输入用户名']"));
            print(byAttr, "//input[@placeholder=...] 定位到");
            // 7.2 层级 + 索引：form 里第 2 个 div 下的 input（form-group 按序：用户名=1，密码=2）
            WebElement byIndex = driver.findElement(By.xpath("//form/div[2]//input"));
            print(byIndex, "//form/div[2]//input 定位到");
            // 7.3 contains 模糊匹配（处理动态/多类名属性）
            WebElement byContains = driver.findElement(By.xpath("//button[contains(@class,'primary')]"));
            print(byContains, "//button[contains(@class,'primary')] 定位到");

            System.out.println("======== 8. By.cssSelector：三种常用写法 ========");
            // 8.1 id 选择器
            WebElement cssId = driver.findElement(By.cssSelector("#login-form"));
            print(cssId, "#login-form 定位到");
            // 8.2 属性选择器
            WebElement cssAttr = driver.findElement(By.cssSelector("input[name='password']"));
            print(cssAttr, "input[name='password'] 定位到");
            // 8.3 类名选择器（css 可以直接写完整类名，className 不行）
            WebElement cssClass = driver.findElement(By.cssSelector("button.btn-primary"));
            print(cssClass, "button.btn-primary 定位到");

            System.out.println("======== 9. 找不到元素会怎样？======== ");
            try {
                driver.findElement(By.id("not-exist"));
                System.out.println("❌ 意外：竟然找到了");
            } catch (NoSuchElementException e) {
                System.out.println("✅ 抛 NoSuchElementException：定位失败就是它");
            }

            System.out.println("======== 全部定位练习完成 ========");
            System.out.println("温馨提示：定位到元素后，还能通过 getText() 读取文本、getAttribute() 读属性");
            System.out.println("登录按钮文本 = " + loginBtn.getText());
            System.out.println("用户名框的 placeholder = " + username.getAttribute("placeholder"));

        } finally {
            driver.quit();
        }
    }

    /** 打印元素摘要，方便肉眼确认定位到了谁 */
    private static void print(WebElement element, String prefix) {
        String summary = "<" + element.getTagName() + ">"
                + " id=" + element.getAttribute("id")
                + " name=" + element.getAttribute("name")
                + " class=" + element.getAttribute("class")
                + " 文本=" + element.getText();
        System.out.println(prefix + " → " + summary);
    }
}
