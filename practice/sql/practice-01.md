# SQL 练习 01 —— 电商订单系统（基础 → 综合）

> 配套库：`sql_practice`（由 `init.sql` 初始化，三张表：users / products / orders）
> 连接命令：`mysql --default-character-set=utf8mb4 -uroot -proot sql_practice`
> ⚠️ Windows 下必须加 `--default-character-set=utf8mb4`，否则中文会乱码报错
>
> 约定：自己先写，写不出来看提示；不会的题标 ⭐ 进错题本。

## 表结构速览

| 表 | 关键字段 | 数据中的"坑" |
|----|---------|-------------|
| users | user_id, username, city, age, vip_level | `zhouba` 的 age 是 **NULL** |
| products | product_id, product_name, category, price, stock | Kindle 的 stock = **0**（缺货） |
| orders | order_id, user_id, product_id, quantity, amount, status, order_date | amount ≠ price×quantity（**有优惠**）；status 有 pending/completed/cancelled |

---

## 第一关：基础查询（热身）

1. 查询所有用户，按年龄从小到大排序
   - ⭐ 思考：`zhouba` 的 NULL 年龄会排在最前还是最后？
2. 查询北京和上海的用户（分别用 `IN` 和 `OR` 写一遍）
3. 查询价格在 1000~5000 之间的商品（`BETWEEN`）
4. 查询用户名以 `zh` 开头的用户（`LIKE`）
5. 查询最新注册的 3 个用户（`ORDER BY` + `LIMIT`）
6. 查询所有订单，按金额从高到低排序；金额相同的话，最新下单的排前面

## 第二关：聚合统计（面试高频）

7. 每个城市有多少用户？按人数从多到少
8. 每个分类的商品：数量、平均价格、最高价格（按平均价格降序）
9. 每个用户的订单数和总金额
   - ⭐ 思考：cancelled（已取消）的订单金额该不该算进去？面试官就爱问这个
10. 只算已支付（completed）的订单，找出消费最高的前 3 个用户
11. 哪个商品累计卖出最多？卖出多少件？（`SUM(quantity)`）
12. 找出"有优惠"的订单：成交金额 < 原价×数量（订单表 amount vs 商品表 price）

## 第三关：JOIN 多表（核心重点）

13. 查询每笔订单详情：订单号、用户名、商品名、数量、金额、状态、下单时间
14. 每个用户买过哪些商品（`DISTINCT`，用户名 → 商品名列表）
15. 找出**从没被下单过**的商品（`LEFT JOIN` + `IS NULL`）
    - ⭐ 提示：这题是 left join 的经典考点，kindle 缺货+没卖出去，应该出现在结果里
16. 查询买过 iPhone 15 的用户名单（三表 join 或 join + 子查询）
17. 每个商品被下单的总数量，**没卖出去的商品也要显示 0**（`LEFT JOIN` + `IFNULL`）

## 第四关：子查询 + NULL 处理（加分）

18. 查询订单数超过"平均订单数"的用户
19. 查询消费总额超过 zhangsan 的用户
20. 把 age 为 NULL 的用户年龄显示为"未知"（`IFNULL` / `COALESCE`）
21. 查询从未下过 completed 订单的用户（`NOT IN` 或 `NOT EXISTS` 两种写法对比）

## 第五关：测试视角综合题（模拟面试）

22. **数据完整性**：orders 表里 status 一共有哪些值？有没有不在规定范围里的"脏数据"？
23. **超卖风险**：找出"累计销量 > 库存"的商品 —— 这在电商里是重大 bug（P0）
24. **优惠统计**：所有订单的总优惠金额 = Σ(原价×数量 − 成交金额) 是多少？
25. **VIP 分析**：vip_level ≥ 2 的用户消费总额是多少？占全站消费的比例？（`SUM + 子查询`）

---

## 通关标准

- 第一关：全对 → 热身上路
- 第二关：独立完成 7、9、10 → 聚合 OK
- 第三关：独立完成 13、15 → JOIN 过关（测试岗必考）
- 第四关：15 分钟内写出 18、20 → 加分
- 第五关：22、23 能当面试案例讲 → 毕业
