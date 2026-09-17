# Agent 智能应用系统学习路线

> 从零开始，系统掌握 Agent 智能应用开发
> 目标：能独立开发、部署、评估 Agent 应用

---

## 学习路线总览

```
第 1 阶段：基础准备（1-2 周）
  ├── Python 基础 ✅（已完成）
  ├── pip + requests ✅（已完成）
  └── LLM 基础 + API 调用（待学习）

第 2 阶段：Prompt Engineering（1 周）
  ├── 基础 Prompt 设计
  ├── 进阶技巧（Few-shot、CoT）
  └── 输出格式控制

第 3 阶段：LangChain 框架（2 周）
  ├── 核心概念（Chain、LCEL）
  ├── Memory（记忆）
  ├── Tool（工具）
  └── Agent（智能体）

第 4 阶段：RAG 检索增强生成（1 周）
  ├── Embedding + 向量数据库
  ├── 文档加载 + 分块
  └── 检索 + 生成

第 5 阶段：Agent 开发实战（2 周）
  ├── Function Calling 原理
  ├── 多工具 Agent
  ├── Multi-Agent 协作
  └── 评估与优化

第 6 阶段：部署 + 面试（1 周）
  ├── FastAPI 部署
  ├── Docker 容器化
  └── 面试准备
```

---

## 第 1 阶段：基础准备

### 1.1 LLM 基础概念

**必学知识点**：

| 概念 | 说明 | 重要程度 |
|------|------|---------|
| **Token** | 模型处理文本的最小单位 | ⭐⭐⭐⭐⭐ |
| **Temperature** | 控制输出随机性（0-1） | ⭐⭐⭐⭐ |
| **Top-P** | 控制采样范围 | ⭐⭐⭐ |
| **Context Window** | 模型一次能处理的最大 token 数 | ⭐⭐⭐⭐⭐ |
| **System Prompt** | 系统提示词，定义模型角色 | ⭐⭐⭐⭐⭐ |

**学习资源**：
- OpenAI 官方文档：https://platform.openai.com/docs
- DeepSeek 官方文档：https://platform.deepseek.com

### 1.2 第一次调用 LLM API

```python
from openai import OpenAI

# 初始化客户端（以 DeepSeek 为例）
client = OpenAI(
    api_key="你的API密钥",
    base_url="https://api.deepseek.com"
)

# 调用大模型
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个AI助手"},
        {"role": "user", "content": "什么是Agent？"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

### 1.3 练习任务

- [ ] 注册 DeepSeek/OpenAI API Key
- [ ] 调用 API 问 5 个问题
- [ ] 实验不同 temperature 值的效果
- [ ] 理解 token 的计算方式

---

## 第 2 阶段：Prompt Engineering

### 2.1 基础 Prompt 设计

**核心原则**：
1. **清晰**：明确告诉模型你要什么
2. **具体**：给出详细的约束和要求
3. **给示例**：用例子说明期望的输出

**模板**：
```
你是一个[角色]，请[任务要求]。
输入：[具体内容]
要求：[格式、长度、风格等约束]
输出：[期望的格式]
```

### 2.2 进阶技巧

| 技巧 | 说明 | 适用场景 |
|------|------|---------|
| **Few-shot** | 给几个示例 | 分类、格式转换 |
| **CoT (Chain of Thought)** | 让模型分步思考 | 复杂推理、数学题 |
| **ReAct** | 思考-行动-观察 | Agent 任务 |
| **输出格式控制** | JSON、Markdown | 结构化输出 |

### 2.3 练习任务

- [ ] 设计一个分类 Prompt（5 类文本分类）
- [ ] 设计一个 JSON 输出 Prompt
- [ ] 用 Few-shot 提升分类准确率
- [ ] 用 CoT 解决复杂推理问题

---

## 第 3 阶段：LangChain 框架

### 3.1 安装

```bash
pip install langchain langchain-openai langchain-community
```

### 3.2 核心概念

| 概念 | 作用 | 例子 |
|------|------|------|
| **LCEL** | 管道符语法，串联组件 | `prompt \| llm \| parser` |
| **Chain** | 把多个组件串起来 | 检索链、对话链 |
| **Memory** | 记住对话历史 | ConversationBufferMemory |
| **Tool** | 定义 Agent 可用的工具 | 搜索、数据库查询 |
| **Agent** | 自动决定用什么工具 | ReAct Agent |

### 3.3 学习路径

```
3.3.1 LCEL 基础（1 天）
  - Prompt Template + LLM + Output Parser
  - 管道符 | 语法

3.3.2 Memory（1 天）
  - ConversationBufferMemory
  - ConversationSummaryMemory

3.3.3 Tool（2 天）
  - @tool 装饰器
  - 自定义工具
  - 工具调用流程

3.3.4 Agent（3 天）
  - ReAct 框架
  - create_react_agent
  - 多工具 Agent
```

### 3.4 练习任务

- [ ] 用 LCEL 构建一个 Chain
- [ ] 实现有记忆的对话机器人
- [ ] 创建 3 个自定义工具
- [ ] 构建一个 ReAct Agent

---

## 第 4 阶段：RAG 检索增强生成

### 4.1 什么是 RAG？

```
用户问题 → 检索相关文档 → 大模型生成答案
```

**解决的问题**：
- 大模型知识过时
- 大模型不知道你的私有数据
- 减少幻觉（胡说八道）

### 4.2 技术栈

| 组件 | 作用 | 推荐方案 |
|------|------|---------|
| **Embedding** | 文本转向量 | OpenAI Embedding / 本地模型 |
| **向量数据库** | 存储和检索向量 | ChromaDB（本地）/ Pinecone（云） |
| **文档加载** | 加载 PDF/Word/TXT | LangChain DocumentLoaders |
| **文本分块** | 把长文档切成小块 | RecursiveCharacterTextSplitter |

### 4.3 学习路径

```
4.3.1 Embedding 基础（1 天）
  - 理解向量
  - 调用 Embedding API

4.3.2 向量数据库（1 天）
  - ChromaDB 安装和使用
  - 存储 + 检索

4.3.3 文档处理（2 天）
  - 加载 PDF/Word/TXT
  - 文本分块策略

4.3.4 RAG Chain（2 天）
  - 构建检索链
  - 评估检索质量
```

### 4.4 练习任务

- [ ] 用 Embedding 把 10 个句子转成向量
- [ ] 用 ChromaDB 存储并检索
- [ ] 加载一个 PDF 文档
- [ ] 构建一个文档问答系统

---

## 第 5 阶段：Agent 开发实战

### 5.1 Function Calling 原理

```
用户问题 → 大模型决定调用哪个函数 → 执行函数 → 返回结果
```

**核心**：让大模型能"调用"你的代码。

### 5.2 多工具 Agent

```python
# 定义多个工具
tools = [
    Tool("search", search_func, "搜索知识库"),
    Tool("calculator", calc_func, "数学计算"),
    Tool("weather", weather_func, "查询天气")
]

# 创建 Agent
agent = create_react_agent(llm, tools, prompt)
```

### 5.3 评估与优化

| 评估维度 | 方法 |
|---------|------|
| **准确性** | 人工评估 + 自动评估 |
| **响应时间** | 记录每个步骤的耗时 |
| **成本** | 计算 token 消耗 |
| **用户体验** | A/B 测试 |

### 5.4 练习任务

- [ ] 实现 Function Calling 调用 3 个函数
- [ ] 构建多工具 Agent
- [ ] 设计评估指标
- [ ] 优化 Prompt 提升准确率

---

## 第 6 阶段：部署 + 面试

### 6.1 FastAPI 部署

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask(question: Question):
    answer = agent.run(question.question)
    return {"answer": answer}
```

### 6.2 Docker 容器化

```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 6.3 面试准备

**高频面试题**：
1. LLM 是什么？Token/Temperature/Top-P？
2. RAG 是什么？为什么需要 RAG？
3. Agent 是什么？和 Chain 的区别？
4. Function Calling 原理？
5. 向量数据库是什么？
6. 你的项目是怎么做的？遇到什么困难？

**项目展示**：
- 项目名称：AI 测试用例生成器
- 一句话介绍：输入需求文档，AI 自动生成结构化测试用例
- 技术栈：Python + LangChain + OpenAI API + FastAPI
- 亮点：结合测试背景，能评估 AI 输出质量

---

## 📚 推荐学习资源

### 官方文档
- OpenAI：https://platform.openai.com/docs
- DeepSeek：https://platform.deepseek.com
- LangChain：https://python.langchain.com
- ChromaDB：https://docs.trychroma.com

### 视频教程
- LangChain 官方教程
- DeepSeek 官方示例
- B 站搜索"LangChain Agent"

### 实战项目
- 智能客服系统
- 文档问答系统
- 测试用例生成器
- 代码助手

---

## 🎯 学习检查点

| 阶段 | 检查标准 | 项目产出 |
|------|---------|---------|
| 第 1 阶段 | 能调用 LLM API | API 调用脚本 |
| 第 2 阶段 | 会设计 Prompt | Prompt 模板库 |
| 第 3 阶段 | 会用 LangChain | Chain + Agent |
| 第 4 阶段 | 会搭建 RAG | 文档问答系统 |
| 第 5 阶段 | 能开发 Agent | 测试用例生成器 |
| 第 6 阶段 | 能部署 + 面试 | Docker + 简历项目 |

---

## 📌 学习建议

1. **每天 2-3 小时**：理论 + 实践
2. **先跑通再理解**：先让代码运行，再深入原理
3. **记录踩坑**：把问题和解决方案记下来
4. **做项目**：学完一个阶段就做个小项目
5. **面试准备**：边学边准备面试题

---

> 这个路线图是系统学习 Agent 智能应用的完整路径。按照这个路线走，10 周后你就能独立开发、部署、评估 Agent 应用。
