# 🚀 部署到 Vercel

## 📋 前置需求

1. [Vercel 帳號](https://vercel.com/signup)（可用 GitHub 登入）
2. [Git](https://git-scm.com/) 或 GitHub 帳號

---

## 方法一：一鍵部署（最快）

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/你的帳號/security-news-collector)

1. 點擊上方按鈕
2. 授權 Vercel 訪問 GitHub
3. 選擇 Repository
4. 點擊 Deploy

---

## 方法二：從 GitHub 部署

### 步驟 1：上傳到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/你的帳號/security-news-collector.git
git push -u origin main
```

### 步驟 2：連接 Vercel

1. 登入 [Vercel Dashboard](https://vercel.com/dashboard)
2. 點擊「**Add New Project**」
3. 選擇「**Import Git Repository**」
4. 選擇你的 `security-news-collector` Repository
5. 點擊「**Deploy**」

---

## 方法三：使用 Vercel CLI

### 安裝 CLI

```bash
npm install -g vercel
```

### 部署

```bash
cd security-news-collector
vercel
```

首次會詢問一些設定，直接按 Enter 使用預設值即可。

### 部署到生產環境

```bash
vercel --prod
```

---

## 📁 專案結構

```
security-news-collector/
├── api/
│   └── index.py          # Serverless API
├── public/
│   └── index.html        # 前端頁面
├── news_collector.py     # 新聞收集模組
├── requirements.txt      # Python 依賴
├── vercel.json           # Vercel 設定
└── README.md
```

---

## 🔧 設定說明

### vercel.json

```json
{
  "version": 2,
  "builds": [
    { "src": "api/index.py", "use": "@vercel/python" },
    { "src": "public/**", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "/api/index.py" },
    { "src": "/", "dest": "/public/index.html" }
  ]
}
```

---

## 🌐 API 端點

部署後可用的 API：

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/news` | GET | 取得新聞列表 |
| `/api/collect` | POST | 觸發新聞收集 |
| `/api/status` | GET | 取得狀態 |
| `/api/sources` | GET | 取得來源列表 |

---

## ⚠️ Vercel 限制

| 項目 | 免費方案限制 |
|------|-------------|
| 執行時間 | 10 秒（Serverless Function） |
| 記憶體 | 1024 MB |
| 每月請求 | 100,000 次 |
| 頻寬 | 100 GB |

> 💡 新聞收集可能需要較長時間，如超時可考慮：
> - 升級到 Pro 方案（60 秒執行時間）
> - 減少來源數量
> - 使用其他平台（Azure、Railway）

---

## 🔄 自動部署

連接 GitHub 後，每次 push 到 main 分支會自動部署。

---

## ❓ 常見問題

**Q: 顯示 504 Gateway Timeout**
- Serverless 執行超時，減少新聞來源數量

**Q: 新聞沒有更新**
- Vercel 可能有快取，在 Dashboard 中清除快取

**Q: 如何查看日誌**
- Vercel Dashboard → 你的專案 → Deployments → 選擇部署 → Functions → Logs

---

## 🆚 Vercel vs 其他平台

| 平台 | Python 支援 | 免費方案 | 執行時間限制 |
|------|------------|---------|-------------|
| **Vercel** | Serverless | ✅ | 10 秒 |
| **Azure** | 完整 | ✅ | 無限制 |
| **Railway** | 完整 | ✅ | 無限制 |
| **Render** | 完整 | ✅ | 無限制 |

> 如果需要長時間執行的任務，建議使用 Azure App Service 或 Railway。
