/**
 * Part 4 — 接口练习
 * Reportable 接口：所有可生成报告的类都应实现此接口
 */
public interface Reportable {

    /**
     * 生成测试报告文本
     */
    String toReport();

    /**
     * 默认方法：打印报告到控制台
     * Java 8+ 允许接口中有 default 方法（带方法体）
     */
    default void printReport() {
        System.out.println("===== 测试报告 =====");
        System.out.println(toReport());
        System.out.println("====================");
    }
}
