import { useState, useCallback, useEffect } from 'react';
import { aiApi } from '../api';
import type {
  AIRecommendationRequest,
  AIRecommendationResponse,
  AISearchRequest,
  AISearchResponse,
  SimilarMoviesResponse,
  ApiError,
  LoadingState,
} from '../types';

/**
 * Hook: AI 智能推薦
 */
export function useAIRecommendation() {
  const [data, setData] = useState<AIRecommendationResponse | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<ApiError | null>(null);

  const getRecommendations = useCallback(async (request: AIRecommendationRequest) => {
    setLoading('loading');
    setError(null);

    try {
      const response = await aiApi.getRecommendations(request);
      setData(response);
      setLoading('success');
      return response;
    } catch (err) {
      setError(err as ApiError);
      setLoading('error');
      throw err;
    }
  }, []);

  return {
    recommendations: data?.recommendations || [],
    intent: data?.intent,
    loading,
    error,
    getRecommendations,
  };
}

/**
 * Hook: AI 語義搜尋
 */
export function useAISearch() {
  const [data, setData] = useState<AISearchResponse | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<ApiError | null>(null);

  const search = useCallback(async (request: AISearchRequest) => {
    setLoading('loading');
    setError(null);

    try {
      const response = await aiApi.semanticSearch(request);
      setData(response);
      setLoading('success');
      return response;
    } catch (err) {
      setError(err as ApiError);
      setLoading('error');
      throw err;
    }
  }, []);

  return {
    results: data?.results || [],
    loading,
    error,
    search,
  };
}

/**
 * Hook: 獲取相似電影
 */
export function useSimilarMovies(movieId: string | null, topK: number = 5) {
  const [data, setData] = useState<SimilarMoviesResponse | null>(null);
  const [loading, setLoading] = useState<LoadingState>('idle');
  const [error, setError] = useState<ApiError | null>(null);

  const fetchSimilar = useCallback(async () => {
    if (!movieId) return;

    setLoading('loading');
    setError(null);

    try {
      const response = await aiApi.getSimilarMovies(movieId, topK);
      setData(response);
      setLoading('success');
    } catch (err) {
      setError(err as ApiError);
      setLoading('error');
    }
  }, [movieId, topK]);

  useEffect(() => {
    fetchSimilar();
  }, [fetchSimilar]);

  return {
    sourceMovie: data?.source_movie,
    similarMovies: data?.similar_movies || [],
    loading,
    error,
    refetch: fetchSimilar,
  };
}
