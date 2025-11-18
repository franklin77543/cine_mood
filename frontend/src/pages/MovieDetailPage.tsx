import { useParams } from 'react-router-dom';
import { useEffect } from 'react';
import { useMovie, useSimilarMovies } from '../hooks';
import { LoadingSpinner, SimpleMovieCard } from '../components/common';
import type { Movie } from '../types';

export function MovieDetailPage() {
  const { id } = useParams<{ id: string }>();
  const movieId = id || null;

  const { movie, loading, error } = useMovie(movieId);
  const { similarMovies } = useSimilarMovies(movieId, 5);

  // 當電影 ID 改變時，滾動到頂部
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [movieId]);

  if (loading === 'loading') {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error || !movie) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-2xl text-slate-400">電影不存在</p>
        </div>
      </div>
    );
  }

  const posterUrl = movie.poster_path 
    ? `https://image.tmdb.org/t/p/w780${movie.poster_path}`
    : 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=1920';
  const backdropUrl = movie.backdrop_path
    ? `https://image.tmdb.org/t/p/original${movie.backdrop_path}`
    : posterUrl;
  const year = movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A';

  return (
    <section className="relative min-h-screen pt-24">
      {/* 背景模糊大圖 */}
      <div className="absolute inset-0 overflow-hidden">
        <div
          className="absolute inset-0 bg-cover bg-center blur-2xl scale-110"
          style={{ backgroundImage: `url(${backdropUrl})` }}
        ></div>
        <div className="absolute inset-0 bg-gradient-to-b from-slate-900/50 via-slate-900/80 to-slate-900"></div>
      </div>

      {/* 內容 */}
      <div className="relative z-10 container mx-auto px-6 py-12">
        <div className="max-w-6xl mx-auto">
          {/* 主要資訊 */}
          <div className="grid md:grid-cols-3 gap-8 mb-16">
            {/* 海報 */}
            <div className="md:col-span-1">
              <div className="sticky top-24">
                <img src={posterUrl} alt={movie.title} className="w-full rounded-2xl shadow-2xl" />

                <div className="mt-6 space-y-3">
                  <button className="w-full px-6 py-3 bg-primary hover:bg-indigo-600 rounded-xl font-medium transition">
                    ▶ 觀看預告
                  </button>
                  <button className="w-full px-6 py-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl font-medium transition">
                    ♡ 加入片單
                  </button>
                </div>
              </div>
            </div>

            {/* 詳細資訊 */}
            <div className="md:col-span-2">
              <h1 className="text-5xl font-bold mb-4">{movie.title}</h1>
              {movie.original_title && movie.original_title !== movie.title && (
                <p className="text-2xl text-slate-400 mb-6">{movie.original_title}</p>
              )}

              {/* 評分與資訊 */}
              <div className="flex flex-wrap items-center gap-4 mb-8">
                <div className="flex items-center space-x-2">
                  <span className="text-4xl">⭐</span>
                  <div>
                    <div className="text-2xl font-bold">{movie.vote_average?.toFixed(1) || 'N/A'}</div>
                    <div className="text-xs text-slate-400">評分 ({movie.vote_count || 0} 票)</div>
                  </div>
                </div>

                <div className="h-12 w-px bg-slate-700"></div>

                <div className="text-slate-300">
                  <div className="text-sm text-slate-400">年份</div>
                  <div className="font-medium">{year}</div>
                </div>

                {movie.runtime && (
                  <>
                    <div className="h-12 w-px bg-slate-700"></div>
                    <div className="text-slate-300">
                      <div className="text-sm text-slate-400">時長</div>
                      <div className="font-medium">{movie.runtime} 分鐘</div>
                    </div>
                  </>
                )}

                {movie.genres && movie.genres.length > 0 && (
                  <>
                    <div className="h-12 w-px bg-slate-700"></div>
                    <div className="text-slate-300">
                      <div className="text-sm text-slate-400">類型</div>
                      <div className="flex gap-2">
                        {movie.genres.map((genre) => (
                          <span key={genre.id} className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">
                            {genre.name}
                          </span>
                        ))}
                      </div>
                    </div>
                  </>
                )}
              </div>

              {/* 劇情簡介 */}
              {movie.overview && (
                <div className="mb-8">
                  <h2 className="text-2xl font-bold mb-4">📝 劇情簡介</h2>
                  <p className="text-slate-300 leading-relaxed text-lg">{movie.overview}</p>
                </div>
              )}
            </div>
          </div>

          {/* 相似電影推薦 */}
          {similarMovies.length > 0 && (
            <div className="mb-16">
              <h2 className="text-3xl font-bold mb-8">🎬 相似電影 (AI 推薦)</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                {similarMovies.map((similar) => {
                  // Convert SimilarMovieItem to Movie for SimpleMovieCard
                  const movieData: Movie = {
                    id: similar.movie_id,
                    title: similar.title,
                    genres: similar.genres?.map(name => ({ id: 0, name })) || [],
                    overview: similar.overview,
                    poster_path: similar.poster_path,
                    backdrop_path: similar.backdrop_path
                  };
                  
                  return (
                    <div key={similar.movie_id} className="relative">
                      <SimpleMovieCard movie={movieData} />
                      <div className="absolute top-2 right-2 px-2 py-1 bg-black/70 backdrop-blur-sm rounded-full text-xs">
                        {(similar.similarity_score * 100).toFixed(0)}%
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
