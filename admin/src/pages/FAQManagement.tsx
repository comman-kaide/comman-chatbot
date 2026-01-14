import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface FAQ {
  id: number;
  question: string;
  answer: string;
  category: string | null;
  tags: string[] | null;
  is_active: boolean;
}

const FAQManagement: React.FC = () => {
  const [faqs, setFaqs] = useState<FAQ[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editingFaq, setEditingFaq] = useState<FAQ | null>(null);
  const [formData, setFormData] = useState({
    question: '',
    answer: '',
    category: '',
    is_active: true,
  });

  useEffect(() => {
    fetchFaqs();
  }, []);

  const fetchFaqs = async () => {
    try {
      const response = await axios.get('/api/admin/faqs');
      setFaqs(response.data);
    } catch (error) {
      console.error('FAQ取得エラー:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (editingFaq) {
        await axios.put(`/api/admin/faqs/${editingFaq.id}`, formData);
      } else {
        await axios.post('/api/admin/faqs', formData);
      }
      setShowModal(false);
      setFormData({ question: '', answer: '', category: '', is_active: true });
      setEditingFaq(null);
      fetchFaqs();
    } catch (error) {
      console.error('保存エラー:', error);
    }
  };

  const handleEdit = (faq: FAQ) => {
    setEditingFaq(faq);
    setFormData({
      question: faq.question,
      answer: faq.answer,
      category: faq.category || '',
      is_active: faq.is_active,
    });
    setShowModal(true);
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('このFAQを削除しますか?')) {
      try {
        await axios.delete(`/api/admin/faqs/${id}`);
        fetchFaqs();
      } catch (error) {
        console.error('削除エラー:', error);
      }
    }
  };

  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-gray-900">FAQ管理</h1>
        <button
          onClick={() => {
            setEditingFaq(null);
            setFormData({ question: '', answer: '', category: '', is_active: true });
            setShowModal(true);
          }}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
        >
          + FAQ追加
        </button>
      </div>

      {isLoading ? (
        <div className="text-center py-12">読み込み中...</div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {faqs.map((faq) => (
              <li key={faq.id} className="px-6 py-4 hover:bg-gray-50">
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="text-lg font-medium text-gray-900">{faq.question}</h3>
                    <p className="mt-1 text-sm text-gray-500">{faq.answer.substring(0, 100)}...</p>
                    {faq.category && (
                      <span className="mt-2 inline-block px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                        {faq.category}
                      </span>
                    )}
                  </div>
                  <div className="ml-4 flex space-x-2">
                    <button
                      onClick={() => handleEdit(faq)}
                      className="px-3 py-1 text-sm text-indigo-600 hover:text-indigo-900"
                    >
                      編集
                    </button>
                    <button
                      onClick={() => handleDelete(faq.id)}
                      className="px-3 py-1 text-sm text-red-600 hover:text-red-900"
                    >
                      削除
                    </button>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* モーダル */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <h2 className="text-2xl font-bold mb-4">
              {editingFaq ? 'FAQ編集' : 'FAQ追加'}
            </h2>
            <form onSubmit={handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700">質問</label>
                  <input
                    type="text"
                    required
                    value={formData.question}
                    onChange={(e) => setFormData({ ...formData, question: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">回答</label>
                  <textarea
                    required
                    rows={6}
                    value={formData.answer}
                    onChange={(e) => setFormData({ ...formData, answer: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">カテゴリ</label>
                  <input
                    type="text"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2"
                  />
                </div>
                <div className="flex items-center">
                  <input
                    type="checkbox"
                    checked={formData.is_active}
                    onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                    className="h-4 w-4 text-indigo-600"
                  />
                  <label className="ml-2 text-sm text-gray-700">有効</label>
                </div>
              </div>
              <div className="mt-6 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
                >
                  キャンセル
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
                >
                  保存
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default FAQManagement;
