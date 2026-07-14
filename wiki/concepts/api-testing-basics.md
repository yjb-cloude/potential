# API 测试基础

## HTTP 核心知识

**请求方法：**

| 方法 | 作用 | 幂等 |
|------|------|------|
| GET | 获取资源 | 是 |
| POST | 创建资源 | 否 |
| PUT | 全量更新资源 | 是 |
| DELETE | 删除资源 | 是 |
| PATCH | 部分更新资源 | 否 |

**状态码分类：**
- **2xx**（成功）：200 OK / 201 Created / 204 No Content
- **3xx**（重定向）：301 Moved Permanently / 302 Found / 304 Not Modified
- **4xx**（客户端错误）：400 Bad Request / 401 Unauthorized / 403 Forbidden / 404 Not Found / 405 Method Not Allowed / 415 Unsupported Media Type / 422 Unprocessable Entity
- **5xx**（服务端错误）：500 Internal Server Error / 502 Bad Gateway / 503 Service Unavailable / 504 Gateway Timeout

**常见请求头：**
- `Content-Type: application/json` — 请求体格式
- `Authorization: Bearer <token>` — 鉴权令牌
- `Accept: application/json` — 期望响应格式
- `X-Request-Id` — 请求追踪（链路追踪）

## RESTful API 设计规范

- **资源命名**：名词复数形式 `/users`、`/orders`，不用动词
- **版本控制**：URL 路径 `/v1/` 或请求头 `Accept: application/vnd.api+json;version=1`
- **使用正确 HTTP 方法**：查询用 GET、创建用 POST、更新用 PUT/PATCH、删除用 DELETE
- **HATEOAS**：返回资源关联链接，实现服务端驱动的客户端导航
- **分页**：`GET /users?page=1&size=20`，响应包含 `totalPages`、`hasMore`

## 接口测试关注点

1. **功能正确性**：请求正确数据得到正确结果
2. **参数校验**：必填参数缺失、参数类型错误、参数越界
3. **异常处理**：请求不存在资源、未授权访问、服务内部错误时的响应
4. **幂等性**：GET / PUT / DELETE 重复执行结果应一致
5. **响应时间**：正常场景应在可接受时间内返回（通常 < 2s）
6. **响应结构**：JSON 字段名、类型、嵌套结构是否符合预期

## 常见鉴权方式

- **Basic Auth**：`Authorization: Basic base64(username:password)`，明文不安全
- **JWT Token**：登录后获取 token，附带在 Authorization Header，支持过期刷新
- **OAuth 2.0**：第三方授权，四种授权模式（Authorization Code / Client Credentials / Password / Implicit）
- **API Key**：最简单方式，放在 Header 或 Query Param 中

## 测试数据准备

- **setUp**：测试执行前构造前置数据（创建用户、生成订单等）
- **tearDown**：测试执行后清理数据，避免污染环境
- **数据隔离**：每条测试用例使用独立的测试数据，互不影响
- **唯一性约束**：使用时间戳或 UUID 保证数据唯一（如用户名、邮箱）

---

关联：[[rest-assured-api]] | [[软件测试知识体系]]
