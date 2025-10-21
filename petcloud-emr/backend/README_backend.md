# PetCloud EMR 后端

基于 FastAPI + SQLite 的轻量级宠物病历管理服务。默认依赖最少，复制 `.env.example` 即可运行。

## 快速开始

```bash
cd backend
cp .env.example .env
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

首次启动会在当前目录生成 `app.db` 和 `uploads/`。

## 主要功能
- JWT 登录注册（宠主/兽医/诊所管理员角色）
- 宠物档案、授权、体重/喂养/疫苗/驱虫记录
- 病历、处方、图片附件上传（保存在 `uploads/`）
- 即将到期提醒接口 `/api/reminders/upcoming`

## 开发提示
- 所有 API 统一前缀 `/api`
- 数据库使用 SQLite 单文件，可直接复制备份
- 若需要清空数据，删除 `app.db` 并重启服务
