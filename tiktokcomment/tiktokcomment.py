import time
import random
import jmespath
from typing import Any, Dict, Iterator, Optional, List
from curl_cffi.requests import Session
from curl_cffi import CurlOpt

from loguru import logger

from tiktokcomment.typing import Comments, Comment

class TiktokComment:
    BASE_URL: str = 'https://www.tiktok.com'
    API_URL: str = f'{BASE_URL}/api'

    def __init__(self, limit: Optional[int] = None) -> None:
        # Initialize Session with Chrome 124 impersonation AND force IPv4
        self.__session: Session = Session(
            impersonate="chrome124",
            curl_options={
                CurlOpt.IPRESOLVE: 1  # <-- FIXED: 1 is the libcurl constant for CURL_IPRESOLVE_V4
            }
        )
        
        self.__session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": self.BASE_URL,
        })
        
        self.aweme_id: str = ""
        self.limit: Optional[int] = limit
        self._scraped_count: int = 0

    def _delay(self):
        # Random delay between 1.0 and 2.5 seconds to avoid rate limiting
        time.sleep(random.uniform(1.0, 2.5))

    # ... [Keep the rest of the file EXACTLY the same: __parse_comment, get_all_replies, etc.] ...

    def __parse_comment(self, data: Dict[str, Any]) -> Optional[Comment]:
        if not data:
            return None
            
        parsed = jmespath.search(
            """
            {
                comment_id: cid,
                username: user.unique_id,
                nickname: user.nickname,
                comment: text,
                create_time: create_time,
                avatar: user.avatar_thumb.url_list[0],
                total_reply: reply_comment_total
            }
            """, data
        )
        
        if not parsed or not parsed.get('comment_id'):
            return None

        # FIX: Safely handle cases where TikTok returns `null` for reply counts
        total_reply = parsed.get('total_reply') or 0

        replies = []
        if total_reply > 0:
            replies = list(self.get_all_replies(parsed['comment_id']))

        return Comment(
            comment_id=parsed['comment_id'],
            username=parsed.get('username') or 'unknown',
            nickname=parsed.get('nickname') or 'unknown',
            comment=parsed.get('comment') or '',
            create_time=parsed.get('create_time', 0),
            avatar=parsed.get('avatar') or '',
            total_reply=total_reply,
            replies=replies
        )

    def get_all_replies(self, comment_id: str) -> Iterator[Comment]:
        cursor = 0
        has_more = True
        while has_more:
            self._delay()
            replies_data = self._get_replies_request(comment_id, cursor=cursor)
            if not replies_data:
                break
                
            for c in replies_data.get('comments', []):
                parsed = self.__parse_comment(c)
                if parsed:
                    yield parsed
                    
            has_more = replies_data.get('has_more', 0) == 1
            cursor = replies_data.get('cursor', 0)


    def _get_replies_request(self, comment_id: str, cursor: int = 0, count: int = 50) -> Optional[Dict[str, Any]]:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.__session.get(
                    f'{self.API_URL}/comment/list/reply/',
                    params={'aid': 1988, 'comment_id': comment_id, 'item_id': self.aweme_id, 'count': count, 'cursor': cursor},
                    timeout=15
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Network error fetching replies (Attempt {attempt + 1}/{max_retries}). Retrying... | {e}")
                    time.sleep(random.uniform(3.0, 6.0))
                else:
                    logger.error(f"Failed to fetch replies for {comment_id} after {max_retries} attempts: {e}")
                    return None

    def get_all_comments(self, aweme_id: str) -> Comments:
        self.aweme_id = aweme_id
        cursor = 0
        has_more = True
        all_comments: List[Comment] = []
        caption = ""
        video_url = ""

        while has_more:
            if self.limit and self._scraped_count >= self.limit:
                logger.info(f"Reached limit of {self.limit} comments.")
                break

            self._delay()
            data = self._get_comments_request(aweme_id, cursor=cursor)
            
            if not data:
                logger.error("Failed to fetch comments or received empty response.")
                break

            if not caption:
                caption = jmespath.search('comments[0].share_info.title', data) or ""
                video_url = jmespath.search('comments[0].share_info.url', data) or ""

            for comment in data.get('comments', []):
                if self.limit and self._scraped_count >= self.limit:
                    break
                parsed = self.__parse_comment(comment)
                if parsed:
                    all_comments.append(parsed)
                    self._scraped_count += 1

            has_more = data.get('has_more', 0) == 1
            cursor = data.get('cursor', 0) # Use native cursor instead of manual calculation
            
            logger.info(f"Scraped {self._scraped_count} comments so far...")

        return Comments(caption=caption, video_url=video_url, comments=all_comments, has_more=1 if has_more else 0)

    def _get_comments_request(self, aweme_id: str, cursor: int = 0, count: int = 50) -> Optional[Dict[str, Any]]:
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.__session.get(
                    f'{self.API_URL}/comment/list/',
                    params={'aid': 1988, 'aweme_id': aweme_id, 'count': count, 'cursor': cursor},
                    timeout=15
                )
                response.raise_for_status()
                return response.json()
            except Exception as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Network error fetching comments (Attempt {attempt + 1}/{max_retries}). Retrying... | {e}")
                    time.sleep(random.uniform(3.0, 6.0))
                else:
                    logger.error(f"Failed to fetch comments for {aweme_id} after {max_retries} attempts: {e}")
                    return None
    
    def __call__(self, aweme_id: str) -> Comments:
        return self.get_all_comments(aweme_id=aweme_id)