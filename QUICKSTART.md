# クイックスタートガイド

このガイドに従って、チャットボットシステムをすぐに起動できます。

## 🚀 5分で起動

### 前提条件

- Docker と Docker Compose がインストールされていること
- Anthropic API キーを取得済みであること

### 手順

#### 1. 環境変数の設定

```bash
# プロジェクトルートに移動
cd comman-chatbot

# .envファイルを作成
cp .env.example .env

# .envファイルを編集
nano .env
```

以下を設定:
```env
DB_PASSWORD=your_secure_password
ANTHROPIC_API_KEY=sk-ant-xxxxx  # ← あなたのAPIキー
SECRET_KEY=random_long_secret_string_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001,https://comman.co.jp
```

#### 2. Docker Composeで起動

```bash
# すべてのサービスを起動
docker-compose up -d

# ログを確認
docker-compose logs -f
```

起動完了まで約30秒〜1分かかります。

#### 3. 管理者ユーザーの作成

```bash
# バックエンドコンテナに入る
docker-compose exec backend bash

# 管理者ユーザー作成スクリプトを実行
python create_admin.py

# コンテナから出る
exit
```

表示される情報を記録してください:
- ユーザー名
- パスワード
- メールアドレス

#### 4. 動作確認

以下のURLにアクセス:

- **バックエンドAPI**: http://localhost:8000
- **APIドキュメント**: http://localhost:8000/docs
- **管理画面**: http://localhost:3001

#### 5. 管理画面にログイン

1. http://localhost:3001 にアクセス
2. 作成した管理者ユーザー名とパスワードでログイン
3. ログイン成功!

#### 6. FAQを追加

1. 「FAQ管理」をクリック
2. 「+ FAQ追加」をクリック
3. 以下の例を入力:

**質問**: カンマンの営業時間を教えてください
**回答**: 株式会社カンマンの営業時間は、平日9:30〜18:00です。土日祝日はお休みをいただいております。
**カテゴリ**: 営業情報

4. 「保存」をクリック

#### 7. チャットボットをテスト

フロントエンドを起動してテスト:

```bash
# 新しいターミナルを開く
cd frontend

# 依存関係をインストール (初回のみ)
npm install

# 開発サーバーを起動
npm run dev
```

http://localhost:3000 にアクセスして、デモページでチャットボットをテスト!

## 📦 本番環境へのデプロイ

### 1. フロントエンドのビルド

```bash
cd frontend
npm run build
```

`dist/chatbot-widget.js` が生成されます。

### 2. 管理画面のビルド

```bash
cd admin

# APIのURLを本番環境に変更
echo "VITE_API_URL=https://api.comman.co.jp" > .env

npm run build
```

`dist/` フォルダが生成されます。

### 3. ホームページへの埋め込み

`embed-code.html` のコードを参考に、あなたのホームページの `</body>` タグの直前に以下を追加:

```html
<script
  src="https://your-cdn.com/chatbot-widget.js"
  data-comman-chatbot
  data-api-url="https://api.comman.co.jp"
  async
></script>
```

## 🛠️ トラブルシューティング

### コンテナが起動しない

```bash
# ログを確認
docker-compose logs

# 特定のサービスのログを確認
docker-compose logs backend
docker-compose logs db
```

### データベース接続エラー

```bash
# データベースの状態を確認
docker-compose ps

# データベースに接続できるか確認
docker-compose exec db psql -U postgres -d comman_chatbot
```

### ポートが使用中

別のポートを使用する場合、`docker-compose.yml` を編集:

```yaml
services:
  backend:
    ports:
      - "8001:8000"  # 8000 → 8001に変更
```

### すべてをリセットして再起動

```bash
# すべてのコンテナとボリュームを削除
docker-compose down -v

# 再起動
docker-compose up -d

# 管理者ユーザーを再作成
docker-compose exec backend python create_admin.py
```

## 📚 次のステップ

1. **FAQを充実させる**: より多くのFAQを追加
2. **ドキュメントを追加**: サービス紹介資料などを登録
3. **チャット履歴を確認**: ユーザーの質問傾向を分析
4. **デザインをカスタマイズ**: `frontend/src/ChatWidget.css` を編集

## 💡 ヒント

- **FAQのカテゴリ分け**: カテゴリを設定することで検索精度が向上します
- **定期的なバックアップ**: PostgreSQLとChromaDBのバックアップを忘れずに
- **ログの監視**: `docker-compose logs -f` でリアルタイムログを確認

## 📞 サポート

問題が解決しない場合は、README.mdの「トラブルシューティング」セクションを確認するか、開発チームにお問い合わせください。

---

**Happy Chatting! 🎉**
