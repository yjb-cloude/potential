# Python 知识体系

> Python 编程语言的核心知识，覆盖基础语法、常用库、与测试和 AI 领域的结合。

---

## 一、Python 基础

### 1.1 变量与数据类型

```python
# 变量定义（不需要声明类型）
name = "张三"        # 字符串
age = 25             # 整数
score = 95.5         # 浮点数
is_active = True     # 布尔值
courses = ["数学", "英语", "Python"]  # 列表
info = {"name": "张三", "age": 25}    # 字典
```

**数据类型对比**：

| 类型 | 示例 | 特点 |
|------|------|------|
| `str` | "hello" | 不可变，支持索引 |
| `list` | [1, 2, 3] | 可变，有序 |
| `tuple` | (1, 2, 3) | 不可变，有序 |
| `dict` | {"key": "value"} | 键值对，无序 |
| `set` | {1, 2, 3} | 无序，去重 |

### 1.2 流程控制

```python
# if-else
if age >= 18:
    print("成年")
elif age >= 12:
    print("青少年")
else:
    print("儿童")

# for 循环
for i in range(10):
    print(i)

# while 循环
count = 0
while count < 5:
    print(count)
    count += 1
```

### 1.3 函数

```python
# 定义函数
def greet(name, greeting="你好"):
    """打招呼函数"""
    return f"{greeting}, {name}!"

# 调用函数
print(greet("张三"))           # 输出: 你好, 张三!
print(greet("张三", "早上好")) # 输出: 早上好, 张三!

# 可变参数
def add(*args):
    return sum(args)
```

---

## 二、常用数据结构

### 2.1 列表（List）

```python
# 创建列表
fruits = ["苹果", "香蕉", "橙子"]

# 常用操作
fruits.append("葡萄")      # 添加
fruits.insert(1, "西瓜")   # 插入
fruits.remove("香蕉")      # 删除
fruits.pop()               # 弹出最后一个
fruits.sort()              # 排序
fruits.reverse()           # 反转
len(fruits)                # 长度
```

### 2.2 字典（Dict）

```python
# 创建字典
user = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

# 常用操作
user["email"] = "zhangsan@example.com"  # 添加
user.pop("age")                         # 删除
user.get("name", "未知")                # 获取（带默认值）
user.keys()                             # 所有键
user.values()                           # 所有值
```

### 2.3 列表推导式

```python
# 传统方式
squares = []
for x in range(10):
    squares.append(x ** 2)

# 列表推导式（一行搞定）
squares = [x ** 2 for x in range(10)]

# 带条件的推导式
evens = [x for x in range(10) if x % 2 == 0]
```

---

## 三、文件操作

### 3.1 读写文件

```python
# 读取文件
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 逐行读取
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

# 写入文件
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, Python!")
```

### 3.2 CSV 文件处理

```python
import csv

# 读取 CSV
with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)

# 写入 CSV
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["姓名", "年龄"])
    writer.writerow(["张三", 25])
```

---

## 四、面向对象编程（OOP）

### 4.1 类与对象

```python
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"我是{self.name}，今年{self.age}岁"

# 创建对象
student = Student("张三", 25)
print(student.greet())
```

### 4.2 继承

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "汪汪汪"

class Cat(Animal):
    def speak(self):
        return "喵喵喵"
```

---

## 五、异常处理

```python
# 基本语法
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零")
except Exception as e:
    print(f"发生错误: {e}")
finally:
    print("无论如何都会执行")

# 自定义异常
class ValueError(Exception):
    pass
```

---

## 六、常用库

### 6.1 requests（HTTP 请求）

```python
import requests

# GET 请求
response = requests.get("https://api.example.com/users")
print(response.json())

# POST 请求
data = {"name": "张三", "age": 25}
response = requests.post("https://api.example.com/users", json=data)
print(response.status_code)
```

### 6.2 pytest（测试框架）

```python
# test_example.py
def test_add():
    assert 1 + 1 == 2

def test_string():
    assert "hello".upper() == "HELLO"

# 运行: pytest test_example.py
```

### 6.3 selenium（Web 自动化）

```python
from selenium import webdriver

# 启动浏览器
driver = webdriver.Chrome()

# 打开网页
driver.get("https://www.baidu.com")

# 查找元素
search_box = driver.find_element("id", "kw")
search_box.send_keys("Python")
search_box.submit()

# 关闭浏览器
driver.quit()
```

### 6.4 pandas（数据处理）

```python
import pandas as pd

# 读取 Excel
df = pd.read_excel("data.xlsx")

# 筛选数据
result = df[df["age"] > 18]

# 保存为 CSV
result.to_csv("output.csv", index=False)
```

---

## 七、Python 在测试中的应用

### 7.1 接口自动化测试

```python
import requests

def test_login():
    url = "https://api.example.com/login"
    data = {"username": "admin", "password": "123456"}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert response.json()["code"] == 200
```

### 7.2 Web 自动化测试

```python
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_search():
    driver = webdriver.Chrome()
    driver.get("https://www.baidu.com")
    
    search_box = driver.find_element(By.ID, "kw")
    search_box.send_keys("Selenium")
    search_box.submit()
    
    assert "Selenium" in driver.title
    driver.quit()
```

---

## 八、与 [[Java开发知识体系]] 的对比

| 对比点 | Python | Java |
|--------|--------|------|
| 语法 | 简洁，动态类型 | 严格，静态类型 |
| 运行速度 | 较慢 | 快 |
| 学习曲线 | 平缓 | 较陡 |
| 测试框架 | pytest | JUnit/TestNG |
| 自动化 | Selenium Python | Selenium Java |
| AI/ML | 更流行 | 较少 |

---

## 九、学习路径建议

### 第 1 阶段：基础语法（1 周）
- 变量、数据类型、流程控制
- 函数、列表、字典
- 文件操作

### 第 2 阶段：面向对象（1 周）
- 类与对象
- 继承、多态
- 异常处理

### 第 3 阶段：常用库（2 周）
- requests（接口测试）
- pytest（测试框架）
- selenium（Web 自动化）

### 第 4 阶段：实战项目（2 周）
- 接口自动化测试项目
- Web 自动化测试项目

---

> **Python 是测试工程师的第二语言**，与 Java 互补。Java 用于企业级自动化框架，Python 用于快速脚本和 AI 领域。
