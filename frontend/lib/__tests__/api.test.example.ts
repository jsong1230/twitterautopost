/**
 * API 클라이언트 테스트 예시
 * 실제 테스트는 jest나 vitest로 작성하세요
 */

import { keywordApi, insightApi, postApi, healthApi } from "../api";

/**
 * 테스트 예시 (실제로는 테스트 프레임워크 사용)
 */
export async function testApiConnection() {
  try {
    // Health check
    const health = await healthApi.checkHealth();
    console.log("✅ 서버 연결 성공:", health);

    // 키워드 목록 조회
    const keywords = await keywordApi.getKeywords();
    console.log("✅ 키워드 목록:", keywords);

    // 인사이트 목록 조회
    const insights = await insightApi.getInsights();
    console.log("✅ 인사이트 목록:", insights);

    // 포스트 목록 조회
    const posts = await postApi.getPosts();
    console.log("✅ 포스트 목록:", posts);
  } catch (error) {
    console.error("❌ API 테스트 실패:", error);
  }
}

