# AI Agent

AI Agent 是以 LLM 为核心驱动器的自主系统，能够感知环境、做出推理决策、调用工具执行行动，并在循环中持续优化。

## Agent 的核心能力

与单纯的 LLM 问答不同，Agent 具备三个核心特征：

1. **自主性（Autonomy）** — 无需每一步的人工干预，能自主规划并执行。
2. **感知与行动（Perception & Action）** — 能感知环境状态（如读取文件、搜索网络），并通过工具对环境产生影响。
3. **循环迭代（Iterative Loop）** — 不是一次性输出，而是在观察-思考-行动的循环中逐步推进。

## ReAct 模式

ReAct（Reasoning + Acting）是 Agent 最经典的设计模式：

```
观察(Observation) → 思考(Thought) → 行动(Action) → 观察(Observation) → ...
```

每一步 Agent 先思考当前状态和下一步行动，然后调用工具执行，观察结果后继续下一轮思考。这种模式让 Agent 能够处理需要多步推理和工具交互的复杂任务。

## Tool Use

Agent 通过 [[function-calling]] 能力与外部工具交互。常见工具包括：
- 搜索引擎（Web Search）
- 计算器（Calculator）
- API 调用（REST / GraphQL）
- 数据库查询（SQL）
- 文件读写（File I/O）
- 代码执行（Sandboxed Runtime）

## 记忆管理

- **短期记忆（Short-term Memory）**：对话历史上下文。受限于 LLM 的 context window。
- **长期记忆（Long-term Memory）**：通过 [[rag-pattern]] 从向量库中检索相关信息，持久化存储经验知识。

## 规划能力

复杂任务需要分解为子任务。Agent 可以自主制定计划（Planning），将目标拆解为可执行的步骤序列，并在执行过程中根据实际情况动态调整。

## 实际应用

- **AI 测试 Agent**：自主探索应用界面、执行测试用例、发现并报告 Bug。
- **代码修复 Agent**：定位 Bug 位置 → 分析根因 → 生成修复代码 → 运行测试验证 → 提交修复。
- **数据分析 Agent**：理解数据问题 → 编写查询/脚本 → 执行分析 → 生成报告。

## 局限与挑战

- **成本高**：多次 LLM 调用循环，token 消耗显著。
- **可能陷入循环**：ReAct 可能在某些状态下持续重复，需要设置最大步数或终止条件。
- **幻觉累积**：早期步骤的错误会沿循环累积放大。
- **工具使用风险**：需要严格控制 Agent 可调用的工具权限。

## 关联

[[function-calling]] | [[rag-pattern]] | [[prompt-engineering]] | [[AI应用开发知识体系]]
