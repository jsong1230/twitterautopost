/**
 * 유틸리티 함수
 */

/**
 * 날짜 포맷팅
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat("ko-KR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
}

/**
 * 상대 시간 표시 (예: "2시간 전")
 */
export function getRelativeTime(dateString: string): string {
  const date = new Date(dateString);
  const now = new Date();
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (diffInSeconds < 60) {
    return "방금 전";
  } else if (diffInSeconds < 3600) {
    const minutes = Math.floor(diffInSeconds / 60);
    return `${minutes}분 전`;
  } else if (diffInSeconds < 86400) {
    const hours = Math.floor(diffInSeconds / 3600);
    return `${hours}시간 전`;
  } else if (diffInSeconds < 604800) {
    const days = Math.floor(diffInSeconds / 86400);
    return `${days}일 전`;
  } else {
    return formatDate(dateString);
  }
}

/**
 * 텍스트 복사
 */
export async function copyToClipboard(text: string): Promise<boolean> {
  try {
    await navigator.clipboard.writeText(text);
    return true;
  } catch (error) {
    console.error("복사 실패:", error);
    return false;
  }
}

/**
 * 해시태그 파싱 (콤마로 구분된 문자열을 배열로)
 */
export function parseHashtags(hashtags: string | null): string[] {
  if (!hashtags) return [];
  return hashtags.split(",").map((tag) => tag.trim()).filter(Boolean);
}

/**
 * 트윗 길이 검증 (280자 제한)
 */
export function isValidTweetLength(text: string): boolean {
  return text.length <= 280;
}

