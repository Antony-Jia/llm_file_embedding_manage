# 文件向量嵌入开发平台 — 开发文档（Python + React）

## 1. 项目概述

本项目是一个支持 **文件向量嵌入 + 语义检索 + 对话问答** 的平台，面向内部研发或对外提供 API 的场景。

平台提供：

* JWT 用户登录与组织管理（组织 / 部门 / 成员 / 权限）
* 可配置的通用 Embedding 接口（可配置 provider、模型、分块大小）
* Word / PDF 文件上传与解析，自动切分并向量化
* 文档元数据管理与文档级访问控制（可见范围到部门级）
* LLM（按 OpenAI 风格）统一配置与调用
* 选择部分文件（按元数据或文件列表）构建对话上下文
* 对话时展示被引用文件及片段元数据（可审计）
* 对外 REST 搜索接口（语义搜索 + 元数据过滤 + 权限控制）

技术栈：

* **后端**：Python 3.13以上（推荐 FastAPI）+ SQLModel + Poetry
* **数据库**：PostgreSQL / SQLite + pgvector 或独立向量库（如 Qdrant/Chroma）
* **前端**：React + TypeScript + UI 库（Ant Design / MUI 等）
* **鉴权**：JWT（JSON Web Token）

---

## 2. 功能需求

### 2.1 用户与组织管理

#### 2.1.1 用户体系

* 邮箱 + 密码登录，返回 JWT
* 用户基本信息：id、邮箱、姓名（可选）、创建时间
* 每个用户隶属于 **一个组织（Organization）**
* 用户可隶属多个部门（Department）

#### 2.1.2 组织（Organization）

* 表示一个公司 / 租户
* 组织下拥有：

  * 用户集合
  * 部门结构
  * 文档和会话
* 不同组织之间完全隔离（数据层面）

#### 2.1.3 部门（Department）

* 挂在组织下，支持树形结构，例如：

  * 技术部 > 平台组
  * 业务部 > 销售一部
* 用户可属于一个或多个部门

#### 2.1.4 角色 & 权限（简要）

* `org_admin`：组织管理员，可管理本组织的部门、成员与文档默认权限
* `dept_admin`（可选）：部门管理员，可管理本部门成员和本部门文档权限
* `member`：普通成员，只能访问有权限的文档和会话

---

### 2.2 身份验证与安全（JWT）

* 前端登录后，后端返回 `access_token`（JWT）
* 每次调用 API 时在 Header 中携带：
  `Authorization: Bearer <token>`
* JWT 内部包含：

  * `user_id`
  * `org_id`
  * 基本角色信息（可选）
* 所有资源的访问都要通过 `org_id` + 权限规则过滤

---

### 2.3 通用 Embedding 接口

#### 2.3.1 目标

* 提供 **统一抽象的向量嵌入服务**，屏蔽不同提供商的差异。
* 支持配置：

  * provider（openai、本地、其他厂商）
  * base_url
  * api_key
  * model_name
  * 文本分块大小（chunk_size）与重叠（chunk_overlap）

#### 2.3.2 Embedding 配置

* 配置范围：

  * 系统级（默认）
  * 组织级（覆盖系统默认）
  * 用户级（可选）

配置字段示例：

```json
{
  "name": "default-embedding",
  "provider": "openai",
  "base_url": "https://api.openai.com/v1",
  "api_key": "***",
  "model": "text-embedding-3-large",
  "chunk_size": 1000,
  "chunk_overlap": 200
}
```

#### 2.3.3 通用 Embedding API

* 输入：文本或文本数组
* 输出：对应的嵌入向量数组
* 内部根据配置选择具体 provider：

  * OpenAI 风格
  * 本地向量模型
  * 其他兼容接口

---

### 2.4 文档上传与解析（Word/PDF）

#### 2.4.1 支持格式

* `.pdf`
* `.docx` (Word)

#### 2.4.2 上传流程

1. 前端通过 `multipart/form-data` 上传：

   * `file`
   * `metadata`（JSON，可选）
2. 后端校验文件类型、大小
3. 保存原文件到文件存储（本地 / 对象存储）
4. 立即标记文档状态为 `uploaded`，并启动后台任务：

   * 解析文本（按页/段落）
   * 分块（chunking）
   * 调用 Embedding 服务向量化
   * 将 chunk + 向量 + 元数据写入向量数据库
   * 完成后将文档状态更新为 `ready`

#### 2.4.3 文本解析

* PDF：`pdfplumber` / `pypdf`
* Word：`python-docx`
* 解析结果可保留：

  * 页码
  * 段落编号
  * 标题层级（可选）

---

### 2.5 文档元数据管理

#### 2.5.1 元数据字段（示例）

通用字段：

* `title`：文档标题
* `description`：简要介绍
* `tags`: string[]（标签）
* `project`: string（项目名）
* `source`: enum（upload/sync/api）
* `created_at`, `updated_at`
* `custom_metadata`: JSON（任意 key-value）

权限相关字段（见 2.6）

#### 2.5.2 元数据操作

* 上传时传入初始元数据
* 后续支持编辑
* 支持批量修改标签 / 项目 / 可见范围等

#### 2.5.3 基于元数据的筛选

* 按 `tags`、`project`、`source`、时间范围等过滤
* 支持组合条件：

  * `tags` 包含任意 / 必须包含
  * 时间区间（如 2025 年内）
* 筛选结果可用于：

  * 文档列表展示
  * 选择作为对话上下文的文档集合

---

### 2.6 文件访问控制（组织 / 部门 / 用户）

#### 2.6.1 权限策略目标

* 文档可见范围支持：

  * 仅上传者本人可见
  * 所在部门（及下级部门）可见
  * 全组织可见
  * 自定义：指定某些部门或用户可见

#### 2.6.2 文档权限字段设计

在 Document 模型中添加：

* `org_id`：所属组织
* `user_id`：上传者
* `visibility_scope`（enum）：

  * `"private"`：仅自己
  * `"department"`：同部门内可见
  * `"organization"`：组织内用户可见
  * `"custom"`：通过列表精细控制
* `allowed_department_ids: int[] | null`（scope=custom 时有效）
* `allowed_user_ids: int[] | null`（scope=custom 时有效）

#### 2.6.3 权限判断逻辑（概念）

对于当前用户 user，文档 doc，可读判断规则：

1. `user.org_id != doc.org_id` → 不可读（组织隔离）
2. 用户是文档 owner (`user.id == doc.user_id`) → 可读
3. `scope == "organization"` 且同 org → 可读
4. `scope == "department"`:

   * 计算用户所属部门列表 `user_dept_ids`
   * 计算文档关联部门 `doc_dept_ids`（可设为 owner 的部门，或文档单独指定）
   * 若两者有交集 → 可读
5. `scope == "custom"`:

   * 若 `user.id` 在 `allowed_user_ids` 中 → 可读
   * 若 `user_dept_ids` 与 `allowed_department_ids` 有交集 → 可读
6. 其它情况 → 不可读

> 所有对 **文档列表、chunk 检索、REST 搜索、对话检索** 的操作，都必须统一走此权限判断。

#### 2.6.4 前端权限配置 UI

在文档上传/编辑页面增加：

* 可见范围选择（Radio）：

  * 仅自己
  * 部门内
  * 组织内
  * 自定义
* 当选「自定义」：

  * 弹出对话框，提供部门树 + 用户搜索，供选择
* 管理员支持批量修改文档可见范围

---

### 2.7 LLM 配置（OpenAI 风格）

#### 2.7.1 目标

* 用 OpenAI 官方接口格式抽象所有 LLM 调用。

#### 2.7.2 配置字段

```json
{
  "name": "default-openai",
  "base_url": "https://api.openai.com/v1",
  "api_key": "sk-***",
  "model": "gpt-4.1-mini",
  "timeout": 60,
  "max_tokens": 1024
}
```

* 支持组织级 / 用户级配置
* 会话时可指定使用哪个 LLM 配置

#### 2.7.3 调用方式

后端封装统一接口：

* 输入：`messages`（role + content 数组）
* 输出：LLM 返回的 assistant 文本 + 调用元数据
* 对前端可提供：

  * 内部使用的 `/api/chat/conversations/{id}/messages`
  * 或兼容 OpenAI 的 `/api/chat/completions`（可选）

---

### 2.8 文档选择与对话范围

#### 2.8.1 对话作用域（Conversation Scope）

创建会话时可指定：

* `scope_type`：

  * `"doc_ids"`：指定文档 ID 列表
  * `"metadata_filter"`：指定元数据过滤条件
* `scope_doc_ids: int[]`
* 或 `scope_metadata_filter: JSON`

在向量检索时，既要满足：

* 文档在 scope 中
* 文档对当前用户可见（权限过滤）

#### 2.8.2 前端操作方式

* 在对话页面左侧：

  * 提供文档筛选区域（按 tags / project / 时间等）
  * 勾选文档构成当前对话的「上下文文档集合」
* 会话保存时记住当前 scope

---

### 2.9 对话与引用展示

#### 2.9.1 对话流程（RAG）

1. 用户在会话中发送问题
2. 后端根据会话 scope + 用户权限：

   * 从向量库中检索 top_k 文档 chunk
   * 构建 prompt：系统指令 + 检索片段 + 用户问题
3. 调用 LLM 生成回答
4. 保存：

   * 消息记录（user / assistant）
   * 本次检索命中的 chunks 信息（作为 citations）

#### 2.9.2 引用结构

返回给前端时，在回答消息后附带：

```json
{
  "message": {
    "id": 10,
    "role": "assistant",
    "content": "总结内容..."
  },
  "citations": [
    {
      "doc_id": 1,
      "doc_title": "合同A.pdf",
      "chunk_id": 100,
      "score": 0.92,
      "snippet": "……被引用的上下文片段……",
      "metadata": {
        "page": 3,
        "project": "ProjectA",
        "tags": ["contract", "2025"]
      }
    }
  ]
}
```

#### 2.9.3 前端展示

* 每条 AI 回答下方展示「引用文档」列表：

  * 文档标题
  * 页码 / 小节信息
  * 片段预览
* 支持点击展开查看全文 / 原文高亮位置（可后续扩展）

---

### 2.10 对外 REST 搜索接口

#### 2.10.1 目标

* 对外提供统一 REST 搜索能力：

  * 支持语义搜索（基于 embedding）
  * 支持关键字搜索（可选）
  * 支持基于元数据的过滤
  * 自动遵循组织 / 部门 / 文档权限

调用方可：

* 使用 query + filters 获取与某类内容相关的文档片段
* 再将这些结果接入其他业务系统或自建对话系统

#### 2.10.2 搜索能力

1. **语义搜索（Embedding-based）**

   * 后端内部调用 Embedding 服务，将 query 转为向量
   * 在向量库中检索 top_k 最相似 chunk

2. **关键字搜索（可选）**

   * 对 chunks / 文档内容做全文检索（Postgres FTS / 其他搜索引擎）
   * 可单独使用或与语义搜索结果组合

3. **过滤条件（filters）**

   * `doc_ids`: 限制在指定文档集合
   * `project`
   * `tags`
   * 自定义 `metadata`（如 `category`, `type` 等）
   * 时间区间：`created_from`, `created_to`

4. **权限控制**

   * 请求需携带 JWT
   * 在搜索逻辑中统一应用 `can_read_document` 权限判断，不允许绕过权限

#### 2.10.3 REST 接口设计

**1）语义搜索接口**

* `POST /api/v1/search/semantic`

请求示例：

```json
{
  "query": "请帮我找和合同违约条款相关的内容",
  "top_k": 10,
  "filters": {
    "doc_ids": [1, 2, 3],
    "project": "ProjectA",
    "tags": ["contract", "legal"],
    "metadata": {
      "category": "contract"
    },
    "created_from": "2025-01-01",
    "created_to": "2025-12-31"
  }
}
```

响应示例：

```json
{
  "results": [
    {
      "doc_id": 1,
      "doc_title": "合同A.pdf",
      "chunk_id": 100,
      "score": 0.93,
      "snippet": "如一方违反本合同约定，须在30日内支付违约金……",
      "metadata": {
        "page": 5,
        "project": "ProjectA",
        "tags": ["contract", "2025"],
        "category": "contract"
      }
    }
  ],
  "total": 10
}
```

**2）关键字搜索接口（可选）**

* `POST /api/v1/search/keyword`

请求示例：

```json
{
  "keyword": "违约金",
  "filters": {
    "project": "ProjectA"
  },
  "page": 1,
  "page_size": 20
}
```

响应示例：

```json
{
  "results": [
    {
      "doc_id": 1,
      "doc_title": "合同A.pdf",
      "snippet": "如一方违反本合同约定，须在30日内支付违约金……",
      "metadata": {
        "page": 5,
        "project": "ProjectA"
      }
    }
  ],
  "page": 1,
  "page_size": 20,
  "total": 3
}
```

---

## 3. 技术架构与代码结构

### 3.1 后端整体结构（Python）

```text
backend/
  app/
    main.py                     # FastAPI 入口
    core/
      config.py                 # 全局配置
      security.py               # JWT 相关
      logging.py
    api/
      v1/
        auth.py                 # 登录/注册/当前用户
        org.py                  # 组织/部门/成员管理
        documents.py            # 文档上传/列表/元数据/权限
        embeddings.py           # （可选）Embedding 测试接口
        chat.py                 # 会话与消息
        llm.py                  # LLM & Embedding 配置管理
        search.py               # REST 搜索接口
    models/                     # ORM 模型
      user.py
      organization.py
      department.py
      user_org.py
      document.py
      document_chunk.py
      conversation.py
      message.py
      citation.py
      config.py                 # LLM/Embedding 配置
    schemas/                    # Pydantic 请求/响应
      auth.py
      org.py
      document.py
      chat.py
      search.py
      config.py
    services/                   # 业务逻辑
      auth_service.py
      org_service.py
      document_service.py
      embedding_service.py
      llm_service.py
      chat_service.py
      search_service.py
    repositories/               # 数据访问封装
      user_repo.py
      org_repo.py
      department_repo.py
      document_repo.py
      chunk_repo.py
      conversation_repo.py
    workers/                    # 异步任务（解析+向量化）
      embedding_worker.py
    utils/
      chunking.py               # 文本分块策略
      file_parser.py            # pdf/docx 解析
      vector_store.py           # 向量库读写封装
      permission.py             # 文档可读性判断
```

### 3.2 前端整体结构（React + TS）

```text
frontend/
  src/
    main.tsx
    app/
      routes.tsx               # 路由定义
      store/                   # 全局状态管理
    api/                       # 后端 API 封装
      auth.ts
      org.ts
      documents.ts
      chat.ts
      config.ts
      search.ts
    components/
      Layout/
      NavBar/
      DocumentTable/
      MetadataForm/
      PermissionForm/
      ChatBox/
      CitationPanel/
      ScopeSelector/
    features/
      auth/
        LoginPage.tsx
      org/
        OrgAdminPage.tsx
        DepartmentTree.tsx
        MemberList.tsx
      documents/
        DocumentListPage.tsx
        DocumentUploadModal.tsx
        DocumentDetailDrawer.tsx
      chat/
        ChatPage.tsx
      settings/
        LLMConfigPage.tsx
        EmbeddingConfigPage.tsx
      search/
        SearchPage.tsx          # 内部统一搜索视图（复用 REST 搜索）
    utils/
      request.ts               # axios 实例 & 拦截器 (JWT)
      storage.ts               # token 本地存储
```

---

## 4. 数据模型（简要）

### 4.1 用户与组织

* **User**

  * `id, email, password_hash, created_at`
* **Organization**

  * `id, name, created_at`
* **Department**

  * `id, org_id, name, parent_id`
* **UserOrganization**

  * `user_id, org_id, role`
* **UserDepartment**

  * `user_id, dept_id`

### 4.2 文档与向量

* **Document**

  * `id, org_id, user_id`
  * `title, filename, file_path, file_type`
  * `status`（uploaded/parsing/embedding/ready/failed）
  * `metadata`（JSON）
  * `visibility_scope`
  * `allowed_department_ids`
  * `allowed_user_ids`
  * `created_at, updated_at`
* **DocumentChunk**

  * `id, document_id, chunk_index`
  * `text`
  * `embedding`（存向量库）
  * `page_number`
  * `metadata`（继承文档 + chunk 级信息）

### 4.3 配置与对话

* **LLMConfig / EmbeddingConfig**

  * `id, org_id/user_id, name, provider, base_url, api_key, model, settings`
* **Conversation**

  * `id, org_id, user_id`
  * `title`
  * `scope_type`（doc_ids/metadata_filter）
  * `scope_doc_ids`
  * `scope_metadata_filter`
  * `llm_config_id`
* **Message**

  * `id, conversation_id, role, content, created_at`
* **Citation**

  * `message_id, document_id, chunk_id, score, snippet, metadata`

---
