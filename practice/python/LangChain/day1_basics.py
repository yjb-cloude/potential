"""
Day1: LangChain 基础 — 连接本地 DeepSeek、Prompt 模板、Chain 链
================================================================
学习目标：
1. 用 LangChain 连接本地 Ollama（替代 Day9 的 requests）
2. 使用 PromptTemplate 构建提示词
3. 用 LCEL 语法构建 Chain（管道）
4. 对比 Day9 的写法，理解 LangChain 的价值

前置条件：
- Ollama 已安装，deepseek-r1:1.5b 已下载
- pip install langchain langchain-community langchain-core

运行方式：python day1_basics.py
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import time


# ============================================================
# TODO 1: 用 LangChain 连接本地 DeepSeek
# ============================================================
def todo1_basic_chat():
    """
    目标：
    - 用 ChatOllama 连接本地 DeepSeek
    - 发送一个问题，获取回答
    - 对比 Day9 的 requests 写法

    知识点：
    - ChatOllama: LangChain 的 Ollama 封装
    - .invoke(): 发送请求（替代 requests.post）
    - .content: 获取回答文本

    对比 Day9：
    Day9 你写了 20 行代码（requests + URL + payload + 异常处理）
    LangChain 只需要 3 行！
    """
    print("=== TODO 1: LangChain 连接 DeepSeek ===\n")

    # 创建 ChatOllama 实例
    llm = ChatOllama(model="deepseek-r1:1.5b")

    # 调用模型
    response = llm.invoke("用一句话解释什么是软件测试")

    # 打印回答
    print("回答:", response.content)

    # 对比 Day9 的写法：
    # Day9: url = "http://localhost:11434/api/generate"
    #       payload = {"model": ..., "prompt": ..., "stream": False}
    #       resp = requests.post(url, json=payload, timeout=60)
    #       data = resp.json()
    #       answer = data.get("response", "")
    #
    # LangChain: llm = ChatOllama(model="deepseek-r1:1.5b")
    #            response = llm.invoke("问题")
    #            answer = response.content


# ============================================================
# TODO 2: PromptTemplate — 提示词模板
# ============================================================
def todo2_prompt_template():
    """
    目标：
    - 创建一个 PromptTemplate
    - 用变量填充模板
    - 理解为什么需要模板（复用、参数化）

    知识点：
    - ChatPromptTemplate: 聊天提示词模板
    - from_template(): 从字符串创建模板
    - {变量名}: 模板中的占位符
    """
    #创建模板
    template = ChatPromptTemplate.from_template("你是一个{role}，请用一句话解释{topic}")

    #填充变量
    prompt = template.invoke({"role": "测试专家", "topic": "什么是单元测试"})

    # 打印模板
    print("模板:", template)

    # 打印填充后的模板
    print("提示词:", prompt)

    #使用llm
     #实例化llm
    llm = ChatOllama(model="deepseek-r1:1.5b")
    response = llm.invoke(prompt)
    time.sleep(1)
    print("回答:", response.content)


# ============================================================
# TODO 3: LCEL Chain — 管道语法（核心！）
# ============================================================
def todo3_lcel_chain():
    """
    目标：
    - 用 LCEL 语法构建一个 Chain
    - 理解 | 管道操作符
    - prompt | llm | output_parser 的含义

    知识点：
    - LCEL (LangChain Expression Language)
    - | 管道符：数据从左往右流
    - StrOutputParser(): 提取纯文本（去掉多余格式）

    流程：
    输入 → PromptTemplate → LLM → StrOutputParser → 输出
    """
    # 创建模板
    template = ChatPromptTemplate.from_template("你是一个{role}，请用一句话解释{topic}")

    # 创建 LLM
    llm = ChatOllama(model="deepseek-r1:1.5b")

    # 创建输出解析器
    parser = StrOutputParser()

    # 用 | 构建 Chain（这就是 LCEL！）
    chain = template | llm | parser

    #调用invoke并打印结果
    print("结果:", chain.invoke({"role": "测试专家", "topic": "什么是集成测试"}))
    # 理解这个链：
    # 1. prompt.invoke({"role": ..., "topic": ...}) → 生成完整提示词
    # 2. llm.invoke(提示词) → 调用模型
    # 3. parser.invoke(response) → 提取纯文本
    #
    # 用 | 连起来就是：prompt | llm | parser
    # 数据自动从左流到右！


# ============================================================
# TODO 4: 带系统提示的 Chain
# ============================================================
def todo4_system_prompt():
    """
    目标：
    - 使用 system + human 双角色提示
    - 控制 AI 的行为风格

    知识点：
    - ("system", "...") → 系统提示，定义 AI 角色
    - ("human", "...") → 用户提示，实际问题
    """
    # 创建模板(多角色提示：系统 + 用户)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个资深软件测试工程师，请用一句话解释："),
        ("human", "{question}")
    ])

    #创建LLM
    llm = ChatOllama(model="deepseek-r1:1.5b")
    
    # 创建 Chain
    chain = prompt | llm | StrOutputParser()

    # 调用 Chain并打印
    print("结果:", chain.invoke({"question": "什么是单元测试？"}))


    print("\n=== TODO 4: 系统提示 ===\n")


# ============================================================
# TODO 5: 批量调用 — 一次处理多个问题
# ============================================================
def todo5_batch():
    """
    目标：
    - 用 .batch() 一次处理多个问题
    - 对比逐个调用的效率

    知识点：
    - chain.batch([输入1, 输入2, ...]) → 批量处理
    - 比循环 invoke 更高效
    """
    print("\n=== TODO 5: 批量调用 ===\n")

    prompt = ChatPromptTemplate.from_template(
        "用一句话解释：{concept}"
    )

    llm = ChatOllama(model="deepseek-r1:1.5b")

    chain = prompt | llm | StrOutputParser()

    questions = [
        {"concept": "单元测试"},
        {"concept": "集成测试"},
        {"concept": "性能测试"},
        {"concept": "安全测试"},
    ]
    results = chain.batch(questions)
    for q, r in zip(questions, results):
        print(f"{q['concept']}: {r}")


# ============================================================
# TODO 6: 综合练习 — 构建一个测试知识问答 Chain
# ============================================================
def todo6_test_qa_chain():
    """
    目标：构建一个测试知识问答 Chain

    要求：
    1. 系统提示：你是资深测试工程师
    2. 输入：{question}
    3. 输出：简洁回答（不超过100字）
    4. 批量回答以下问题：
       - 什么是黑盒测试？
       - 什么是白盒测试？
       - 测试用例包括哪些要素？
       - Bug 报告包括哪些要素？
    """
    print("\n=== TODO 6: 综合练习 ===\n")

    # TODO: 自己写完整实现
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是资深软件测试工程师，请用不超过100字回答问题："),
        ("human", "{question}")
    ]) 

    llm = ChatOllama(model="deepseek-r1:1.5b")

    chain = prompt | llm | StrOutputParser()

    questions = [
        {"question": "什么是黑盒测试？"},
        {"question": "什么是白盒测试？"},
        {"question": "测试用例包括哪些要素？"},
        {"question": "Bug 报告包括哪些要素？"},
    ]
    results = chain.batch(questions)
    for q, r in zip(questions, results):
        print(f"{q['question']}: {r}")
   


# ============================================================
# 主程序入口
# ============================================================
if __name__ == "__main__":
    print("LangChain Day1 练习")
    print("=" * 50)
    print("前置条件：Ollama + deepseek-r1:1.5b 已运行")
    print("逐步取消注释 TODO 中的代码来学习")
    print("=" * 50)

    # 逐个测试（取消注释你想运行的函数）
    todo1_basic_chat()
    # todo2_prompt_template()
    # todo3_lcel_chain()
    # todo4_system_prompt()
    # todo5_batch()
    todo6_test_qa_chain()
