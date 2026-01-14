# ⚡ クイックデプロイガイド (5分)

最速でGitHubにデプロイする手順です。

## 🚀 3ステップでデプロイ

### ステップ1: GitHubでリポジトリを作成 (1分)

1. https://github.com/new にアクセス
2. **Repository name**: `comman-chatbot`
3. **Private** または **Public** を選択
4. **何もチェックせずに** 「Create repository」をクリック
5. 表示されるURLをコピー (例: `https://github.com/your-username/comman-chatbot.git`)

### ステップ2: コマンド1つでプッシュ (2分)

```bash
cd comman-chatbot

# 自動初期化スクリプトを実行
./init-git.sh https://github.com/your-username/comman-chatbot.git
```

**または手動で:**

```bash
git init
git add .
git commit -m "Initial commit: Complete chatbot system"
git branch -M main
git remote add origin https://github.com/your-username/comman-chatbot.git
git push -u origin main
```

### ステップ3: GitHub Pagesを有効化 (2分)

1. GitHubリポジトリページで **Settings** をクリック
2. 左サイドバーの **Pages** をクリック
3. **Source** で `GitHub Actions` を選択
4. 完了! 🎉

数分後、以下のURLでアクセス可能:
```
https://your-username.github.io/comman-chatbot/
```

---

## 📱 動作確認

### フロントエンド (GitHub Pages)

```
https://your-username.github.io/comman-chatbot/
```

にアクセスして、チャットボットのデモページを確認。

### バックエンド (別途デプロイ必要)

以下のいずれかでバックエンドをデプロイ:

#### 最速: Railway.app (推奨)

1. https://railway.app でGitHubログイン
2. 「New Project」→ GitHubリポジトリを選択
3. `backend` ディレクトリを指定
4. PostgreSQLを追加
5. 環境変数を設定して完了 (5分)

#### 代替: Render.com

1. https://render.com でGitHubログイン
2. 「New」→「Web Service」
3. リポジトリを選択
4. Root Directory: `backend`
5. Build: `pip install -r requirements.txt`
6. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

## ⚙️ 環境変数の設定

### GitHub Secrets (管理画面用)

リポジトリの **Settings** → **Secrets and variables** → **Actions**:

- `API_URL`: バックエンドAPIのURL

### バックエンドサービス (Railway/Render等)

- `ANTHROPIC_API_KEY`: Anthropic APIキー
- `SECRET_KEY`: ランダムな長い文字列
- `DATABASE_URL`: 自動設定される (PostgreSQL追加時)

---

## ✅ 完了チェックリスト

- [ ] GitHubリポジトリが作成されている
- [ ] コードがプッシュされている
- [ ] GitHub Actionsが実行されている (緑チェック)
- [ ] GitHub Pagesでフロントエンドが表示される
- [ ] バックエンドがデプロイされている
- [ ] チャットボットが動作する

---

## 🆘 トラブル時

### GitHub Actionsが失敗

→ **Actions** タブでエラーログを確認

### GitHub Pagesが404

→ 数分待ってから再アクセス

### その他

→ 詳細は `GITHUB_DEPLOY.md` を参照

---

**これで完了です! 🎉**

詳細な手順は [GITHUB_DEPLOY.md](./GITHUB_DEPLOY.md) をご覧ください。
