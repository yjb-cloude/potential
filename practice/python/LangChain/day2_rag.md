# LangChain Day2: RAG 实战

## 什么是 RAG
- 检索增强生成（Retrieval-Augmented Generation）
- 让 AI 基于你的文档回答问题，不是瞎编
- 流程：用户提问 → 搜索相关文档 → 给 LLM 生成回答

## 为什么需要 RAG
- 你问"公司测试流程是什么"，AI 不知道
- RAG 把你的文档变成可搜索知识库
- 面试话术："我用 LangChain + ChromaDB 做过 RAG 知识库问答系统"

## TODO 1: 分块
- 把长文档切成小块
- 原因：大模型有 token 限制，装不下整篇文档
- 参数
  - chunk_size：每块最大字符数（推荐 500-1000）
  - chunk_overlap：块间重叠，防止句子被切断
  - separators：分割优先级（段落 → 句子 → 词）

## TODO 2: 向量化 + 存储
- Embedding：文字变一串数字
  - 相似文字 → 向量距离近 → 能被搜到
- ChromaDB：轻量级向量数据库
  - 存储向量，支持相似度搜索
- 例："回归测试" 和 "改完代码重新测" 向量很近，能互相找到

## TODO 3: 完整 RAG 流程
- 1. 用户提问
- 2. 向量检索相关文档（找最相关的块）
- 3. 把文档 + 问题给 LLM
- 4. LLM 生成回答
- 核心组件：Retriever（检索器）、RAG Prompt、RAG Chain

## TODO 4: 个人知识库
- 综合练习，整合前步骤
- 创建知识库 → 分块 → 向量化 → 构建 Chain → 提问验证
- 完成这就是一个真正的 RAG 应用

## 技术栈
- LangChain：开发框架
- Ollama + DeepSeek：本地大模型
- ChromaDB：向量数据库
- HuggingFace：中文 Embedding 模型
