import { useState, type FormEvent } from 'react';

export interface AISearchBoxProps {
  onSearch: (query: string) => void;
  loading?: boolean;
}

const MOOD_SUGGESTIONS = [
  { emoji: '😊', label: '輕鬆', query: '輕鬆搞笑的週末電影' },
  { emoji: '😢', label: '療癒', query: '我心情不好，想看療癒的電影' },
  { emoji: '🔥', label: '刺激', query: '刺激的動作冒險片' },
  { emoji: '🌿', label: '平靜', query: '平靜的奇幻故事' },
  { emoji: '🤔', label: '深度', query: '讓人思考的深度劇情' },
];

export function AISearchBox({ onSearch, loading = false }: AISearchBoxProps) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  const handleMoodClick = (moodQuery: string) => {
    setQuery(moodQuery);
    // 可選：自動觸發搜尋
    // onSearch(moodQuery);
  };

  return (
    <div className="max-w-3xl mx-auto">
      {/* 輸入框 */}
      <form onSubmit={handleSubmit} className="relative mb-8">
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full px-6 py-4 bg-slate-800/50 backdrop-blur-sm border-2 border-slate-700 rounded-2xl text-lg resize-none focus:outline-none focus:border-primary transition"
          rows={3}
          placeholder="💬 告訴我你的心情，或想看什麼電影..."
          disabled={loading}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSubmit(e);
            }
          }}
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="absolute bottom-4 right-4 px-6 py-2 gradient-ai text-white rounded-lg hover:opacity-90 transition font-medium disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <span className="flex items-center space-x-2">
              <span className="animate-spin">⚙️</span>
              <span>思考中...</span>
            </span>
          ) : (
            'AI 推薦'
          )}
        </button>
      </form>

      <p className="text-center text-sm text-slate-400 mb-6">
        💡 例如: "輕鬆搞笑的週末電影" 或 "關於時間旅行的科幻片"
      </p>

      {/* 心情快捷按鈕 */}
      <div className="flex flex-wrap justify-center gap-3">
        {MOOD_SUGGESTIONS.map((mood) => (
          <button
            key={mood.label}
            onClick={() => handleMoodClick(mood.query)}
            className="px-6 py-3 bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-full hover:border-primary hover:bg-primary/10 transition"
          >
            <span className="mr-2">{mood.emoji}</span>
            {mood.label}
          </button>
        ))}
      </div>
    </div>
  );
}
