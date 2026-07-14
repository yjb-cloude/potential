# Java 并发编程

Java 并发编程是多线程应用开发的核心能力，涵盖从基础的线程创建到高级的并发容器和异步编程模型。理解并发机制是成为高级 Java 开发者的必修课。

## 线程基础

### 创建线程的三种方式

1. **Thread 类：** 继承 Thread，重写 `run()` 方法
2. **Runnable 接口：** 实现 Runnable，传递给 Thread，更灵活（避免单继承限制）
3. **Callable + Future：** 实现 Callable（带返回值），通过 FutureTask 或 ThreadPoolExecutor 提交，获取异步结果

### 线程六种状态

```
NEW → RUNNABLE → BLOCKED / WAITING / TIMED_WAITING → TERMINATED
```

- **NEW：** 创建后尚未启动
- **RUNNABLE：** 可运行状态（包含操作系统就绪和运行中）
- **BLOCKED：** 等待锁（synchronized 阻塞）
- **WAITING：** 无限期等待（`wait()`, `join()`, `park()`）
- **TIMED_WAITING：** 限时等待（`sleep()`, `wait(timeout)`, `join(timeout)`）
- **TERMINATED：** 执行完毕

## synchronized 原理

### 锁升级（偏向锁→轻量级锁→重量级锁）

JDK6 引入的锁升级机制是为了减少锁的开销：

- **无锁 → 偏向锁：** 第一个线程获取锁时，在对象头 Mark Word 记录线程 ID，后续该线程无需 CAS 操作即可进入
- **偏向锁 → 轻量级锁：** 其他线程竞争时，升级为轻量级锁（自旋锁），通过 CAS 尝试获取
- **轻量级锁 → 重量级锁：** 自旋达到阈值（默认 10 次）或自旋线程数超过 CPU 核数一半时，膨胀为重量级锁，未获取到的线程进入 BLOCKED 状态

**Mark Word** 是对象头中的关键字段，存储对象的 hashCode、GC 分代年龄和锁状态信息。

## volatile 关键字

volatile 保证两条语义：
- **可见性：** 写 volatile 变量时强制刷新到主内存；读 volatile 变量时强制从主内存读取，通过 **内存屏障** 实现
- **禁止指令重排序：** 插入内存屏障阻止编译器和 CPU 的重排序优化

volatile 不保证原子性，所以 `count++` 这类复合操作仍需加锁。

## JMM（Java 内存模型）

JMM 定义了线程与主内存之间的抽象关系：
- 所有变量存储在主内存
- 每个线程拥有自己的工作内存（线程私有，缓存变量副本）
- 线程不能直接操作主内存，必须通过工作内存读写

### happens-before 规则

如果一个操作 happens-before 另一个操作，那么前者的执行结果对后者可见。核心规则有：
- 程序次序规则：线程内书写在前面的操作 happens-before 后面的
- volatile 规则：对 volatile 变量的写 happens-before 后续对该变量的读
- 锁规则：解锁 happens-before 加锁
- 传递性：A happens-before B, B happens-before C → A happens-before C

## Lock 体系

### ReentrantLock

相比 synchronized 更灵活：
- **可重入：** 同一线程可多次加锁，需对应次数 unlock
- **公平/非公平：** 构造参数 fair 控制是否按等待队列顺序获取锁
- **可中断：** `lockInterruptibly()` 可响应中断
- **超时：** `tryLock(timeout, unit)` 尝试获取锁

### Condition

类似 Object 的 wait/notify 机制，但更强大。一个 Lock 可创建多个 Condition 实例，实现更精细的线程协作：
```java
lock.lock();
try {
    while (!condition) {
        condition.await();  // 释放锁并等待
    }
    condition.signalAll();
} finally {
    lock.unlock();
}
```

### ReentrantReadWriteLock

读写分离锁：
- **读锁：** 共享锁，多个读线程可同时持有
- **写锁：** 独占锁，写操作时不允许其他读写

## ThreadPoolExecutor 核心参数（面试必考）

```java
ThreadPoolExecutor(
    int corePoolSize,      // 核心线程数
    int maxPoolSize,       // 最大线程数
    long keepAliveTime,    // 空闲线程存活时间
    TimeUnit unit,         // 时间单位
    BlockingQueue<Runnable> workQueue,  // 任务队列
    ThreadFactory threadFactory,        // 线程工厂
    RejectedExecutionHandler handler    // 拒绝策略
)
```

**工作流程：** 核心线程 → 任务队列 → 扩展线程 → 拒绝策略

### 四种拒绝策略

| 策略 | 行为 |
|------|------|
| AbortPolicy（默认） | 抛出 RejectedExecutionException |
| CallerRunsPolicy | 提交任务的线程自己执行 |
| DiscardPolicy | 静默丢弃 |
| DiscardOldestPolicy | 丢弃队列最前面的任务 |

## CompletableFuture

JDK8 引入的函数式异步编程模型：
- **thenApply：** 转换异步结果
- **thenCompose：** 异步结果扁平化连接
- **thenCombine：** 合并两个异步任务的结果
- **allOf：** 等待所有 CompletableFuture 完成
- **anyOf：** 任意一个完成即返回

## 线程安全最佳实践

1. **优先使用并发容器：** CopyOnWriteArrayList（读多写少）、ConcurrentHashMap、BlockingQueue（生产者-消费者）
2. **使用原子类：** AtomicInteger、AtomicReference（基于 CAS 实现）
3. **避免锁的粗粒度：** 缩小同步块的作用范围
4. **使用 ThreadLocal：** 代替共享变量，每个线程持有独立副本
5. **合理设置线程池参数：** 根据 CPU 密集 / IO 密集计算线程数

---

**关联知识点：** [[collections-framework]] | [[jvm-basics]] | [[Java开发知识体系]]
