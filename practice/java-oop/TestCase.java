/**
 * Part 1 — 封装练习
 * 表示一条测试用例
 */
public abstract class TestCase {

    // ===== 私有字段 =====
    private int id;
    private String name;
    private String priority;   // "P0" ~ "P3"
    private String status;     // "PASS" / "FAIL" / "SKIP" / "PENDING"

    // ===== 构造器 =====
    public TestCase(int id, String name, String priority) {
        setId(id);
        setName(name);
        setPriority(priority);
        this.status = "PENDING";
    }

    // ===== Getter / Setter =====
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPriority() {
        return priority;
    }

    public void setPriority(String priority) {
        if (priority == null || !priority.matches("P[0-3]")) {
            throw new IllegalArgumentException("priority 必须是 P0 ~ P3，当前值: " + priority);
        }
        this.priority = priority;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        if (status == null || !status.matches("PASS|FAIL|SKIP|PENDING")) {
            throw new IllegalArgumentException("status 必须是 PASS / FAIL / SKIP / PENDING，当前值: " + status);
        }
        this.status = status;
    }

    // ===== 抽象方法 =====
    public abstract void execute();

    @Override
    public String toString() {
        return "[" + this.priority + "] " + this.name + " —— " + this.status;
    }

    // ===== 测试入口 =====
    public static void main(String[] args) {
        // ===== Part 3 — 多态测试 =====
        TestCase[] tests = new TestCase[3];
        tests[0] = new UITestCase(1, "UI测试", "P0", "Firefox");
        tests[1] = new APITestCase(2, "API测试", "P2", "/api/users", "POST");
        tests[2] = new UITestCase(3, "兼容性测试", "P1", "Edge");

        // 遍历数组，逐个执行（多态：编译看 TestCase，运行看实际类型）
        for (TestCase t : tests) {
            t.execute();
        }

        // 测试异常情况：传非法 priority（通过子类触发父类的 setter 校验）
        try {
            new UITestCase(4, "异常测试", "P5", "Chrome");
        } catch (IllegalArgumentException e) {
            System.out.println("priority 校验通过 —— 捕获异常: " + e.getMessage());
        }

        // 测试异常情况：传非法 status
        try {
            tests[0].setStatus("UNKNOWN");
        } catch (IllegalArgumentException e) {
            System.out.println("status 校验通过 —— 捕获异常: " + e.getMessage());
        }

        // ===== Part 4 — 接口多态测试 =====
        System.out.println("\n--- 生成测试报告 ---");
        Reportable[] reports = new Reportable[3];
        reports[0] = new UITestCase(4, "登录页面", "P0", "Chrome");
        reports[1] = new APITestCase(5, "用户接口", "P1", "/api/user", "GET");
        reports[2] = new UITestCase(6, "注册页面", "P2", "Edge");

        for (Reportable r : reports) {
            r.printReport();  // 默认方法：打印报告
        }
    }
}
