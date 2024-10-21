import json

from datetime import datetime

from typing import Optional, List, Dict, Any

class Comment:
    def __init__(
        self: 'Comment',
        comment_id: str,
        username: str,
        nickname: str,
        comment: str,
        create_time: str,
        avatar: str,
        total_reply: int,
        replies: Optional[List['Comment']] = []
    ) -> None:
        self._comment_id: str = comment_id
        self._username: str = username
        self._nickname: str = nickname
        self._comment: str = comment
        self._create_time: str = datetime\
            .fromtimestamp(
                create_time
            ).strftime("%Y-%m-%dT%H:%M:%S")
        self._avatar: str = avatar
        self._total_reply: int = total_reply
        self._replies: List['Comment'] = replies

    @property
    def comment_id(
        self: 'Comment'
    ) -> str:
        return self._comment_id
    
    @property
    def username(
        self: 'Comment'
    ) -> str:
        return self._username
    
    @property
    def nickname(
        self: 'Comment'
    ) -> str:
        return self._nickname
    
    @property
    def comment(
        self: 'Comment'
    ) -> str:
        return self._comment
    
    @property
    def create_time(
        self: 'Comment'
    ) -> str:
        return self._create_time
    
    @property
    def avatar(
        self: 'Comment'
    ) -> str:
        return self._avatar
    
    @property
    def total_reply(
        self: 'Comment'
    ) -> int:
        return self._total_reply
    
    @property
    def replies(
        self: 'Comment'
    ) -> List['Comment']:
        return self._replies
    
    @property
    def dict(
        self: 'Comment'
    ) -> Dict[str, Any]:
        return {
            'comment_id': self._comment_id,
            'username': self._username,
            'nickname': self._nickname,
            'comment': self._comment,
            'create_time': self._create_time,
            'avatar': self._avatar,
            'total_reply': self._total_reply,
            'replies': [reply.dict for reply in self._replies]
        }
    
    @property
    def json(
        self: 'Comment'
    ) -> str:
        return json.dumps(self.json)
    
    def __str__(
        self: 'Comment'
    ) -> str:
        return self.json