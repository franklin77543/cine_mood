import axios, { type AxiosInstance, type AxiosError } from 'axios';
import type { ApiError } from '../types';

// API Base URL (可從環境變數讀取)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// 建立 Axios 實例
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // AI 推薦可能需要較長時間
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request 攔截器 (可加入 token)
apiClient.interceptors.request.use(
  (config) => {
    // 未來可加入 JWT token
    // const token = localStorage.getItem('token');
    // if (token) {
    //   config.headers.Authorization = `Bearer ${token}`;
    // }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response 攔截器 (統一錯誤處理)
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const apiError: ApiError = {
      message: error.message || 'Unknown error occurred',
      status: error.response?.status,
      detail: (error.response?.data as any)?.detail || undefined,
    };

    // 統一錯誤處理
    if (error.response?.status === 401) {
      // 未授權，可跳轉登入頁
      console.error('Unauthorized access');
    } else if (error.response?.status === 500) {
      // 伺服器錯誤
      console.error('Server error:', apiError.detail);
    }

    return Promise.reject(apiError);
  }
);

export default apiClient;
