from typing import List, Dict, Optional
from datetime import datetime, timedelta
import httpx
from backend.config import settings


class TwitterService:
    def __init__(self):
        self.bearer_token = settings.twitter_bearer_token
        self.base_url = "https://api.twitter.com/2"

    async def search_tweets(
        self, 
        keyword: str, 
        max_results: int = 10,
        hours: int = 24
    ) -> List[str]:
        """
        키워드로 트윗 검색 (최근 N시간, 상위 N개)
        Returns: List of tweet texts
        """
        if not self.bearer_token:
            # 더미 데이터 반환
            return self._get_dummy_tweets(keyword, max_results)

        try:
            # 실제 Twitter API v2 호출
            start_time = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/tweets/search/recent",
                    headers={
                        "Authorization": f"Bearer {self.bearer_token}"
                    },
                    params={
                        "query": keyword,
                        "max_results": min(max_results, 100),
                        "start_time": start_time,
                        "tweet.fields": "text,created_at,public_metrics"
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    tweets = [
                        tweet["text"] 
                        for tweet in data.get("data", [])
                    ]
                    return tweets
                else:
                    # API 오류 시 더미 데이터 반환
                    return self._get_dummy_tweets(keyword, max_results)
                    
        except Exception as e:
            print(f"Twitter API 오류: {e}")
            # 오류 시 더미 데이터 반환
            return self._get_dummy_tweets(keyword, max_results)

    def _get_dummy_tweets(self, keyword: str, count: int) -> List[str]:
        """더미 트윗 데이터 생성"""
        dummy_tweets = [
            f"{keyword}에 대한 최신 트렌드가 흥미롭네요! 많은 사람들이 관심을 보이고 있습니다.",
            f"최근 {keyword} 관련해서 정말 많은 논의가 오가고 있네요. 주목할 만한 포인트들이 있습니다.",
            f"{keyword}에 대한 다양한 의견들이 나오고 있어요. 특히 젊은 세대의 관점이 인상적입니다.",
            f"오늘 {keyword}에 대한 뉴스가 화제가 되고 있네요. 많은 사람들이 공감하고 있습니다.",
            f"{keyword}와 관련된 새로운 인사이트가 나오고 있어요. 앞으로의 전개가 기대됩니다.",
            f"최근 {keyword}에 대한 관심이 급증하고 있습니다. 트렌드를 주도하는 요소들이 보입니다.",
            f"{keyword}에 대한 실용적인 팁들이 공유되고 있네요. 많은 도움이 될 것 같습니다.",
            f"오늘 {keyword}에 대한 토론이 활발하게 진행되고 있어요. 다양한 시각이 제시되고 있습니다.",
            f"{keyword}와 관련된 혁신적인 아이디어들이 나오고 있네요. 미래가 기대됩니다.",
            f"최근 {keyword}에 대한 긍정적인 반응이 많아지고 있어요. 트렌드 변화가 느껴집니다.",
        ]
        
        return dummy_tweets[:count]

