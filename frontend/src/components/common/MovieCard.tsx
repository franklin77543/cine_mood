import type { Movie } from '../../types';
import { Link } from 'react-router-dom';

export interface MovieCardProps {
  movie: Movie;
  reason?: string;
  similarityScore?: number;
  onClick?: () => void;
}

export function MovieCard({ movie, reason, similarityScore, onClick }: MovieCardProps) {
  const posterUrl = movie.poster_path 
    ? `https://image.tmdb.org/t/p/w500${movie.poster_path}`
    : 'https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400';

  // Extract year from release_date
  const year = movie.release_date ? new Date(movie.release_date).getFullYear() : 'N/A';

  return (
    <Link
      to={`/movie/${movie.id}`}
      className="card-hover bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 block"
      onClick={onClick}
    >
      {/* 海報 */}
      <div className="relative h-80 bg-gradient-to-br from-slate-700 to-slate-800">
        <img
          src={posterUrl}
          alt={movie.title}
          className="w-full h-full object-cover"
          loading="lazy"
        />
        <div className="absolute top-3 right-3 px-3 py-1 bg-black/70 backdrop-blur-sm rounded-full text-sm">
          ⭐ {movie.vote_average?.toFixed(1) || 'N/A'}
        </div>
      </div>

      {/* 資訊 */}
      <div className="p-5">
        <h3 className="text-xl font-bold mb-2 truncate">{movie.title}</h3>
        <div className="flex items-center space-x-2 text-sm text-slate-400 mb-3">
          <span>📅 {year}</span>
          <span>•</span>
          <span>🎭 {movie.genres?.map(g => g.name).join('、') || 'N/A'}</span>
        </div>

        {/* AI 推薦理由 */}
        {reason && (
          <div className="bg-slate-900/50 rounded-lg p-3 mb-4">
            <p className="text-xs text-slate-400 mb-1">💡 AI 推薦理由:</p>
            <p className="text-sm text-slate-200 line-clamp-3">{reason}</p>
          </div>
        )}

        {/* 相似度 */}
        {similarityScore !== undefined && (
          <div className="mb-4">
            <div className="flex justify-between text-xs text-slate-400 mb-1">
              <span>相似度</span>
              <span>{(similarityScore * 100).toFixed(0)}%</span>
            </div>
            <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
              <div
                className="h-full gradient-ai"
                style={{ width: `${similarityScore * 100}%` }}
              ></div>
            </div>
          </div>
        )}

        {/* 按鈕 */}
        <div className="flex space-x-2">
          <button className="flex-1 px-4 py-2 bg-primary hover:bg-indigo-600 rounded-lg text-sm transition">
            詳情
          </button>
          <button
            className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg text-sm transition"
            onClick={(e) => {
              e.preventDefault();
              // TODO: 加入片單功能
            }}
          >
            ♡
          </button>
        </div>
      </div>
    </Link>
  );
}

export function SimpleMovieCard({ movie, onClick }: { movie: Movie; onClick?: () => void }) {
  const posterUrl = movie.poster_path 
    ? `https://image.tmdb.org/t/p/w300${movie.poster_path}`
    : 'https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=300';

  return (
    <Link
      to={`/movie/${movie.id}`}
      className="card-hover bg-slate-800 rounded-xl overflow-hidden border border-slate-700 block"
      onClick={onClick}
    >
      <div className="relative h-60 bg-slate-700">
        <img src={posterUrl} alt={movie.title} className="w-full h-full object-cover" loading="lazy" />
      </div>
      <div className="p-3">
        <p className="font-medium truncate">{movie.title}</p>
        <p className="text-sm text-slate-400">⭐ {movie.vote_average?.toFixed(1) || 'N/A'}</p>
      </div>
    </Link>
  );
}
