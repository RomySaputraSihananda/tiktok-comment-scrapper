import json

from typing import List, Any, Dict

from .comment import Comment

class Comments:
    def __init__(
        self: 'Comments',
        caption: str,
        video_url: str,
        comments: List[Comment],
        has_more: int
    ) -> None:
        self._caption: str = caption
        self._video_url: str = video_url
        self._comments: List[Comment] = comments
        self._has_more: int = has_more

    @property
    def caption(
        self: 'Comments'
    ) -> str:
        return self._caption
    
    @property
    def video_url(
        self: 'Comments'
    ) -> str:
        return self._video_url
    
    @property
    def comments(
        self: 'Comments'
    ) -> List[Comment]:
        return self._comments
    
    @property
    def has_more(
        self: 'Comments'
    ) -> int:
        return self._has_more
    
    @property
    def dict(
        self: 'Comments'
    ) -> Dict[str, Any]:
        return {
            'caption': self._caption,
            'video_url': self._video_url,
            'comments': [comment.dict for comment in self._comments],
            'has_more': self._has_more  
        }
    
    @property
    def json(
        self: 'Comments'
    ) -> str:
        return json.dumps(self.dict)
    
    def __str__(
        self: 'Comments'
    ) -> str:
        return self.json