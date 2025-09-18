# LifePlanWebApp (MVP)

スマホ向けFastAPIアプリ。7027番ポートで起動。

## 起動
```bash
./run.sh
```
- 初回は仮想環境作成と依存インストールを自動実行
- `http://localhost:7027` にアクセス

## 構成
- FastAPI + Jinja2（Tailwind CDN）
- SQLite（`data/app.db`）
- セッションCookieでの簡易ログイン

## 環境変数
`.env` を作成（任意）
```
SECRET_KEY=change-me
DATABASE_URL=sqlite:///./data/app.db
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
MAIL_FROM=
```

## 機能（MVP）
- ユーザー登録/ログイン/ログアウト
- ダッシュボード/ライフプラン/設定のプレースホルダ

## ライセンス
Private
