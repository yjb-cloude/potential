/**
 * Lambda + Stream 练习
 * 基于 TestCase 体系操作测试用例集合
 *
 * 使用前确保在同一目录下有：
 *   TestCase.java  UITestCase.java  APITestCase.java  Reportable.java
 *
 * 编译：javac TestManager.java
 * 运行：java TestManager
 *
 * TODO 标记就是你要补的练习，补完看看输出对不对
 */

import java.util.*;
import java.util.stream.Collectors;

public class TestManager {

    // ===== 准备测试数据 =====
    private static List<TestCase> createTestCases() {
        List<TestCase> list = new ArrayList<>();
        list.add(new UITestCase(1,  "登录页面UI验证",    "P0", "Chrome"));
        list.add(new APITestCase(2,  "用户登录接口",      "P0", "/api/login", "POST"));
        list.add(new UITestCase(3,  "注册页面兼容性",    "P1", "Firefox"));
        list.add(new APITestCase(4,  "获取用户信息",      "P1", "/api/user", "GET"));
        list.add(new APITestCase(5,  "创建订单接口",      "P0", "/api/order", "POST"));
        list.add(new UITestCase(6,  "订单列表UI",        "P2", "Chrome"));
        list.add(new APITestCase(7,  "删除订单接口",      "P2", "/api/order/1", "DELETE"));
        list.add(new APITestCase(8,  "批量查询用户",      "P3", "/api/users", "GET"));
        list.add(new UITestCase(9,  "个人中心页面",      "P3", "Edge"));
        list.add(new APITestCase(10, "更新用户信息",     "P1", "/api/user", "PUT"));

        // 模拟部分用例已执行
        list.get(0).setStatus("PASS");
        list.get(1).setStatus("FAIL");
        list.get(2).setStatus("PASS");
        list.get(3).setStatus("PASS");
        list.get(4).setStatus("PENDING");
        list.get(5).setStatus("SKIP");
        return list;
    }

    public static void main(String[] args) {
        List<TestCase> cases = createTestCases();

        // =============================================
        // 示例：传统 for 循环 vs Stream
        // =============================================
        System.out.println("========== 全部测试用例 ==========");
        cases.forEach(tc -> System.out.println("  " + tc));

        // =============================================
        // 练习 1：filter —— 筛选
        // =============================================
        System.out.println("\n========== 练习1：filter 筛选 ==========");

        // ---- 示例 ----
        System.out.println("--- [示例] 筛选 P0 用例 ---");
        cases.stream()
            .filter(tc -> "P0".equals(tc.getPriority()))
            .forEach(tc -> System.out.println("  " + tc));

        // ---- TODO 1 自己写 ----
        System.out.println("--- [TODO 1] 筛选出 FAIL 的用例 ---");
        // ↓ 把下划线改成你的代码（删掉 ! 号）
        cases.stream()
            .filter(tc -> "FAIL".equals(tc.getStatus()))
            .forEach(tc -> System.out.println("  " + tc));

        // ---- TODO 2 自己写 ----
        System.out.println("--- [TODO 2] 筛选出 APITestCase 类型的用例 ---");
        // 提示：用 instanceof，如 tc -> tc instanceof APITestCase
        cases.stream()
            .filter(tc -> tc instanceof APITestCase)
            .forEach(tc -> System.out.println("  " + tc));

        // =============================================
        // 练习 2：map —— 转换
        // =============================================
        System.out.println("\n========== 练习2：map 转换 ==========");

        // ---- 示例 ----
        System.out.println("--- [示例] 提取所有用例的名称 ---");
        cases.stream()
            .map(tc -> tc.getName())
            .forEach(name -> System.out.println("  " + name));

        // ---- TODO 3 自己写 ----
        System.out.println("--- [TODO 3] 转成短格式：[P0] 登录页面UI验证 ---");
        // 提示：map(tc -> "[" + tc.getPriority() + "] " + tc.getName())
        cases.stream()
            .map(___________________________)
            .forEach(line -> System.out.println("  " + line));

        // =============================================
        // 练习 3：collect —— 收集到集合
        // =============================================
        System.out.println("\n========== 练习3：collect 收集 ==========");

        // ---- 示例：收集到 List ----
        List<TestCase> p0Cases = cases.stream()
            .filter(tc -> "P0".equals(tc.getPriority()))
            .collect(Collectors.toList());
        System.out.println("P0 用例数量: " + p0Cases.size());

        // ---- 示例：收集到 Set（自动去重） ----
        Set<String> levels = cases.stream()
            .map(tc -> tc.getPriority())
            .collect(Collectors.toSet());
        System.out.println("存在的优先级: " + levels);

        // ---- TODO 4 自己写 ----
        System.out.println("--- [TODO 4] 收集所有 FAIL 的用例到 List ---");
        // 配合 .filter() + .collect(Collectors.toList())，打印数量
        List<TestCase> ________ = _______________
        System.out.println("FAIL 用例数量: " + __________);

        // =============================================
        // 练习 4：sorted —— 排序
        // =============================================
        System.out.println("\n========== 练习4：sorted 排序 ==========");

        // ---- 示例 ----
        System.out.println("--- [示例] 按优先级排序 ---");
        cases.stream()
            .sorted((a, b) -> a.getPriority().compareTo(b.getPriority()))
            .forEach(tc -> System.out.println("  " + tc));

        // ---- TODO 5 自己写 ----
        System.out.println("--- [TODO 5] 按 ID 降序排列（大的在前） ---");
        // 提示：Integer.compare(b.getId(), a.getId()) 就是降序
        cases.stream()
            .sorted(_________________________)
            .forEach(tc -> System.out.println("  " + tc));

        // =============================================
        // 练习 5：组合查询
        // =============================================
        System.out.println("\n========== 练习5：组合查询 ==========");

        // ---- TODO 6 自己写 ----
        System.out.println("--- [TODO 6] 找到所有 P1 且 PASS 的用例名称 ---");
        // 提示：两个 filter 再接 map
        cases.stream()
            .filter(tc -> "P1".equals(tc.getPriority()))
            .filter(___________________________)
            .map(___________________________)
            .forEach(System.out::println);

        // =============================================
        // 练习 6：统计
        // =============================================
        System.out.println("\n========== 练习6：统计 ==========");

        // ---- 示例 ----
        long total = cases.stream().count();
        long failCount = cases.stream()
            .filter(tc -> "FAIL".equals(tc.getStatus()))
            .count();
        System.out.println("总计: " + total + "  |  失败: " + failCount);

        // ---- TODO 7 自己写 ----
        System.out.println("--- [TODO 7] 统计 PENDING 的用例数 ---");
        long pendingCount = cases.stream()
            .___________________________
            .___________________________
        System.out.println("待执行: " + pendingCount);

        // ---- TODO 8 自己写 ----
        System.out.println("--- [TODO 8] 有没有 FAIL 的 P0 用例？ ---");
        // 提示：anyMatch 返回 boolean
        boolean hasCriticalFail = cases.stream()
            .filter(___________________________)
            .anyMatch(___________________________);
        System.out.println("有 P0 失败了？ " + hasCriticalFail);

        // =============================================
        // 全部通关 ✅
        // =============================================
        System.out.println("\n================================");
        System.out.println("练习完成！改完后 javac TestManager.java 编译运行看看");
        System.out.println("================================");
    }
}
