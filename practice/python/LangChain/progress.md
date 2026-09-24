# LangChain 学习进度

## 2026-09-23 完成

### Day1: LangChain 基础 ✅ 全部完成
| TODO | 内容 | 状态 |
|------|------|------|
| TODO 1 | ChatOllama 连接 DeepSeek | ✅ |
| TODO 2 | PromptTemplate 提示词模板 | ✅ |
| TODO 3 | LCEL Chain 管道语法 (`prompt | llm | parser`) | ✅ |
| TODO 4 | 系统提示 (system + human 双角色) | ✅ |
| TODO 5 | 批量调用 `.batch()` | ✅ |
| TODO 6 | 综合练习 — 测试知识问答 Chain | ✅ |

**核心收获：**
- LCEL 管道语法：`chain = prompt | llm | parser`，数据从左流到右
- 多角色提示：`from_messages([("system", "..."), ("human", "...")])`
- 批量调用比逐个 invoke 高效

### Day2: RAG 实战 🔄 进行中
| TODO | 内容 | 状态 |
|------|------|------|
| TODO 1 | 文档加载与分块 | ✅ |
| TODO 2 | 向量化与存储 | 🔄 |
| TODO 3 | 完整 RAG 流程 | ❌ |
| TODO 4 | 个人知识库问答 | ❌ |

**核心收获：**
- RAG = Retrieval-Augmented Generation = 检索增强生成
- 流程：分块 → 向量化 → 存储 → 检索 → 生成
- 向量化靠语义相似度，不是关键词匹配
- 已生成 XMind 导图：`day2_rag.md`

### 面试话术积累
1. "我用 LangChain 连接本地 DeepSeek，用 LCEL 管道构建 Chain，比手写 requests 简洁很多"
2. "我用 LangChain + ChromaDB 做过 RAG 知识库问答系统，支持文档分块、向量检索、带引用来源的智能问答"

### 待办
- Day1-6 全部学完后，集中一天从头重写所有 TODO（不看代码）
- 继续 Day2 TODO 2-4
- 安装依赖（如需）：`pip install pypdf langchain-chroma`
