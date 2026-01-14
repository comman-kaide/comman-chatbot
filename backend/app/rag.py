import chromadb
from chromadb.config import Settings as ChromaSettings
from sentence_transformers import SentenceTransformer
from typing import List, Dict
from app.config import settings
import uuid

class RAGSystem:
    def __init__(self):
        self.client = chromadb.Client(ChromaSettings(
            persist_directory=settings.chroma_persist_directory,
            anonymized_telemetry=False
        ))

        # 既存のコレクションを取得または新規作成
        try:
            self.collection = self.client.get_collection(name="comman_knowledge")
        except:
            self.collection = self.client.create_collection(
                name="comman_knowledge",
                metadata={"description": "株式会社カンマンの知識ベース"}
            )

        self.embedding_model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    def add_document(self, text: str, metadata: Dict = None, doc_id: str = None):
        """ドキュメントを追加"""
        if doc_id is None:
            doc_id = str(uuid.uuid4())

        # テキストを埋め込みに変換
        embedding = self.embedding_model.encode(text).tolist()

        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            ids=[doc_id]
        )
        return doc_id

    def add_documents_batch(self, texts: List[str], metadatas: List[Dict] = None):
        """複数のドキュメントをバッチで追加"""
        doc_ids = [str(uuid.uuid4()) for _ in texts]
        embeddings = self.embedding_model.encode(texts).tolist()

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas or [{} for _ in texts],
            ids=doc_ids
        )
        return doc_ids

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        """類似ドキュメントを検索"""
        query_embedding = self.embedding_model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # 結果を整形
        search_results = []
        if results['documents'] and len(results['documents']) > 0:
            for i, doc in enumerate(results['documents'][0]):
                search_results.append({
                    'document': doc,
                    'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                    'distance': results['distances'][0][i] if results['distances'] else None
                })

        return search_results

    def delete_document(self, doc_id: str):
        """ドキュメントを削除"""
        self.collection.delete(ids=[doc_id])

    def update_document(self, doc_id: str, text: str, metadata: Dict = None):
        """ドキュメントを更新"""
        self.delete_document(doc_id)
        return self.add_document(text, metadata, doc_id)

# シングルトンインスタンス
rag_system = RAGSystem()
