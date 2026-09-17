/**
 * Stream API 练习
 * 场景：Bug 管理系统 —— 对 Bug 列表做各种查询统计
 *
 * 编译：javac -encoding utf-8 StreamPractice.java
 * 运行：java StreamPractice
 *
 * 把 TODO 标记的 ________ 替换成你的代码，然后编译运行看结果
 */
import java.util.*;
import java.util.stream.Collectors;

public class StreamPractice {

    // ===== Bug 类 =====
    static class Bug {
        int id;
        String title;
        String severity;   // "CRITICAL" / "MAJOR" / "MINOR" / "TRIVIAL"
        String status;     // "OPEN" / "FIXED" / "CLOSED" / "REOPENED"
        String module;

        Bug(int id, String title, String severity, String status, String module) {
            this.id = id;
            this.title = title;
            this.severity = severity;
            this.status = status;
            this.module = module;
        }

        @Override
        public String toString() {
            return "[#" + id + "][" + severity + "] " + title + " (" + status + ")";
        }
    }

    // ===== 准备测试数据 =====
    private static List<Bug> createBugs() {
        List<Bug> list = Arrays.asList(
            new Bug(101, "登录页 500 错误",           "CRITICAL", "OPEN",     "用户模块"),
            new Bug(102, "注册邮箱未做格式校验",       "MAJOR",    "OPEN",     "用户模块"),
            new Bug(103, "个人中心头像上传超时",       "MINOR",    "FIXED",    "用户模块"),
            new Bug(104, "订单列表翻页后数据重复",     "CRITICAL", "REOPENED", "订单模块"),
            new Bug(105, "搜索框输入特殊字符崩溃",     "MAJOR",    "OPEN",     "搜索模块"),
            new Bug(106, "首页 banner 图错位",        "TRIVIAL",  "CLOSED",   "首页模块"),
            new Bug(107, "支付回调未处理重复通知",     "CRITICAL", "OPEN",     "订单模块"),
            new Bug(108, "用户列表导出为空",           "MAJOR",    "FIXED",    "用户模块"),
            new Bug(109, "搜索历史记录未去重",         "MINOR",    "CLOSED",   "搜索模块"),
            new Bug(110, "优惠券过期未自动失效",       "MAJOR",    "REOPENED", "订单模块")
        );
        return list;
    }

    public static void main(String[] args) {
        List<Bug> bugs = createBugs();

        System.out.println("========== 全部 Bug ==========");
        bugs.forEach(b -> System.out.println("  " + b));

        // =============================================
        // 练习 1：filter —— 筛选
        // =============================================
        System.out.println("\n========== 练习1：filter 筛选 ==========");

        // ---- 示例 ----
        System.out.println("--- [示例] 筛选 CRITICAL 级别的 Bug ---");
        bugs.stream()
            .filter(b -> "CRITICAL".equals(b.severity))
            .forEach(b -> System.out.println("  " + b));

        // ---- TODO 1 ----
        System.out.println("--- [TODO 1] 筛选出所有 OPEN 状态的 Bug ---");
        bugs.stream()
            .filter(b -> "OPEN".equals(b.status))
            .forEach(b -> System.out.println("  " + b));

        // ---- TODO 2 ----
        System.out.println("--- [TODO 2] 筛选出 订单模块 的 Bug ---");
        bugs.stream()
            .filter(b -> "订单模块".equals(b.module))
            .forEach(b -> System.out.println("  " + b));

        // =============================================
        // 练习 2：map —— 转换
        // =============================================
        System.out.println("\n========== 练习2：map 转换 ==========");

        // ---- 示例 ----
        System.out.println("--- [示例] 提取所有 Bug 的标题 ---");
        bugs.stream()
            .map(b -> b.title)
            .forEach(t -> System.out.println("  " + t));

        // ---- TODO 3 ----
        System.out.println("--- [TODO 3] 转换成短格式：\"[CRITICAL] 登录页 500 错误\" ---");
        bugs.stream()
            .map(b -> "[" + b.severity + "] " + b.title)
            .forEach(line -> System.out.println("  " + line));

        // ---- TODO 4 ----
        System.out.println("--- [TODO 4] 提取所有模块名（去重） ---");
        // 提示：用 map 提取 module，再用 distinct() 去重
        bugs.stream()
            .map(b -> b.module)
            .distinct()
            .forEach(m -> System.out.println("  " + m));

        // =============================================
        // 练习 3：collect —— 收集
        // =============================================
        System.out.println("\n========== 练习3：collect 收集 ==========");

        // ---- 示例 ----
        System.out.println("--- [示例] 收集 CRITICAL 的 Bug 到 List ---");
        List<Bug> criticalBugs = bugs.stream()
            .filter(b -> "CRITICAL".equals(b.severity))
            .collect(Collectors.toList());
        System.out.println("CRITICAL Bug 数量: " + criticalBugs.size());

        // ---- TODO 5 ----
        System.out.println("--- [TODO 5] 收集所有 MAJOR 级别的 Bug 标题到 List ---");
        // 提示：filter + map + collect
        List<String> majorTitles = bugs.stream()
            .filter(b -> "MAJOR".equals(b.severity))
            .map(b -> b.title)
            .collect(Collectors.toList());
        System.out.println("MAJOR Bug 标题: " + majorTitles);

        // =============================================
        // 练习 4：sorted —— 排序
        // =============================================
        System.out.println("\n========== 练习4：sorted 排序 ==========");

        // ---- 示例 ----
        System.out.println("--- [示例] 按严重级别排序 ---");
        bugs.stream()
            .sorted((a, b) -> a.severity.compareTo(b.severity))
            .forEach(b -> System.out.println("  " + b));

        // ---- TODO 6 ----
        System.out.println("--- [TODO 6] 按 ID 降序排列 ---");
        bugs.stream()
            .sorted((a, b) -> b.id - a.id)
            .forEach(b -> System.out.println("  " + b));

        // =============================================
        // 练习 5：组合查询
        // =============================================
        System.out.println("\n========== 练习5：组合查询 ==========");

        // ---- TODO 7 ----
        System.out.println("--- [TODO 7] 找到 OPEN 状态的 CRITICAL Bug ---");
        // 提示：两个 filter 叠加
        bugs.stream()
            .filter(b -> "OPEN".equals(b.status))
            .filter(b -> "CRITICAL".equals(b.severity))
            .forEach(b -> System.out.println("  " + b));

        // ---- TODO 8 ----
        System.out.println("--- [TODO 8] 对 用户模块 按 ID 升序输出标题 ---");
        // 提示：filter + sorted + map
        bugs.stream()
            .filter(b -> "用户模块".equals(b.module))
            .sorted((a,b) -> a.id - b.id)
            .map(b -> b.title)
            .forEach(System.out::println);

        // =============================================
        // 练习 6：统计与匹配
        // =============================================
        System.out.println("\n========== 练习6：统计与匹配 ==========");

        // ---- 示例 ----
        long total = bugs.stream().count();
        long openCount = bugs.stream()
            .filter(b -> "OPEN".equals(b.status))
            .count();
        System.out.println("总计: " + total + "  |  OPEN: " + openCount);

        // ---- TODO 9 ----
        System.out.println("--- [TODO 9] 统计 REOPENED 的 Bug 数量 ---");
        long reopenedCount = bugs.stream()
            .filter(b -> "REOPENED".equals(b.status))
            .count();
        System.out.println("REOPENED: " + reopenedCount);

        // ---- TODO 10 ----
        System.out.println("--- [TODO 10] 有没有 CRITICAL 级别的 OPEN Bug？ ---");
        boolean hasCriticalOpen = bugs.stream()
            .filter(b -> "CRITICAL".equals(b.severity))
            .anyMatch(b -> "OPEN".equals(b.status));
        System.out.println("存在未处理的严重 Bug？ " + hasCriticalOpen);

        // ---- TODO 11（选做） ----
        System.out.println("--- [TODO 11] 所有 Bug 是否都包含标题？ ---");
        // 提示：allMatch(b -> b.title != null && !b.title.isEmpty())
        boolean allHaveTitle = bugs.stream()
            .allMatch(b -> b.title != null && !b.title.isEmpty());
        System.out.println("所有 Bug 都有标题？ " + allHaveTitle);

        // =============================================
        // 全部通关 ✅
        // =============================================
        System.out.println("\n================================");
        System.out.println("全部填完就编译运行：");
        System.out.println("  javac -encoding utf-8 StreamPractice.java");
        System.out.println("  java StreamPractice");
        System.out.println("================================");
    }
}
