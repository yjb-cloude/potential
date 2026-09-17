# Day 1: Hello World + 变量 + 数据类型

# 1. Hello World（Python 只需要一行）
print("Hello, World!")
print("你好，我开始学 Python 了！")

# 2. 变量（不需要声明类型，直接赋值）
name = "张三"        # 字符串
age = 25             # 整数
score = 95.5         # 浮点数
is_student = True    # 布尔值

# 3. 打印变量
print("姓名:", name)
print("年龄:", age)
print("分数:", score)
print("是学生吗:", is_student)

# 4. 查看变量类型（type() 函数）
print("name 的类型:", type(name))
print("age 的类型:", type(age))
print("score 的类型:", type(score))
print("is_student 的类型:", type(is_student))

# 5. f-string 格式化（推荐的输出方式）
print(f"我叫{name}，今年{age}岁，成绩{score}分")

# 6. 列表（List）
fruits = ["苹果", "香蕉", "橙子"]
print("水果列表:", fruits)
print("第一个水果:", fruits[0])  # 索引从 0 开始

# 7. 字典（Dict）
person = {"name": "李四", "age": 30, "city": "北京"}
print("字典:", person)
print("名字:", person["name"])  # 用 key 取值

# 8. 简单运算
a = 10
b = 3
print(f"{a} + {b} = {a + b}")
print(f"{a} × {b} = {a * b}")
print(f"{a} ÷ {b} = {a / b:.2f}")  # 保留 2 位小数
