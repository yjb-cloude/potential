# Rest Assured API 测试

## 简介

Rest Assured 是 Java 领域最主流的 RESTful API 自动化测试框架，提供类 DSL 的链式调用语法，让接口测试代码像自然语言一样可读。

## 核心语法：BDD 风格

```java
given()
    .header("Content-Type", "application/json")
    .body(requestBody)
.when()
    .post("/api/users")
.then()
    .statusCode(201)
    .body("data.name", equalTo("张三"));
```

三部分结构：
- **given()** — 前置条件：请求头、参数、鉴权、请求体
- **when()** — 执行动作：HTTP 方法 + 端点路径
- **then()** — 结果验证：状态码、响应体、响应时间

**extract()** 用于提取响应数据供后续使用：`response = given()...when()...then().extract().response()`

## 支持的 HTTP 方法

| 方法 | Rest Assured 方式 | 用途 |
|------|------------------|------|
| GET | `when().get(url)` | 查询资源 |
| POST | `when().post(url)` | 创建资源 |
| PUT | `when().put(url)` | 全量更新 |
| PATCH | `when().patch(url)` | 部分更新 |
| DELETE | `when().delete(url)` | 删除资源 |

## 参数传递

- **pathParam**：路径参数，`given().pathParam("id", 1).when().get("/users/{id}")`
- **queryParam**：查询参数，`given().queryParam("page", 1).when().get("/users")`
- **requestBody**：请求体，可传 String / POJO / JSONObject

## 响应验证

```java
.then()
    .statusCode(200)
    .body("code", equalTo(0))                    // 精确匹配
    .body("message", containsString("成功"))      // 包含字符串
    .body("data.items", hasItems("A", "B"))       // 列表包含
    .body("data.size()", greaterThan(0))          // 集合大小
    .time(lessThan(2000L))                        // 响应时间 < 2s
```

## JSON Schema 校验

将响应体与预定义的 JSON Schema 文件匹配，确保接口返回值结构完整：

```java
.then().body(matchesJsonSchemaInClasspath("schemas/user-schema.json"));
```

## 认证处理

- **OAuth 2.0**：`given().auth().oauth2(token)`
- **Basic Auth**：`given().auth().basic("username", "password")`
- **Bearer Token**：`given().header("Authorization", "Bearer " + token)`

## 链式调用设计原则

- 每个方法返回 `ValidatableResponse`，支持无限链式追加
- 配合 `ResponseSpecification` 可复用公共验证逻辑
- 支持 `filter()` 机制实现请求日志记录、Cookie 管理、鉴权自动注入

---

关联：[[api-testing-basics]] | [[auto-framework-design]] | [[软件测试知识体系]]
