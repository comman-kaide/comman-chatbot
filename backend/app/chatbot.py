from anthropic import Anthropic
from app.config import settings
from app.rag import rag_system
from typing import List, Dict

class ChatbotService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_response(self, user_message: str, session_history: List[Dict] = None) -> tuple[str, List[Dict]]:
        """
        ユーザーメッセージに対して応答を生成
        Returns: (response_text, context_used)
        """
        # RAGで関連情報を検索
        relevant_docs = rag_system.search(user_message, n_results=3)

        # コンテキストを構築
        context = self._build_context(relevant_docs)

        # システムプロンプトを構築
        system_prompt = self._build_system_prompt(context)

        # 会話履歴を構築
        messages = self._build_messages(user_message, session_history)

        # Claude APIを呼び出し
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2000,
            system=system_prompt,
            messages=messages
        )

        response_text = response.content[0].text

        # 使用したコンテキストを返す
        context_used = [
            {
                'document': doc['document'][:200] + '...',
                'metadata': doc['metadata']
            }
            for doc in relevant_docs
        ]

        return response_text, context_used

    def _build_context(self, relevant_docs: List[Dict]) -> str:
        """関連ドキュメントからコンテキストを構築"""
        if not relevant_docs:
            return "関連情報が見つかりませんでした。"

        context_parts = []
        for i, doc in enumerate(relevant_docs, 1):
            metadata = doc.get('metadata', {})
            source = metadata.get('source', '不明')
            context_parts.append(f"【参考情報{i}】({source})\n{doc['document']}")

        return "\n\n".join(context_parts)

    def _build_system_prompt(self, context: str) -> str:
        """システムプロンプトを構築"""
        return f"""あなたは株式会社カンマンの公式チャットボットアシスタントです。

【会社概要】
株式会社カンマンは、生成AIとブランディングで企業の競争力を高めるAI導入支援パートナーです。
主に徳島県を中心に地方の中小企業向けにサービスを提供しています。

【主要サービス】
1. 生成AI研修 - 生成AIの基本知識と実務的な活用方法を教育
2. ホームページ制作 - 目標設定から成果に繋がるサイト制作
3. システム開発 - 業務効率化やデジタル化推進のためのシステム・アプリ開発
4. ブランディング研修 - 企業の独自性と目指す姿を導き出す支援
5. その他 - 集客コンサルティング、Web・SNS広告運用、動画制作、保守サービス

【会社情報】
- 所在地: 徳島県
- 電話: 088-611-2333
- 営業時間: 平日 9:30～18:00
- 実績: 徳島県内で500プロジェクト以上のホームページ制作実績

【対応方針】
- 丁寧で親しみやすい日本語で応答してください
- 専門用語は必要に応じて分かりやすく説明してください
- 以下の参考情報を活用して、具体的で正確な回答を心がけてください
- 分からないことは正直に「確認が必要です」と答え、お問い合わせへの誘導を提案してください
- お問い合わせ先: 088-611-2333 (平日 9:30～18:00)

【参考情報】
{context}

上記の参考情報を基に、ユーザーの質問に適切に回答してください。"""

    def _build_messages(self, user_message: str, session_history: List[Dict] = None) -> List[Dict]:
        """会話履歴を含むメッセージリストを構築"""
        messages = []

        # 過去の会話履歴を追加(最大5件)
        if session_history:
            for history in session_history[-5:]:
                messages.append({
                    "role": "user",
                    "content": history.get("user_message", "")
                })
                messages.append({
                    "role": "assistant",
                    "content": history.get("bot_response", "")
                })

        # 現在のユーザーメッセージを追加
        messages.append({
            "role": "user",
            "content": user_message
        })

        return messages

# シングルトンインスタンス
chatbot_service = ChatbotService()
