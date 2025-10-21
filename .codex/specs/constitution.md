# CONSTITUTION（项目原则 / 边界）

项目名：petcloud-emr（宠物云病历 / PetCloud EMR）
目标：一次性交付可运行的 MVP，安装简、依赖少、代码清晰，非技术用户也能本地跑起来。

【硬约束】
- 后端：Python FastAPI + SQLAlchemy + Pydantic，**仅 SQLite**。
- 前端：Vue 3 + Vite + Pinia + Vue Router + Tailwind。
- 认证：JWT（HS256）；角色：OWNER / VET / CLINIC_ADMIN。
- 上传：病历图片存本地 `uploads/` 并返回可访问 URL。
- 提醒：基于疫苗/驱虫记录计算即将到期提醒。
- 不使用 Docker、Postgres、Alembic、K8s、云依赖。
- 所有 API 路径统一前缀 `/api`。
- 输出必须是可运行项目，文档清晰，脚本简单。

【软约束 / 风格】
- 代码可读性优先；中文注释适度。
- 前后端分离、目录清晰；README 写清“最小启动步骤”。
- 错误提示友好；默认放开 CORS（README 提醒生产环境收紧）。

【非目标】
- 复杂权限审计、第三方存储、消息队列、复杂 DevOps。
- 医疗合规的全面实现（仅做基础提醒）。
