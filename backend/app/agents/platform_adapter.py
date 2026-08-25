"""Platform-specific adapters for posting content."""

import requests
import logging
from typing import Optional, Dict, Any
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class PlatformAdapter:
    """Handle platform-specific API interactions."""

    def __init__(self, platform: str, access_token: str):
        """Initialize platform adapter."""
        self.platform = platform
        self.access_token = access_token
        self.base_urls = {
            "instagram": "https://graph.instagram.com",
            "tiktok": "https://open.tiktokapis.com",
            "facebook": "https://graph.facebook.com",
            "linkedin": "https://api.linkedin.com",
        }

    async def post_content(
        self,
        account_id: str,
        content: str,
        media_urls: Optional[list] = None,
        hashtags: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Post content to platform."""
        if self.platform == "instagram":
            return await self._post_instagram(account_id, content, media_urls, hashtags)
        elif self.platform == "tiktok":
            return await self._post_tiktok(account_id, content, media_urls)
        elif self.platform == "facebook":
            return await self._post_facebook(account_id, content, media_urls)
        elif self.platform == "linkedin":
            return await self._post_linkedin(account_id, content, media_urls)
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")

    async def _post_instagram(
        self, account_id: str, content: str, media_urls: Optional[list] = None, hashtags: Optional[str] = None
    ) -> Dict[str, Any]:
        """Post to Instagram using Graph API."""
        try:
            # Instagram caption endpoint
            url = f"{self.base_urls['instagram']}/{account_id}/media"
            caption = f"{content}\n{hashtags}" if hashtags else content
            params = {
                "media_type": "CAROUSEL" if media_urls and len(media_urls) > 1 else "IMAGE",
                "caption": caption,
                "access_token": self.access_token,
            }

            if media_urls:
                params["media_source_url"] = media_urls[0]

            response = requests.post(url, params=params)
            response.raise_for_status()
            return {"success": True, "platform_id": response.json().get("id")}

        except Exception as e:
            logger.error(f"Failed to post to Instagram: {e}")
            return {"success": False, "error": str(e)}

    async def _post_tiktok(
        self, account_id: str, content: str, media_urls: Optional[list] = None
    ) -> Dict[str, Any]:
        """Post to TikTok using TikTok API."""
        try:
            # TikTok video upload endpoint
            url = f"{self.base_urls['tiktok']}/v1/post/publish/action/upload/"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            payload = {
                "video": {"source": "PULL_FROM_URL", "video_url": media_urls[0]} if media_urls else {},
                "caption": content,
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "platform_id": response.json().get("data", {}).get("video_id")}

        except Exception as e:
            logger.error(f"Failed to post to TikTok: {e}")
            return {"success": False, "error": str(e)}

    async def _post_facebook(
        self, account_id: str, content: str, media_urls: Optional[list] = None
    ) -> Dict[str, Any]:
        """Post to Facebook using Graph API."""
        try:
            url = f"{self.base_urls['facebook']}/{account_id}/feed"
            payload = {"message": content, "access_token": self.access_token}

            if media_urls:
                payload["link"] = media_urls[0]

            response = requests.post(url, data=payload)
            response.raise_for_status()
            return {"success": True, "platform_id": response.json().get("id")}

        except Exception as e:
            logger.error(f"Failed to post to Facebook: {e}")
            return {"success": False, "error": str(e)}

    async def _post_linkedin(
        self, account_id: str, content: str, media_urls: Optional[list] = None
    ) -> Dict[str, Any]:
        """Post to LinkedIn using LinkedIn API."""
        try:
            url = f"{self.base_urls['linkedin']}/v2/ugcPosts"
            headers = {"Authorization": f"Bearer {self.access_token", "X-Restli-Protocol-Version": "2.0.0"}
            payload = {"author": f"urn:li:person:{account_id}", "lifecycleState": "PUBLISHED", "specificContent": {"com.linkedin.ugc.text.Share": {"shareCommentary": {"text": content}}}}

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return {"success": True, "platform_id": response.json().get("id")}

        except Exception as e:
            logger.error(f"Failed to post to LinkedIn: {e}")
            return {"success": False, "error": str(e)}

    async def get_analytics(
        self, platform_post_id: str, metric_type: str = "all"
    ) -> Dict[str, Any]:
        """Fetch analytics for a posted content."""
        try:
            if self.platform == "instagram":
                return await self._get_instagram_analytics(platform_post_id)
            elif self.platform == "tiktok":
                return await self._get_tiktok_analytics(platform_post_id)
            else:
                logger.warning(f"Analytics not implemented for {self.platform}")
                return {}

        except Exception as e:
            logger.error(f"Failed to fetch analytics: {e}")
            return {}

    async def _get_instagram_analytics(self, platform_post_id: str) -> Dict[str, Any]:
        """Get Instagram post analytics."""
        try:
            url = f"{self.base_urls['instagram']}/{platform_post_id}/insights"
            params = {"metric": "engagement,impressions,reach", "access_token": self.access_token}
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to get Instagram analytics: {e}")
            return {}

    async def _get_tiktok_analytics(self, platform_post_id: str) -> Dict[str, Any]:
        """Get TikTok video analytics."""
        try:
            url = f"{self.base_urls['tiktok']}/v1/video/query/"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            params = {"fields": "id,video_description,like_count,comment_count,share_count,view_count"}
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("data", {})
        except Exception as e:
            logger.error(f"Failed to get TikTok analytics: {e}")
            return {}
