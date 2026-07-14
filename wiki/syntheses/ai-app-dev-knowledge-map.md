# AI 应用开发知识体系

> 本文是 AI 应用开发的全景知识地图，涵盖从 LLM 基础到工程化落地的完整链路。与 [[Java开发知识体系]]（AI 后端主力语言）和 [[软件测试知识体系]]（AI 最佳落地场景）深度关联。

---

## 1. LLM 基础概念

### 什么是大语言模型（LLM）

大语言模型（Large Language Model）本质上是基于 Transformer 架构的深度神经网络，通过海量文本训练学会"下一个词的预测"。GPT 系列的核心思路是 **自回归生成**——每次预测一个 token，把新 token 拼回输入，再预测下一个，直到达到终止条件。

**通俗理解**：
- LLM 是一个"极度擅长文字接龙"的模型
- 它没有真正的"理解"，但有极强的模式匹配和统计推断能力
- ChatGPT 等产品 = LLM + 对话界面 + 安全对齐（RLHF）

### 关键参数

| 参数 | 含义 | 调参要点 |
|------|------|---------|
| **Token** | 模型的最小处理单位（≈0.75 个英文词 / ≈1.5 个中文字） | API 按 Token 计费，请求+回复总 token 不能超过上下文限制 |
| **上下文窗口**（Context Window） | 模型一次能处理的最大 token 数 | 窗口越大能处理越长的内容，但成本和延迟也越高 |
| **Temperature** | 控制输出的随机性（0~2） | 0-0.3 适合确定性任务（代码生成、分类），0.7-1.0 适合创意任务（写作、头脑风暴） |
| **Top-P**（Nucleus Sampling） | 累积概率阈值，控制采样范围 | 通常与 Temperature 配合使用，Top-P=0.9 意味着只从概率最高的 90% 的 token 中采样 |
| **Max Tokens** | 限制模型输出的最大 token 数 | 防止无限生成，控制成本 |

### LLM 的能力边界

**能做什么**：
- 文本生成、总结、翻译、改写
- 代码生成、解释、重构
- 知识问答（存在于训练数据中的）
- 逻辑推理（Chain-of-Thought 下表现显著提升）
- 结构化输出（JSON、表格、代码）

**不能做什么（局限性和误区）**：
- **事实幻觉**：会自信地编造不存在的知识
- **数学不精确**：复杂计算需要借助外部计算器
- **时效性限制**：知识截止于训练数据时间（除非结合 RAG）
- **缺乏真正理解**：没有意识、情感或主观体验
- **上下文遗忘**：长对话中会忘记早期内容
- **无法自主学习**：每次调用都是独立的，不记住之前的交互（除非手动管理 history）

### 主流模型概览

| 模型 | 厂商 | 特点 | 适用场景 |
|------|------|------|---------|
| **GPT-4o / GPT-4o-mini** | OpenAI | 多模态、综合能力强、生态成熟 | 通用场景、复杂推理、多模态 |
| **Claude 3.5 / 4** | Anthropic | 长上下文（200K）、安全性好、代码能力强 | 长文档处理、代码生成、安全敏感场景 |
| **DeepSeek V3 / R1** | 深度求索 | 性价比极高、推理能力强 | 成本敏感场景、复杂推理 |
| **Qwen 2.5 / 3** | 阿里巴巴 | 中文能力强、开源生态好 | 中文场景、私有化部署 |
| **Gemini** | Google | 多模态原生、百万级上下文 | 超长上下文、多模态应用 |

---

## 2. Prompt Engineering

关联页面：[[prompt-engineering]]

### 角色体系（Message Roles）

```
┌─────────────────────────────────────────────┐
│  System Message（系统指令）                    │
│  → 设定 AI 的角色、行为边界、输出规则           │
│  → 优先级最高，用户消息不能覆盖                 │
├─────────────────────────────────────────────┤
│  User Message（用户输入）                      │
│  → 用户的问题或任务描述                         │
├─────────────────────────────────────────────┤
│  Assistant Message（AI 回复）                  │
│  → AI 的回复，也可用于 few-shot 提供示例       │
└─────────────────────────────────────────────┘
```

### 提示策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| **Zero-shot** | 不给例子，直接提要求 | 简单任务（翻译、总结） |
| **Few-shot** | 给 2-5 个输入/输出示例 | 格式要求严格的输出、分类任务 |
| **Chain-of-Thought（CoT）** | 让 AI 展示推理过程 | 数学题、逻辑推理、复杂决策 |
| **Tree-of-Thought（ToT）** | 多路径推理后选最优 | 搜索、规划类任务 |

### 结构化输出

- **JSON mode**：强制 AI 输出合法 JSON（OpenAI 支持 `response_format={ "type": "json_object" }`）
- **Structured Outputs**：定义 JSON Schema，让 AI 严格按 schema 输出（支持嵌套、枚举、条件字段）
- **Function Calling**：定义可调用的函数签名，AI 自主选择是否调用

### 提示词工程技巧

1. **角色设定**："你是一位资深软件测试工程师，精通边界值分析和等价类划分..."
2. **分步指令**：将复杂任务拆解为步骤，Step 1 → Step 2 → Step 3
3. **格式约束**："以 Markdown 表格输出，包含用例编号、输入、预期结果"
4. **反面示例**："不要解释你的思考过程，只输出 JSON"
5. **温度控制**：输出格式敏感的任务设 Temperature=0，确保一致性

---

## 3. API 集成开发

### 基础调用模式

```java
// Java 示例：调用 LLM API（使用 HttpClient）
HttpClient client = HttpClient.newHttpClient();
String requestBody = """
    {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": "你是一个测试专家"},
            {"role": "user", "content": "生成登录功能的测试用例"}
        ],
        "temperature": 0.3
    }
    """;

HttpRequest request = HttpRequest.newBuilder()
    .uri(URI.create("https://api.openai.com/v1/chat/completions"))
    .header("Authorization", "Bearer " + apiKey)
    .header("Content-Type", "application/json")
    .POST(HttpRequest.BodyPublishers.ofString(requestBody))
    .build();

HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
```

### Streaming 响应处理

非流式（一次性返回）在大段输出时延迟高。Streaming 通过 SSE（Server-Sent Events）逐 token 返回，用户体验更流畅。

**技术要点**：
- 客户端使用 `HttpClient` 的 `BodyHandlers.ofLines()` 或 Java 的 SSE 库
- 逐行解析 `data: {"choices":[{"delta":{"content":"..."}}]}`
- 注意连接超时和断线重连

### 多轮对话管理

```
对话轮次 1: User → AI → 将 {User, AI} 存入 history
对话轮次 2: User + history → AI → 更新 history
对话轮次 3: User + history → AI → ...
```

**关键实践**：
- 每次请求都携带完整的 message history（受上下文窗口限制）
- 超出窗口时进行截断：丢弃最早的消息、摘要历史、或使用滑动窗口
- 考虑 Token 消耗：history 越长成本越高

### 错误处理

| 错误类型 | HTTP 状态码 | 处理策略 |
|---------|------------|---------|
| Rate Limit（频率限制） | 429 | 指数退避重试、请求队列 |
| Token Limit（超长） | 400 | 截断输入、切换大窗口模型 |
| 超时（Timeout） | 请求级 | 设置合理的 connect/read timeout |
| 服务不可用 | 500/503 | 重试 + 降级（切换到备用模型） |

### Function Calling / Tool Use

关联页面：[[function-calling]]

Function Calling 是 AI 应用开发的核心模式——让 AI 不仅能"说话"，还能"做事"。

```
用户：查询我的订单状态
        ↓
AI 分析：需要调用 get_order API
        ↓
应用执行：get_order(userId="123") → 返回订单数据
        ↓
AI 根据结果组织自然语言回复
```

**应用场景**：查询数据库、调用外部 API、执行系统命令、计算数学表达式

---

## 4. RAG 模式

关联页面：[[rag-pattern]]

### RAG 原理

RAG（Retrieval-Augmented Generation）通过向 LLM 提供外部知识库的相关片段，让模型基于事实信息回答，从根本上缓解幻觉问题。

```
用户提问
    ↓
        ┌──────────────────┐
        │  Embedding 模型   │ ← 将用户问题转为向量
        └────────┬─────────┘
                 ↓
        ┌──────────────────┐
        │   向量数据库      │ ← 检索最相似的 K 个文档片段
        └────────┬─────────┘
                 ↓
用户问题 + 检索到的文档片段 → [LLM] → 基于事实的回答
```

### 完整流程

```
文档加载（Document Loading）
    → PDF/Word/HTML/Markdown 等格式解析
    ↓
文本分块（Chunking）
    → 按段落/固定长度/语义边界切分，通常 256-1024 tokens
    ↓
向量化（Embedding）
    → 用 Embedding 模型将文本转为高维向量
    ↓
向量存储（Vector Store）
    → 存入向量数据库，建立索引
    ↓
检索（Retrieval）
    → 用户查询向量化 → 近似最近邻（ANN）搜索
    ↓
生成（Generation）
    → 用户问题 + 检索结果 → LLM 组织回答
```

### 向量数据库

| 数据库 | 部署方式 | 特点 |
|--------|---------|------|
| **Milvus** | 分布式部署 | 大规模生产环境、高可用 |
| **Pinecone** | 全托管 SaaS | 开箱即用、无需运维 |
| **Chroma** | 嵌入式/本地 | 开发原型阶段、轻量 |
| **Weaviate** | 自托管/云 | 内置向量+对象存储 |
| **Qdrant** | 自托管/云 | Rust 实现、性能好 |

### Embedding 模型选择

- **text-embedding-3-small/large**（OpenAI）：综合能力强，通用场景首选
- **BGE**（BAAI）：中文场景优秀
- **text2vec**（国人开发）：中文嵌入，适合私有化部署
- **M3E**：多语言 Embedding，中文友好

---

## 5. AI Agent

关联页面：[[ai-agent]]

### Agent 概念

AI Agent 是能够**自主决策和执行**的 AI 系统。不同于简单的"请求-响应"，Agent 具备：

1. **感知**（Perception）：理解用户意图和环境状态
2. **规划**（Planning）：拆解任务、制定执行步骤
3. **执行**（Execution）：通过 Tool Use 调用外部能力
4. **记忆**（Memory）：记录历史信息供后续决策
5. **反思**（Reflection）：评估执行结果，调整策略

### ReAct 模式

ReAct（Reasoning + Acting）是 Agent 的核心思想——让 AI 交替进行"推理"和"行动"。

```
思考（Thought）：用户想查天气，我需要调用天气 API
行动（Action）：call weather_api(location="Beijing")
观察（Observation）：返回 "Beijing: 25°C, Sunny"
思考（Thought）：获取到了天气，现在组织回复
回答（Answer）：北京今天 25°C，天气晴朗
```

### Tool Use 实战

工具定义示例（以 Java 后端为例）：

```java
// 定义 AI 可调用的工具
Tool getWeatherTool = Tool.builder()
    .name("get_weather")
    .description("查询指定城市的天气")
    .parameters(Map.of(
        "type", "object",
        "properties", Map.of(
            "location", Map.of("type", "string", "description", "城市名称")
        ),
        "required", List.of("location")
    ))
    .build();
```

### 多步推理与规划

- **任务分解**：将"测试这个电商系统的下单流程"分解为：登录→搜索→加购→下单→支付→验证
- **动态规划**：Agent 根据中间结果调整后续步骤
- **用于反馈**：执行失败时 AI 自主决定重试或换方案

### 实际应用场景

| 场景 | 说明 | 复杂度 |
|------|------|--------|
| **AI 测试 Agent** | 自动探索 Web 应用、生成用例、执行并报告 Bug | 高 |
| **自动 Bug 修复** | 分析错误日志 → 定位代码 → 生成修复 → 创建 PR | 高 |
| **智能客服** | 理解用户问题 → 查知识库 → 调内部系统 → 回复 | 中 |
| **代码审查助手** | 审查 PR diff → 调用静态分析 → 生成审查意见 | 中 |

---

## 6. AI + 测试实战场景

> 这是 [[软件测试知识体系]] 与 AI 应用开发的核心交汇点，也是面试中体现差异化的最佳切入点。

### AI 生成测试用例

**思路**：将功能描述输入 LLM，利用其知识生成边界覆盖的测试用例。

**Prompt 示例**：
```
你是一位资深测试工程师。请对以下功能生成测试用例，
要求覆盖：正常流程、异常流程、边界值、安全测试。

功能：用户注册
- 用户名：6-20 位字母数字
- 密码：8-16 位，含大小写字母+数字+特殊字符
- 邮箱：合法邮箱格式

以 JSON 数组格式输出，每条包含：用例编号、描述、输入、预期结果、测试类型
```

**Java 后端架构**：Spring Boot + LLM API + JSON 解析 → 前端展示

### AI 智能 Bug 分类与分析

**流程**：
```
Bug 描述文本 → [LLM] → 结构化输出
{
  "severity": "critical",
  "category": "空指针异常",
  "component": "UserService",
  "root_cause": "user.getId() 返回 null",
  "suggested_owner": "后端-张三"
}
```

**进阶**：结合 RAG 模式，检索历史相似 Bug，推荐解决方案。

### AI 视觉回归测试

- 截图差异比对 + LLM 理解"变化是否算 Bug"
- 区分：UI 友好修改 vs 回归缺陷
- 工具：Playwright + 多模态模型（GPT-4o / Claude Vision）

### AI 辅助性能测试

- JMeter 结果文件（.jtl）自动分析
- AI 识别瓶颈模式："TPS 在并发 100 时出现拐点，平均响应时间从 200ms 飙升到 2s，建议检查数据库连接池配置"
- 自动生成性能测试报告

### 测试报告自动生成

- AI 汇总测试执行结果、失败用例分析、覆盖率趋势
- 用自然语言描述问题分布、风险区域、改进建议
- 支持邮件/飞书/钉钉推送

---

## 7. 工程化考量

### 成本控制

| 策略 | 说明 | 效果 |
|------|------|------|
| **Token 计算** | 调用前估算 token 数，选择合适模型 | 避免不必要的昂贵模型调用 |
| **缓存策略** | 相同输入的请求缓存结果（如 LLM Cache） | 降低成本 40-70% |
| **Embedding 缓存** | 已向量化的文档无需重复计算 | 降低 Embedding API 调用 |
| **模型分级** | 简单任务用小模型（GPT-4o-mini），复杂任务用大模型 | 平衡成本与质量 |
| **Prompt 压缩** | 精简 prompt，去除冗余描述 | 减少 20-50% Token |

### 质量保障

- **输出验证**：对 AI 输出做格式校验、约束检查
- **Human-in-the-loop**：关键决策加入人工审核环节（如 AI 建议的 Bug 修复需人工确认）
- **A/B 测试**：对比不同 prompt / 模型的输出质量
- **回归测试**：AI 应用的输出也应有自动化断言验证
- **监控告警**：LLM API 的错误率、延迟、Token 消耗监控

### 数据安全

- **敏感信息过滤**：在发送给 LLM 前脱敏（手机号、身份证、密码）
- **PII 检测**：用正则/模型检测输入中的个人信息
- **私有化部署**：敏感数据场景使用私有化模型（如 Qwen、DeepSeek 本地部署）
- **数据隔离**：多租户场景确保知识库隔离
- **日志脱敏**：API 日志中的请求/响应内容进行脱敏处理后再存储

---

## 8. 面试相关

### 描述 AI 项目的套路（STAR 变体）

```
背景（Context）："在 XXX 项目中，测试团队每天需要手工分类 50+ 条 Bug，耗时 2 小时"
方案（Solution）："我基于 Spring Boot + LLM API 开发了一个 Bug 分类机器人"
难点（Challenge）："最困难的是 Bug 描述的多样性导致分类不准，我通过 few-shot 示例和自定义 category schema 将准确率从 70% 提升到 92%"
成果（Result）："Bug 分类从 2 小时缩短到 15 分钟，准确率 92%，项目已开源在 GitHub"
```

### 常见问题

**如何评估 AI 输出质量？**
- 定量指标：准确率、精确率、召回率（适合分类任务）
- 定性指标：人工评分、A/B 测试、用户满意度
- 自动化评估：用更强模型（如 GPT-4o）评估弱模型输出
- 业务指标：Bug 分类后处理时间缩短多少、用例生成覆盖率达到多少

**如何处理幻觉？**
- RAG 模式：让 AI 基于检索到的知识回答，而非凭空生成
- 引用溯源：强制 AI 在回答中标注信息来源
- 不确定性表达：让 AI 在不确定时明确说"我不确定"
- Human-in-the-loop：关键决策由人确认
- 输出验证：用规则引擎校验关键事实

### 差异点：测试 + AI 结合的独特价值

```
传统测试工程师          你
────────────────────────────────────────
会写自动化用例          + AI 生成测试用例
手工分析 Bug            + AI 自动分类 + 根因分析
画 Excel 报告           + AI 自动生成报告
手动做回归验证          + AI 视觉比对
等开发修复 Bug          + AI 辅助定位代码问题
```

**面试金句**："AI 不会取代测试工程师，但会用 AI 的测试工程师会取代不会用的。我的价值在于，我既懂测试流程，又能把 AI 能力工程化落地。"

---

## 关联知识体系

- [[Java开发知识体系]] — AI 后端开发的主力语言，Spring Boot 是 AI 应用的首选框架
- [[软件测试知识体系]] — 测试是 AI 应用的最佳落地场景，测试数据是 AI 模型的燃料
- [[prompt-engineering]] — 提示词工程深度详解
- [[function-calling]] — Tool Use 实战指南
- [[rag-pattern]] — 检索增强生成完整实现
- [[ai-agent]] — Agent 架构与多步推理
