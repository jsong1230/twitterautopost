/**
 * Backend API 응답 타입 정의
 */

// 키워드 관련 타입
export interface Keyword {
  id: number;
  keyword: string;
  is_active: boolean;
  created_at: string;
}

export interface KeywordCreate {
  keyword: string;
}

// 인사이트 관련 타입
export interface Post {
  id: number;
  insight_id: number;
  post_type: "tweet" | "instagram";
  content: string;
  hashtags: string | null;
  created_at: string;
}

export interface Insight {
  id: number;
  keyword_id: number;
  keyword: string;
  summary_kr: string | null;
  summary_en: string | null;
  tweets_analyzed: number;
  created_at: string;
  posts: Post[];
}

// API 응답 타입
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}

