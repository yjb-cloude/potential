# Day 2: 函数 + 流程控制

# ===== 函数基础 =====

# 1. 无参数函数
def say_hello():
    print("Hello!")

say_hello()

# 2. 有参数函数
def greet(name):
    print(f"你好，{name}！")

greet("张三")
greet("李四")

# 3. 有返回值函数
def add(a, b):
    return a + b

result = add(3, 5)
print(f"3 + 5 = {result}")

# 4. 默认参数
def greet_formal(name, greeting="你好"):
    print(f"{greeting}，{name}！")

greet_formal("张三")           # 你好，张三！
greet_formal("张三", "早上好")  # 早上好，张三！

# ===== 流程控制 =====

# 5. if-else 判断
age = 18

if age >= 18:
    print(f"年龄{age}，成年了")
elif age >= 12:
    print(f"年龄{age}，青少年")
else:
    print(f"年龄{age}，儿童")

# 6. for 循环
print("\n===== 水果列表 =====")
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"我喜欢吃{fruit}")

# 7. while 循环
print("\n===== 倒计时 =====")
count = 3
while count > 0:
    print(count)
    count -= 1
print("发射！")

# ===== 综合练习 =====

# 8. 判断是否成年（函数 + if）
def check_adult(name, age):
    if age >= 18:
        print(f"{name}，你成年了！")
    else:
        print(f"{name}，你还未成年。")

check_adult("张三", 20)
check_adult("小明", 15)

# 9. 计算列表平均值（函数 + for）
def average(numbers):
    total = 0
    for num in numbers:
        total += num
    return total / len(numbers)

scores = [85, 92, 78, 90, 88]
avg = average(scores)
print(f"\n平均分: {avg:.2f}")
