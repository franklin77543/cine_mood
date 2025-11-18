import { useState } from 'react';
import { AISearchBox, MovieCard, LoadingSkeleton } from '../components/common';
import { SimpleMovieCard } from '../components/common/MovieCard';
import { useMovies, useAIRecommendation } from '../hooks';
import type { Movie } from '../types';

export function HomePage() {
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [userQuery, setUserQuery] = useState('');

  // 獲取熱門電影
  const { movies: popularMovies, loading: popularLoading } = useMovies({
    page: 1,
    page_size: 6,
    sort_by: 'rating',
  });

  // AI 推薦hook
  const { recommendations, intent, loading: aiLoading, getRecommendations } = useAIRecommendation();

  const handleSearch = async (query: string) => {
    setUserQuery(query);
    setShowRecommendations(true);

    try {
      await getRecommendations({ query, top_k: 5 });
      
      // 滾動到推薦區
      setTimeout(() => {
        document.getElementById('recommendation-section')?.scrollIntoView({
          behavior: 'smooth',
        });
      }, 100);
    } catch (error) {
      console.error('AI 推薦失敗:', error);
    }
  };

  return (
    <div>
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* 背景漸變 */}
        <div className="absolute inset-0 gradient-hero opacity-20"></div>

        {/* 背景模糊電影圖 */}
        <div className="absolute inset-0 opacity-10">
          <div
            className="w-full h-full bg-cover bg-center"
            style={{
              backgroundImage: "url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920')",
            }}
          ></div>
        </div>

        {/* 內容 */}
        <div className="relative z-10 container mx-auto px-6 text-center">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 fade-in-up">今天想看什麼？</h1>
          <p className="text-xl md:text-2xl text-slate-300 mb-12 fade-in-up" style={{ animationDelay: '0.1s' }}>
            告訴我你的心情，讓 AI 為你找到最適合的電影
          </p>

          {/* AI 搜尋框 */}
          <div className="fade-in-up" style={{ animationDelay: '0.2s' }}>
            <AISearchBox onSearch={handleSearch} loading={aiLoading === 'loading'} />
          </div>
        </div>
      </section>

      {/* AI 推薦結果 */}
      {showRecommendations && (
        <section id="recommendation-section" className="py-20 bg-slate-900">
          <div className="container mx-auto px-6">
            {/* AI 分析結果 */}
            {intent && (
              <div className="max-w-4xl mx-auto mb-12 fade-in-up">
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700 rounded-2xl p-6">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-gradient-ai rounded-full flex items-center justify-center pulse-ai">
                        🤖
                      </div>
                    </div>
                    <div className="flex-1">
                      <p className="text-slate-400 mb-3">
                        💭 你說: <span className="text-white font-medium">{userQuery}</span>
                      </p>
                      <div className="bg-slate-900/50 rounded-lg p-4">
                        <p className="text-sm text-slate-300 mb-2">🧠 AI 理解:</p>
                        <div className="flex flex-wrap gap-2">
                          {intent.mood && (
                            <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">
                              心情: {intent.mood}
                            </span>
                          )}
                          {intent.genres && intent.genres.length > 0 && (
                            <span className="px-3 py-1 bg-secondary/20 text-secondary rounded-full text-sm">
                              類型: {intent.genres.join('、')}
                            </span>
                          )}
                          {intent.keywords && intent.keywords.length > 0 && (
                            <span className="px-3 py-1 bg-accent/20 text-accent rounded-full text-sm">
                              關鍵字: {intent.keywords.join('、')}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 推薦卡片 */}
            {aiLoading === 'loading' ? (
              <LoadingSkeleton />
            ) : (
              <>
                <h2 className="text-3xl font-bold text-center mb-12">
                  ✨ 為你推薦 <span className="text-primary">{recommendations.length}</span> 部電影
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
                  {recommendations
                    .filter(rec => rec && rec.movie_id && rec.title) // 過濾無效資料
                    .map((rec, index) => {
                      // Convert flat recommendation to Movie object for MovieCard
                      const movie: Movie = {
                        id: rec.movie_id,
                        title: rec.title,
                        genres: rec.genres?.map(name => ({ id: 0, name })) || [],
                        overview: rec.overview,
                        release_date: rec.release_date,
                        poster_path: rec.poster_path,
                        backdrop_path: rec.backdrop_path,
                        vote_average: rec.vote_average,
                        popularity: rec.popularity
                      };
                      
                      return (
                        <div key={rec.movie_id} className="fade-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
                          <MovieCard
                            movie={movie}
                            reason={rec.reason}
                            similarityScore={rec.similarity_score}
                          />
                        </div>
                      );
                    })}
                </div>
              </>
            )}
          </div>
        </section>
      )}

      {/* 熱門推薦 */}
      <section className="py-20 bg-slate-950/50">
        <div className="container mx-auto px-6">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold">🔥 熱門推薦</h2>
            <button className="text-primary hover:text-indigo-400 transition">查看全部 →</button>
          </div>

          {popularLoading === 'loading' ? (
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {[1, 2, 3, 4, 5, 6].map((i) => (
                <div key={i} className="bg-slate-800 rounded-xl h-80 animate-pulse"></div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {popularMovies
                .filter(movie => movie && movie.id) // 過濾無效的電影資料
                .map((movie) => (
                  <SimpleMovieCard key={movie.id} movie={movie} />
                ))}
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
