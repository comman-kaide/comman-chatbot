import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface ChatRecord {
  id: number;
  session_id: string;
  user_message: string;
  bot_response: string;
  created_at: string;
}

const ChatHistory: React.FC = () => {
  const [history, setHistory] = useState<ChatRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await axios.get('/api/admin/chat-history');
      setHistory(response.data);
    } catch (error) {
      console.error('履歴取得エラー:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('ja-JP');
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">チャット履歴</h1>

      {isLoading ? (
        <div className="text-center py-12">読み込み中...</div>
      ) : (
        <div className="space-y-4">
          {history.map((record) => (
            <div key={record.id} className="bg-white shadow rounded-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <span className="text-xs text-gray-500">
                  セッションID: {record.session_id}
                </span>
                <span className="text-xs text-gray-500">
                  {formatDate(record.created_at)}
                </span>
              </div>
              <div className="space-y-3">
                <div className="bg-blue-50 p-4 rounded-lg">
                  <p className="text-sm font-medium text-blue-900 mb-1">ユーザー:</p>
                  <p className="text-gray-700">{record.user_message}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-sm font-medium text-gray-900 mb-1">ボット:</p>
                  <p className="text-gray-700">{record.bot_response}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default ChatHistory;
