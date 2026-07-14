# Spring Boot 核心

Spring Boot 是当前 Java 后端开发的事实标准框架。它以"约定大于配置"的理念，大幅简化了 Spring 应用的搭建和开发，同时保留了 Spring 框架最核心的 IoC、AOP 和 MVC 能力。

## IoC（控制反转）与 DI（依赖注入）

IoC 的核心思想是**将对象的创建和管理权交给容器**，开发者只需要声明依赖关系，容器负责注入。

### 依赖注入方式

| 方式 | 说明 | 推荐度 |
|------|------|--------|
| 字段注入 `@Autowired` | 直接标记字段，最简洁 | 不推荐（不利于测试和不可变性） |
| Setter 注入 | 通过 setter 方法注入 | 可选 |
| **构造器注入** | 通过构造方法注入 | **强烈推荐** |

**推荐构造器注入的原因：** 保证依赖不可变性（final）、明确初始化顺序、便于单元测试、避免循环依赖警告。

### @Resource 与 @Autowired

- `@Autowired`：Spring 注解，按类型注入（Type），可配合 `@Qualifier` 按名称
- `@Resource`：JSR-250 注解，默认按名称注入（Name），找不到则按类型

### 循环依赖与三级缓存

Spring 通过**三级缓存**解决单例 Bean 的构造器之外的循环依赖：

1. **singletonObjects：** 一级缓存，完全初始化好的 Bean
2. **earlySingletonObjects：** 二级缓存，提前曝光的半成品 Bean（已实例化但未完成属性赋值和初始化）
3. **singletonFactories：** 三级缓存，生产 Bean 的 ObjectFactory

**解决过程：** A 依赖 B，B 依赖 A。创建 A 时提前暴露到三级缓存，A 注入 B 时触发 B 的创建，B 注入 A 时从三级缓存获取 A 的半成品，完成循环。

**注意：** 构造器注入无法解决循环依赖，会抛出 `BeanCurrentlyInCreationException`。

### Bean 生命周期

```
实例化 → 属性赋值 → 初始化 → 使用 → 销毁
```

初始化阶段按顺序执行：
1. `@PostConstruct` 标注的方法
2. `InitializingBean.afterPropertiesSet()`
3. `<bean init-method="">` 或 `@Bean(initMethod="")`

销毁阶段：`@PreDestroy` → `DisposableBean.destroy()` → 自定义 destroy-method

## AOP（面向切面编程）

### 核心概念

| 概念 | 说明 |
|------|------|
| **JoinPoint** | 被拦截的方法调用点 |
| **Pointcut** | 匹配 JoinPoint 的表达式（`execution()`, `@annotation()`） |
| **Advice** | 切面执行的逻辑（Before / After / Around / AfterReturning / AfterThrowing） |
| **Aspect** | Pointcut + Advice 的组合，用 `@Aspect` 标注 |

### 实现机制

Spring AOP 基于代理实现：
- **JDK 动态代理：** 目标类实现接口时使用，基于反射的 Proxy + InvocationHandler
- **CGLIB 代理：** 目标类未实现接口时使用，基于字节码增强生成子类

**性能对比：** CGLIB 创建代理开销大但调用性能高；JDK 代理创建快但在 JDK8+ 性能与 CGLIB 相近。

### 典型应用

日志记录、事务管理、权限校验、性能监控、缓存管理、异常处理。

## Spring MVC

### 常用注解

```java
@RestController                // @Controller + @ResponseBody
@RequestMapping("/users")      // 类级别路径映射
@GetMapping("/{id}")           // GET 请求，@RequestMapping(method=GET) 的简写
@PostMapping                   // POST 请求简写
```

### 参数绑定

| 注解 | 来源 | 说明 |
|------|------|------|
| `@RequestParam` | 查询参数 | 可设置 required / defaultValue |
| `@PathVariable` | URL 路径 | `/users/{id}` |
| `@RequestBody` | 请求体 | JSON/XML 反序列化 |
| `@RequestHeader` | 请求头 | 获取 Header 值 |

### 全局异常处理

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(BusinessException.class)
    public Result<?> handleBusiness(BusinessException e) {
        return Result.error(e.getCode(), e.getMessage());
    }
}
```

## 数据访问

### 事务管理 `@Transactional`

**传播行为（Propagation）：**
| 传播级别 | 行为 |
|----------|------|
| REQUIRED（默认） | 有事务则加入，无则创建新事务 |
| REQUIRES_NEW | 挂起当前事务，创建新事务 |
| NESTED | 嵌套事务，子事务回滚不影响主事务 |
| SUPPORTS | 有事务则加入，无事务则以非事务方式执行 |
| MANDATORY | 必须在事务中执行，否则抛异常 |
| NEVER | 必须在非事务中执行，否则抛异常 |
| NOT_SUPPORTED | 挂起当前事务，以非事务方式执行 |

**隔离级别：** READ_UNCOMMITTED / READ_COMMITTED / REPEATABLE_READ / SERIALIZABLE

**回滚规则：** 默认运行时异常（RuntimeException）和 Error 触发回滚，受检异常（Checked Exception）不触发。

### MyBatis

```java
@Mapper
public interface UserMapper {
    @Select("SELECT * FROM users WHERE id = #{id}")
    User findById(Long id);
}
```

使用 `resultMap` 处理复杂映射，通过 `<collection>` 和 `<association>` 解决一对多/多对一关系。

### JPA / Hibernate

```java
@Entity
public class User {
    @Id @GeneratedValue
    private Long id;
    @OneToMany(mappedBy = "user")
    private List<Order> orders;
}
```

## 拦截器 HandlerInterceptor

```java
@Component
public class LoginInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse resp, Object handler) {
        // 请求处理前执行，返回 false 中断后续处理
        return true;
    }
    @Override
    public void postHandle(...) { /* 控制器执行后，视图渲染前 */ }
    @Override
    public void afterCompletion(...) { /* 请求完成后，用于清理 */ }
}
```

## Spring Boot Starter 机制

**自动配置**的核心是 `@EnableAutoConfiguration` 注解，Spring Boot 通过 `spring.factories` 或 `AutoConfiguration.imports` 文件加载所有自动配置类，再根据 `@Conditional` 条件注解按需生效。

常见 Starter：
- `spring-boot-starter-web`：嵌入式 Tomcat + Spring MVC
- `spring-boot-starter-data-jpa`：JPA + Hibernate
- `spring-boot-starter-data-redis`：Redis 客户端

---

**关联知识点：** [[Java开发知识体系]] | [[软件测试知识体系]] | [[jvm-basics]]
