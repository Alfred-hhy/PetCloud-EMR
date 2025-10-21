# PetCloud EMR

一站式宠物健康档案（Electronic Medical Record, EMR）MVP。后端使用 FastAPI + SQLite，前端基于 Vue 3 + Vite，开箱即用、部署简单。

## 快速体验

### 1. 准备环境
- 已安装 **Python 3.10+**
- 已安装 **Node.js 18+**（附带 npm）

### 2. 启动后端 API
```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```
首次运行会自动创建 `app.db`（SQLite 数据库）与 `uploads/`（附件目录）。

### 3. 启动前端界面
```bash
cd frontend
npm install
npm run dev
```
然后打开命令行中提示的本地地址（默认 http://localhost:5173）。

### 4. 初始体验建议
1. 在前端注册三个账号，分别选择角色：宠主（OWNER）、兽医（VET）、诊所管理员（CLINIC_ADMIN）。
2. 以宠主身份登录，新增宠物并填写体重、喂养、疫苗、驱虫等记录。
3. 以兽医身份登录，让宠主在“共享”页面授权后添加病历与处方，可上传图片附件。
4. 返回首页 Dashboard 查看未来 30 天的提醒和最新病历。

### 5. 常见问题（FAQ）
- **无法登录**：确认后端是否在运行，并检查 `.env` 中 `JWT_SECRET` 是否设置。
- **跨域提示**：默认开放 `CORS_ORIGINS=*`，若部署上线请根据域名修改。
- **上传失败**：确认 `uploads/` 目录存在（后端会在启动时自动创建）。

祝使用愉快！
