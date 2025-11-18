// ========== 電影相關類型 ==========

export interface Genre {
  id: number;
  name: string;
}

export interface Movie {
  id: string; // UUID from backend
  tmdb_id?: number;
  title: string;
  original_title?: string;
  release_date?: string;
  runtime?: number;
  overview?: string;
  poster_path?: string;
  backdrop_path?: string;
  vote_average?: number;
  vote_count?: number;
  popularity?: number;
  genres?: Genre[]; // Genre objects from backend
  created_at?: string;
  updated_at?: string;
}

export interface MovieListResponse {
  movies: Movie[];
  total: number;
  page: number;
  page_size: number;
}

// ========== AI 推薦相關類型 ==========

export interface AIIntent {
  mood?: string;
  genres?: string[];
  keywords?: string[];
}

export interface MovieRecommendation {
  movie_id: string;
  title: string;
  genres: string[];
  overview?: string;
  release_date?: string;
  poster_path?: string;
  backdrop_path?: string;
  vote_average?: number;
  popularity?: number;
  similarity_score: number;
  reason?: string;
}

export interface AIRecommendationRequest {
  query: string;
  top_k?: number;
  generate_reasons?: boolean;
}

export interface AIRecommendationResponse {
  query: string;
  intent: AIIntent;
  recommendations: MovieRecommendation[];
  total: number;
}

// ========== 語義搜尋類型 ==========

export interface SearchResult {
  movie_id: string;
  title: string;
  genres: string[];
  overview?: string;
  poster_path?: string;
  backdrop_path?: string;
  similarity_score: number;
}

export interface AISearchRequest {
  query: string;
  top_k?: number;
  filters?: {
    genres?: string[];
    min_rating?: number;
    year_from?: number;
    year_to?: number;
  };
}

export interface AISearchResponse {
  query: string;
  results: SearchResult[];
  total: number;
}

// ========== 相似電影類型 ==========

export interface SimilarMovieItem {
  movie_id: string;
  title: string;
  genres: string[];
  overview?: string;
  poster_path?: string;
  backdrop_path?: string;
  similarity_score: number;
}

export interface SourceMovie {
  movie_id: string;
  title: string;
  genres: string[];
}

export interface SimilarMoviesResponse {
  source_movie?: SourceMovie;
  similar_movies: SimilarMovieItem[];
  total: number;
}

// ========== UI 狀態類型 ==========

export type LoadingState = 'idle' | 'loading' | 'success' | 'error';

export interface ApiError {
  message: string;
  status?: number;
  detail?: string;
}

// ========== 分頁類型 ==========

export interface PaginationParams {
  page?: number;
  page_size?: number;
  genre?: string;
  min_rating?: number;
  sort_by?: 'rating' | 'year' | 'title';
}
