from .config import YOUTUBE_CHANNELS
from .scrapers.youtube import YouTubeScraper
from .scrapers.openai import OpenAIScraper
from .scrapers.anthropic import AnthropicScraper
from .database.repository import Repository


def run_scrapers(hours: int = 24) -> dict:

    youtube_scraper = YouTubeScraper()
    openai_scraper = OpenAIScraper()
    anthropic_scraper = AnthropicScraper()

    repo = Repository()

    # ==========================================
    # YouTube
    # ==========================================

    youtube_videos = []
    video_dicts = []

    for channel_id in YOUTUBE_CHANNELS:

        videos = youtube_scraper.get_latest_videos(
            channel_id=channel_id,
            hours=hours
        )

        youtube_videos.extend(videos)

        for video in videos:

            video_dicts.append(
                {
                    "video_id": video.video_id,
                    "title": video.title,
                    "url": video.url,
                    "channel_id": channel_id,
                    "published_at": video.published_at,
                    "description": video.description,
                    "transcript": video.transcript,
                }
            )

    # ==========================================
    # OpenAI
    # ==========================================

    openai_articles = openai_scraper.get_articles(
        hours=hours
    )

    # ==========================================
    # Anthropic
    # ==========================================

    anthropic_articles = anthropic_scraper.get_articles(
        hours=hours
    )

    # ==========================================
    # Save YouTube videos
    # ==========================================

    if video_dicts:

        repo.bulk_create_youtube_videos(
            video_dicts
        )

    # ==========================================
    # Save OpenAI articles
    # ==========================================

    if openai_articles:

        article_dicts = []

        for article in openai_articles:

            article_dicts.append(
                {
                    "guid": article.guid,
                    "title": article.title,
                    "url": article.url,
                    "published_at": article.published_at,
                    "description": article.description,
                    "category": article.category,
                }
            )

        repo.bulk_create_openai_articles(
            article_dicts
        )

    # ==========================================
    # Save Anthropic articles
    # ==========================================

    if anthropic_articles:

        article_dicts = []

        for article in anthropic_articles:

            article_dicts.append(
                {
                    "guid": article.guid,
                    "title": article.title,
                    "url": article.url,
                    "published_at": article.published_at,
                    "description": article.description,
                    "category": article.category,
                }
            )

        repo.bulk_create_anthropic_articles(
            article_dicts
        )

    # ==========================================
    # Return results
    # ==========================================

    return {
        "youtube": youtube_videos,
        "openai": openai_articles,
        "anthropic": anthropic_articles,
    }


if __name__ == "__main__":

    results = run_scrapers(hours=24)

    print("\n========== Scraping Complete ==========\n")

    print(
        f"YouTube videos: "
        f"{len(results['youtube'])}"
    )

    print(
        f"OpenAI articles: "
        f"{len(results['openai'])}"
    )

    print(
        f"Anthropic articles: "
        f"{len(results['anthropic'])}"
    )