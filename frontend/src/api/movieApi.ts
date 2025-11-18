import apiClient from './client';
import type {
  Movie,
  MovieListResponse,
  Genre,
  PaginationParams,
} from '../types';

/**
 * 電影 API Service
 * 負責所有電影相關的 API 呼叫
 */
class MovieApiService {
  private readonly basePath = '/api/v1/movies';

  /**
   * 獲取電影列表 (支援分頁、篩選、排序)
   */
  async getMovies(params: PaginationParams = {}): Promise<MovieListResponse> {
    const response = await apiClient.get<MovieListResponse>(this.basePath, {
      params: {
        page: params.page || 1,
        page_size: params.page_size || 20,
        genre: params.genre,
        min_rating: params.min_rating,
        sort_by: params.sort_by || 'rating',
      },
    });
    return response.data;
  }

  /**
   * 根據 ID 獲取單一電影詳情
   */
  async getMovieById(id: string): Promise<Movie> {
    const response = await apiClient.get<Movie>(`${this.basePath}/${id}`);
    return response.data;
  }

  /**
   * 獲取所有電影類型
   */
  async getGenres(): Promise<Genre[]> {
    const response = await apiClient.get<Genre[]>('/api/v1/genres');
    return response.data;
  }

  /**
   * 搜尋電影 (關鍵字搜尋)
   */
  async searchMovies(query: string, params: PaginationParams = {}): Promise<MovieListResponse> {
    const response = await apiClient.get<MovieListResponse>(`${this.basePath}/search`, {
      params: {
        q: query,
        page: params.page || 1,
        page_size: params.page_size || 20,
      },
    });
    return response.data;
  }
}

// 匯出單例
export const movieApi = new MovieApiService();
