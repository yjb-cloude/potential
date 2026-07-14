# Java Collections Framework

Java Collections Framework（JCF）是 Java 标准库中最核心的 API 之一，提供了一套统一的接口和实现来管理对象组。它位于 `java.util` 包中，是日常开发的基石。

## 接口体系

整个框架围绕两个顶层接口展开：

### Collection 接口

```
Collection
  ├── List（有序可重复，允许 null）
  │   ├── ArrayList    ← 动态数组实现，随机访问 O(1)，插入/删除 O(n)
  │   └── LinkedList   ← 双向链表实现，插入/删除 O(1)，随机访问 O(n)
  ├── Set（不可重复）
  │   ├── HashSet          ← 基于 HashMap，无序，O(1)
  │   ├── LinkedHashSet    ← 继承 HashSet，双向链表维护插入顺序
  │   └── TreeSet          ← 红黑树实现，自然排序/Comparator，O(log n)
  └── Queue / Deque
      ├── PriorityQueue    ← 堆实现，优先级队列
      └── ArrayDeque       ← 循环数组实现的双端队列
```

### Map 接口

```
Map
  ├── HashMap           ← 数组+链表+红黑树，O(1)，允许 null
  ├── LinkedHashMap     ← 双向链表维护访问/插入顺序
  ├── TreeMap           ← 红黑树，有序，O(log n)
  ├── Hashtable         ← 线程安全（已淘汰），不允许 null
  └── ConcurrentHashMap ← 高并发安全
```

## HashMap 深度解析（面试高频）

### 数据结构

JDK8 采用 **数组 + 链表 + 红黑树** 结构。每个数组元素称为 bucket（桶），存储链表的头节点或红黑树根节点。当链表长度达到阈值 8 时，链表转换为红黑树，优化极端哈希冲突场景的查询性能。

### put 流程

1. 调用 `hash(key)` 计算 key 的散列值（高位参与扰动）
2. `(n - 1) & hash` 确定 bucket 索引
3. 若 bucket 为空，直接创建 Node 插入
4. 若 bucket 非空，遍历链表/红黑树：
   - 找到相同 key → 覆盖旧值
   - 未找到 → 尾部插入（JDK7 是头插，JDK8 改为尾插解决死循环问题）
5. 插入后检查 size > threshold（capacity × loadFactor）→ 触发扩容

### 扩容机制

- **初始容量：** 16
- **负载因子：** 0.75（时间与空间的平衡）
- **扩容倍数：** 2 倍（保证容量始终为 2 的幂，便于位运算）
- **rehash：** 元素在新数组中的位置要么在原索引，要么在原索引 + oldCap

### 线程安全问题

HashMap 不是线程安全的，多线程环境下会引发：
- **JDK7 死循环：** 头插法在并发扩容时形成循环链表，get 时无限循环
- **数据丢失：** 多个线程同时 put 覆盖彼此的修改

解决方案：使用 `ConcurrentHashMap` 或 `Collections.synchronizedMap()`。

## ConcurrentHashMap

- **JDK7：** 分段锁（Segment 继承 ReentrantLock），默认 16 段，写操作锁单段
- **JDK8：** 放弃分段锁，采用 **synchronized + CAS**，锁的粒度更细（单个 bucket），并发度更高

## ArrayList vs LinkedList

| 操作 | ArrayList | LinkedList |
|------|-----------|------------|
| 尾部插入 | O(1) 均摊 | O(1) |
| 指定位置插入/删除 | O(n) 数组移动 | O(n) 遍历到位置 |
| 随机访问 get(i) | O(1) | O(n) |
| 内存占用 | 连续内存，略少 | 每个节点多存前后指针 |

## Collections 工具类

提供大量操作集合的静态方法：
- **排序/搜索：** `sort()`, `binarySearch()`, `reverse()`, `shuffle()`
- **不可变包装：** `unmodifiableList()`, `unmodifiableMap()`, `unmodifiableSet()`
- **同步包装：** `synchronizedList()`, `synchronizedMap()`——早期线程安全替代方案
- **空安全：** `emptyList()`, `singletonList()`

适用场景：日常编程中优先使用 Collections 工具类提供的不可变视图来防御性拷贝。

---

**关联知识点：** [[concurrency-java]] | [[Java开发知识体系]] | [[jvm-basics]]
