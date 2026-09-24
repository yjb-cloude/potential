"""
Day2: RAG 实战 — 检索增强生成（Agent 的核心能力）
==================================================
学习目标：
1. 理解 RAG 流程：文档加载 → 分块 → 向量化 → 存储 → 检索 → 生成
2. 用 ChromaDB 做向量数据库
3. 构建一个"文档问答"系统

前置条件：
- pip install langchain langchain-community langchain-chroma sentence-transformers

运行方式：python day2_rag.py
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformerEmbeddings
from langchain_chroma import Chroma
import os


# ============================================================
# TODO 1: 文档加载与分块
# ============================================================
def todo1_load_and_split():
    """
    目标：
    - 加载一个文本文件
    - 将长文本分成小块（chunk）
    - 理解为什么需要分块

    知识点：
    - 大模型有 token 限制（上下文窗口）
    - 文档太长 → 装不下 → 需要分块
    - 分块后每块独立向量化，检索时找最相关的块

    分块参数：
    - chunk_size: 每块最大字符数（推荐 500-1000）
    - chunk_overlap: 块之间重叠的字符数（防止上下文断裂）
    """
    print("=== TODO 1: 文档加载与分块 ===\n")

    # 先创建一个测试文档
    test_doc = """软件测试是软件开发过程中不可或缺的一部分。它的目的是发现软件中的缺陷，确保软件质量。

单元测试是对软件中最小可测试单元进行检查和验证。在Java中，通常使用JUnit框架进行单元测试。单元测试应该覆盖正常流程、边界条件和异常情况。

集成测试是在单元测试的基础上，将所有模块按照设计要求组装成为子系统或系统，进行集成测试。集成测试主要检查模块之间的接口是否正确。

系统测试是将已经集成好的软件系统，作为整个基于计算机系统的一个元素，与计算机硬件、外设、某些支持软件、数据和人员等其他系统元素结合在一起，在实际运行环境下，对计算机系统进行一系列的测试。

验收测试是部署软件之前的最后一个测试操作。验收测试的目的是确保软件准备就绪，并且可以让最终用户将其用于执行软件的既定功能和任务。

回归测试是指修改了旧代码后，重新进行测试以确认修改没有引入新的错误或导致其他代码产生错误。回归测试是软件测试中非常重要的一环。

性能测试是通过自动化的测试工具模拟多种正常、峰值以及异常负载条件来对系统的各项性能指标进行测试。负载测试和压力测试都属于性能测试的范畴。

安全测试是在软件产品的生命周期中，对产品进行安全缺陷和漏洞的测试。安全测试包括身份认证、授权、加密、会话管理等方面的测试。"""

    # TODO: 创建文本分割器
    splitter = RecursiveCharacterTextSplitter(
         chunk_size=200,      # 每块最多200字符
         chunk_overlap=50,    # 块之间重叠50字符
         separators=["\n\n", "\n", "。", "，", " "]  # 分割优先级
     )

    # TODO: 分割文档
    chunks = splitter.split_text(test_doc)

    # TODO: 打印分块结果
    print(f"原文档长度: {len(test_doc)} 字符")
    print(f"分成 {len(chunks)} 块:\n")
    for i, chunk in enumerate(chunks):
        print(f"==块{i+1} {len(chunk)}字符==")
        print(chunk)
        print()


# ============================================================
# TODO 2: 向量化与存储（Embedding + ChromaDB）
# ============================================================
def todo2_embed_and_store():
    """
    目标：
    - 用 HuggingFace 模型将文本转为向量
    - 存入 ChromaDB 向量数据库

    知识点：
    - Embedding（向量化）：把文字变成一串数字
    - 相似的文字 → 向量距离近 → 能被检索到
    - ChromaDB：轻量级向量数据库，适合学习
    """
    print("\n=== TODO 2: 向量化与存储 ===\n")

    # 准备一些测试文本
    texts = [
        "单元测试是对最小可测试单元进行验证",
        "集成测试检查模块之间的接口是否正确",
        "系统测试在实际运行环境下对系统进行测试",
        "验收测试是部署前的最后一个测试",
        "回归测试确认修改没有引入新的错误",
    ]

    # TODO: 创建 Embedding 模型（用本地模型，不需要 API Key）
    embeddings = SentenceTransformerEmbeddings(
        model_name="shibing624/text2vec-base-chinese"  # 中文向量模型
    )

    # TODO: 创建向量数据库并存储
    vectorstore = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        collection_name="test_knowledge"
    )

    # TODO: 测试相似度搜索
    results = vectorstore.similarity_search("什么是回归测试？", k=2)
    for doc in results:
        print(f"相似内容: {doc.page_content}")


# ============================================================
# TODO 3: 完整 RAG 流程
# ============================================================
def todo3_full_rag():
    """
    目标：构建完整的 RAG 流程

    流程：
    用户提问 → 向量检索相关文档 → 将文档+问题一起给LLM → 生成回答

    知识点：
    - Retriever：检索器，从向量库中找相关文档
    - RAG Chain：检索 → 格式化 → 生成
    """
    print("\n=== TODO 3: 完整 RAG ===\n")

    # 准备文档
    knowledge_base = """
    软件测试是软件开发过程中不可或缺的一部分。它的目的是发现软件中的缺陷，确保软件质量。
    单元测试是对软件中最小可测试单元进行检查和验证。在Java中，通常使用JUnit框架进行单元测试。
    集成测试是将所有模块按照设计要求组装成为子系统或系统，进行测试。主要检查模块之间的接口是否正确。
    系统测试是在实际运行环境下，对计算机系统进行一系列的测试。
    验收测试是部署软件之前的最后一个测试操作，确保软件准备就绪。
    回归测试是修改了旧代码后，重新进行测试以确认修改没有引入新的错误。
    性能测试是通过自动化工具模拟多种负载条件来对系统的各项性能指标进行测试。
    安全测试是对产品进行安全缺陷和漏洞的测试。
    黑盒测试不关注程序内部结构，只关注输入和输出。
    白盒测试关注程序内部逻辑结构和代码实现。
    """

    # TODO: 分块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=30,
        separators=["\n", "。", "，", " "]
    )
    chunks = splitter.split_text(knowledge_base)
    print(f"文档分成 {len(chunks)} 块")

    # TODO: 向量化并存储
    embeddings = SentenceTransformerEmbeddings(
        model_name="shibing624/text2vec-base-chinese"
    )
    vectorstore = Chroma.from_texts(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # TODO: 构建 RAG Prompt
    rag_prompt = ChatPromptTemplate.from_template("""
基于以下参考资料回答问题。如果参考资料中没有相关内容，请说"我不知道"。

参考资料：
{context}

问题：{question}
""")

    # TODO: 构建 RAG Chain
    llm = ChatOllama(model="deepseek-r1:1.5b")

    def format_docs(docs):
        return "\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    # TODO: 测试 RAG
    questions = [
        "什么是单元测试？",
        "黑盒测试和白盒测试有什么区别？",
        "回归测试的目的是什么？",
    ]
    for q in questions:
        answer = rag_chain.invoke(q)
        print(f"问: {q}")
        print(f"答: {answer}\n")


# ============================================================
# TODO 4: 综合练习 — 构建个人知识库问答
# ============================================================
def todo4_personal_kb():
    """
    目标：构建一个基于自定义文档的问答系统

    步骤：
    1. 创建一个 txt 文件作为知识库
    2. 加载并分块
    3. 向量化存储
    4. 构建 RAG Chain
    5. 提问并验证

    这就是一个最简单的 RAG 应用！
    面试时可以说："我用 LangChain + ChromaDB 做过 RAG 知识库问答系统"
    """
    print("\n=== TODO 4: 个人知识库 ===\n")

    # 步骤 1: 创建知识库文件
    kb_content = """HTTP协议基础

HTTP（超文本传输协议）是客户端和服务器之间通信的协议。
HTTP是无状态的，每次请求都是独立的。
HTTP使用请求-响应模型，客户端发送请求，服务器返回响应。

HTTP请求方法

GET：从服务器获取数据，参数在URL中，适合查询操作。
POST：向服务器提交数据，数据在请求体中，适合创建操作。
PUT：更新服务器资源，通常用于整体替换资源。
DELETE：删除服务器上的指定资源。
PATCH：对资源进行部分更新。

HTTP状态码

200 OK：请求成功。
201 Created：资源创建成功（POST请求成功）。
301 Moved Permanently：永久重定向。
302 Found：临时重定向。
400 Bad Request：请求格式错误。
401 Unauthorized：未授权，需要身份认证。
403 Forbidden：已认证但无权限访问。
404 Not Found：请求的资源不存在。
500 Internal Server Error：服务器内部错误。
502 Bad Gateway：网关或代理服务器收到无效响应。
503 Service Unavailable：服务器暂时无法处理请求。

接口测试核心概念

接口测试是验证系统组件间接口交互的正确性。
接口测试不依赖UI，直接通过API发送请求和验证响应。
接口自动化测试可以集成到CI/CD流程中。
接口测试的主要内容包括：功能验证、异常处理、性能测试、安全测试。

Postman工具

Postman是最常用的接口测试工具之一。
支持发送HTTP请求、查看响应、编写测试脚本。
Collection可以组织和管理多个接口测试用例。
环境变量支持在不同环境间切换（开发/测试/生产）。

pytest自动化测试框架

pytest是Python最流行的测试框架之一。
使用 assert 语句进行断言，比 unittest 更简洁。
支持 fixture 管理测试前置条件和资源。
支持 parametrize 数据驱动，一个测试函数跑多组数据。
conftest.py 用于定义共享 fixture。
"""

    kb_path = "personal_kb.txt"
    with open(kb_path, "w", encoding="utf-8") as f:
        f.write(kb_content)
    print(f"✅ 知识库文件已创建: {kb_path} ({len(kb_content)} 字符)")

    # 步骤 2: 加载并分块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=30,
        separators=["\n\n", "\n", "。", "，", " "]
    )
    with open(kb_path, "r", encoding="utf-8") as f:
        doc_text = f.read()
    chunks = splitter.split_text(doc_text)
    print(f"✅ 文档分成 {len(chunks)} 块")

    # 步骤 3: 向量化存储
    embeddings = SentenceTransformerEmbeddings(
        model_name="shibing624/text2vec-base-chinese"
    )
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name="personal_kb"
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    print(f"✅ 向量库已创建，检索器已就绪")

    # 步骤 4: 构建 RAG Chain
    rag_prompt = ChatPromptTemplate.from_template("""
你是一个测试工程师助手。基于以下参考资料回答问题，回答要简洁明了。
如果参考资料中没有相关内容，请说"我不知道，但可以尝试根据经验回答"。

参考资料：
{context}

问题：{question}
""")

    llm = ChatOllama(model="deepseek-r1:1.5b")

    def format_docs(docs):
        return "\n---\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    # 步骤 5: 提问验证
    questions = [
        "HTTP 401 和 403 有什么区别？",
        "POST 和 GET 有什么不同？",
        "pytest 的数据驱动怎么写？",
    ]

    print(f"\n{'='*50}")
    print("开始问答测试：")
    print(f"{'='*50}\n")

    for q in questions:
        # 先看看检索到了什么
        retrieved = retriever.invoke(q)
        print(f"🔍 问题: {q}")
        print(f"   检索到 {len(retrieved)} 条相关资料")

        answer = rag_chain.invoke(q)
        print(f"💬 回答: {answer[:200]}...\n" if len(answer) > 200 else f"💬 回答: {answer}\n")


# ============================================================
# 主程序入口
# ============================================================
if __name__ == "__main__":
    print("LangChain Day2: RAG 实战")
    print("=" * 50)
    print("RAG = 检索增强生成 = 让 AI 基于你的文档回答问题")
    print("这是 Agent 开发的核心技能！")
    print("=" * 50)

    # 逐个测试
    todo1_load_and_split()
    todo2_embed_and_store()
    todo3_full_rag()
    todo4_personal_kb()
