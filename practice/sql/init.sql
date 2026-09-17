-- ============================================
-- SQL 练习初始化脚本 —— 电商订单系统
-- 场景:测试岗位最常见的表结构(用户/订单/商品)
-- 用法: mysql -uroot -proot < init.sql
-- ============================================

DROP DATABASE IF EXISTS sql_practice;
CREATE DATABASE sql_practice DEFAULT CHARACTER SET utf8mb4;
USE sql_practice;

-- ---------- 1. 用户表 ----------
CREATE TABLE users (
    user_id   INT PRIMARY KEY AUTO_INCREMENT,
    username  VARCHAR(50) NOT NULL,
    phone     VARCHAR(20),
    age       INT,
    city      VARCHAR(50),
    reg_date  DATE,
    vip_level INT DEFAULT 0              -- 0=普通 1=银卡 2=金卡 3=钻石
);

INSERT INTO users (username, phone, age, city, reg_date, vip_level) VALUES
('zhangsan', '13800000001', 25, '北京', '2024-01-15', 2),
('lisi',     '13800000002', 30, '上海', '2024-02-20', 1),
('wangwu',   '13800000003', 22, '广州', '2024-03-05', 0),
('zhaoliu',  '13800000004', 35, '深圳', '2024-03-18', 3),
('sunqi',    '13800000005', 28, '北京', '2024-05-01', 1),
('zhouba',   '13800000006', NULL, '上海', '2024-06-10', 0),
('wujiu',    '13800000007', 40, '成都', '2024-07-22', 2),
('zhengshi', '13800000008', 26, '杭州', '2024-08-08', 0);

-- ---------- 2. 商品表 ----------
CREATE TABLE products (
    product_id   INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category     VARCHAR(50),
    price        DECIMAL(10,2),
    stock        INT
);

INSERT INTO products (product_name, category, price, stock) VALUES
('iPhone 15',      '手机',   5999.00, 100),
('华为 Mate60',    '手机',   4999.00,  80),
('MacBook Air',    '电脑',   7999.00,  50),
('联想小新',       '电脑',   4299.00, 120),
('AirPods Pro',    '耳机',   1899.00, 200),
('机械键盘',       '外设',    399.00, 500),
('显示器 27寸',    '外设',   1299.00, 150),
('Kindle',         '阅读器',  998.00,   0);   -- 注意:缺货商品

-- ---------- 3. 订单表 ----------
CREATE TABLE orders (
    order_id   INT PRIMARY KEY AUTO_INCREMENT,
    user_id    INT NOT NULL,
    product_id INT NOT NULL,
    quantity   INT,
    amount     DECIMAL(10,2),              -- 成交金额(可能有优惠,不=单价*数量)
    status     VARCHAR(20),                -- pending/completed/cancelled
    order_date DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO orders (user_id, product_id, quantity, amount, status, order_date) VALUES
(1, 1, 1, 5999.00, 'completed', '2024-08-01 10:23:00'),
(1, 5, 2, 3698.00, 'completed', '2024-08-05 14:02:00'),
(2, 3, 1, 7999.00, 'pending',   '2024-08-02 09:15:00'),
(3, 6, 3, 1197.00, 'completed', '2024-08-03 20:45:00'),
(3, 7, 1, 1299.00, 'cancelled', '2024-08-06 11:30:00'),
(4, 2, 2, 9598.00, 'completed', '2024-08-07 16:08:00'),
(5, 5, 1, 1899.00, 'pending',   '2024-08-08 08:59:00'),
(5, 4, 1, 4299.00, 'completed', '2024-08-09 12:12:00'),
(6, 1, 1, 5999.00, 'completed', '2024-08-10 19:40:00'),
(7, 3, 1, 7999.00, 'completed', '2024-08-10 21:33:00'),
(8, 6, 2,  798.00, 'pending',   '2024-08-11 07:26:00'),
(8, 2, 1, 4999.00, 'completed', '2024-08-11 09:50:00');

SELECT '数据库初始化完成,共创建 3 张表' AS 提示;
