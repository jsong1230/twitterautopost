/**
 * API 클라이언트
 * Backend API와 통신하는 유틸리티
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import type {
  Keyword,
  KeywordCreate,
  Insight,
  Post,
  ApiError,
} from "./types";

// API 베이스 URL (환경 변수 또는 기본값)
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Axios 인스턴스 생성
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000, // 30초
});

/**
 * 에러 핸들링 헬퍼
 */
export function handleApiError(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    if (axiosError.response) {
      // 서버에서 에러 응답을 받은 경우
      return (
        axiosError.response.data?.detail ||
        `에러가 발생했습니다: ${axiosError.response.status}`
      );
    } else if (axiosError.request) {
      // 요청은 보냈지만 응답을 받지 못한 경우
      return "서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.";
    }
  }
  return "알 수 없는 오류가 발생했습니다.";
}

/**
 * 키워드 API
 */
export const keywordApi = {
  /**
   * 키워드 목록 조회
   */
  async getKeywords(skip = 0, limit = 100): Promise<Keyword[]> {
    try {
      const response = await apiClient.get<Keyword[]>("/api/keywords/", {
        params: { skip, limit },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * 키워드 추가
   */
  async createKeyword(keyword: string): Promise<Keyword> {
    try {
      const response = await apiClient.post<Keyword>("/api/keywords/", {
        keyword,
      } as KeywordCreate);
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * 키워드 삭제
   */
  async deleteKeyword(keywordId: number): Promise<void> {
    try {
      await apiClient.delete(`/api/keywords/${keywordId}`);
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * 키워드 활성/비활성 토글
   */
  async toggleKeyword(keywordId: number): Promise<Keyword> {
    try {
      const response = await apiClient.patch<Keyword>(
        `/api/keywords/${keywordId}/toggle`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};

/**
 * 인사이트 API
 */
export const insightApi = {
  /**
   * 인사이트 목록 조회
   */
  async getInsights(skip = 0, limit = 50): Promise<Insight[]> {
    try {
      const response = await apiClient.get<Insight[]>("/api/insights/", {
        params: { skip, limit },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * 특정 인사이트 조회
   */
  async getInsight(insightId: number): Promise<Insight> {
    try {
      const response = await apiClient.get<Insight>(
        `/api/insights/${insightId}`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },

  /**
   * 키워드에 대한 인사이트 생성 (수동)
   */
  async generateInsight(keywordId: number): Promise<{ insight_id: number }> {
    try {
      const response = await apiClient.post<{ insight_id: number }>(
        `/api/insights/generate/${keywordId}`
      );
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};

/**
 * 포스트 API
 */
export const postApi = {
  /**
   * 포스트 목록 조회
   */
  async getPosts(
    skip = 0,
    limit = 100,
    insightId?: number
  ): Promise<Post[]> {
    try {
      const response = await apiClient.get<Post[]>("/api/posts/", {
        params: { skip, limit, insight_id: insightId },
      });
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};

/**
 * Health Check API
 */
export const healthApi = {
  /**
   * 서버 상태 확인
   */
  async checkHealth(): Promise<{ status: string }> {
    try {
      const response = await apiClient.get<{ status: string }>("/health");
      return response.data;
    } catch (error) {
      throw new Error(handleApiError(error));
    }
  },
};

// 기본 export
export default apiClient;

