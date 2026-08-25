"""AI content generation agent using Anthropic Claude."""

import anthropic
import logging
from typing import Optional
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class ContentGenerator:
    """Generate content using Anthropic Claude API with prompt caching."""

    def __init__(self):
        """Initialize the content generator."""
        self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        self.model = settings.claude_model
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature

    def generate_caption(
        self,
        platform: str,
        theme: str,
        template: Optional[str] = None,
        additional_context: Optional[str] = None,
    ) -> str:
        """Generate a platform-specific caption."""
        system_prompt = self._get_system_prompt(platform)
        user_prompt = self._build_user_prompt(platform, theme, template, additional_context)

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
            ):
                return message.content[0].text

        except Exception as e:
            logger.error(f"Failed to generate caption: {e}")
            raise

    def generate_multiple_captions(
        self,
        platform: str,
        themes: list,
        count: int = 3,
    ) -> list:
        """Generate multiple captions at once (batch processing for efficiency)."""
        system_prompt = self._get_system_prompt(platform)
        user_prompt = f"""
        Generate {count} unique, engaging {platform} captions for a fashion & fabric marketplace.
        Topics: {', '.join(themes)}
        
        Requirements:
        - Each caption should be original and unique
        - Use relevant emojis
        - Include 3-5 relevant hashtags per caption
        - Keep platform-specific character limits in mind
        - Focus on:
          * Styling tips and inspiration
          * Fabric quality and materials
          * Rental and selling opportunities
          * Sustainability and fashion trends
        
        Format your response as a numbered list (1., 2., 3., etc)
        """

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens * 2,
                temperature=self.temperature,
                system=[
                    {
                        "type": "text",
                        "text": system_prompt,
                        "cache_control": {"type": "ephemeral"},
                    }
                ],
                messages=[
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ],
            )
            content = message.content[0].text
            captions = [cap.strip() for cap in content.split("\n") if cap.strip()]
            return captions[:count]

        except Exception as e:
            logger.error(f"Failed to generate multiple captions: {e}")
            raise

    def _get_system_prompt(self, platform: str) -> str:
        """Get platform-specific system prompt."""
        base_prompt = """
        You are an expert social media content creator specializing in fashion and fabric marketing.
        You create engaging, authentic content for a platform that sells and rents fabrics and dresses.
        
        Your content should:
        - Be original and avoid clichés
        - Include storytelling elements
        - Use relevant, trending hashtags
        - Include a call-to-action when appropriate
        - Maintain brand voice: modern, inclusive, and sustainability-focused
        """

        platform_specific = {
            "instagram": """
            Platform: Instagram
            - Captions should be 125-300 characters for optimal engagement
            - Use 3-5 relevant hashtags
            - Include emojis strategically
            - Focus on visual storytelling
            - Can include product recommendations
            """,
            "tiktok": """
            Platform: TikTok
            - Captions should be 40-150 characters for hook impact
            - Use trending sounds/audio mentions when relevant
            - Include trending hashtags (#FYP, #ForYouPage, etc.)
            - Keep it casual and authentic
            - Start with a hook to grab attention in first 3 seconds
            """,
            "facebook": """
            Platform: Facebook
            - Captions can be longer (200-500 characters)
            - Include personal touches and community engagement
            - Use conversational tone
            - Include clear CTAs
            """,
            "linkedin": """
            Platform: LinkedIn
            - Professional yet approachable tone
            - Focus on industry insights and business value
            - Can be longer form (300-500 characters)
            - Include relevant professional hashtags
            """,
        }

        return base_prompt + platform_specific.get(platform, "")

    def _build_user_prompt(
        self,
        platform: str,
        theme: str,
        template: Optional[str] = None,
        additional_context: Optional[str] = None,
    ) -> str:
        """Build user prompt for content generation."""
        prompt = f"Generate a {platform} caption for: {theme}\n"

        if template:
            prompt += f"\nUsing template style: {template}\n"

        if additional_context:
            prompt += f"\nAdditional context: {additional_context}\n"

        prompt += """
        Remember to:
        - Make it engaging and authentic
        - Include relevant hashtags
        - Use emojis appropriately
        - Follow platform best practices
        """

        return prompt
