# Java 开发知识体系

> Java 全栈知识图谱，覆盖核心语言特性、进阶并发与 JVM、Spring Boot 框架、数据库、工具链，以及与测试和 AI 领域的交叉连接。
>
> 关联知识体系：[[软件测试知识体系]] | [[AI应用开发知识体系]] | [[collections-framework]] | [[concurrency-java]] | [[jvm-basics]] | [[spring-boot-core]]

---

## 一、Java 核心基础

### 1.1 OOP 三大特性

| 特性 | 核心要点 | 面试高频 |
|------|---------|---------|
| **封装 (Encapsulation)** | 通过 `private` + `getter/setter` 隐藏内部实现，暴露安全接口 | 封装的好处、权限修饰符对比 |
| **继承 (Inheritance)** | `extends` 单继承、`super` 关键字、构造器调用链 | 继承与组合优先选用组合、菱形问题 |
| **多态 (Polymorphism)** | 编译时多态（方法重载） + 运行时多态（方法重写） | 多态的底层原理 |

**多态的底层原理 -- 虚方法表 (vtable)**：
- JVM 在类加载阶段为每个类创建虚方法表，表中存放实际方法的入口地址
- 子类重写父类方法时，虚方法表中对应槽位的指针指向子类实现
- 调用虚方法时，通过对象的 `klass` 指针找到虚方法表，再根据方法索引定位到实际方法——这就是**动态分派 (Dynamic Dispatch)**
- `static` 方法（静态分派）和 `private` 方法（不可重写）不走虚方法表

**面试重点**：
- 重写 (Override) vs 重载 (Overload) 的区别
- 静态多态 vs 动态多态
- 虚方法表在 JVM 中的存储位置（方法区）
- 变量 `Hiding`：子类定义与父类同名字段时，不构成多态

---

### 1.2 抽象类 vs 接口

| 对比维度 | 抽象类 (`abstract class`) | 接口 (`interface`) |
|---------|-------------------------|-------------------|
| 继承方式 | 单继承 | 多实现 |
| 构造器 | 可以有 | 不能有 |
| 成员变量 | 任意类型 | `public static final`（常量） |
| 方法实现 | 可以有抽象方法和普通方法 | JDK7：仅抽象方法；JDK8+：`default` + `static` 方法；JDK9：`private` 方法 |
| 语义 | "是什么"（is-a） | "能做什么"（can-do） |

**JDK8+ 接口关键变化**：
- `default` 方法：解决接口演进兼容性问题（如 `List.sort()`），子类可选择重写
- `static` 方法：接口内的工具方法（如 `Comparator.comparing()`）
- 冲突解决：类优先原则；同时继承两个有相同 `default` 方法的接口必须手动重写

**面试重点**：
- `abstract class` vs `interface` 的设计差异（什么时候用哪个）
- JDK8 接口默认方法的引入动机
- 接口中的 `default` 方法与抽象类中普通方法的本质区别（状态 vs 行为）

---

### 1.3 内部类 (Inner Class)

| 类型 | 定义位置 | 持有外部类引用 | 特点 |
|------|---------|--------------|------|
| **成员内部类** | 类内部 | 是 | 可访问外部类的所有成员（包括 private） |
| **静态内部类** | 类内部，`static` | 否 | 不依赖外部类实例，相当于独立类 |
| **局部内部类** | 方法内部 | 是 | 作用域限于方法内 |
| **匿名内部类** | 方法内，`new 接口/类(){}` | 是 | 实现回调、事件监听，Lambda 出现后较少使用 |

**面试重点**：
- 为什么局部内部类和匿名内部类访问局部变量时要求变量是 `final`（或 effectively final）？（变量捕获 / Variable Capture）
- 静态内部类与成员内部类的使用场景差异
- 内部类编译后的 `.class` 文件名（`Outer$Inner.class`）

---

### 1.4 Collections 框架

详细笔记：[[collections-framework]]

**核心容器概览**：

```
Collection
├── List（有序可重复）
│   ├── ArrayList  ← 数组实现，查询快增删慢
│   └── LinkedList ← 双向链表，增删快查询慢
├── Set（不可重复）
│   ├── HashSet    ← HashMap 底层
│   ├── LinkedHashSet ← 可维护插入顺序
│   └── TreeSet    ← 红黑树，可排序
└── Queue（队列）
    └── PriorityQueue

Map
├── HashMap    ← 数组+链表+红黑树
├── LinkedHashMap ← 可维护迭代顺序
├── TreeMap    ← 红黑树，Key 排序
└── ConcurrentHashMap ← 分段锁/CAS
```

**HashMap 核心原理**：
- **put 流程**：计算 key 的 `hashCode()` → 二次扰动（`h ^ (h >>> 16)`）→ 取模定位桶 → 桶空直接插入 → 桶不空则遍历链表/红黑树找 key，找到覆盖、未找到插入
- **扩容机制**：默认容量 16，负载因子 0.75，扩容为原容量的 2 倍并 rehash
- **红黑树化**：链表长度 >= 8 且数组长度 >= 64 时转为红黑树（`TREEIFY_THRESHOLD`）；长度降回 <= 6 时退化为链表
- **ConcurrentHashMap**：Java 7 采用 Segment 分段锁；Java 8 改用 `synchronized` + CAS，锁粒度更细（仅锁桶头节点）

**面试重点**：
- `ArrayList` 扩容机制（`grow()` 方法，1.5 倍）
- `HashMap` 为什么线程不安全（死循环、数据覆盖）
- `ConcurrentHashMap` 的 `size()` 如何计算（CounterCells）
- `TreeMap` / `TreeSet` 的排序逻辑：`Comparable` vs `Comparator`
- `Collections.synchronizedXxx()` 与 `ConcurrentHashMap` 的性能差异

---

### 1.5 泛型 (Generics)

**核心概念**：
- 泛型类、泛型接口、泛型方法
- 泛型通配符：
  - `? extends T` —— 上界通配符（生产者，只读不写）
  - `? super T` —— 下界通配符（消费者，可写）
  - `?` —— 无界通配符

**类型擦除 (Type Erasure)**：
- Java 泛型是编译期特性，编译后泛型信息被擦除为原始类型（`Raw Type`）
- 擦除规则：无限定擦除为 `Object`，有上界擦除为第一个边界
- 桥方法（Bridge Method）：编译器自动生成以维持多态

**面试重点**：
- `List<? extends Number>` 为什么不能 `add()`？（编译器无法确定具体类型）
- PECS 原则（Producer Extends, Consumer Super）
- 类型擦除带来的限制：不能 `new T()`、不能 `new T[]`、不能 `instanceof T`
- `List<String>` 能通过 `getClass()` 区分 `List<Integer>` 吗？（不能，运行时都是 `ArrayList`）

---

### 1.6 异常体系

```
Throwable
├── Error（不可恢复，程序不应捕获）
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── NoClassDefFoundError
└── Exception
    ├── RuntimeException（非受检异常，可避免）
    │   ├── NullPointerException
    │   ├── IllegalArgumentException
    │   ├── IndexOutOfBoundsException
    │   └── ConcurrentModificationException
    └── Checked Exception（受检异常，必须处理）
        ├── IOException
        ├── SQLException
        └── ClassNotFoundException
```

**try-with-resources (JDK7+)**：
- 自动关闭实现了 `AutoCloseable` 的资源
- 比传统 `try-finally` 更简洁，且能正确处理 `close()` 抛出的异常（被抑制的异常可通过 `getSuppressed()` 获取）

**最佳实践**：
- 异常只用于异常情况，不用作流程控制
- 调用方更关心 "发生了什么错误" 时用 Checked Exception
- 调用方更关心 "哪个分支出错" 时（如参数校验）用 RuntimeException
- 日志记录异常时保留完整堆栈（`log.error("msg", e)`，不要只 `e.getMessage()`）

**面试重点**：
- `Error` vs `Exception` vs `RuntimeException`
- `try-with-resources` 的字节码原理
- `throws` vs `throw` vs `try-catch-finally` 执行顺序

---

### 1.7 Optional

**最佳实践**：
- ✅ `Optional.ofNullable(obj).orElse(defaultValue)` / `.orElseGet(() -> computeValue())`
- ✅ `Optional.ofNullable(obj).orElseThrow(() -> new CustomException("..."))`
- ✅ 链式操作：`flatMap()` 处理嵌套 Optional，`filter()` 按条件过滤
- ❌ 不要用 `Optional.get()` —— 不如直接判空
- ❌ 不要用 `Optional` 做字段类型（不可序列化）
- ❌ 不要用 `Optional` 做方法参数（增加调用方负担）
- ❌ 不要用 `Optional` 包装集合（`Optional<List<T>>` 应替换为 `Collections.emptyList()`）

**面试重点**：
- `Optional.of()` vs `Optional.ofNullable()` 的区别
- `orElse()` vs `orElseGet()` 的区别（前者无论是否为空都会执行参数表达式）
- JDK9+ 新增方法：`Optional.ifPresentOrElse()`、`Optional.or()`、`Optional.stream()`

---

### 1.8 Lambda + Stream API

**函数式接口 (Functional Interface)**：
- 只有一个抽象方法的接口（可包含 `default` / `static` 方法）
- 常用函数式接口：

| 接口 | 方法签名 | 用途 |
|------|---------|------|
| `Predicate<T>` | `boolean test(T)` | 条件判断 |
| `Function<T,R>` | `R apply(T)` | 类型转换 |
| `Consumer<T>` | `void accept(T)` | 消费处理 |
| `Supplier<T>` | `T get()` | 延迟生产 |
| `UnaryOperator<T>` | `T apply(T)` | 同类型转换 |
| `BinaryOperator<T>` | `T apply(T,T)` | 二元合并 |

**方法引用 (Method Reference)**：

| 语法 | 等价于 Lambda | 示例 |
|------|--------------|------|
| `类::静态方法` | `(args) -> 类.静态方法(args)` | `Math::max` |
| `对象::实例方法` | `(args) -> 对象.实例方法(args)` | `System.out::println` |
| `类::实例方法` | `(obj, args) -> obj.实例方法(args)` | `String::length` |
| `类::new` | `(args) -> new 类(args)` | `ArrayList::new` |

**Stream 操作分类**：

```
Stream
├── 中间操作 (Intermediate) — 惰性求值
│   ├── 筛选：filter / distinct / limit / skip
│   ├── 映射：map / flatMap / mapToInt
│   ├── 排序：sorted
│   └── 调试：peek
└── 终止操作 (Terminal) — 触发执行
    ├── 匹配：allMatch / anyMatch / noneMatch
    ├── 查找：findFirst / findAny
    ├── 归约：reduce / count / min / max
    ├── 收集：collect(Collectors.toList() / toSet() / toMap() / groupingBy() / partitioningBy())
    └── 遍历：forEach
```

**面试重点**：
- Lambda 表达式的编译原理（invokedynamic + LambdaMetafactory）
- `parallelStream()` 与线程池的关系（共享 `ForkJoinPool.commonPool()`）
- `stream()` vs `parallelStream()` 适用场景（CPU 密集型 vs IO 密集型）
- `Collectors.toMap()` 遇到重复 key 的处理（需传入 mergeFunction）

---

### 1.9 IO流与文件操作

**核心概念**：
- **流的方向**：输入流（读）vs 输出流（写）
- **流的单位**：字节流（8-bit）vs 字符流（16-bit）
- **流的角色**：节点流（直接连接数据源）vs 处理流（包装节点流，提供更丰富的操作）

**IO 体系结构**：

```
字节流                         字符流
├── InputStream                ├── Reader
│   ├── FileInputStream        │   ├── FileReader
│   ├── BufferedInputStream    │   ├── BufferedReader
│   ├── DataInputStream        │   ├── InputStreamReader
│   └── ObjectInputStream      │   └── ... 
├── OutputStream               ├── Writer
│   ├── FileOutputStream       │   ├── FileWriter
│   ├── BufferedOutputStream   │   ├── BufferedWriter
│   ├── DataOutputStream       │   ├── OutputStreamWriter
│   └── ObjectOutputStream     │   └── PrintWriter
```

**关键知识点**：

| 知识点 | 说明 | 面试要点 |
|--------|------|---------|
| **字节流 vs 字符流** | 字节流处理所有二进制文件；字符流处理文本（自动处理编码） | 什么时候用哪个 |
| **缓冲流 (Buffered)** | 包装节点流，提供缓冲区减少 IO 次数，显著提升性能 | 为什么 Buffered 更快？ |
| **转换流** | `InputStreamReader` / `OutputStreamWriter` 连接字节流和字符流 | 编码转换场景 |
| **对象序列化** | `ObjectOutputStream` / `ObjectInputStream`，实现 `Serializable` | transient 关键字、serialVersionUID |
| **try-with-resources** | JDK7+ 自动关闭资源，实现 `AutoCloseable` | 底层原理（编译成 try-finally） |
| **File 类** | 文件和目录路径名的抽象表示 | 不支持文件内容读写，只操作元数据 |

**NIO (New IO, JDK1.4+)**：

```
传统 IO（流式）          NIO（缓冲式）
┌──────────────┐       ┌──────────────────┐
│   单向字节流    │       │   Channel + Buffer  │
│   阻塞式 IO    │       │   非阻塞/多路复用    │
│   无选择器     │       │   Selector（事件驱动）│
└──────────────┘       └──────────────────┘
```

**NIO 三大核心**：
- **Channel（通道）**：双向数据传输，`FileChannel` / `SocketChannel` / `ServerSocketChannel`
- **Buffer（缓冲区）**：数据存储容器，`ByteBuffer` / `CharBuffer` / `IntBuffer`
- **Selector（选择器）**：单线程管理多个 Channel 的事件（连接、读、写）

**NIO vs BIO 对比**：

| 特性 | BIO (传统 IO) | NIO |
|------|-------------|-----|
| 模型 | 同步阻塞 | 同步非阻塞（可多路复用） |
| 线程模型 | 一个连接一个线程 | 一个线程处理多个连接（Selector） |
| 数据流 | 单向字节流 | 双向 Channel |
| 适用场景 | 连接数少、低延迟 | 连接数多、高并发 |

**JDK7+ NIO.2 (Files / Paths)**：
- `Files.readAllBytes()` / `Files.write()` — 简化读写
- `Files.walk()` / `Files.find()` — 遍历文件树
- `Path` / `Paths` / `Files` 工具类取代了 `File`
- `WatchService` — 文件系统事件监听

**面试重点**：
- 字节流与字符流的本质区别（编码/解码）
- `BufferedInputStream` 为什么比 `FileInputStream` 快？（内存缓冲区减少系统调用）
- `transient` 关键字在序列化中的作用
- `try-with-resources` 的异常抑制机制（`getSuppressed()`）
- NIO 的零拷贝（`FileChannel.transferTo()`）在数据传输中的优势
- Java 序列化 vs JSON 序列化的区别

---

## 二、Java 进阶

### 2.1 并发编程

详细笔记：[[concurrency-java]]

**线程状态转换**：

```
NEW → RUNNABLE ←→ BLOCKED
                   ←→ WAITING
                   ←→ TIMED_WAITING
                         → TERMINATED
```

**synchronized 原理**：
- JDK6 引入**偏向锁 → 轻量级锁 → 重量级锁**的锁升级过程
- 偏向锁：无竞争时，Mark Word 记录线程 ID，避免 CAS
- 轻量级锁：CAS 自旋获取锁，避免线程切换
- 重量级锁：依赖操作系统互斥量（mutex），线程阻塞
- 锁升级不可逆（批量重偏向除外）

**volatile 原理**：
- **可见性**：对 volatile 变量的写会立即刷新到主存，读从主存加载
- **有序性**：禁止指令重排序（通过内存屏障，Load-Load / Load-Store / Store-Load / Store-Store）
- 注意：volatile **不保证原子性**（如 `count++` 仍需要 synchronized 或 AtomicInteger）

**Lock vs synchronized**：

| 对比 | synchronized | Lock (ReentrantLock) |
|------|-------------|---------------------|
| 自动释放 | 是（块结束自动释放） | 否（需手动 unlock） |
| 锁超时 | 不支持 | 支持 tryLock(timeout) |
| 可中断 | 不响应中断 | lockInterruptibly() |
| 公平性 | 非公平 | 可设置公平/非公平 |
| 条件等待 | wait/notify | Condition.await/signal |
| 读/写分离 | 不支持 | ReentrantReadWriteLock |

**ThreadPoolExecutor 核心参数**：

```java
new ThreadPoolExecutor(
    corePoolSize,      // 核心线程数
    maximumPoolSize,   // 最大线程数
    keepAliveTime,     // 空闲线程存活时间
    unit,              // 时间单位
    workQueue,         // 任务队列（BlockingQueue）
    threadFactory,     // 线程工厂
    handler            // 拒绝策略
);
```

- **工作流程**：核心线程 → 任务队列 → 最大线程 → 拒绝策略
- **拒绝策略**：
  - `AbortPolicy`（默认，抛异常）
  - `CallerRunsPolicy`（调用线程执行）
  - `DiscardPolicy`（静默丢弃）
  - `DiscardOldestPolicy`（丢弃队列最旧任务）

**CompletableFuture**：
- `supplyAsync()` / `runAsync()` 异步执行
- `thenApply()` / `thenAccept()` / `thenRun()` 串行编排
- `thenCombine()` / `thenCompose()` 合并结果
- `allOf()` / `anyOf()` 多任务组合
- `exceptionally()` / `handle()` 异常处理

**面试重点**：
- `wait()` vs `sleep()` 的区别
- `ThreadLocal` 原理（每个线程维护一个 ThreadLocalMap）及内存泄漏风险
- `synchronized` 锁升级过程及 Mark Word 变化
- `volatile` 内存屏障 vs `synchronized` 互斥 —— 各自解决什么问题
- 线程池大小估算（CPU 密集型：N+1；IO 密集型：2N）
- `ForkJoinPool` 工作窃取（Work-Stealing）原理

---

### 2.2 JVM 基础

详细笔记：[[jvm-basics]]

**运行时数据区**：

```
┌─────────────────────────────────┐
│          线程私有                  │
│  ┌──────────┐  ┌──────────┐     │
│  │  程序计数器  │  │  本地方法栈│     │
│  └──────────┘  └──────────┘     │
│  ┌──────────────────────┐       │
│  │      虚拟机栈         │       │
│  │  (栈帧: 局部变量表     │       │
│  │   操作数栈/动态链接    │       │
│  │   方法出口)           │       │
│  └──────────────────────┘       │
├─────────────────────────────────┤
│          线程共享                  │
│  ┌──────────────────────┐       │
│  │       堆 (Heap)       │       │
│  │  新生代(Eden/S0/S1)   │       │
│  │  老年代 (Old Gen)     │       │
│  └──────────────────────┘       │
│  ┌──────────────────────┐       │
│  │   方法区 (Metaspace)   │       │
│  │   类信息/常量池/JIT    │       │
│  └──────────────────────┘       │
└─────────────────────────────────┘
```

**GC 算法**：

| 算法 | 原理 | 优缺点 |
|------|------|--------|
| 标记-清除 (Mark-Sweep) | 标记存活对象，清除未标记对象 | 产生内存碎片 |
| 复制 (Copying) | 将存活对象复制到另一半空间 | 无碎片，但浪费一半空间 |
| 标记-整理 (Mark-Compact) | 标记后将存活对象向一端移动 | 无碎片，但移动开销大 |

**垃圾收集器**：

| 收集器 | 作用区域 | 算法 | 特点 |
|--------|---------|------|------|
| Serial | 新生代 | 复制 | 单线程，Stop-The-World |
| ParNew | 新生代 | 复制 | Serial 多线程版 |
| Parallel Scavenge | 新生代 | 复制 | 关注吞吐量 |
| Serial Old | 老年代 | 标记-整理 | Serial 老年代版 |
| Parallel Old | 老年代 | 标记-整理 | Parallel 老年代版 |
| CMS | 老年代 | 标记-清除 | 低延迟，会产生碎片 |
| **G1** | 整堆 | Region 化 | 可预测停顿，JDK9+ 默认 |
| **ZGC** | 整堆 | 染色指针 | 亚毫秒级停顿，JDK15+ 正式 |

**类加载机制**：
- 加载 → 验证 → 准备 → 解析 → 初始化（→ 使用 → 卸载）
- **双亲委派模型**：`Bootstrap ClassLoader` → `Extension ClassLoader` → `Application ClassLoader`
- 打破双亲委派：`Thread.setContextClassLoader()`（如 Tomcat、JDBC SPI）

**JVM 调优常用参数**：

```
-Xms4g -Xmx4g                      # 堆大小
-Xss512k                           # 栈大小
-XX:MetaspaceSize=256m             # 元空间
-XX:+UseG1GC                       # 使用 G1 收集器
-XX:MaxGCPauseMillis=200           # 最大 GC 停顿
-XX:+HeapDumpOnOutOfMemoryError    # OOM 时 dump 堆
-XX:HeapDumpPath=/path/to/dump     # dump 路径
-verbose:gc -Xlog:gc*              # GC 日志
```

**面试重点**：
- 强引用 vs 软引用 vs 弱引用 vs 虚引用（Reference 类型）
- Minor GC / Major GC / Full GC 的触发条件
- CMS 的并发阶段与"Concurrent Mode Failure"
- G1 的 Young / Mixed GC 及 SATB（Snapshot-At-The-Beginning）
- 双亲委派模型的作用（避免类重复加载 + 保证核心类安全）
- `class.forName()` vs `classLoader.loadClass()` 的区别

---

### 2.3 反射 (Reflection)

**核心 API**：
- `Class.forName("全限定类名")` / `obj.getClass()` / `类名.class`
- `Constructor<?>[]` → `constructor.newInstance(args)`
- `Method` → `method.invoke(obj, args)`
- `Field` → `field.set(obj, value)` / `field.get(obj)`

**反射优化**：
- `setAccessible(true)` 取消 Java 语言访问检查，显著提升性能
- `MethodHandle`（JDK7）比反射更轻量
- `VarHandle`（JDK9）提供更细粒度的内存操作

**面试重点**：
- 反射的性能开销原因（类型检查、安全校验、装箱拆箱）
- 反射与 Spring IoC 的关系
- `getFields()` vs `getDeclaredFields()` 的区别

---

### 2.4 注解 (Annotation)

**元注解**：

| 元注解 | 作用 |
|--------|------|
| `@Retention` | 注解保留策略：`SOURCE` / `CLASS` / `RUNTIME` |
| `@Target` | 注解应用目标：`TYPE` / `FIELD` / `METHOD` / `PARAMETER` 等 |
| `@Inherited` | 子类是否继承父类的注解 |
| `@Documented` | 是否包含在 Javadoc 中 |
| `@Repeatable` | 是否可在同一位置重复使用（JDK8+） |

**运行时注解 vs 编译期注解**：
- **运行时注解**（`@Retention(RUNTIME)`）：通过反射读取，如 `@Test`、`@Spring` 相关注解
- **编译期注解**（`@Retention(SOURCE)` / `CLASS`）：通过 Annotation Processor 处理，如 `@Lombok`（在编译时生成代码）

**面试重点**：
- 自定义注解的步骤（`@interface` + 元注解 + 处理器）
- 编译期注解处理（`AbstractProcessor`）的典型应用（Lombok、MapStruct）
- `@Inherited` 在类上有效，在方法/字段上无效

---

### 2.5 序列化 (Serialization)

**核心机制**：
- `Serializable` 标记接口（无方法）
- `transient` 关键字：标记字段不参与序列化
- `serialVersionUID`：版本号控制，反序列化时校验一致性
- JDK 序列化的替代方案：JSON (Jackson/Gson) / ProtoBuf / Kryo

**面试重点**：
- `serialVersionUID` 的作用（显式声明避免反序列化失败）
- `transient` 修饰的 `static` 字段：`static` 本身就属于类而非实例
- `readObject()` / `writeObject()` 自定义序列化逻辑
- `Externalizable` vs `Serializable` 的区别

---

### 2.6 网络编程基础

**TCP/IP 协议栈**：

```
应用层   HTTP / FTP / SMTP / DNS
传输层   TCP（可靠） / UDP（不可靠）
网络层   IP / ICMP / ARP
网络接口  以太网 / WiFi
```

**Socket 编程**：

| 类型 | 特点 | 适用场景 |
|------|------|---------|
| **TCP Socket** | 面向连接、可靠、有序 | 文件传输、网页浏览 |
| **UDP Socket** | 无连接、不可靠、高效 | 视频直播、DNS 查询 |

```java
// TCP 服务端示例
ServerSocket server = new ServerSocket(8080);
Socket client = server.accept();  // 阻塞等待客户端连接
BufferedReader in = new BufferedReader(
    new InputStreamReader(client.getInputStream()));
PrintWriter out = new PrintWriter(client.getOutputStream(), true);
String msg = in.readLine();
out.println("Server received: " + msg);
client.close(); server.close();
```

**HTTP 协议要点**：
- 请求结构：请求行（Method URL HTTP/1.1）+ 请求头 + 空行 + 请求体
- 响应结构：状态行（HTTP/1.1 200 OK）+ 响应头 + 空行 + 响应体
- 无状态协议：每个请求独立，通过 Cookie/Session 维持状态
- HTTPS：在 HTTP 和 TCP 之间加一层 SSL/TLS 加密

**面试重点**：
- TCP 三次握手 / 四次挥手的过程与状态（SYN_SENT, ESTABLISHED, TIME_WAIT）
- TCP 与 UDP 的区别及各自适用场景
- Socket 与 WebSocket 的区别（全双工 vs 半双工）
- HTTP/1.1 vs HTTP/2 vs HTTP/3 的核心改进（多路复用、头部压缩、QUIC）

---

### 2.7 设计模式

详细笔记：[[design-patterns]]（待创建）

设计模式是软件设计中常见问题的典型解决方案。测试自动化框架中大量使用设计模式。

**创建型模式**：

| 模式 | 核心思想 | 测试框架中的应用 |
|------|---------|----------------|
| **单例模式 (Singleton)** | 确保一个类只有一个实例，提供全局访问点 | 配置管理器、Driver 管理器、Token 管理器 |
| **工厂模式 (Factory)** | 定义一个创建对象的接口，让子类决定实例化哪个类 | `WebDriverFactory` 根据配置创建 Chrome/Firefox/Edge 实例 |
| **建造者模式 (Builder)** | 分步构造复杂对象，链式调用 | 测试数据构造：`User.builder().name("xx").age(20).build()` |
| **原型模式 (Prototype)** | 通过复制现有对象创建新实例 | 复杂测试数据的克隆 |

**结构型模式**：

| 模式 | 核心思想 | 测试框架中的应用 |
|------|---------|----------------|
| **代理模式 (Proxy)** | 为另一个对象提供一个替身或占位符以控制对它的访问 | AOP 底层、Remote WebDriver、延迟加载 |
| **装饰器模式 (Decorator)** | 动态给对象添加新职责，比继承更灵活 | 给 WebDriver 添加日志、截图、超时重试功能 |
| **适配器模式 (Adapter)** | 将一个类的接口转换成客户希望的另一个接口 | `WebDriver` 接口统一不同浏览器驱动 |
| **外观模式 (Facade)** | 为子系统提供统一的简化接口 | 测试 API 封装层，对外提供简单的操作方法 |

**行为型模式**：

| 模式 | 核心思想 | 测试框架中的应用 |
|------|---------|----------------|
| **策略模式 (Strategy)** | 定义一系列算法，把它们封装起来并可互换 | 不同的等待策略、不同的登录方式、不同的数据源 |
| **模板方法模式 (Template Method)** | 定义算法的骨架，子类重写特定步骤 | 测试用例的固定流程：setUp → test → tearDown |
| **观察者模式 (Observer)** | 定义一对多依赖关系，状态变化通知所有观察者 | 测试事件监听（TestNG ITestListener）、Allure 报告 |
| **责任链模式 (Chain of Responsibility)** | 多个对象依次处理请求 | 测试数据预处理链、中间件过滤器 |

**设计原则 SOLID**：

| 原则 | 含义 | 测试中的体现 |
|------|------|-------------|
| **S**RP 单一职责 | 一个类只做一件事 | Page Object 中每个页面类只封装该页面的元素和操作 |
| **O**CP 开闭原则 | 对扩展开放，对修改封闭 | 添加新浏览器时只需新增 Driver 类，无需修改现有代码 |
| **L**SP 里氏替换 | 子类必须能替换父类 | `ChromeDriver` 替换 `WebDriver` 不改变测试代码 |
| **I**SP 接口隔离 | 接口应该小而专 | 测试报告接口分离为 `Reportable`（生成报告）和 `Loggable`（记录日志）|
| **D**IP 依赖倒转 | 依赖抽象而非具体实现 | 测试代码依赖 `WebDriver` 接口而非 `ChromeDriver` 具体类 |

**面试重点**：
- 单例模式的各种实现方式（饿汉、懒汉、双重检查、枚举）及线程安全
- 工厂模式与策略模式的区别
- 代理模式在 AOP 中的应用（JDK 动态代理 vs CGLIB）
- 你用过哪些设计模式？结合项目讲（用测试框架项目举例最佳）

---

## 三、Spring Boot

详细笔记：[[spring-boot-core]]

### 3.1 IoC 容器

**核心概念**：
- **控制反转 (IoC)**：对象的创建和管理权从代码转移到容器
- **依赖注入 (DI)**：容器在运行时将依赖注入到对象中
- **Bean 生命周期**：

```
加载 BeanDefinition → 实例化 → 属性赋值 → 各种 Aware 接口 →
BeanPostProcessor前置 → @PostConstruct → InitializingBean →
BeanPostProcessor后置 → 就绪 → @PreDestroy → DisposableBean → 销毁
```

**@Autowired vs @Resource**：

| 对比 | @Autowired | @Resource |
|------|-----------|-----------|
| 来源 | Spring 注解 | JSR-250 规范 |
| 注入方式 | ByType 优先 | ByName 优先 |
| 允许 null | 可配合 `required=false` | 默认不允许 |
| 配合 @Qualifier | `@Autowired + @Qualifier(name)` | `@Resource(name="xxx")` |

**面试重点**：
- 循环依赖的解决机制（三级缓存：singletonObjects / earlySingletonObjects / singletonFactories）
- 为什么要三级缓存？二级不够吗？（需要区分原始对象和代理对象）
- `@Lazy` 注解解决循环依赖的原理

---

### 3.2 AOP (面向切面编程)

**核心概念**：

```
├── Aspect（切面）—— 关注点模块化
├── Join Point（连接点）—— 方法执行
├── Pointcut（切入点）—— 匹配连接点的表达式
├── Advice（通知/增强）
│   ├── @Before  前
│   ├── @After   后
│   ├── @AfterReturning  返回后
│   ├── @AfterThrowing   异常后
│   └── @Around  环绕
└── Weaving（织入）—— 将切面应用到目标对象
```

**执行顺序**：
```
@Around 开始 → @Before → 目标方法 → @AfterReturning/@AfterThrowing →
@After → @Around 结束
```

**面试重点**：
- AOP 底层实现：JDK 动态代理（接口）vs CGLIB（类）
- `@Transactional` 注解的失效场景（private 方法、同类中调用、异常类型不匹配）
- Pointcut 表达式语法：`execution(* com.xxx.service.*.*(..))`

---

### 3.3 REST 开发

```java
@RestController
@RequestMapping("/api/users")
public class UserController {

    @GetMapping("/{id}")                    // GET /api/users/1
    public User getUser(@PathVariable Long id) { }

    @PostMapping                            // POST /api/users
    public User createUser(@RequestBody User user) { }

    @PutMapping("/{id}")                    // PUT /api/users/1
    public User updateUser(@PathVariable Long id, @RequestBody User user) { }

    @DeleteMapping("/{id}")                 // DELETE /api/users/1
    public void deleteUser(@PathVariable Long id) { }
}
```

**参数绑定**：
- `@PathVariable`：路径参数
- `@RequestParam`：查询参数（`?name=xxx`）
- `@RequestBody`：请求体 JSON 绑定到 Java 对象
- `@RequestHeader`：请求头
- `@Valid` / `@Validated`：JSR-303 参数校验

**面试重点**：
- `@RestController` vs `@Controller` + `@ResponseBody`
- `@RequestMapping` vs 简写注解（`@GetMapping` 等）
- 全局日期格式配置（Jackson 的 `@JsonFormat` / `application.yml`）

---

### 3.4 数据访问

**JPA vs MyBatis**：

| 对比 | JPA / Hibernate | MyBatis |
|------|----------------|---------|
| 映射方式 | ORM（对象关系映射） | SQL 映射 |
| SQL 控制 | JPQL / Criteria，自动生成 | 手写 SQL，完全控制 |
| 开发效率 | 高（CRUD 几乎不用写 SQL） | 中 |
| 优化空间 | 有限（N+1 问题需注意） | 大（可精细优化 SQL） |
| 复杂查询 | 相对困难 | 灵活 |

**@Transactional 关键属性**：

| 属性 | 说明 | 默认值 |
|------|------|--------|
| `propagation` | 传播行为（REQUIRED / REQUIRES_NEW / NESTED 等） | REQUIRED |
| `isolation` | 隔离级别（READ_COMMITTED / REPEATABLE_READ 等） | 数据库默认 |
| `timeout` | 超时时间 | -1 |
| `rollbackFor` | 触发回滚的异常类型 | RuntimeException 和 Error |
| `readOnly` | 只读优化 | false |

**面试重点**：
- JPA N+1 问题的原因和解决方案（`@EntityGraph` / `JOIN FETCH` / `@BatchSize`）
- MyBatis `#{}` vs `${}` 的区别（预编译 vs 字符串替换）
- 事务传播行为 `REQUIRED` vs `REQUIRES_NEW` 的实际应用
- 同类内方法调用导致 `@Transactional` 失效的原因（AOP 代理）

---

### 3.5 异常处理

```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public Result<?> handleValidation( MethodArgumentNotValidException e) {
        // 参数校验异常
    }

    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusiness(BusinessException e) {
        // 业务异常
    }

    @ExceptionHandler(Exception.class)
    public Result<?> handleException(Exception e) {
        // 兜底异常
    }
}
```

**常见 HTTP 状态码与业务含义**：

| 状态码 | 含义 | 典型场景 |
|--------|------|---------|
| 200 | OK | 成功 |
| 201 | Created | 创建成功 |
| 400 | Bad Request | 参数错误 |
| 401 | Unauthorized | 未登录 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 500 | Internal Server Error | 服务端异常 |

---

### 3.6 拦截器 / 过滤器

| 组件 | 位置 | 用途 |
|------|------|------|
| **Filter** | Servlet 容器层（Web.xml / @WebFilter） | 通用处理：编码、CORS、XSS 过滤 |
| **Interceptor** | Spring MVC 层（HandlerInterceptor） | 更细粒度：登录校验、日志、权限 |

**Filter 执行链**：
```
Filter.doFilter(request, response, chain) → Servlet → HandlerInterceptor
```

**HandlerInterceptor 方法**：
```java
public class LogInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) {
        // 请求前，返回 false 中断请求
    }
    @Override
    public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler, ModelAndView mv) {
        // 请求后、视图渲染前
    }
    @Override
    public void afterCompletion(HttpServletRequest request, HttpServletResponse response, Object handler, Exception ex) {
        // 请求完成后（无论是否异常）
    }
}
```

---

## 四、数据库

### 4.1 SQL 基础

**必会操作**：
```sql
-- CRUD
SELECT / INSERT / UPDATE / DELETE

-- JOIN
INNER JOIN / LEFT JOIN / RIGHT JOIN / FULL OUTER JOIN / CROSS JOIN

-- 聚合
GROUP BY ... HAVING ...  -- HAVING 用于过滤聚合后结果

-- 子查询
WHERE id IN (SELECT user_id FROM orders)
EXISTS (SELECT 1 FROM orders WHERE user_id = u.id)

-- 窗口函数 (JDK8+ SQL)
ROW_NUMBER() / RANK() / DENSE_RANK() / LAG() / LEAD() OVER (PARTITION BY ... ORDER BY ...)
```

**面试重点**：
- `WHERE` vs `HAVING` 的区别
- 子查询 vs JOIN 的性能比较（取决于具体场景和数据量）
- SQL 执行顺序：`FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`

---

### 4.2 索引

**B+ 树索引结构**：
- 非叶子节点只存储键值（索引列值 + 指向子节点的指针）
- 叶子节点存储完整记录（聚簇索引）或主键 + 指向记录的指针（非聚簇索引）
- 叶子节点之间通过双向链表连接，支持范围查询

| 类型 | 说明 |
|------|------|
| **聚簇索引 (Clustered Index)** | InnoDB 主键索引，叶子节点存储整行数据 |
| **非聚簇索引 (Secondary Index)** | 普通索引，叶子节点存储主键值（需回表） |
| **联合索引 (Composite Index)** | 多列组成的索引，遵循最左前缀原则 |
| **覆盖索引 (Covering Index)** | 索引已包含查询所需的所有字段，无需回表 |

**最左前缀原则**：
- 联合索引 `(a, b, c)` 有效查询组合：
  - `WHERE a = ?` / `WHERE a = ? AND b = ?` / `WHERE a = ? AND b = ? AND c = ?`
  - `WHERE a IN (?, ?)` 也走索引
- 无效查询：`WHERE b = ?` / `WHERE c = ?`（跳过了 a）

**面试重点**：
- B+ 树为什么适合做索引？（树高低、IO 次数少、范围查询快）
- 为什么建议使用自增主键？（页分裂少、数据顺序写入）
- 回表 vs 覆盖索引的判断（看 Extra 列）

---

### 4.3 事务

**ACID 特性**：

| 特性 | 含义 | 实现机制 |
|------|------|---------|
| **原子性 (Atomicity)** | 事务要么全部成功，要么全部回滚 | undo log |
| **一致性 (Consistency)** | 事务前后数据状态一致 | 应用层 + 数据库约束 |
| **隔离性 (Isolation)** | 并发事务之间互不干扰 | MVCC + 锁 |
| **持久性 (Durability)** | 事务提交后数据永久保存 | redo log |

**隔离级别**：

| 级别 | 脏读 | 不可重复读 | 幻读 |
|------|------|-----------|------|
| READ UNCOMMITTED | &#x2716; | &#x2716; | &#x2716; |
| READ COMMITTED | &#x2714; | &#x2716; | &#x2716; |
| REPEATABLE READ (MySQL 默认) | &#x2714; | &#x2714; | &#x2716; |
| SERIALIZABLE | &#x2714; | &#x2714; | &#x2714; |

**MVCC (Multi-Version Concurrency Control)**：
- 每行数据维护多个版本，每个版本有事务 ID 标记
- `Read View` 决定事务能看到哪些版本
- 核心字段：`DB_TRX_ID`（事务ID）、`DB_ROLL_PTR`（回滚指针，指向 undo log）
- MVCC 实现 RR 级别下不存在幻读（但 `SELECT ... FOR UPDATE` 加锁后仍可能存在幻读，需 `gap lock`）

**面试重点**：
- MVCC 在 RC 和 RR 下的区别（RC 每条语句生成新 Read View，RR 复用事务开始时的 Read View）
- `Next-Key Lock`（行锁 + gap 锁）如何解决 RR 下的幻读

---

### 4.4 慢 SQL 优化

**优化流程**：
1. 开启慢查询日志（`long_query_time`）
2. `EXPLAIN` 分析执行计划
3. 索引优化 / SQL 改写 / 分库分表

**EXPLAIN 关键字段**：

| 字段 | 重点值 | 说明 |
|------|--------|------|
| `type` | `const` > `ref` > `range` > `index` > `ALL` | 访问类型，从好到差 |
| `possible_keys` | — | 可能使用的索引 |
| `key` | 实际使用的索引 | 关注是否为空 |
| `rows` | 越小越好 | 扫描行数估算 |
| `Extra` | `Using index`（覆盖索引）/ `Using filesort`（需要优化）/ `Using temporary`（需要优化） | 补充信息 |

**常见优化手段**：
- 使用覆盖索引避免回表
- 避免 `SELECT *`，只取需要的字段
- `LIKE '%xxx'` 不走索引（前导通配符）
- 函数操作列不走索引（`WHERE DATE(create_time) = '2024-01-01'` 改为范围查询）
- 小表驱动大表（`IN` vs `EXISTS`的选择）
- 分页优化：`LIMIT 100000, 20` 改成 `WHERE id > 100000 LIMIT 20`

---

## 五、工具链

### 5.1 Maven / Gradle

**Maven 核心概念**：
- 坐标：`groupId:artifactId:version`
- 依赖范围：`compile` / `provided` / `runtime` / `test` / `system` / `import`
- 依赖传递与冲突解决：**最短路径优先**，同路径先声明优先
- 生命周期：`clean` → `validate` → `compile` → `test` → `package` → `verify` → `install` → `deploy`

**Gradle vs Maven**：

| 对比 | Maven | Gradle |
|------|-------|--------|
| 配置文件 | XML（pom.xml） | Groovy/Kotlin DSL |
| 性能 | 较慢 | 快（增量编译、构建缓存） |
| 灵活性 | 约定大于配置 | 更加灵活 |
| 学习曲线 | 平缓 | 较陡 |

**面试重点**：
- Maven 依赖冲突解决策略
- `dependencyManagement` vs `dependencies` 的区别
- Gradle 中 `implementation` vs `api` 的区别

---

### 5.2 Git

**分支策略对比**：

| 模型 | 特点 | 适用 |
|------|------|------|
| **Git Flow** | master / develop / feature / release / hotfix | 大项目、版本发布 |
| **GitHub Flow** | main → feature → PR | 持续部署 |
| **GitLab Flow** | 环境分支（pre-production / production） | 环境隔离 |

**rebase vs merge**：

| 操作 | 结果 | 适用场景 |
|------|------|---------|
| `merge` | 保留合并历史，生成 merge commit | 公共分支、需要保留真实合并记录 |
| `rebase` | 线性历史，无 merge commit | 私有分支、保持提交历史整洁 |
| `squash merge` | 将整个分支压缩为一个 commit | 功能分支合并到主分支 |

**冲突解决**：
- 标记冲突文件 → 手动编辑 → `git add` → `git commit` 或 `git rebase --continue`
- `git mergetool` 图形化解决
- `git stash` 暂存当前工作

**面试重点**：
- `git reset` vs `git revert` vs `git restore` 的区别
- `git rebase` 的黄金法则（不要对已推送的公共分支 rebase）
- `cherry-pick` 的适用场景

---

### 5.3 Linux 常用命令

**必会命令分类**：

| 类别 | 命令 |
|------|------|
| 文件操作 | `ls` / `cd` / `cp` / `mv` / `rm` / `find` / `tar` |
| 文本处理 | `grep` / `sed` / `awk` / `cut` / `sort` / `uniq` / `wc` |
| 进程管理 | `ps` / `top` / `htop` / `kill` / `nohup` |
| 网络 | `netstat` / `ss` / `curl` / `ping` / `telnet` |
| 权限 | `chmod` / `chown` / `useradd` |
| 磁盘 | `df` / `du` / `fdisk` |
| 系统 | `uname` / `free` / `uptime` / `dmesg` |
| 日志 | `tail -f` / `less` / `journalctl` |

**排查 Java 应用问题常用命令**：
```bash
# 查看进程
ps -ef | grep java
jps -l

# 查看端口
netstat -tlnp | grep 8080
ss -tlnp | grep 8080

# 查看日志
tail -f application.log | grep ERROR
less application.log

# 系统负载
top -Hp <pid>
free -h
df -h

# JVM 工具
jstack <pid>          # 线程堆栈
jmap -heap <pid>      # 堆信息
jstat -gc <pid> 1000  # GC 情况
```

---

## 六、与 [[软件测试知识体系]] 的连接

### 6.1 Java 是自动化测试框架的主力语言

- **Selenium / WebDriver**：Java 是最主流的 Web UI 自动化语言，通过 WebDriver API 操作浏览器
- **Rest Assured**：Java 的 HTTP API 测试框架，天然与 Spring Boot 应用匹配
- **JUnit / TestNG**：Java 单元测试框架，注解体系与 Java 注解机制深度绑定
- **JMeter**：基于 Java 的性能测试工具，可编写 Java Sampler 自定义逻辑

### 6.2 设计模式在自动化框架中的应用

| 模式 | 测试中的应用 |
|------|------------|
| **Page Object** | 每个页面封装为一个类，解耦页面元素与测试逻辑 |
| **Factory** | 根据配置创建不同的 WebDriver 实例（Chrome / Firefox / Edge） |
| **Builder** | 构造复杂的测试数据对象（如 `User.builder().name("xxx").build()`） |
| **Singleton** | 全局唯一的配置管理、Token 管理器 |
| **Strategy** | 不同的登录方式（密码 / OAuth / SSO） |
| **Template Method** | 测试用例的固定流程模版（setup → execute → verify → teardown） |
| **Chain of Responsibility** | 测试数据处理的过滤链 |

### 6.3 Spring Boot 在测试中的应用

- `@SpringBootTest`：加载完整 Spring 上下文进行集成测试
- `@WebMvcTest`：仅加载 Web 层进行 Controller 测试
- `@DataJpaTest`：仅加载 JPA 层进行数据访问测试
- `@MockBean` / `@SpyBean`：在 Spring 上下文中替换 Bean 为 Mock 对象
- `TestRestTemplate` / `WebTestClient`：REST API 测试客户端
- `@Sql`：测试前准备 / 测试后清理数据库数据

### 6.4 SQL 知识与测试

- 测试数据准备：`INSERT` + `DELETE` / 事务回滚
- 数据库校验：查询落库数据与期望值对比
- 造数工具：`SQL` 脚本 / `Faker` 库 / 自动化生成

---

## 七、与 [[AI应用开发知识体系]] 的连接

### 7.1 Java 调用 LLM API

```java
// 使用 HttpClient (JDK11+)
HttpClient client = HttpClient.newHttpClient();
HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.openai.com/v1/chat/completions"))
    .header("Authorization", "Bearer " + apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
    .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

// Spring RestTemplate（传统方式）
RestTemplate restTemplate = new RestTemplate();
ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.POST, entity, String.class);

// Spring WebClient（响应式方式）
WebClient webClient = WebClient.create();
Mono<String> mono = webClient.post()
    .uri(url)
    .header("Authorization", "Bearer " + apiKey)
    .bodyValue(requestBody)
    .retrieve()
    .bodyToMono(String.class);

// 流式输出 (Server-Sent Events)
webClient.post()
    .uri(url)
    .accept(MediaType.TEXT_EVENT_STREAM)
    .retrieve()
    .bodyToFlux(String.class)
    .subscribe(System.out::println);
```

### 7.2 Spring Boot 作为 AI 工具的后端

- **REST API 服务层**：封装 LLM 调用逻辑，对外提供统一接口
- **Prompt 模板管理**：使用数据库或配置管理不同的 Prompt 模板
- **结果缓存**：对高频或重复的 AI 请求使用 Redis 缓存（相同输入命中缓存）
- **请求限流**：使用 `RateLimiter`（Guava / Resilience4j）控制 API 调用频率
- **异步处理**：`@Async` + `CompletableFuture` 处理批量 AI 请求

### 7.3 多线程处理 AI 请求

```java
// 批量调用 LLM API
List<CompletableFuture<Result>> futures = inputs.stream()
    .map(input -> CompletableFuture.supplyAsync(() -> callLLM(input), executor))
    .collect(Collectors.toList());

List<Result> results = futures.stream()
    .map(CompletableFuture::join)
    .collect(Collectors.toList());

// 流式处理多个请求
ExecutorService executor = Executors.newFixedThreadPool(5);
List<Future<Result>> futures = executor.invokeAll(tasks);
```

---

## 八、学习路径建议（结合 Java 路线图）

本路径按路线图的阶段结构展开，标注了与测试领域的交叉点。

### 第一阶段：Java 基础入门（路线图第1阶段）
1. **环境搭建**：JDK + IDE + Maven
2. **基础语法**：变量、流程控制、数组、方法
3. **面向对象**：封装/继承/多态、抽象类/接口、内部类（⭐ 自动化框架基础）
4. **常用类库**：String、包装类、日期时间、异常体系
5. **练手项目**：学生管理系统（控制台版）
6. **与测试交叉**：OOP 设计思想是 Page Object 模式的基础

### 第二阶段：Java 核心进阶（路线图第2阶段）
1. **集合框架**：List/Set/Map 体系、HashMap 底层（⭐ 自动化中大量数据处理）
2. **IO 流与 NIO**：字节流/字符流、缓冲流、序列化（⭐ 测试数据读写、文件上传测试）
3. **多线程与并发**：线程池、JUC、CompletableFuture（⭐ 并发测试、性能测试基础）
4. **网络编程**：Socket、HTTP 协议（⭐ 接口测试理论基础）
5. **反射与注解**：Class 对象、自定义注解（⭐ 测试框架底层机制，JUnit/TestNG 原理）
6. **设计模式**：单例/工厂/Builder/代理/策略（⭐ 自动化框架设计必备）

### 第三阶段：数据库与 JDBC（路线图第3阶段）
1. **MySQL 核心**：SQL 基础、索引原理、事务与 MVCC、存储引擎
2. **JDBC 编程**：PreparedStatement、连接池（Druid/HikariCP）
3. **与测试交叉**：测试数据准备/清理、数据库断言、慢 SQL 定位

### 第四阶段：Web 开发基础（路线图第4阶段，了解即可）
1. **JavaWeb 核心**：Servlet 生命周期、Filter/Listener、Session/Cookie
2. **前端基础**：HTML/CSS/JS（能看懂即可）
3. **与测试交叉**：理解 Web 请求流程有助于接口调试和安全测试

### 第五阶段：主流框架（路线图第5阶段，⭐ 核心）
1. **Spring 核心**：IoC/DI/AOP 原理、Bean 生命周期
2. **SpringMVC**：请求处理流程、RESTful API
3. **MyBatis**：动态 SQL、关联查询、缓存
4. **Spring Boot**：自动配置、Starter、整合测试（⭐ `@SpringBootTest` / MockBean）
5. **与测试交叉**：Spring Boot 测试全家桶是测试开发的核心技能

### 第六阶段：中间件与分布式（路线图第6阶段，理解概念）
1. **Redis**：数据结构、缓存策略、分布式锁（⭐ 性能测试中缓存场景分析）
2. **消息队列**：RabbitMQ/Kafka 核心概念（⭐ 理解异步解耦，MQ 测试场景设计）
3. **微服务**：Spring Cloud 基本概念（面试了解级）
4. **Docker**：容器化部署、Docker Compose（⭐ 测试环境管理必备）

### 第七阶段：JVM 与性能优化（路线图第7阶段）
1. **JVM 内存模型**：堆/栈/方法区、GC 算法（⭐ 性能测试分析基础）
2. **调优与监控**：JVM 参数、Arthas、MAT（⭐ 线上性能问题定位）

### 第八阶段：设计模式与代码质量（路线图第8阶段，持续学习）
1. **23 种设计模式**：重点掌握单例/工厂/Builder/代理/策略/模板方法
2. **代码规范**：阿里巴巴 Java 开发手册
3. **单元测试**：JUnit + Mockito（⭐ 测试核心技能）

### 第九阶段：项目实战（路线图第9阶段，贯穿始终）
1. **练手项目**：博客系统（SSM）/ 商城项目（Spring Boot）
2. **与测试交叉**：每个练手项目都应配套自动化测试

---

> **本文是 Java 开发知识体系的索引和思维导图**，每个子主题对应独立的 wiki 页面（如 [[collections-framework]]、[[concurrency-java]]、[[jvm-basics]]、[[spring-boot-core]]），请点击链接查看详细内容。
>
> 关联体系：[[软件测试知识体系]] | [[AI应用开发知识体系]]
