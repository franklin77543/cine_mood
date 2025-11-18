import apiClient from './client';
import type {
  AIRecommendationRequest,
  AIRecommendationResponse,
  AISearchRequest,
  AISearchResponse,
  SimilarMoviesResponse,
} from '../types';

/**
 * AI API Service
 * 負責所有 AI 推薦相關的 API 呼叫
 */
class AIApiService {
  private readonly basePath = '/api/v1/ai';

  /**
   * 智能推薦 (LLM + Vector Search)
   * 輸入: 自然語言查詢
   * 輸出: 推薦電影 + AI 理由 + 相似度
   */
  async getRecommendations(
    request: AIRecommendationRequest
  ): Promise<AIRecommendationResponse> {
    const response = await apiClient.post<AIRecommendationResponse>(
      `${this.basePath}/recommend`,
      {
        query: request.query,
        top_k: request.top_k || 5,
      }
    );
    return response.data;
  }

  /**
   * 語義搜尋 (純 Vector Search)
   * 支援類型篩選、評分篩選
   */
  async semanticSearch(request: AISearchRequest): Promise<AISearchResponse> {
    const response = await apiClient.post<AISearchResponse>(
      `${this.basePath}/search`,
      {
        query: request.query,
        filters: request.filters,
        top_k: request.top_k || 10,
      }
    );
    return response.data;
  }

  /**
   * 獲取相似電影 (基於向量相似度)
   */
  async getSimilarMovies(movieId: string, topK: number = 5): Promise<SimilarMoviesResponse> {
    const response = await apiClient.get<SimilarMoviesResponse>(
      `${this.basePath}/similar/${movieId}`,
      {
        params: { top_k: topK },
      }
    );
    return response.data;
  }
}

// 匯出單例
export const aiApi = new AIApiService();
