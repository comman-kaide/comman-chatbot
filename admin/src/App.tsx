import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import axios from 'axios';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import FAQManagement from './pages/FAQManagement';
import DocumentManagement from './pages/DocumentManagement';
import ChatHistory from './pages/ChatHistory';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// Axiosのデフォルト設定
axios.defaults.baseURL = API_URL;

// 認証トークンをインターセプターで自動追加
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

const App: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // 認証状態を確認
    const token = localStorage.getItem('token');
    if (token) {
      // トークンの有効性を確認
      axios.get('/api/auth/me')
        .then(() => {
          setIsAuthenticated(true);
        })
        .catch(() => {
          localStorage.removeItem('token');
          setIsAuthenticated(false);
        })
        .finally(() => {
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, []);

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-xl text-gray-600">読み込み中...</div>
      </div>
    );
  }

  return (
    <Router>
      {!isAuthenticated ? (
        <Routes>
          <Route path="/login" element={<Login onLogin={handleLogin} />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      ) : (
        <div className="min-h-screen bg-gray-100">
          {/* ナビゲーションバー */}
          <nav className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16">
                <div className="flex items-center space-x-8">
                  <h1 className="text-xl font-bold">カンマンチャットボット管理</h1>
                  <div className="flex space-x-4">
                    <Link
                      to="/"
                      className="px-3 py-2 rounded-md text-sm font-medium hover:bg-white hover:bg-opacity-10 transition"
                    >
                      ダッシュボード
                    </Link>
                    <Link
                      to="/faqs"
                      className="px-3 py-2 rounded-md text-sm font-medium hover:bg-white hover:bg-opacity-10 transition"
                    >
                      FAQ管理
                    </Link>
                    <Link
                      to="/documents"
                      className="px-3 py-2 rounded-md text-sm font-medium hover:bg-white hover:bg-opacity-10 transition"
                    >
                      ドキュメント管理
                    </Link>
                    <Link
                      to="/history"
                      className="px-3 py-2 rounded-md text-sm font-medium hover:bg-white hover:bg-opacity-10 transition"
                    >
                      チャット履歴
                    </Link>
                  </div>
                </div>
                <div className="flex items-center">
                  <button
                    onClick={handleLogout}
                    className="px-4 py-2 rounded-md text-sm font-medium bg-white bg-opacity-20 hover:bg-opacity-30 transition"
                  >
                    ログアウト
                  </button>
                </div>
              </div>
            </div>
          </nav>

          {/* メインコンテンツ */}
          <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/faqs" element={<FAQManagement />} />
              <Route path="/documents" element={<DocumentManagement />} />
              <Route path="/history" element={<ChatHistory />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
      )}
    </Router>
  );
};

export default App;
