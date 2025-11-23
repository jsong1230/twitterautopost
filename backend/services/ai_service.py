from typing import List, Dict, Optional
import json
import logging
from backend.config import settings

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.openai_api_key = settings.openai_api_key
        self.claude_api_key = settings.claude_api_key

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
        
        # 프롬프트 생성
        prompt = f"""다음 트윗들을 분석하여 주요 트렌드를 요약해주세요.

트윗 목록:
{tweets_text}

다음 형식으로 응답해주세요:
한글 요약: [한국어로 주요 트렌드 요약]
영문 요약: [영어로 주요 트렌드 요약]

요약은 3-5개의 주요 포인트로 구성하고, 구체적이고 실용적인 인사이트를 제공해주세요."""

        try:
            # OpenAI API 시도
            if self.openai_api_key:
                result = await self._call_openai(prompt, model="gpt-4o-mini")
                if result and "OpenAI API key" not in result:
                    return self._parse_insights(result)
            
            # Claude API 시도
            if self.claude_api_key:
                result = await self._call_claude(prompt, model="claude-3-5-sonnet-20241022")
                if result and "Claude API key" not in result:
                    return self._parse_insights(result)
        except Exception as e:
            logger.error(f"AI API 호출 중 오류: {e}", exc_info=True)

        # API 호출 실패 시 더미 데이터 반환
        logger.warning("AI API 호출 실패, 더미 데이터 반환")
        summary_kr = f"최근 {len(tweets)}개의 트윗을 분석한 결과, 주요 트렌드는 다음과 같습니다:\n\n"
        summary_kr += "- 사용자들이 공유하는 주요 주제들이 확인됩니다.\n"
        summary_kr += "- 감정적 반응과 참여도가 높은 게시물들이 눈에 띕니다.\n"
        summary_kr += "- 새로운 관점과 의견들이 다양하게 제시되고 있습니다."
        
        summary_en = f"After analyzing {len(tweets)} recent tweets, the main trends are:\n\n"
        summary_en += "- Key topics shared by users have been identified.\n"
        summary_en += "- Posts with high emotional engagement stand out.\n"
        summary_en += "- Diverse perspectives and opinions are being presented."

        return {
            "summary_kr": summary_kr,
            "summary_en": summary_en
        }
    
    def _parse_insights(self, text: str) -> Dict:
        """AI 응답에서 한글/영문 요약 파싱"""
        summary_kr = ""
        summary_en = ""
        
        # 한글 요약 추출
        if "한글 요약:" in text or "한국어" in text:
            parts = text.split("한글 요약:") if "한글 요약:" in text else text.split("한국어")
            if len(parts) > 1:
                summary_kr = parts[1].split("영문 요약:")[0].split("영어")[0].strip()
        
        # 영문 요약 추출
        if "영문 요약:" in text or "영어" in text:
            parts = text.split("영문 요약:") if "영문 요약:" in text else text.split("영어")
            if len(parts) > 1:
                summary_en = parts[-1].strip()
        
        # 파싱 실패 시 전체 텍스트를 한글 요약으로 사용
        if not summary_kr:
            summary_kr = text[:500]
        if not summary_en:
            summary_en = text[:500]
        
        return {
            "summary_kr": summary_kr,
            "summary_en": summary_en
        }

    async def generate_tweets(self, insights: Dict, count: int = 5) -> List[str]:
        """
        인사이트를 바탕으로 트윗 초안 생성
        Returns: List of tweet drafts
        """
        summary = insights.get('summary_kr', insights.get('summary_en', '최신 트렌드'))
        
        prompt = f"""다음 트렌드 인사이트를 바탕으로 {count}개의 트윗 초안을 작성해주세요.

인사이트:
{summary}

요구사항:
- 각 트윗은 280자 이내로 작성
- 독창적이고 매력적인 내용
- 해시태그는 최대 2-3개만 포함
- 각 트윗은 서로 다른 관점이나 포인트를 다루기
- 번호 없이 각 트윗을 한 줄씩 작성

형식:
트윗 1
트윗 2
트윗 3
..."""

        try:
            # OpenAI API 시도
            if self.openai_api_key:
                result = await self._call_openai(prompt, model="gpt-4o-mini")
                if result and "OpenAI API key" not in result:
                    tweets = self._parse_tweets(result, count)
                    if tweets:
                        return tweets
            
            # Claude API 시도
            if self.claude_api_key:
                result = await self._call_claude(prompt, model="claude-3-5-sonnet-20241022")
                if result and "Claude API key" not in result:
                    tweets = self._parse_tweets(result, count)
                    if tweets:
                        return tweets
        except Exception as e:
            logger.error(f"트윗 생성 중 오류: {e}", exc_info=True)

        # API 호출 실패 시 더미 데이터 반환
        logger.warning("AI API 호출 실패, 더미 트윗 반환")
        tweet_list = []
        for i in range(count):
            tweet_list.append(
                f"📊 트렌드 분석: {summary[:100]}... "
                f"더 많은 인사이트를 확인해보세요!"
            )
        
        return tweet_list[:count]
    
    def _parse_tweets(self, text: str, count: int) -> List[str]:
        """AI 응답에서 트윗 목록 파싱"""
        tweets = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # 번호나 불필요한 접두사 제거
            if line and len(line) > 10:
                # "트윗 1:", "1.", "-" 등의 패턴 제거
                for prefix in ["트윗", "Tweet", "1.", "2.", "3.", "4.", "5.", "-", "•"]:
                    if line.startswith(prefix):
                        line = line[len(prefix):].strip()
                        if line.startswith(":"):
                            line = line[1:].strip()
                
                if line and len(line) <= 280:  # 트윗 길이 제한
                    tweets.append(line)
                    if len(tweets) >= count:
                        break
        
        return tweets if tweets else None

    async def generate_instagram_post(self, insights: Dict) -> Dict:
        """
        인사이트를 바탕으로 인스타그램 캡션 + 해시태그 생성
        Returns: {caption: str, hashtags: List[str]}
        """
        summary = insights.get('summary_kr', insights.get('summary_en', '최신 동향을 분석했습니다.'))
        
        prompt = f"""다음 트렌드 인사이트를 바탕으로 인스타그램 포스트 캡션과 해시태그를 작성해주세요.

인사이트:
{summary}

요구사항:
- 캡션은 500-1000자 정도로 작성
- 이모지를 적절히 사용하여 시각적 매력 추가
- 해시태그는 5-10개 정도, 관련성 높은 것만
- 캡션과 해시태그를 구분하여 작성

형식:
캡션: [캡션 내용]
해시태그: [해시태그1] [해시태그2] [해시태그3] ..."""

        try:
            # Claude API 우선 사용 (인스타그램 포스트에 더 적합)
            if self.claude_api_key:
                result = await self._call_claude(prompt, model="claude-3-5-sonnet-20241022")
                if result and "Claude API key" not in result:
                    parsed = self._parse_instagram_post(result)
                    if parsed:
                        return parsed
            
            # OpenAI API 시도
            if self.openai_api_key:
                result = await self._call_openai(prompt, model="gpt-4o-mini")
                if result and "OpenAI API key" not in result:
                    parsed = self._parse_instagram_post(result)
                    if parsed:
                        return parsed
        except Exception as e:
            logger.error(f"인스타그램 포스트 생성 중 오류: {e}", exc_info=True)

        # API 호출 실패 시 더미 데이터 반환
        logger.warning("AI API 호출 실패, 더미 인스타그램 포스트 반환")
        caption = f"""📈 최신 트렌드 인사이트

{summary[:200]}

더 많은 인사이트와 분석 결과를 확인해보세요!"""

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
    
    def _parse_instagram_post(self, text: str) -> Optional[Dict]:
        """AI 응답에서 인스타그램 캡션과 해시태그 파싱"""
        caption = ""
        hashtags = []
        
        # 캡션 추출
        if "캡션:" in text:
            parts = text.split("캡션:")
            if len(parts) > 1:
                caption_part = parts[1].split("해시태그:")[0].strip()
                caption = caption_part
        
        # 해시태그 추출
        if "해시태그:" in text:
            parts = text.split("해시태그:")
            if len(parts) > 1:
                hashtag_text = parts[1].strip()
                # 해시태그 파싱 (# 제거하고 리스트로)
                for tag in hashtag_text.split():
                    tag = tag.strip("#[]")
                    if tag:
                        hashtags.append(tag)
        
        if caption:
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
                        "content": "You are a helpful assistant that analyzes social media trends and creates engaging content."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
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
                max_tokens=2000,
                temperature=0.7,
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

