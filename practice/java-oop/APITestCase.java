/**
 * Part 2 — 继承练习
 * API 测试用例，继承自 TestCase
 */
public class APITestCase extends TestCase implements Reportable {

    private String url;           // API 地址
    private String httpMethod;    // GET / POST / PUT / DELETE

    public APITestCase(int id, String name, String priority, String url, String httpMethod) {
        super(id, name, priority);
        setUrl(url);
        setHttpMethod(httpMethod);
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        if (url == null || url.isEmpty()) {
            throw new IllegalArgumentException("url 不能为空");
        }
        this.url = url;
    }

    public String getHttpMethod() {
        return httpMethod;
    }

    public void setHttpMethod(String httpMethod) {
        if (httpMethod == null || !httpMethod.matches("GET|POST|PUT|DELETE")) {
            throw new IllegalArgumentException("httpMethod 必须是 GET/POST/PUT/DELETE，当前值: " + httpMethod);
        }
        this.httpMethod = httpMethod;
    }

    /**
     * 重写 execute()：先打印请求信息，再标记执行通过
     */
    @Override
    public void execute() {
        System.out.println("发送 [" + httpMethod + "] 请求到 " + url + "...");
        setStatus("PASS");
        System.out.println("执行测试用例: " + getName());
    }

    /**
     * 实现 Reportable 接口：生成 API 测试报告
     */
    @Override
    public String toReport() {
        return "[API报告] 用例: " + getName()
                + " | 优先级: " + getPriority()
                + " | 请求: " + httpMethod + " " + url
                + " | 状态: " + getStatus();
    }

    @Override
    public String toString() {
        return "[API-" + getPriority() + "] " + getName() + " (" + httpMethod + " " + url + ") —— " + getStatus();
    }

    public static void main(String[] args) {
        APITestCase tc = new APITestCase(1, "用户登录接口", "P0", "/api/login", "POST");
        tc.execute();
        System.out.println(tc.toString());

        // 测试非法 httpMethod
        try {
            new APITestCase(2, "异常测试", "P1", "/api/test", "PATCH");
        } catch (IllegalArgumentException e) {
            System.out.println("httpMethod 校验通过 —— 捕获异常: " + e.getMessage());
        }
    }
}
