# SQL 错题本

> SQL 实战练习 + 面试模拟记录（2026-08-17 开始）
> 配套：`practice/sql/init.sql` + `practice-01.md`

---

# SQL 实战训练（2026-08-17 开始）

> 配套：`practice/sql/init.sql` + `practice-01.md`（电商订单系统，三张表）
> 连接：`mysql --default-character-set=utf8mb4 -uroot -proot sql_practice`（必须带 utf8mb4，否则中文乱码）

## 第三关 JOIN 实战 — 踩坑三连（13-17 题通关）

### 坑 1：字段名拼错 → 直接报错

`o.order_data` ❌ → 正确是 `o.order_date`（少写个 e）
- MySQL 报错：`ERROR 1054: Unknown column 'o.order_data' in 'field list'`
- 教训：写 SQL 前先 `DESCRIBE 表名` 看真实字段，别凭记忆

### 坑 2：quantity（数量）≠ amount（金额）——漏选字段

题目要"数量"，我选了 amount，以为金额就是数量。看数据：
- AirPods Pro 单价 1899：`quantity = 2`（买几件）`amount = 3698`（花多少钱）
- 这个库里 amount ≠ price × quantity（有优惠 100 元）

**测试思维金句：对照需求逐项核对，而不是"能跑就行"——用例全绿 ≠ 需求全覆盖。**

### 坑 3：需求理解偏差（二刷！7 月记过一次）

把"**从没被下单过的商品**"写成了 `WHERE o.status = 'pending'`（订单待支付的商品）——返回 MacBook Air 等 3 个错误结果。

错在哪：MacBook Air 有订单（lisi 的，只是没付款）→ 它是"被下单过"的。"没被下单" = 订单表里**完全没有记录** = LEFT JOIN 后 IS NULL。

**正确写法（经典考点，必背）：**
```sql
SELECT p.product_name FROM products p
LEFT JOIN orders o ON o.product_id = p.product_id
WHERE o.order_id IS NULL;   -- 用主键判断，不用 product_id
```

### ✅ 本关已掌握的硬核知识点

1. **JOIN 心法：谁全保留？** users LEFT JOIN orders → 8 行；orders LEFT JOIN users → 12 行（左表行数）
2. **三表 JOIN**：`FROM orders o JOIN users u ON ... JOIN products p ON ...` 一步步拼
3. **LEFT JOIN + IS NULL** = 查"从没出现过"（面试必考）
4. **LEFT JOIN + GROUP BY + IFNULL(SUM(),0)** = "每个都要显示，没数据的补 0"（三件套）
5. **判断 NULL 用主键**（order_id 永不 NULL），普通字段可能被脏数据骗
6. **字符串用单引号** 'iPhone 15'（双引号在某些 SQL 模式下是列名，会报错）
7. **GROUP BY 用主键**（同名商品不会错误合并）
8. **SQL 模板**：`SELECT 字段, 聚合函数 FROM 表 JOIN 表 ON 条件 GROUP BY 非聚合字段`

## SQL 面试模拟第 1 题 — 四种 JOIN 区别（2026-08-18，⭐⭐）

**我的回答**：记录左表的数据，右表作为外键补充左表。

**纠错**：

1. **"右表作为外键补充左表"** — 概念偏差。JOIN 靠 `ON` 条件把两行匹配起来，不是"外键补充"。外键是**建表时**的约束，JOIN 是**查询时**的拼接。而且匹配不上不是"不补"，是**补 NULL**。
2. **只说了 LEFT JOIN 的一半** — INNER / RIGHT / FULL 全漏了，面试官会追问。
3. **8 vs 12 行没答**：LEFT JOIN 的行数 = **左表行数**。users(8) LEFT JOIN orders → 8 行（每个用户都保留，没订单的用户订单字段为 NULL）；orders(12) LEFT JOIN users → 12 行（每条订单都保留）。

**正确理解（四种 JOIN 一图流）**：

| JOIN | 保留谁 | 匹配不上时 |
|------|--------|-----------|
| INNER | 两表都有（交集） | 直接不出现 |
| LEFT | 左表全保留 | 右表位置填 NULL |
| RIGHT | 右表全保留 | 左表位置填 NULL |
| FULL | 两表全保留 | 另一侧填 NULL |

- MySQL 没有 FULL JOIN，用 `LEFT JOIN ... UNION RIGHT JOIN ...` 模拟
- **口诀：INNER 只留交集，LEFT 保左补 NULL，RIGHT 保右补 NULL，FULL 全都要**
- 判断用哪个：问"谁要全保留"——"每个用户都要显示" → LEFT JOIN users

### 待完成（下次继续）

- [x] 面试模拟题 1：四种 JOIN（2026-08-18 已作答+纠错）
- [x] 面试模拟题 2：WHERE vs HAVING（2026-08-18 已作答+纠错）
- [x] 面试模拟题 3：COUNT 三兄弟（2026-08-18 已作答+纠错）
- [x] 面试模拟题 4：IS NULL 用主键（2026-08-18 已作答+纠错）
- [x] 面试模拟题 5：慢查询优化（2026-08-18 已作答+纠错）
- [x] 第四关：子查询 + NULL 处理（18-20 题完成，21 题待补）
- [x] 第五关：测试视角综合题（22-25 题完成，2026-08-18）

---

## SQL 面试模拟第 2 题 — WHERE vs HAVING（2026-08-18，⭐⭐）

**我的回答**：where 分组前进行，不能和聚合函数一起使用，having 分组后使用

**纠错**：

1. **方向正确，但不够完整**：只说了执行时机，没说作用对象和具体例子
2. **漏了面试官问的重点**："什么情况下只能用 HAVING？"
3. **没举具体例子**：面试官要听到 SQL 语句

**正确理解**：

| 对比 | WHERE | HAVING |
|------|-------|--------|
| 执行时机 | GROUP BY 之前 | GROUP BY 之后 |
| 作用对象 | 筛选**行** | 筛选**组** |
| 聚合函数 | ❌ 不能使用 | ✅ 可以使用 |

**什么情况下只能用 HAVING？**
> 当筛选条件涉及聚合函数时，比如"订单数超过 3 的用户"

```sql
-- ❌ 错误：WHERE 不能用聚合函数
SELECT user_id, COUNT(*) as cnt
FROM orders
WHERE COUNT(*) > 3  -- 报错！
GROUP BY user_id;

-- ✅ 正确：用 HAVING
SELECT user_id, COUNT(*) as cnt
FROM orders
GROUP BY user_id
HAVING COUNT(*) > 3;  -- 正确！
```

**WHERE 和 HAVING 可以同时使用**：
```sql
-- 先用 WHERE 筛选行，再用 HAVING 筛选组
SELECT u.username, COUNT(o.order_id) as cnt
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE u.city = '北京'  -- 先筛选北京市用户
GROUP BY u.user_id, u.username
HAVING COUNT(o.order_id) > 3;  -- 再筛选订单数 > 3 的
```

**面试答题模板**：
> "WHERE 和 HAVING 都是筛选条件，但有三个核心区别：
> 1. 执行时机：WHERE 在 GROUP BY 之前，HAVING 在之后
> 2. 作用对象：WHERE 筛选行，HAVING 筛选组
> 3. 聚合函数：WHERE 不能用，HAVING 可以
>
> 当筛选条件涉及聚合函数时，比如'订单数超过 3 的用户'，必须用 HAVING。"

---

## SQL 面试模拟第 3 题 — COUNT 三兄弟（2026-08-18，⭐⭐⭐）

**我的回答**：count（列名）效率最高

**纠错**：

1. **方向完全错误**：`COUNT(列名)` 效率最低，不是最高
2. **效率排序**：`COUNT(1)` ≈ `COUNT(*)` > `COUNT(列名)`

**正确理解**：

| 写法 | 统计内容 | NULL 值 | 效率 |
|------|---------|---------|------|
| `COUNT(*)` | 所有行数 | ✅ 包含 | ⭐⭐⭐ 最高 |
| `COUNT(1)` | 所有行数 | ✅ 包含 | ⭐⭐⭐ 最高 |
| `COUNT(列名)` | 该列非 NULL 的行数 | ❌ 排除 | ⭐ 较低 |

**为什么 COUNT(列名) 效率低？**
> 需要读取该列数据，判断每个值是否为 NULL，NULL 不计入。多了一步判断。

**例子**：
```sql
-- users 表：张三(age=25), 李四(age=NULL), 王五(age=30)
SELECT COUNT(*) FROM users;        -- 3（所有行）
SELECT COUNT(1) FROM users;        -- 3（所有行）
SELECT COUNT(age) FROM users;      -- 2（排除 NULL）
```

**面试答题模板**：
> "COUNT(*) 和 COUNT(1) 效率最高，统计所有行数（包含 NULL）；COUNT(列名) 效率较低，只统计非 NULL 的行数。一般用 COUNT(*) 统计总行数，用 COUNT(列名) 统计某个字段的非 NULL 数量。"

---

## SQL 面试模拟第 4 题 — IS NULL 用主键（2026-08-18，⭐⭐）

**我的回答**：主键要非空

**纠错**：

1. **方向正确，但不够完整**：只说了主键非空，没说为什么用主键更可靠
2. **漏了具体例子**：面试官要听到 SQL 语句
3. **漏了经典坑**：为什么不能用 `= NULL`

**正确理解**：

**为什么用主键判断更可靠？**
> 主键有 `NOT NULL` 约束，永远不会是 NULL。普通字段可能有脏数据（NULL）。

**例子：找出从没被下单过的商品**
```sql
-- ✅ 推荐：用主键判断
SELECT p.product_name
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
WHERE o.product_id IS NULL;  -- 用主键判断

-- ❌ 不推荐：用普通字段判断
SELECT p.product_name
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
WHERE o.product_name IS NULL;  -- 可能有歧义
```

**为什么不能用 `= NULL`？**
```sql
-- ❌ 错误：NULL 不能用 = 判断
SELECT * FROM products WHERE product_id = NULL;  -- 不会返回任何结果

-- ✅ 正确：必须用 IS NULL
SELECT * FROM products WHERE product_id IS NULL;  -- 正确
```

**原因**：NULL 表示"未知"，不是"空值"。任何与 NULL 的比较都是 `UNKNOWN`，不是 `TRUE`。

**面试答题模板**：
> "用主键判断更可靠，因为主键有 NOT NULL 约束，永远不会是 NULL。普通字段可能有脏数据，用普通字段判断可能产生歧义。另外，NULL 不能用 = 判断，必须用 IS NULL，因为 NULL 表示'未知'，不是'空值'。"

---

## SQL 面试模拟第 5 题 — 慢查询优化（2026-08-18，⭐⭐⭐）

**我的回答**：添加索引

**纠错**：

1. **方向正确但太简单**：只说了"添加索引"一个手段
2. **漏了完整排查流程**：发现 → 定位 → 优化
3. **漏了 EXPLAIN 分析**：这是面试官最想听到的关键步骤

**正确理解（三步排查法）**：

**① 发现慢查询**：
```sql
-- 开启慢查询日志
SET long_query_time = 1;  -- 阈值 1 秒
SHOW VARIABLES LIKE 'slow_query_log';
```

**② 定位慢在哪（EXPLAIN）**：
```sql
EXPLAIN SELECT * FROM orders WHERE user_id = 123;
-- 重点看：
-- type: const > ref > range > index > ALL（访问类型）
-- key: 是否走索引（NULL = 没走）
-- rows: 扫描行数（越大越慢）
-- Extra: Using filesort / Using temporary（需要优化）
```

**③ 优化手段（按优先级）**：

| 手段 | 说明 |
|------|------|
| 添加索引 | 给 WHERE 条件列建索引，多条件用联合索引 |
| SQL 改写 | 避免 SELECT *、深分页优化、子查询改 JOIN |
| 避免索引失效 | LIKE '%xxx'、函数操作列、隐式类型转换 |

**索引失效的常见情况**：
- `LIKE '%xxx'`（前导通配符）
- `WHERE DATE(create_time) = '2026-01-01'`（函数操作）
- `WHERE phone = 13800138000`（隐式类型转换）

**面试答题模板**：
> "我会按三步排查：① 开启慢查询日志发现慢 SQL；② 用 EXPLAIN 分析执行计划（看 type/key/rows/Extra）；③ 优化——最常见的是加索引，配合 SQL 改写、避免索引失效。优化后用 EXPLAIN 验证 rows 是否减少。"

---

## 第四关第 18 题 — 订单数超过平均数的用户（2026-08-18）

**我的思路**：先分组，计算每个用户的订单数再算平均数，用 having

**纠错**：

1. **方向正确**：分组 + HAVING 思路对
2. **关键坑**：MySQL 不允许聚合函数直接嵌套，`AVG(COUNT(*))` 会报错
3. **正确做法**：平均值用子查询先算出来

**正确写法**：
```sql
SELECT user_id, COUNT(*) AS order_count
FROM orders
GROUP BY user_id
HAVING COUNT(*) > (
    SELECT AVG(cnt)
    FROM (
        SELECT COUNT(*) AS cnt
        FROM orders
        GROUP BY user_id
    ) t
);
```

**关键知识点**：

| 写法 | 是否允许 |
|------|---------|
| `AVG(COUNT(*))` | ❌ 报错 |
| 子查询先算，外层再聚合 | ✅ 正确 |

**追问**：空表时 AVG 返回 NULL，比较结果都是 NULL → 用 IFNULL 兜底：
```sql
HAVING COUNT(*) > IFNULL((SELECT AVG(cnt) FROM ...), 0);
```

---

## 第四关第 19 题 — 消费总额超过 zhangsan 的用户（2026-08-18）

**正确写法**：
```sql
SELECT u.username, SUM(o.amount) AS total_spent
FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'completed'   -- 只算已支付订单
GROUP BY u.user_id, u.username
HAVING SUM(o.amount) > (
    SELECT SUM(amount)
    FROM orders
    WHERE user_id = (SELECT user_id FROM users WHERE username = 'zhangsan')
      AND status = 'completed'
);
```

**关键坑：cancelled 订单算不算？**

> 消费总额要**排除已取消的订单**，只统计 `completed` 的。因为 cancelled 的钱没有真正支付，算进去数据失真。

```sql
-- ❌ 不排除：金额虚高
SELECT u.username, SUM(o.amount) FROM users u
JOIN orders o ON u.user_id = o.user_id
GROUP BY u.username;

-- ✅ 排除 cancelled：只算真实消费
SELECT u.username, SUM(o.amount) FROM users u
JOIN orders o ON u.user_id = o.user_id
WHERE o.status = 'completed'
GROUP BY u.username;
```

**面试话术**：
> "消费总额我会排除已取消的订单，只统计 completed 的。因为 cancelled 的钱没有真正支付，算进去会让数据失真。这也是测试视角——验证金额统计时要注意状态过滤。"

---

## 第四关第 20 题 — age 为 NULL 显示为"未知"（2026-08-18）

**两种写法**：
```sql
-- 写法 1：IFNULL（MySQL 专用）
SELECT username, IFNULL(age, '未知') AS age FROM users;

-- 写法 2：COALESCE（标准 SQL，通用）
SELECT username, COALESCE(age, '未知') AS age FROM users;
```

**关键坑：类型问题！**
> age 是 INT 类型，'未知' 是字符串，直接替换会报错或显示异常。要先转字符串：

```sql
-- ✅ 先 CAST 转字符串
SELECT username, IFNULL(CAST(age AS CHAR), '未知') AS age FROM users;
```

**IFNULL vs COALESCE**：

| 对比 | IFNULL | COALESCE |
|------|--------|----------|
| 参数个数 | 2 个 | 多个（2+） |
| 适用数据库 | MySQL 专用 | 标准 SQL，通用 |

**测试视角的坑**：
> "NULL 在页面上直接显示会变成空或 'null'，用户体验差。而且统计时 NULL 和 0 被区别对待——COUNT(列名) 不算 NULL，SUM 会忽略 NULL。所以测试时要专门验证 NULL 字段的显示和统计。"

---

## 第五关：测试视角综合题（2026-08-18）

### 第 22 题：数据完整性 — status 脏数据检查

```sql
-- ① 查看有哪些不同的 status 值
SELECT DISTINCT status FROM orders;

-- ② 找出不在合法范围内的脏数据
SELECT * FROM orders
WHERE status NOT IN ('pending', 'completed', 'cancelled');

-- ③ 更严谨：检查大小写/空格/隐藏字符
SELECT DISTINCT status, LENGTH(status) AS len FROM orders;
```

**测试视角**：
> "如果 status 出现 'Completed'（大小写）、'pending '（空格）或 'PAID'（不在枚举里），说明数据校验不严，可能是上游系统没控制枚举值，或者数据库没加 CHECK 约束。"

### 第 23 题：超卖风险（P0 案例）⭐

```sql
SELECT 
    p.product_name,
    p.stock,
    IFNULL(SUM(o.quantity), 0) AS sold_total
FROM products p
LEFT JOIN orders o ON p.product_id = o.product_id
WHERE o.status = 'completed'  -- 只算真正卖出的
GROUP BY p.product_id, p.product_name, p.stock
HAVING sold_total > p.stock;  -- 销量 > 库存 = 超卖
```

**面试案例素材**：
> "超卖是电商的 P0 级 Bug。我在测试中会专门用 SQL 找出销量超过库存的商品。这能发现两类问题：① 系统 Bug（并发下单库存扣减错误）；② 数据问题（库存维护错误）。超卖直接导致用户付了钱拿不到货，会造成财务损失和信任危机。"

### 第 24 题：优惠统计

```sql
-- 总优惠金额 = Σ(原价×数量 − 成交金额)
SELECT SUM(p.price * o.quantity - o.amount) AS total_discount
FROM orders o
JOIN products p ON o.product_id = p.product_id;
```

**测试视角**：
> "优惠金额是财务测试重点：① 优惠金额 ≥ 0（不能出现负优惠）；② 总优惠 = 各订单优惠之和；③ 与报表/前端显示一致。出现负优惠说明价格计算有 Bug，Severity 直接判高。"

### 第 25 题：VIP 分析

```sql
SELECT 
    SUM(CASE WHEN u.vip_level >= 2 THEN o.amount ELSE 0 END) AS vip_total,
    SUM(o.amount) AS all_total,
    ROUND(SUM(CASE WHEN u.vip_level >= 2 THEN o.amount ELSE 0 END) / SUM(o.amount) * 100, 2) AS vip_percent
FROM orders o
JOIN users u ON o.user_id = u.user_id
WHERE o.status = 'completed';
```

**测试视角**：
> "VIP 分析测试验证：① 统计口径（vip_level ≥ 2 的边界）；② 状态过滤（cancelled 不算）；③ 金额精度（百分比保留几位小数）；④ 数据一致性（VIP + 非 VIP = 全站）。"
