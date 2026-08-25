"""Analyze engagement data and provide insights for AI feedback loop."""

import logging
from typing import Dict, List, Any
from app.config import get_settings

logger = logging.getLogger(__name__)

settings = get_settings()


class AnalyticsAnalyzer:
    """Analyze post performance and extract learnings."""

    def __init__(self):
        """Initialize analytics analyzer."""
        self.engagement_threshold = 0.05  # 5% engagement rate is good

    def analyze_post_performance(
        self, post_data: Dict[str, Any], analytics_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze post performance and extract insights."""
        insights = {
            "engagement_rate": self._calculate_engagement_rate(analytics_data),
            "performance_level": self._determine_performance_level(analytics_data),
            "top_metrics": self._identify_top_metrics(analytics_data),
            "recommendations": self._generate_recommendations(
                post_data, analytics_data
            ),
        }
        return insights

    def _calculate_engagement_rate(self, analytics_data: Dict[str, Any]) -> float:
        """Calculate engagement rate."""
        impressions = analytics_data.get("impressions", 1)
        interactions = (
            analytics_data.get("likes", 0)
            + analytics_data.get("comments", 0)
            + analytics_data.get("shares", 0)
        )
        return (interactions / impressions * 100) if impressions > 0 else 0.0

    def _determine_performance_level(self, analytics_data: Dict[str, Any]) -> str:
        """Determine if post performed well."""
        engagement_rate = self._calculate_engagement_rate(analytics_data)
        if engagement_rate >= self.engagement_threshold * 10:  # 50%+
            return "exceptional"
        elif engagement_rate >= self.engagement_threshold * 2:  # 10%+
            return "high"
        elif engagement_rate >= self.engagement_threshold:  # 5%+
            return "good"
        elif engagement_rate >= self.engagement_threshold / 2:  # 2.5%+
            return "average"
        else:
            return "low"

    def _identify_top_metrics(self, analytics_data: Dict[str, Any]) -> Dict[str, int]:
        """Identify which metrics performed best."""
        return {
            "impressions": analytics_data.get("impressions", 0),
            "likes": analytics_data.get("likes", 0),
            "comments": analytics_data.get("comments", 0),
            "shares": analytics_data.get("shares", 0),
        }

    def _generate_recommendations(
        self, post_data: Dict[str, Any], analytics_data: Dict[str, Any]
    ) -> List[str]:
        """Generate recommendations for future content."""
        recommendations = []
        engagement_rate = self._calculate_engagement_rate(analytics_data)
        theme = post_data.get("theme", "")

        if engagement_rate < self.engagement_threshold:
            recommendations.append(
                f"Consider adjusting caption style for {theme} content"
            )
            recommendations.append("Try different hashtag combinations")
            recommendations.append("Experiment with different posting times")

        if analytics_data.get("comments", 0) < analytics_data.get("likes", 0) * 0.1:
            recommendations.append("Add question in caption to encourage comments")

        if analytics_data.get("shares", 0) > analytics_data.get("likes", 0) * 0.5:
            recommendations.append("This content is highly shareable - use similar style")

        return recommendations

    def extract_learning_patterns(
        self, recent_posts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract patterns from recent posts to inform future content."""
        if not recent_posts:
            return {}

        themes_performance = {}
        hashtags_performance = {}
        content_types_performance = {}

        for post in recent_posts:
            theme = post.get("theme", "unknown")
            engagement_rate = post.get("engagement_rate", 0)

            if theme not in themes_performance:
                themes_performance[theme] = []
            themes_performance[theme].append(engagement_rate)

            # Extract hashtag performance
            hashtags = post.get("hashtags", "").split(",")
            for tag in hashtags:
                tag = tag.strip()
                if tag not in hashtags_performance:
                    hashtags_performance[tag] = []
                hashtags_performance[tag].append(engagement_rate)

            # Track content type performance
            content_type = post.get("content_type", "unknown")
            if content_type not in content_types_performance:
                content_types_performance[content_type] = []
            content_types_performance[content_type].append(engagement_rate)

        # Calculate averages
        theme_avg = {
            k: sum(v) / len(v) for k, v in themes_performance.items()
        }
        hashtag_avg = {
            k: sum(v) / len(v) for k, v in hashtags_performance.items()
        }
        content_type_avg = {
            k: sum(v) / len(v) for k, v in content_types_performance.items()
        }

        return {
            "top_themes": sorted(
                theme_avg.items(), key=lambda x: x[1], reverse=True
            )[:3],
            "top_hashtags": sorted(
                hashtag_avg.items(), key=lambda x: x[1], reverse=True
            )[:10],
            "top_content_types": sorted(
                content_type_avg.items(), key=lambda x: x[1], reverse=True
            ),
        }
