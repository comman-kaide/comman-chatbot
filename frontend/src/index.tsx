import React from 'react';
import ReactDOM from 'react-dom/client';
import ChatWidget from './ChatWidget';

// グローバルに公開するための関数
(window as any).initCommanChatbot = function(config: any = {}) {
  const container = document.createElement('div');
  container.id = 'comman-chatbot-container';
  document.body.appendChild(container);

  const root = ReactDOM.createRoot(container);
  root.render(
    <React.StrictMode>
      <ChatWidget apiUrl={config.apiUrl} />
    </React.StrictMode>
  );
};

// 自動初期化(data-auto-init属性がある場合)
document.addEventListener('DOMContentLoaded', () => {
  const script = document.querySelector('script[data-comman-chatbot]');
  if (script) {
    const apiUrl = script.getAttribute('data-api-url');
    (window as any).initCommanChatbot({ apiUrl });
  }
});
