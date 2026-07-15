/**
 * Part 1 — 封装练习
 * 表示一条测试用例
 */
public class TestCase {

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

    // ===== 方法 =====
    public void execute() {
        this.status = "PASS";
        System.out.println("执行测试用例: " + this.name);
    }

    @Override
    public String toString() {
        return "[" + this.priority + "] " + this.name + " —— " + this.status;
    }

    // ===== 测试入口 =====
    public static void main(String[] args) {
        // 正常流程：创建一个 TestCase 对象，调 execute()，打印 toString()
        TestCase tc = new TestCase(1, "登录功能测试", "P0");
        tc.execute();
        System.out.println(tc.toString());

        // 测试异常情况：传非法 priority
        try {
            new TestCase(2, "异常测试", "P5");
        } catch (IllegalArgumentException e) {
            System.out.println("priority 校验通过 —— 捕获异常: " + e.getMessage());
        }

        // 测试异常情况：传非法 status
        try {
            tc.setStatus("UNKNOWN");
        } catch (IllegalArgumentException e) {
            System.out.println("status 校验通过 —— 捕获异常: " + e.getMessage());
        }
    }
}
