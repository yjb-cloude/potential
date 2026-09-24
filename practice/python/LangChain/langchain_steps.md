# LangChain 调用步骤（思维导图）

## 1. 安装依赖
- `pip install langchain`
- `pip install langchain-community`
- `pip install langchain-ollama`
- `pip install langchain-core`

## 2. 启动 Ollama
- `ollama serve`
- `ollama pull deepseek-r1:1.5b`

## 3. 创建 LLM 实例
- `from langchain_ollama import ChatOllama`
- `llm = ChatOllama(model="deepseek-r1:1.5b")`
- 作用：连接本地大模型

## 4. 构建 Prompt 模板
- `from langchain_core.prompts import ChatPromptTemplate`
- 简单模板：`ChatPromptTemplate.from_template("你是{role}，请解释{topic}")`
- 多角色模板：
  - `("system", "...")` → 定义 AI 角色和行为规则
  - `("human", "...")` → 用户的实际问题
- 作用：参数化提示词，复用性高

## 5. 创建输出解析器
- `from langchain_core.output_parsers import StrOutputParser`
- `parser = StrOutputParser()`
- 作用：从 LLM 返回对象中提取纯文本

## 6. 用 LCEL 构建 Chain
- `chain = prompt | llm | parser`
- `|` 管道符：数据从左往右流
- 流程：
  - 输入变量 → PromptTemplate → 生成完整提示词
  - 提示词 → LLM → 返回模型响应
  - 响应 → StrOutputParser → 纯文本

## 7. 调用 Chain
- 单次调用：`chain.invoke({"role": "测试专家", "topic": "单元测试"})`
- 批量调用：`chain.batch([{输入1}, {输入2}, ...])`

---

## 核心概念对比

| 概念 | 类比 | 说明 |
|------|------|------|
| ChatOllama | 驱动 | 连接大模型 |
| PromptTemplate | 模板 | 定义怎么问 |
| Chain | 管道 | 串联步骤 |
| StrOutputParser | 过滤器 | 提取结果 |

## 对比 Day9

| | Day9 | LangChain |
|---|------|-----------|
| 代码量 | 20 行 | 3 行 |
| 模型切换 | 改 URL + 参数 | 改一行 model |
| 扩展性 | 自己写 | 框架封装 |
