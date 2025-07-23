# NestJS 11.1.1 course outline

## Module 1: Foundations & Project Setup

1. **Why NestJS?**

   * Comparison with Express, Koa, Fastify
   * Architectural overview (inspired by Angular DI)
2. **Monorepo with Nx**

   * Nx workspace vs. standalone app
   * Generators, caching, affected commands
3. **Feature-Based Folder Structure**

   * Vertical slices vs. technical layers
   * Organizing modules, controllers, services, DTOs, entities
4. **Bootstrapping & Configuration**

   * `@nestjs/config` with Zod for schema validation
   * Environment variables & multiple environments
5. **Dependency Injection Deep Dive**

   * Custom providers, `useClass`/`useFactory`/`useValue`
   * Scoped providers & request context (AsyncLocalStorage)

---

## Module 2: Core Building Blocks

1. **Controllers & Routing**

   * Path parameters, query parameters, versioning
   * Request/response lifecycle
2. **Pipes, Guards & Interceptors**

   * Validation with `class-validator` v0.15 & `class-transformer` v2
   * Auth guards (JWT, API-Key), RBAC, ACL
   * Logging, transformation, timeout, caching interceptors
3. **Exception Filters & Global Error Handling**

   * Built-in HTTP exceptions
   * Custom filter patterns
4. **DTOs & Serialization**

   * DTO vs. Entity vs. ViewModel
   * `@nestjs/swagger` decorators for OpenAPI

---

## Module 3: Data Layer & Persistence

1. **ORM Choices: TypeORM vs. Prisma**

   * Trade-offs, schema migrations with `Prisma Migrate`
   * QueryBuilder vs. Prisma Client
2. **Repository & Unit-of-Work Patterns**

   * Abstracting data access
   * Custom repositories
3. **Caching & Data Loading**

   * Redis integration (`@nestjs/redis`)
   * DataLoader pattern for batching
4. **Transactions & Concurrency**

   * Distributed transactions with `@nestjs/cqrs` sagas

---

## Module 4: API Styles & Gateways

1. **RESTful API Design**

   * HATEOAS principles, pagination, filtering
2. **GraphQL with `@nestjs/graphql`**

   * Schema-first vs. code-first
   * Query, Mutation, Subscription (WebSockets)
3. **gRPC & Microservice Transport**

   * Protobuf schemas, NestJS microservice clients/servers
4. **WebSockets & Real-Time**

   * `@nestjs/websockets`, gateway decorators, rooms/namespaces

---

## Module 5: Advanced Architecture Patterns

1. **CQRS & Event Sourcing**

   * Command vs. Query separation
   * Event store (e.g., EventStoreDB) integration
2. **Domain-Driven Design (DDD)**

   * Entities, Value Objects, Aggregates, Bounded Contexts
3. **Plugin & Module Extensibility**

   * Dynamic modules, on-module-init/hooks
4. **Feature Flags & Configuration Management**

   * LaunchDarkly, OpenFeature SDK

---

## Module 6: Security, Testing & Quality

1. **Security Best Practices**

   * Helmet, rate limiting, CORS, CSRF mitigation
   * OAuth2 / OpenID Connect (Keycloak, Auth0)
2. **Automated Testing**

   * Unit tests (Jest with DI mocks)
   * E2E tests (SuperTest, Testcontainers for databases)
   * Mutation testing (Stryker)
3. **Type Checking & Linting**

   * ESLint, Prettier, strict TSconfig, TSC watch scripts
4. **Code Coverage & Quality Gates**

   * SonarQube integration

---

## Module 7: CI/CD, Deployment & Observability

1. **CI Pipelines**

   * GitHub Actions workflows (lint → test → build → publish)
   * Nx affected-apps caching
2. **Containerization & Kubernetes**

   * Docker best practices (multi-stage builds)
   * Helm charts, Kustomize, GitOps (Argo CD)
3. **Service Mesh & API Gateway**

   * Istio/Linkerd basics, Kong/Gloo for ingress
4. **Logging, Metrics & Tracing**

   * OpenTelemetry (OTel) instrumentation
   * Prometheus + Grafana dashboards
   * Distributed tracing (Jaeger)
5. **Error Tracking & Performance**

   * Sentry or Elastic APM integration

---

## Module 8: Scaling, Maintenance & Beyond

1. **Scaling Strategies**

   * Horizontal scaling, statelessness, sticky sessions
   * Database sharding & read replicas
2. **Code Evolution & Migrations**

   * Schema evolution strategies, backward compatibility
3. **Developer DX & Workspace Optimization**

   * VS Code extensions, live-reload, Hot Module Replacement (HMR)
4. **Capstone Project & FAANG-Style Code Review**

   * Build a full end-to-end microservices app
   * Peer review session with architecture critique

---

### Recommended Resources & Tooling

* **Books:**

  * *Designing Data-Intensive Applications* (Kleppmann)
  * *Domain-Driven Design Distilled* (Vaughn Vernon)
* **Repos & Examples:**

  * NestJS official examples
  * Nx Monorepo Starter Templates
* **Extensions & CLI Tools:**

  * Prisma VSCode extension
  * Nx Console
  * Swagger UI

