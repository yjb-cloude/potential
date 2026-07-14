# JVM 基础

Java 虚拟机（JVM）是 Java 跨平台的基石，理解 JVM 的内存结构、垃圾回收和类加载机制，是 Java 开发者进阶的必经之路。

## JVM 内存结构（运行时数据区）

JVM 在运行时将内存划分为不同的区域：

```
线程私有:
  ├── PC 寄存器（Program Counter Register）：当前线程执行的字节码行号
  ├── Java 虚拟机栈（JVM Stack）：存储栈帧（局部变量表、操作数栈、动态链接、方法出口）
  └── 本地方法栈（Native Method Stack）：执行 native 方法

线程共享:
  ├── 堆（Heap）：对象实例和数组
  └── 方法区（Method Area / Metaspace）：类信息、常量池、静态变量
```

### 虚拟机栈

每个方法调用创建一个栈帧，方法执行完毕后出栈。栈帧包含：
- **局部变量表：** 存储方法参数和局部变量（基本类型和对象引用）
- **操作数栈：** 字节码指令的操作数存放区域
- **动态链接：** 指向运行时常量池中的符号引用

栈深度过大时抛出 `StackOverflowError`；栈动态扩展失败时抛出 `OutOfMemoryError`。

## 堆内存分代

传统分代 GC 将堆划分为不同区域，基于弱分代假说（大部分对象朝生夕死）：

### 新生代（Young Generation）

- **Eden 区：** 新对象分配（大对象直接进入老年代）
- **Survivor 0 / Survivor 1（From / To）：** 存放从 Eden 区存活下来的对象

默认比例 **Eden : S0 : S1 = 8 : 1 : 1**，可用新生代空间为 Eden + 一个 Survivor（90%）。

### 老年代（Old Generation）

存放经过多次 Minor GC 仍存活的对象（默认 15 次，通过 `-XX:MaxTenuringThreshold` 设置）以及大对象（`-XX:PretenureSizeThreshold`）。

### 元空间（Metaspace）

JDK8 开始替代永久代（PermGen），存放类元数据、常量池和静态变量。元空间使用本地内存（Native Memory），不在堆中，默认无上限（需注意物理内存限制）。

## GC 算法

| 算法 | 原理 | 优缺点 |
|------|------|--------|
| **标记-清除** | 标记存活对象→清除未被标记的 | 产生大量内存碎片 |
| **标记-复制** | Eden→Survivor 复制存活对象 | 无碎片，但浪费 1 个 Survivor 空间 |
| **标记-整理** | 标记存活对象→向一端移动 | 无碎片，但需要移动对象 |

## 垃圾收集器（面试重点）

### G1 Garbage Collector

JDK9+ 的默认垃圾收集器：
- **分区（Region）：** 将堆划分为多个大小相等的 Region（1MB-32MB），新生代和老年代不再是连续区域
- **并发标记：** 标记与用户线程并发执行
- **可预测停顿：** `-XX:MaxGCPauseMillis` 设置目标停顿时间
- **混合收集：** 回收新生代的同时回收部分高收益的老年代 Region

启用参数：`-XX:+UseG1GC`

### ZGC

JDK11 引入的低延迟收集器：
- **并发执行：** 几乎所有阶段与业务线程并发
- **着色指针（Colored Pointers）：** 通过指针高位存储元数据
- **停顿时间：** 通常 <1ms，与堆大小无关
- **适用场景：** 超大堆（TB 级）、对延迟极为敏感的应用

## 类加载机制

### 三个阶段

1. **加载（Loading）：** 通过全限定名获取二进制字节流，在方法区生成 Class 对象
2. **链接（Linking）：** 验证（Verify）→ 准备（Prepare，分配静态变量默认值）→ 解析（Resolve，符号引用→直接引用）
3. **初始化（Initialization）：** 执行 `<clinit>()` 方法，为静态变量赋初始值

### 双亲委派模型

**工作流程：** 类加载器收到类加载请求时，先将请求委派给父类加载器处理，只有父类加载器无法加载时，才由子类加载器自行加载。

```
Bootstrap ClassLoader（C++ 实现，加载 rt.jar）
  ↑ 委派
Extension ClassLoader（加载 jre/lib/ext）
  ↑ 委派
Application ClassLoader（加载 classpath）
```

**好处：** 保证核心类库的安全性，防止用户自定义的 `java.lang.Object` 覆盖标准实现。

## JVM 调优常用参数

| 参数 | 作用 |
|------|------|
| `-Xms` | 初始堆大小 |
| `-Xmx` | 最大堆大小（通常与 -Xms 相同避免动态调整） |
| `-Xss` | 虚拟机栈大小（默认 1MB，可调小增加线程数） |
| `-XX:+PrintGCDetails` | 打印详细 GC 日志 |
| `-XX:+HeapDumpOnOutOfMemoryError` | OOM 时生成堆转储快照 |
| `-XX:MetaspaceSize` | 元空间初始大小 |
| `-XX:+UseG1GC` | 启用 G1 垃圾收集器 |

---

**关联知识点：** [[concurrency-java]] | [[spring-boot-core]] | [[Java开发知识体系]]
