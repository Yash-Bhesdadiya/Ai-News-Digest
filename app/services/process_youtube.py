from typing import Optional

from app.scrapers.youtube import YouTubeScraper
from app.database.repository import Repository


TRANSCRIPT_UNAVAILABLE_MARKER = "__UNAVAILABLE__"


def process_youtube_transcripts(
    limit: Optional[int] = None
) -> dict:

    scraper = YouTubeScraper()
    repo = Repository()

    videos = repo.get_youtube_videos_without_transcript(
        limit=limit
    )

    processed = 0
    unavailable = 0
    failed = 0

    print(
        f"Found {len(videos)} YouTube videos "
        f"without transcripts."
    )

    for video in videos:

        print(
            f"\nProcessing: {video.title}"
        )

        try:

            transcript_result = scraper.get_transcript(
                video.video_id
            )

            # ======================================
            # Transcript found
            # ======================================

            if transcript_result:

                repo.update_youtube_video_transcript(
                    video.video_id,
                    transcript_result.text
                )

                processed += 1

                print(
                    f"Transcript saved: "
                    f"{video.video_id}"
                )

            # ======================================
            # Transcript unavailable
            # ======================================

            else:

                repo.update_youtube_video_transcript(
                    video.video_id,
                    TRANSCRIPT_UNAVAILABLE_MARKER
                )

                unavailable += 1

                print(
                    f"Transcript unavailable: "
                    f"{video.video_id}"
                )

        # ==========================================
        # Unexpected error
        # ==========================================

        except Exception as e:

            failed += 1

            print(
                f"Failed processing "
                f"{video.video_id}: {e}"
            )

    return {
        "total": len(videos),
        "processed": processed,
        "unavailable": unavailable,
        "failed": failed,
    }


if __name__ == "__main__":

    result = process_youtube_transcripts()

    print("\n========== Transcript Processing ==========\n")

    print(
        f"Total videos: "
        f"{result['total']}"
    )

    print(
        f"Processed: "
        f"{result['processed']}"
    )

    print(
        f"Unavailable: "
        f"{result['unavailable']}"
    )

    print(
        f"Failed: "
        f"{result['failed']}"
    )