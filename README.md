# 🛡️ 資安新聞收集器 Security News Collector

自動收集多個資安新聞來源，提供分類、搜尋、篩選功能的 Serverless 應用。

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Vercel](https://img.shields.io/badge/Vercel-Serverless-black.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 功能特色

- 🔍 **自動收集** - 從 10+ 個資安新聞來源收集最新消息
- 📊 **智能分類** - 自動分類為惡意程式、漏洞、資料外洩等類別
- 🔎 **即時搜尋** - 關鍵字即時篩選
- 🌐 **響應式設計** - 深色主題，支援手機瀏覽
- ⚡ **Serverless** - 部署到 Vercel，無需管理伺服器

## 📰 新聞來源

- 🇹🇼 iThome 資安、TWCERT/CC
- 🌍 The Hacker News、Krebs on Security、BleepingComputer
- 🌍 Dark Reading、SecurityWeek、Threatpost、HackRead、Sophos News

## 🚀 一鍵部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/你的帳號/security-news-collector)

## 📁 專案結構

```
├── api/
│   └── index.py          # Serverless API
├── public/
│   └── index.html        # 前端頁面
├── news_collector.py     # 新聞收集模組
├── requirements.txt      # Python 依賴
├── vercel.json           # Vercel 設定
└── README.md
```

## 🔧 本地開發

```bash
# 安裝 Vercel CLI
npm install -g vercel

# 本地執行
vercel dev
```

## 🌐 API 端點

| 端點 | 方法 | 說明 |
|------|------|------|
| `/api/news` | GET | 取得新聞列表 |
| `/api/collect` | POST | 觸發新聞收集 |
| `/api/sources` | GET | 取得來源列表 |

## 📖 詳細部署說明

請參考 [VERCEL_DEPLOY.md](VERCEL_DEPLOY.md)

## 📄 授權

MIT License
