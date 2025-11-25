import httpx
from backend.config import settings
from typing import List, Dict

class InstagramService:
    """Simple Instagram service placeholder.
    Currently returns dummy post data. Replace with real Instagram Graph API calls.
    """
    def __init__(self):
        # In a real implementation you would use access token from settings
        self.access_token = getattr(settings, "instagram_access_token", None)
        self.base_url = "https://graph.facebook.com/v20.0"  # Instagram Graph API base

    async def fetch_posts(self, hashtag: str, max_results: int = 10) -> List[Dict[str, any]]:
        """Fetch recent Instagram posts for a given hashtag.
        Returns a list of dicts with at least ``caption`` and ``hashtags`` keys.
        Currently returns dummy data when no access token is configured.
        """
        if not self.access_token:
            # Return dummy posts
            dummy = []
            for i in range(max_results):
                dummy.append({
                    "caption": f"Dummy Instagram post {i+1} for #{hashtag}",
                    "hashtags": [hashtag]
                })
            return dummy
        # Real implementation would call the Instagram Graph API here.
        # For brevity, we raise NotImplementedError.
        raise NotImplementedError("Real Instagram API integration not implemented yet.")
