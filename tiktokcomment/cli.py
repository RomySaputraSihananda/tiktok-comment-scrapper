# tiktokcomment/cli.py
import re
import os
import json
import sys
import click
from loguru import logger
from typing import Optional

from tiktokcomment import TiktokComment

__title__ = 'TikTok Comment Scrapper'
__version__ = '2.1.0'

def parse_aweme_id(value: str) -> Optional[str]:
    if not value:
        return None
    # If it's already just digits (TikTok IDs are typically 19 digits)
    if re.match(r"^\d{15,}$", value):
        return value
    # Try to extract from URL (e.g., /video/1234567890123456789)
    match = re.search(r"(?:video/|/v/)(\d{15,})", value)
    if match:
        return match.group(1)
    return None

@click.command(help=__title__)
@click.version_option(version=__version__, prog_name=__title__)
@click.option(
    "-id", "--aweme_id",
    required=True,
    help='TikTok video URL or ID (e.g., 7170139292767882522 or https://...)',
    callback=lambda ctx, param, value: parse_aweme_id(value)
)
@click.option(
    "-o", "--output",
    default='data',
    help='Output directory (default: data)'
)
@click.option(
    "--format",
    type=click.Choice(['json', 'jsonl'], case_sensitive=False),
    default='json',
    help='Output format: json or jsonl (JSON Lines is recommended for large datasets)'
)
@click.option(
    "-l", "--limit",
    type=int,
    default=None,
    help='Maximum number of comments to scrape (default: all)'
)
def main(aweme_id: str, output: str, format: str, limit: Optional[int]):
    if not aweme_id:
        logger.error("Invalid aweme_id or URL provided.")
        sys.exit(1)

    logger.info(f"Starting to scrape comments for video: {aweme_id}")
    
    try:
        scraper = TiktokComment(limit=limit)
        comments_data = scraper(aweme_id=aweme_id)
    except KeyboardInterrupt:
        logger.warning("\nScraping interrupted by user. Exiting gracefully.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {sys.exc_info()}")
        sys.exit(1)

    # Normalize output path
    output_dir = output.rstrip("/\\") or "data"
    os.makedirs(output_dir, exist_ok=True)

    if format == 'jsonl':
        final_path = os.path.join(output_dir, f"{aweme_id}.jsonl")
        logger.info(f"Saving comments to {final_path} in JSONL format...")
        with open(final_path, 'w', encoding='utf-8') as f:
            # Write metadata as the first line
            f.write(json.dumps({"caption": comments_data.caption, "video_url": comments_data.video_url}, ensure_ascii=False) + '\n')
            for comment in comments_data.comments:
                f.write(json.dumps(comment.dict, ensure_ascii=False) + '\n')
    else:
        final_path = os.path.join(output_dir, f"{aweme_id}.json")
        logger.info(f"Saving comments to {final_path} in JSON format...")
        with open(final_path, 'w', encoding='utf-8') as f:
            json.dump(comments_data.dict, f, ensure_ascii=False, indent=4)

    logger.success(f"Successfully saved data to {final_path}")

if __name__ == '__main__':
    main()