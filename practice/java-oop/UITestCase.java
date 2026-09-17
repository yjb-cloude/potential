/**
 * Part 2 — 继承练习
 * UI 测试用例，继承自 TestCase
 */
public class UITestCase extends TestCase implements Reportable {

    private String browser;  // 新增字段：浏览器

    public UITestCase(int id, String name, String priority, String browser) {
        super(id, name, priority);  // 调用父类构造器，初始化 id, name, priority
        setBrowser(browser);        // 用 setter 做校验
    }

    public String getBrowser() {
        return browser;
    }

    public void setBrowser(String browser) {
        if (browser == null || !browser.matches("Chrome|Firefox|Edge")) {
            throw new IllegalArgumentException("browser 必须是 Chrome / Firefox / Edge，当前值: " + browser);
        }
        this.browser = browser;
    }

    /**
     * 重写 execute()：先打印浏览器信息，再标记执行通过
     */
    @Override
    public void execute() {
        System.out.println("在 " + browser + " 上打开页面...");
        setStatus("PASS");
        System.out.println("执行测试用例: " + getName());
    }

    /**
     * 实现 Reportable 接口：生成 UI 测试报告
     */
    @Override
    public String toReport() {
        return "[UI报告] 用例: " + getName()
                + " | 优先级: " + getPriority()
                + " | 浏览器: " + browser
                + " | 状态: " + getStatus();
    }

    @Override
    public String toString() {
        return "[UI-" + getPriority() + "] " + getName() + " (浏览器: " + browser + ") —— " + getStatus();
    }

    public static void main(String[] args) {
        UITestCase tc = new UITestCase(1, "登录页面测试", "P0", "Chrome");
        tc.execute();
        System.out.println(tc.toString());

        // 测试非法 browser
        try {
            new UITestCase(2, "异常测试", "P1", "Safari");
        } catch (IllegalArgumentException e) {
            System.out.println("browser 校验通过 —— 捕获异常: " + e.getMessage());
        }
    }
}
