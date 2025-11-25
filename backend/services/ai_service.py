from typing import List, Dict, Optional
import json
import logging
import hashlib
import asyncio
from functools import wraps
from datetime import datetime, timedelta
from backend.config import settings
from backend.services.ai_models import InsightResponse, TweetResponse, InstagramPostResponse

logger = logging.getLogger(__name__)

# 간단한 인메모리 캐시
_cache = {}
_cache_timestamps = {}


def cache_response(ttl: int = None):
    """응답 캐싱 데코레이터"""
    if ttl is None:
        ttl = settings.ai_cache_ttl
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 캐시 키 생성
            cache_key = hashlib.md5(
                f"{func.__name__}:{str(args)}:{str(kwargs)}".encode()
            ).hexdigest()
            
            # 캐시 확인
            if cache_key in _cache:
                timestamp = _cache_timestamps.get(cache_key)
                if timestamp and (datetime.now() - timestamp).total_seconds() < ttl:
                    logger.info(f"캐시 히트: {func.__name__}")
                    return _cache[cache_key]
                else:
                    # 만료된 캐시 삭제
                    del _cache[cache_key]
                    del _cache_timestamps[cache_key]
            
            # 캐시 미스 - 함수 실행
            logger.info(f"캐시 미스: {func.__name__}")
            result = await func(*args, **kwargs)
            
            # 결과 캐싱
            _cache[cache_key] = result
            _cache_timestamps[cache_key] = datetime.now()
            
            return result
        return wrapper
    return decorator


async def retry_with_backoff(func, max_retries: int = None, timeout: int = None):
    """재시도 로직 with exponential backoff"""
    if max_retries is None:
        max_retries = settings.ai_max_retries
    if timeout is None:
        timeout = settings.ai_timeout
    
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            # 타임아웃 적용
            result = await asyncio.wait_for(func(), timeout=timeout)
            return result
        except asyncio.TimeoutError:
            last_exception = TimeoutError(f"API 호출 타임아웃 ({timeout}초)")
            logger.warning(f"타임아웃 발생 (시도 {attempt + 1}/{max_retries})")
        except Exception as e:
            last_exception = e
            logger.warning(f"API 호출 실패 (시도 {attempt + 1}/{max_retries}): {e}")
        
        # 마지막 시도가 아니면 대기
        if attempt < max_retries - 1:
            wait_time = 2 ** attempt  # exponential backoff: 1, 2, 4초
            logger.info(f"{wait_time}초 후 재시도...")
            await asyncio.sleep(wait_time)
    
    # 모든 재시도 실패
    raise last_exception


class AIService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        self.claude_api_key = settings.claude_api_key

    @cache_response()
    async def generate_insights(self, tweets: List[str]) -> Dict:
        """
        트윗 리스트를 분석하여 트렌드 요약 생성
        Returns: {summary_kr: str, summary_en: str}
        """
        if not tweets:
            return {
                "summary_kr": "분석할 트윗이 없습니다.",
                "summary_en": "No tweets to analyze."
            }

        tweets_text = "\n".join(tweets[:20])  # 상위 20개만 사용
        
        # 개선된 프롬프트 - JSON 응답 강제
        prompt = f"""다음 트윗들을 분석하여 주요 트렌드를 요약해주세요.

트윗 목록:
{tweets_text}

반드시 다음 JSON 형식으로만 응답해주세요:
{{
  "summary_kr": "한국어로 작성된 주요 트렌드 요약 (3-5개의 구체적인 포인트)",
  "summary_en": "English summary of main trends (3-5 specific points)"
}}

요약 작성 가이드:
- 구체적이고 실용적인 인사이트 제공
- 감정적 톤과 주요 키워드 파악
- 트렌드의 맥락과 의미 설명
- 각 언어로 독립적으로 작성 (단순 번역 X)"""

        try:
            # OpenAI API 시도
            if self.openai_api_key:
                result = await retry_with_backoff(
                    lambda: self._call_openai(prompt, model="gpt-4o-mini")
                )
                if result and "OpenAI API key" not in result:
                    parsed = self._parse_insights(result)
                    if parsed:
                        return parsed
            
            # Claude API 시도
            if self.claude_api_key:
                result = await retry_with_backoff(
                    lambda: self._call_claude(prompt, model="claude-3-5-sonnet-20241022")
                )
                if result and "Claude API key" not in result:
                    parsed = self._parse_insights(result)
                    if parsed:
                        return parsed
        except Exception as e:
            logger.error(f"AI API 호출 중 오류: {e}", exc_info=True)

        # API 호출 실패 시 더미 데이터 반환
        logger.warning("AI API 호출 실패, 더미 데이터 반환")
        return self._get_dummy_insights(len(tweets))
    
    def _parse_insights(self, text: str) -> Optional[Dict]:
        """AI 응답에서 한글/영문 요약 파싱 (JSON 우선)"""
        try:
            # JSON 파싱 시도
            # 코드 블록 제거
            text = text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(text)
            
            # Pydantic 모델로 검증
            validated = InsightResponse(**data)
            return {
                "summary_kr": validated.summary_kr,
                "summary_en": validated.summary_en
            }
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"JSON 파싱 실패, 텍스트 파싱 시도: {e}")
            # 폴백: 텍스트 기반 파싱
            return self._parse_insights_text(text)
    
    def _parse_insights_text(self, text: str) -> Optional[Dict]:
        """텍스트 기반 파싱 (폴백)"""
        summary_kr = ""
        summary_en = ""
        
        # 한글 요약 추출
        if "summary_kr" in text:
            parts = text.split('"summary_kr"')
            if len(parts) > 1:
                summary_kr = parts[1].split('"summary_en"')[0].strip(' :,"')
        elif "한글 요약:" in text or "한국어" in text:
            parts = text.split("한글 요약:") if "한글 요약:" in text else text.split("한국어")
            if len(parts) > 1:
                summary_kr = parts[1].split("영문 요약:")[0].split("영어")[0].strip()
        
        # 영문 요약 추출
        if "summary_en" in text:
            parts = text.split('"summary_en"')
            if len(parts) > 1:
                summary_en = parts[1].strip(' :,"{}')
        elif "영문 요약:" in text or "영어" in text:
            parts = text.split("영문 요약:") if "영문 요약:" in text else text.split("영어")
            if len(parts) > 1:
                summary_en = parts[-1].strip()
        
        # 검증
        if summary_kr and summary_en and len(summary_kr) >= 10 and len(summary_en) >= 10:
            return {
                "summary_kr": summary_kr,
                "summary_en": summary_en
            }
        
        return None

    @cache_response()
    async def generate_tweets(self, insights: Dict, count: int = 5) -> List[str]:
        """
        인사이트를 바탕으로 트윗 초안 생성
        Returns: List of tweet drafts
        """
        summary = insights.get('summary_kr', insights.get('summary_en', '최신 트렌드'))
        
        # 개선된 프롬프트 - JSON 응답 강제
        prompt = f"""다음 트렌드 인사이트를 바탕으로 {count}개의 트윗 초안을 작성해주세요.

인사이트:
{summary}

반드시 다음 JSON 형식으로만 응답해주세요:
{{
  "tweets": [
    "첫 번째 트윗 내용",
    "두 번째 트윗 내용",
    ...
  ]
}}

트윗 작성 가이드:
- 각 트윗은 280자 이내
- 독창적이고 매력적인 내용
- 해시태그는 최대 2-3개만 포함
- 각 트윗은 서로 다른 관점이나 포인트를 다루기
- 이모지를 적절히 활용하여 시각적 매력 추가
- 행동을 유도하는 CTA 포함 고려"""

        try:
            # OpenAI API 시도
            if self.openai_api_key:
                result = await retry_with_backoff(
                    lambda: self._call_openai(prompt, model="gpt-4o-mini")
                )
                if result and "OpenAI API key" not in result:
                    tweets = self._parse_tweets(result, count)
                    if tweets:
                        return tweets
            
            # Claude API 시도
            if self.claude_api_key:
                result = await retry_with_backoff(
                    lambda: self._call_claude(prompt, model="claude-3-5-sonnet-20241022")
                )
                if result and "Claude API key" not in result:
                    tweets = self._parse_tweets(result, count)
                    if tweets:
                        return tweets
        except Exception as e:
            logger.error(f"트윗 생성 중 오류: {e}", exc_info=True)

        # API 호출 실패 시 더미 데이터 반환
        logger.warning("AI API 호출 실패, 더미 트윗 반환")
        return self._get_dummy_tweets(summary, count)
    
    def _parse_tweets(self, text: str, count: int) -> Optional[List[str]]:
        """AI 응답에서 트윗 목록 파싱 (JSON 우선)"""
        try:
            # JSON 파싱 시도
            text = text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(text)
            
            # Pydantic 모델로 검증
            validated = TweetResponse(**data)
            return validated.tweets[:count]
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"JSON 파싱 실패, 텍스트 파싱 시도: {e}")
            # 폴백: 텍스트 기반 파싱
            return self._parse_tweets_text(text, count)
    
    def _parse_tweets_text(self, text: str, count: int) -> Optional[List[str]]:
        """텍스트 기반 트윗 파싱 (폴백)"""
        tweets = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # 번호나 불필요한 접두사 제거
            if line and len(line) > 10:
                # "트윗 1:", "1.", "-" 등의 패턴 제거
                for prefix in ["트윗", "Tweet", "1.", "2.", "3.", "4.", "5.", "-", "•", "*"]:
                    if line.startswith(prefix):
                        line = line[len(prefix):].strip()
                        if line.startswith(":"):
                            line = line[1:].strip()
                        break
                
                if line and 10 <= len(line) <= 280:  # 트윗 길이 제한
                    tweets.append(line)
                    if len(tweets) >= count:
                        break
        
        return tweets if tweets else None

    @cache_response()
    async def generate_instagram_post(self, insights: Dict) -> Dict:
        """
        인사이트를 바탕으로 인스타그램 캡션 + 해시태그 생성
        Returns: {caption: str, hashtags: List[str]}
        """
        summary = insights.get('summary_kr', insights.get('summary_en', '최신 동향을 분석했습니다.'))
        
        # 개선된 프롬프트 - JSON 응답 강제
        prompt = f"""다음 트렌드 인사이트를 바탕으로 인스타그램 포스트 캡션과 해시태그를 작성해주세요.

인사이트:
{summary}

반드시 다음 JSON 형식으로만 응답해주세요:
{{
  "caption": "캡션 내용 (이모지 포함)",
  "hashtags": ["해시태그1", "해시태그2", "해시태그3", ...]
}}

작성 가이드:
- 캡션은 500-1000자 정도로 작성
- 이모지를 적절히 사용하여 시각적 매력 추가
- 해시태그는 5-10개 정도, 관련성 높은 것만
- 스토리텔링 요소 포함
- 독자의 참여를 유도하는 질문이나 CTA 포함"""

        try:
            # Claude API 우선 사용 (인스타그램 포스트에 더 적합)
            if self.claude_api_key:
                result = await retry_with_backoff(
                    lambda: self._call_claude(prompt, model="claude-3-5-sonnet-20241022")
                )
                if result and "Claude API key" not in result:
                    parsed = self._parse_instagram_post(result)
                    if parsed:
                        return parsed
            
            # OpenAI API 시도
            if self.openai_api_key:
                result = await retry_with_backoff(
                    lambda: self._call_openai(prompt, model="gpt-4o-mini")
                )
                if result and "OpenAI API key" not in result:
                    parsed = self._parse_instagram_post(result)
                    if parsed:
                        return parsed
        except Exception as e:
            logger.error(f"인스타그램 포스트 생성 중 오류: {e}", exc_info=True)

        # API 호출 실패 시 더미 데이터 반환
        logger.warning("AI API 호출 실패, 더미 인스타그램 포스트 반환")
        return self._get_dummy_instagram_post(summary)
    
    def _parse_instagram_post(self, text: str) -> Optional[Dict]:
        """AI 응답에서 인스타그램 캡션과 해시태그 파싱 (JSON 우선)"""
        try:
            # JSON 파싱 시도
            text = text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(text)
            
            # Pydantic 모델로 검증
            validated = InstagramPostResponse(**data)
            return {
                "caption": validated.caption,
                "hashtags": validated.hashtags
            }
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"JSON 파싱 실패, 텍스트 파싱 시도: {e}")
            # 폴백: 텍스트 기반 파싱
            return self._parse_instagram_post_text(text)
    
    def _parse_instagram_post_text(self, text: str) -> Optional[Dict]:
        """텍스트 기반 인스타그램 포스트 파싱 (폴백)"""
        caption = ""
        hashtags = []
        
        # 캡션 추출
        if "caption" in text:
            parts = text.split('"caption"')
            if len(parts) > 1:
                caption_part = parts[1].split('"hashtags"')[0].strip(' :,"')
                caption = caption_part
        elif "캡션:" in text:
            parts = text.split("캡션:")
            if len(parts) > 1:
                caption_part = parts[1].split("해시태그:")[0].strip()
                caption = caption_part
        
        # 해시태그 추출
        if "hashtags" in text:
            parts = text.split('"hashtags"')
            if len(parts) > 1:
                hashtag_text = parts[1].strip(' :,[]{}')
                for tag in hashtag_text.split(','):
                    tag = tag.strip(' "\'#[]')
                    if tag:
                        hashtags.append(tag)
        elif "해시태그:" in text:
            parts = text.split("해시태그:")
            if len(parts) > 1:
                hashtag_text = parts[1].strip()
                for tag in hashtag_text.split():
                    tag = tag.strip("#[]")
                    if tag:
                        hashtags.append(tag)
        
        if caption and len(caption) >= 50:
            return {
                "caption": caption,
                "hashtags": hashtags if hashtags else ["트렌드분석", "인사이트", "데이터분석"]
            }
        
        return None

    async def _call_openai(self, prompt: str, model: str = "gpt-4o-mini") -> str:
        """OpenAI API 호출"""
        if not self.openai_api_key:
            return "OpenAI API key가 설정되지 않았습니다."
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert social media analyst and content creator. You analyze trends and create engaging, high-quality content. Always respond in valid JSON format when requested."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=settings.ai_temperature,
                max_tokens=settings.ai_max_tokens,
                response_format={"type": "json_object"}  # JSON 모드 강제
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API 호출 오류: {e}", exc_info=True)
            raise

    async def _call_claude(self, prompt: str, model: str = "claude-3-5-sonnet-20241022") -> str:
        """Claude API 호출"""
        if not self.claude_api_key:
            return "Claude API key가 설정되지 않았습니다."
        
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.claude_api_key)
            
            response = client.messages.create(
                model=model,
                max_tokens=settings.ai_max_tokens,
                temperature=settings.ai_temperature,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.content[0].text.strip()
            
        except Exception as e:
            logger.error(f"Claude API 호출 오류: {e}", exc_info=True)
            raise
    
    # 더미 데이터 생성 메서드들
    def _get_dummy_insights(self, tweet_count: int) -> Dict:
        """더미 인사이트 생성"""
        summary_kr = f"최근 {tweet_count}개의 트윗을 분석한 결과, 주요 트렌드는 다음과 같습니다:\n\n"
        summary_kr += "- 사용자들이 공유하는 주요 주제들이 확인됩니다.\n"
        summary_kr += "- 감정적 반응과 참여도가 높은 게시물들이 눈에 띕니다.\n"
        summary_kr += "- 새로운 관점과 의견들이 다양하게 제시되고 있습니다."
        
        summary_en = f"After analyzing {tweet_count} recent tweets, the main trends are:\n\n"
        summary_en += "- Key topics shared by users have been identified.\n"
        summary_en += "- Posts with high emotional engagement stand out.\n"
        summary_en += "- Diverse perspectives and opinions are being presented."

        return {
            "summary_kr": summary_kr,
            "summary_en": summary_en
        }
    
    def _get_dummy_tweets(self, summary: str, count: int) -> List[str]:
        """더미 트윗 생성"""
        tweet_list = []
        for i in range(count):
            tweet_list.append(
                f"📊 트렌드 분석 #{i+1}: {summary[:100]}... "
                f"더 많은 인사이트를 확인해보세요! #트렌드 #인사이트"
            )
        return tweet_list[:count]
    
    def _get_dummy_instagram_post(self, summary: str) -> Dict:
        """더미 인스타그램 포스트 생성"""
        caption = f"""📈 최신 트렌드 인사이트

{summary[:200]}

더 많은 인사이트와 분석 결과를 확인해보세요!

어떤 트렌드가 가장 흥미로우신가요? 댓글로 알려주세요! 👇"""

        hashtags = [
            "트렌드분석",
            "인사이트",
            "데이터분석",
            "소셜미디어",
            "마케팅"
        ]

        return {
            "caption": caption,
            "hashtags": hashtags
        }
