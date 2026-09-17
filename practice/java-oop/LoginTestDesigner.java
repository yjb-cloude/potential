yisi /**
 * Part 5 — 测试用例设计实战
 *
 * 学习目标：
 *   ① 等价类划分（Equivalence Partitioning）
 *   ② 边界值分析（Boundary Value Analysis）
 *
 * 被测功能：用户登录
 *   用户名: 6~20位，字母/数字/下划线
 *   密码:   8~16位，必须含字母 + 数字
 *   验证码: 4位纯数字
 *
 * 思路：
 *   先分析每个字段的等价类 + 边界值 → 设计 TestData → 跑模拟登录验证 → 出报告
 */
public class LoginTestDesigner {

    // =================================================================
    //  测试数据（等价类 + 边界值分析的结果）
    // =================================================================

    static class TestData {
        String username;
        String password;
        String captcha;
        String expected;   // 预期结果

        TestData(String username, String password, String captcha, String expected) {
            this.username = username;
            this.password = password;
            this.captcha  = captcha;
            this.expected = expected;
        }
    }

    public static void main(String[] args) {

        System.out.println("=" .repeat(65));
        System.out.println("  登录功能 — 测试用例设计（等价类划分 + 边界值分析）");
        System.out.println("=" .repeat(65));
        System.out.println("  用户名: 6~20位字母/数字/下划线");
        System.out.println("  密码:   8~16位含字母+数字");
        System.out.println("  验证码: 4位数字");
        System.out.println("=" .repeat(65));
        System.out.println();

        // ===== 等价类 + 边界值 测试数据 =====
        TestData[] data = {

            // ======= P0: Happy Path（有效等价类） =======
            new TestData("john_doe",  "Pass1234",       "1234",  "SUCCESS"),               // 所有字段合法

            // ======= P1: 用户名异常 =======
            // —— 等价类：不足6位 / 含非法字符 / 为空
            // —— 边界值：离点 5 位
            new TestData("ab",        "Pass1234",       "1234",  "用户名长度不足6位"),      // 等价类: <6
            new TestData("abcde",     "Pass1234",       "1234",  "用户名长度不足6位"),      // 边界: 离点(5)
            new TestData("user@123",  "Pass1234",       "1234",  "用户名包含非法字符"),     // 等价类: 特殊字符
            new TestData("",          "Pass1234",       "1234",  "用户名不能为空"),          // 等价类: 空串

            // —— 边界值：上点 6 位 + 内点 7 位（这俩应该成功）
            new TestData("abcde1",    "Pass1234",       "1234",  "SUCCESS"),                // 边界: 上点(6)
            new TestData("abcdef1",   "Pass1234",       "1234",  "SUCCESS"),                // 边界: 内点(7)

            // —— 边界值：上点 20 位 + 内点 19 位 + 离点 21 位
            // （造一个 20 位的用户名）
            new TestData("abcdefghijabcdefghij",  "Pass1234",  "1234",  "SUCCESS"),         // 边界: 上点(20)
            new TestData("abcdefghijabcdefghi",   "Pass1234",  "1234",  "SUCCESS"),         // 边界: 内点(19)
            new TestData("abcdefghijabcdefghijk","Pass1234",   "1234",  "用户名超过20位"),  // 边界: 离点(21)

            // ======= P2: 密码异常 =======
            new TestData("john_doe",  "abcdefgh",       "1234",  "密码必须含字母和数字"),  // 等价类: 只有字母
            new TestData("john_doe",  "12345678",       "1234",  "密码必须含字母和数字"),  // 等价类: 只有数字
            new TestData("john_doe",  "Pass12",         "1234",  "密码长度不足8位"),       // 边界: 离点(7)
            new TestData("john_doe",  "Pass1234567890123","1234",  "密码超过16位"),         // 边界: 离点(17位)

            // ======= P3: 验证码异常 =======
            // 验证码只有 4 位数字，上点=4，离点=3和5
            new TestData("john_doe",  "Pass1234",       "12",    "验证码必须是4位数字"),   // 边界: 离点(2)
            new TestData("john_doe",  "Pass1234",       "12345", "验证码必须是4位数字"),   // 边界: 离点(5)
            new TestData("john_doe",  "Pass1234",       "abcd",  "验证码必须是4位数字"),   // 等价类: 非数字
            new TestData("john_doe",  "Pass1234",       "12ab",  "验证码必须是4位数字"),   // 等价类: 数字+字母混合
        };

        // ===== 执行测试 =====
        int passCount = 0;

        for (int i = 0; i < data.length; i++) {
            TestData td  = data[i];
            String actual = simulateLogin(td);
            boolean isPass = actual.equals(td.expected);

            // 构造简洁的用例名称
            String desc = describeCase(i, td);
            String priority = getPriority(i);
            String status = isPass ? "PASS" : "FAIL";
            if (isPass) passCount++;

            // 打印:  编号 [优先级] 描述 —— 状态 | 预期: xxx | 实际: xxx
            System.out.printf("  %s | 预期: %s | 实际: %s%n",
                    "[" + priority + "] " + desc + " —— " + status,
                    td.expected, actual);
        }

        // ===== 汇总报告 =====
        System.out.println();
        System.out.println("=" .repeat(65));
        System.out.printf("  测试结果:  %d / %d 通过  (%d 失败)%n",
                passCount, data.length, data.length - passCount);
        if (passCount == data.length) {
            System.out.println("  ✅ 所有用例预期结果与实际一致");
        } else {
            System.out.println("  ❌ 存在失败的用例，请检查测试数据或模拟逻辑");
        }
        System.out.println("=" .repeat(65));
    }

    // =================================================================
    //  模拟登录校验
    //  （假装这是被测系统的后台逻辑）
    // =================================================================
    static String simulateLogin(TestData d) {

        // ---------- 用户名校验 ----------
        if (d.username == null || d.username.isEmpty()) {
            return "用户名不能为空";
        }
        if (d.username.length() < 6) {
            return "用户名长度不足6位";
        }
        if (d.username.length() > 20) {
            return "用户名超过20位";
        }
        if (!d.username.matches("[a-zA-Z0-9_]+")) {
            return "用户名包含非法字符";
        }

        // ---------- 密码校验 ----------
        if (d.password == null || d.password.length() < 8) {
            return "密码长度不足8位";
        }
        if (d.password.length() > 16) {
            return "密码超过16位";
        }
        if (!d.password.matches(".*[a-zA-Z].*") || !d.password.matches(".*[0-9].*")) {
            return "密码必须含字母和数字";
        }

        // ---------- 验证码校验 ----------
        if (d.captcha == null || !d.captcha.matches("\\d{4}")) {
            return "验证码必须是4位数字";
        }

        return "SUCCESS";
    }

    // =================================================================
    //  辅助方法
    // =================================================================

    /** 生成人类可读的用例描述 */
    static String describeCase(int index, TestData d) {
        String[] descs = {
            /*  0 */ "[Happy Path] 所有字段合法",
            /*  1 */ "[用户名] 等价类-不足6位(2位)",
            /*  2 */ "[用户名] 边界-离点(5位)",
            /*  3 */ "[用户名] 等价类-含特殊字符",
            /*  4 */ "[用户名] 等价类-空串",
            /*  5 */ "[用户名] 边界-上点(6位)",
            /*  6 */ "[用户名] 边界-内点(7位)",
            /*  7 */ "[用户名] 边界-上点(20位)",
            /*  8 */ "[用户名] 边界-内点(19位)",
            /*  9 */ "[用户名] 边界-离点(21位)",
            /* 10 */ "[密码] 等价类-只有字母",
            /* 11 */ "[密码] 等价类-只有数字",
            /* 12 */ "[密码] 边界-离点(7位)",
            /* 13 */ "[密码] 边界-离点(17位)",
            /* 14 */ "[验证码] 边界-离点(2位)",
            /* 15 */ "[验证码] 边界-离点(5位)",
            /* 16 */ "[验证码] 等价类-纯字母",
            /* 17 */ "[验证码] 等价类-字母数字混合",
        };
        return (index < descs.length) ? descs[index] : ("未知用例 #" + index);
    }

    /** 优先级分配 */
    static String getPriority(int index) {
        if (index == 0)              return "P0";   // Happy Path
        if (index >= 1 && index <= 9) return "P1";   // 用户名
        if (index >= 10 && index <= 13) return "P2"; // 密码
        return "P3";                                   // 验证码
    }
}
