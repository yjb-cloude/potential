# 题目 1：基础类与对象
# 创建一个 Student 类，包含：

# 属性：name（姓名）、age（年龄）
# 方法：introduce()，输出"我叫XXX，今年XX岁"
# 然后创建两个对象并调用方法。
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def introduce(self):
       print(f"我叫{self.name},今年{self.age}岁")

s1 = Student("小王", 18)
s2 = Student("小李", 20)

s1.introduce()
s2.introduce()

# 题目 2：init 参数
# 创建一个 Car 类，包含：

# 属性：brand（品牌）、year（年份）
# 方法：info()，输出"这是一辆2020年的丰田"
# 要求：创建对象时必须传品牌和年份参数。
class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

    def info(self):
        print(f"这是一辆{self.year}年的{self.brand}")

c1 = Car("丰田", 2020)
c1.info()
    


# 题目 3：继承
# 创建父类 Animal 和子类 Cat：

# Animal 有 eat() 方法，输出"吃东西"
# Cat 继承 Animal，添加 meow() 方法，输出"喵喵喵"
# Cat 重写 eat() 方法，输出"吃鱼"

class Animal:
      def eat(self):
        print("吃东西")

class Cat(Animal):
  
    def meow(self):
        print(f"{self.name}在喵喵叫")

    def eat(self):
        print(f"{self.name}在吃鱼")


class Animal:
    def __init__(self, name):
        self.name = name
    def eat(self):
        print("吃东西")

class Cat(Animal):
      def meow(self):
        print(f"{self.name}在喵喵叫")

      def eat(self):
        print(f"{self.name}在吃鱼")

def animal_action(animal):
    animal.eat()
   

dog = Animal("小狗")
cat = Cat("小猫")
animal_action(dog)
animal_action(cat)


import requests

HEADERS = {
    "Content-Type": "application/json",
    "blade-auth":"bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJpc3N1c2VyIiwiYXVkIjoiYXVkaWVuY2UiLCJ0ZW5hbnRfaWQiOiIxOTgzMDY4NDYyMzExNzIzMDEwIiwicm9sZV9uYW1lIjoiIiwidGVuYW50X25hbWUiOiIiLCJ1c2VyX2lkIjoiMjA1ODgxNDMwNDQ4MzE5NjkyOSIsInJvbGVfaWQiOiIxNjMxMTMyMDY1NDI2NjY5NTY5IiwidXNlcl9uYW1lIjoieWFuZ2ppbmdiaWFvIiwidG9rZW5fdHlwZSI6ImFjY2Vzc190b2tlbiIsImRlcHRfaWQiOiIxNjYxNTUzNjc2MzczODU2MjU2IiwidXNlcm5hbWUiOiJ5YW5namluZ2JpYW8iLCJjbGllbnRfaWQiOiJuenkiLCJleHAiOjE3ODkwNjk2MDksIm5iZiI6MTc4OTAyNjQwOX0.Pes-3Nrvx0oZMRWic6Dab6VBK6kxlxHNI5qzH_W_07_JbNyen6lGNE08h99fyb6ptb8rph0qY9XPxYw9qhmDJA"


}
data = {
    "tenantId": "1983068462311723010",
    "username": "yangjingbiao",
    "password": "123456",
    "captcha": "true",
    "grantType": "captcha"
}


# 访问百度
response = requests.post("http://192.168.9.55:5666/api/mes-auth/token", json=data, headers=HEADERS)

print(f"状态码: {response.status_code}")
if response.status_code == 200:
    print(f"响应: {response.json()}")
else:
    print("接口请求失败")
    print(response.text)

#列表增删改
fruits = ["apple", "banana", "cherry", "date", "elderberry"]
list1 = [1,2,3]
list2 = [4,5,6]

a = list1 + list2
print(a)
print(len(a))

for i in range(len(fruits)):
    print(f"索引 {i}: {fruits[i]}")

#增
fruits.append("fig")
print(fruits)

fruits.insert(2, "grape")
print(fruits)

#删
fruits.remove("banana")
print(fruits)

fruits.pop(3)
print(fruits)

del fruits[0]
print(fruits)

#改
fruits[1] = "orange"
print(fruits)


import json

data = '''
{
  "code": 200,
  "data": {
    "records": [
      {"id": 1, "planCode": "P001", "status": 0},
      {"id": 2, "planCode": "P002", "status": 1},
      {"id": 3, "planCode": "P003", "status": 2}
    ]
  }
}
'''

# 解析 JSON 字符串
result = json.loads(data)
records = result["data"]["records"]
print(len(records))


import json

data = '''
{
  "code": 200,
  "data": {
    "records": [
      {"id": 1, "planCode": "P001", "status": 0},
      {"id": 2, "planCode": "P002", "status": 1},
      {"id": 3, "planCode": "P003", "status": 2},
      {"id": 4, "planCode": "P004", "status": 1}
    ]
  }
}
'''

# 提示：
# - json.loads(data) 解析
# - for item in records: 遍历
# - if item["status"] == 1: 判断
# - print(item["planCode"]) 打印


result = json.loads(data)
records = result["data"]["records"]
for record in records:
      if(record["status"] == 1):
           print(record["planCode"])