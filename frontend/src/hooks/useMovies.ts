import { useState, useEffect, useCallback } from 'react';
import { movieApi } from '../api';
import type { Movie, MovieListResponse, PaginationParams, ApiError, LoadingState } from '../types';

/**
 * Hook: 獲取電影列表
 */
export function useMovies(params: PaginationParams = {}) {
  const [data, setData] = useState<MovieListResponse | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<ApiError | null>(null);

  const fetchMovies = useCallback(async () => {
    setLoading('loading');
    setError(null);

    try {
      const response = await movieApi.getMovies(params);
      setData(response);
      setLoading('success');
    } catch (err) {
      setError(err as ApiError);
      setLoading('error');
    }
  }, [JSON.stringify(params)]);

  useEffect(() => {
    fetchMovies();
  }, [fetchMovies]);

  return {
    movies: data?.movies || [],
    total: data?.total || 0,
    page: data?.page || 1,
    pageSize: data?.page_size || 20,
    loading,
    error,
    refetch: fetchMovies,
  };
}

/**
 * Hook: 獲取單一電影詳情
 */
export function useMovie(id: string | null) {
  const [movie, setMovie] = useState<Movie | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    if (!id) return;

    const fetchMovie = async () => {
      setLoading('loading');
      setError(null);

      try {
        const data = await movieApi.getMovieById(id);
        setMovie(data);
        setLoading('success');
      } catch (err) {
        setError(err as ApiError);
        setLoading('error');
      }
    };

    fetchMovie();
  }, [id]);

  return { movie, loading, error };
}

/**
 * Hook: 獲取所有電影類型
 */
export function useGenres() {
  const [genres, setGenres] = useState<string[]>([]);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<ApiError | null>(null);

  useEffect(() => {
    const fetchGenres = async () => {
      setLoading('loading');
      setError(null);

      try {
        const data = await movieApi.getGenres();
        setGenres(data.map(g => g.name));
        setLoading('success');
      } catch (err) {
        setError(err as ApiError);
        setLoading('error');
      }
    };

    fetchGenres();
  }, []);

  return { genres, loading, error };
}
