# Day 3: 文件操作 + 异常处理

# ===== 文件操作 =====

# 1. 写入文件
print("===== 写入文件 =====")
with open("data.txt", "w", encoding="utf-8") as f:
    f.write("张三,25,北京\n")
    f.write("李四,30,上海\n")
    f.write("王五,28,广州\n")
print("写入完成！")

# 2. 读取文件
print("\n===== 读取文件 =====")
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)

# 3. 逐行读取
print("\n===== 逐行读取 =====")
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(f"读到: {line.strip()}")

# 4. 读取后处理
print("\n===== 读取后处理 =====")
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        parts = line.strip().split(",")
        name, age, city = parts
        print(f"{name} 今年 {age} 岁，来自 {city}")

# ===== 异常处理 =====

# 5. 没有异常处理：程序崩溃
print("\n===== 没有异常处理 =====")
try:
    num = int("abc")
except ValueError:
    print("输入的不是数字！程序没有崩溃")

# 6. 捕获不同类型的异常
print("\n===== 捕获不同异常 =====")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("不能除以零！")
except ValueError:
    print("值错误！")
except Exception as e:
    print(f"其他错误: {e}")

# 7. finally（无论是否出错都执行）
print("\n===== finally =====")
try:
    f = open("data.txt", "r")
    content = f.read()
except FileNotFoundError:
    print("文件不存在！")
finally:
    print("无论如何都会执行这里")

# 8. 实战：安全读取文件
print("\n===== 实战：安全读取 =====")
def safe_read_file(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "文件不存在"
    except Exception as e:
        return f"读取失败: {e}"

result = safe_read_file("data.txt")
print(f"读取结果: {result}")

result2 = safe_read_file("不存在.txt")
print(f"读取结果: {result2}")
