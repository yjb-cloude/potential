# LangChain + RAG 学习路线

## 学习目标
掌握 AI Agent 开发核心技能，同时为 AI 测试打基础。

## 每日安排

| Day | 主题 | 文件 | 核心知识点 |
|-----|------|------|-----------|
| Day1 | LangChain 基础 | `day1_basics.py` | ChatOllama、PromptTemplate、LCEL Chain |
| Day2 | RAG 实战 | `day2_rag.py` | 文档分块、Embedding、ChromaDB、RAG Chain |
| Day3 | RAG 进阶 | `day3_rag_advanced.py` | PDF加载、多文档检索、检索优化 |
| Day4 | Tool Calling | `day4_tools.py` | Function Calling、自定义工具、Agent基础 |
| Day5 | Agent 实战 | `day5_agent.py` | ReAct Agent、多工具调用、对话记忆 |
| Day6 | 项目整合 | `day6_project.py` | 完整 RAG 问答系统 + 测试用例 |

## 技术栈

| 组件 | 用途 |
|------|------|
| LangChain | LLM 应用开发框架 |
| Ollama + DeepSeek | 本地大模型 |
| ChromaDB | 向量数据库 |
| sentence-transformers | 中文 Embedding 模型 |
| pytest | 测试框架 |

## 面试话术

> "我用 LangChain + ChromaDB + DeepSeek 搭建了一个 RAG 知识库问答系统，
> 支持文档加载、向量检索、智能问答，并编写了自动化测试用例评估回答质量。"

## 运行前置条件

```bash
# 1. 确保 Ollama 在运行
ollama serve

# 2. 确保 DeepSeek 已下载
ollama pull deepseek-r1:1.5b

# 3. 安装依赖（已安装则跳过）
pip install langchain langchain-community langchain-chroma sentence-transformers
```
