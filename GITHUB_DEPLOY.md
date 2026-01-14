# GitHub デプロイガイド

このガイドでは、チャットボットシステムをGitHubにデプロイする手順を説明します。

## 📋 目次

1. [GitHubリポジトリの作成](#1-githubリポジトリの作成)
2. [ローカルGitリポジトリの初期化](#2-ローカルgitリポジトリの初期化)
3. [GitHubへのプッシュ](#3-githubへのプッシュ)
4. [GitHub Pagesの設定](#4-github-pagesの設定)
5. [GitHub Actionsの確認](#5-github-actionsの確認)
6. [バックエンドのデプロイオプション](#6-バックエンドのデプロイオプション)

---

## 1. GitHubリポジトリの作成

### ステップ1: GitHubにログイン

https://github.com にアクセスしてログインします。

### ステップ2: 新しいリポジトリを作成

1. 右上の「+」→「New repository」をクリック
2. 以下の情報を入力:
   - **Repository name**: `comman-chatbot`
   - **Description**: `株式会社カンマンのチャットボットシステム`
   - **Visibility**: `Private` または `Public` (お好みで)
   - **Initialize this repository with**: チェックを**入れない**
3. 「Create repository」をクリック

### ステップ3: リポジトリURLをコピー

表示されるページで、HTTPSのURLをコピーします。
例: `https://github.com/your-username/comman-chatbot.git`

---

## 2. ローカルGitリポジトリの初期化

プロジェクトディレクトリに移動して、Gitリポジトリを初期化します。

```bash
cd comman-chatbot

# Gitリポジトリを初期化
git init

# すべてのファイルをステージング
git add .

# 最初のコミット
git commit -m "Initial commit: Complete chatbot system"

# mainブランチに変更 (デフォルトがmasterの場合)
git branch -M main

# リモートリポジトリを追加
git remote add origin https://github.com/your-username/comman-chatbot.git
```

---

## 3. GitHubへのプッシュ

```bash
# GitHubにプッシュ
git push -u origin main
```

これで、すべてのコードがGitHubにアップロードされます!

**確認**: GitHubのリポジトリページを更新すると、すべてのファイルが表示されているはずです。

---

## 4. GitHub Pagesの設定

フロントエンド(チャットウィジェット)をGitHub Pagesでホスティングします。

### ステップ1: Settingsを開く

1. GitHubリポジトリページで「Settings」タブをクリック
2. 左サイドバーから「Pages」を選択

### ステップ2: GitHub Pagesを有効化

**Source**セクションで:
- **Source**: `GitHub Actions` を選択

### ステップ3: 自動デプロイの確認

1. リポジトリの「Actions」タブをクリック
2. 「Deploy Frontend to GitHub Pages」ワークフローが実行中/完了していることを確認
3. 完了後、緑色のチェックマークが表示されます

### ステップ4: URLを確認

再度「Settings」→「Pages」を開くと、以下のようなURLが表示されます:

```
Your site is live at https://your-username.github.io/comman-chatbot/
```

このURLにアクセスすると、チャットボットのデモページが表示されます!

### カスタムドメインの設定 (オプション)

カスタムドメイン (例: `chatbot.comman.co.jp`) を使用する場合:

1. `frontend/public/CNAME` ファイルを編集:
   ```
   chatbot.comman.co.jp
   ```

2. DNSレコードを追加:
   ```
   CNAME chatbot your-username.github.io
   ```

3. 再度プッシュ:
   ```bash
   git add frontend/public/CNAME
   git commit -m "Add custom domain"
   git push
   ```

---

## 5. GitHub Actionsの確認

リポジトリには3つのワークフローが設定されています:

### 1. Deploy Frontend to GitHub Pages
- **トリガー**: `frontend/` フォルダの変更時
- **動作**: フロントエンドをビルドしてGitHub Pagesにデプロイ
- **URL**: リポジトリの「Actions」タブで確認

### 2. Build and Test Admin Panel
- **トリガー**: `admin/` フォルダの変更時
- **動作**: 管理画面をビルドして成果物を保存
- **成果物**: ビルド完了後、Artifactsからダウンロード可能

### 3. Test Backend
- **トリガー**: `backend/` フォルダの変更時
- **動作**: バックエンドの構造をテスト

すべてのワークフローは、リポジトリの「Actions」タブで確認できます。

---

## 6. バックエンドのデプロイオプション

バックエンドAPIは、以下のいずれかの方法でデプロイできます:

### オプション1: Heroku (無料プラン廃止後は有料)

```bash
# Herokuにログイン
heroku login

# アプリケーションを作成
heroku create comman-chatbot-api

# PostgreSQLアドオンを追加
heroku addons:create heroku-postgresql:mini

# 環境変数を設定
heroku config:set ANTHROPIC_API_KEY=your_api_key
heroku config:set SECRET_KEY=your_secret_key

# デプロイ
git subtree push --prefix backend heroku main
```

### オプション2: Railway.app (推奨・無料枠あり)

1. https://railway.app にアクセス
2. GitHubアカウントでログイン
3. 「New Project」→「Deploy from GitHub repo」
4. `comman-chatbot` リポジトリを選択
5. 「backend」ディレクトリを指定
6. PostgreSQLサービスを追加
7. 環境変数を設定:
   - `ANTHROPIC_API_KEY`
   - `SECRET_KEY`
   - `DATABASE_URL` (自動設定)

### オプション3: Render.com (無料枠あり)

1. https://render.com にアクセス
2. GitHubアカウントでログイン
3. 「New」→「Web Service」
4. GitHubリポジトリを接続
5. 以下を設定:
   - **Name**: comman-chatbot-api
   - **Root Directory**: backend
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. PostgreSQLデータベースを追加
7. 環境変数を設定

### オプション4: VPS (DigitalOcean, Linode, etc.)

Docker Composeを使用:

```bash
# サーバーにSSH接続
ssh user@your-server-ip

# リポジトリをクローン
git clone https://github.com/your-username/comman-chatbot.git
cd comman-chatbot

# 環境変数を設定
cp .env.example .env
nano .env

# Docker Composeで起動
docker-compose up -d

# Nginxでリバースプロキシを設定 (オプション)
```

---

## 7. 環境変数の設定

### GitHub Secrets

機密情報はGitHub Secretsに保存します:

1. リポジトリの「Settings」→「Secrets and variables」→「Actions」
2. 「New repository secret」をクリック
3. 以下を追加:
   - `ANTHROPIC_API_KEY`: Anthropic APIキー
   - `API_URL`: デプロイしたバックエンドAPIのURL

### フロントエンドの設定

バックエンドAPIのURLを設定:

```javascript
// frontend/src/ChatWidget.tsx の apiUrl を変更
const ChatWidget: React.FC<ChatWidgetProps> = ({
  apiUrl = 'https://your-api-url.com'  // ← ここを変更
}) => {
```

---

## 8. デプロイ後の確認

### チェックリスト

- [ ] GitHubリポジトリにすべてのファイルがプッシュされている
- [ ] GitHub Actionsのワークフローがすべて成功している
- [ ] GitHub Pagesでフロントエンドが表示される
- [ ] バックエンドAPIがデプロイされて動作している
- [ ] チャットボットが正常に動作する

### テスト方法

1. **フロントエンドのテスト**:
   - GitHub PagesのURLにアクセス
   - チャットウィジェットが表示されるか確認

2. **バックエンドAPIのテスト**:
   ```bash
   curl https://your-api-url.com/
   ```
   正常に応答が返ってくることを確認

3. **統合テスト**:
   - チャットウィジェットでメッセージを送信
   - 正常に応答が返ってくることを確認

---

## 9. 継続的デプロイ

コードを変更してGitHubにプッシュすると、自動的に再デプロイされます:

```bash
# コードを変更
nano frontend/src/ChatWidget.tsx

# 変更をコミット
git add .
git commit -m "Update chat widget design"

# GitHubにプッシュ
git push

# GitHub Actionsが自動的に実行され、デプロイされます
```

---

## 🎉 完了!

これで、チャットボットシステムがGitHubにデプロイされました!

- **リポジトリ**: `https://github.com/your-username/comman-chatbot`
- **フロントエンド**: `https://your-username.github.io/comman-chatbot/`
- **バックエンド**: デプロイ先によって異なります

---

## 📞 トラブルシューティング

### GitHub Actionsが失敗する

1. 「Actions」タブでエラーログを確認
2. 依存関係のインストールエラーの場合:
   - `package-lock.json` を削除して再生成
   - `npm install` を実行してコミット

### GitHub Pagesが404エラー

1. 「Settings」→「Pages」で設定を確認
2. ワークフローが正常に完了しているか確認
3. 数分待ってから再度アクセス

### カスタムドメインが動作しない

1. DNSレコードが正しく設定されているか確認
2. DNS伝播に最大48時間かかることがあります
3. `CNAME` ファイルが正しく設定されているか確認

---

**Happy Deploying! 🚀**
