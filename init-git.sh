#!/bin/bash

# Git初期化とGitHubへのプッシュスクリプト
# 使用方法: ./init-git.sh https://github.com/your-username/comman-chatbot.git

set -e  # エラーが発生したら停止

echo "=========================================="
echo "  Git リポジトリ初期化スクリプト"
echo "=========================================="
echo ""

# 引数チェック
if [ -z "$1" ]; then
    echo "❌ エラー: GitHubリポジトリのURLを指定してください"
    echo ""
    echo "使用方法:"
    echo "  ./init-git.sh https://github.com/your-username/comman-chatbot.git"
    echo ""
    exit 1
fi

REPO_URL=$1

echo "📋 ステップ 1/5: Gitリポジトリを初期化中..."
if [ -d ".git" ]; then
    echo "⚠️  既存の .git ディレクトリが見つかりました"
    read -p "削除して再初期化しますか? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf .git
        git init
        echo "✅ Gitリポジトリを再初期化しました"
    else
        echo "ℹ️  既存のGitリポジトリを使用します"
    fi
else
    git init
    echo "✅ Gitリポジトリを初期化しました"
fi

echo ""
echo "📋 ステップ 2/5: ファイルをステージング中..."
git add .
echo "✅ すべてのファイルをステージングしました"

echo ""
echo "📋 ステップ 3/5: 最初のコミットを作成中..."
git commit -m "Initial commit: Complete chatbot system

- FastAPI backend with Claude API integration
- RAG system with ChromaDB
- React frontend chat widget
- React admin panel with Tailwind CSS
- Docker Compose configuration
- GitHub Actions workflows
- Complete documentation"
echo "✅ コミットを作成しました"

echo ""
echo "📋 ステップ 4/5: mainブランチに変更中..."
git branch -M main
echo "✅ ブランチをmainに変更しました"

echo ""
echo "📋 ステップ 5/5: リモートリポジトリを追加してプッシュ中..."
git remote add origin "$REPO_URL"

echo "🚀 GitHubにプッシュしています..."
git push -u origin main

echo ""
echo "=========================================="
echo "  ✅ デプロイ完了!"
echo "=========================================="
echo ""
echo "次のステップ:"
echo "1. GitHubリポジトリページにアクセス: $REPO_URL"
echo "2. Settings → Pages でGitHub Pagesを有効化"
echo "3. Actions タブでワークフローの実行状態を確認"
echo ""
echo "詳細は GITHUB_DEPLOY.md を参照してください"
echo ""
