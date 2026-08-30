import json
from datetime import datetime
from typing import Optional, List, Dict, Any

class Comment:
    def __init__(
        self,
        comment_id: str,
        username: str,
        nickname: str,
        comment: str,
        create_time: Any,
        avatar: str,
        total_reply: int,
        replies: Optional[List['Comment']] = None # FIXED: No mutable default
    ) -> None:
        self._comment_id: str = comment_id
        self._username: str = username
        self._nickname: str = nickname
        self._comment: str = comment
        self._avatar: str = avatar
        self._total_reply: int = total_reply
        self._replies: List['Comment'] = replies or [] # FIXED
        
        # FIXED: Robust timestamp parsing
        if isinstance(create_time, (int, float)):
            try:
                self._create_time: str = datetime.fromtimestamp(create_time).strftime("%Y-%m-%dT%H:%M:%S")
            except (ValueError, TypeError, OverflowError):
                self._create_time: str = str(create_time)
        else:
            self._create_time: str = str(create_time)

    @property
    def comment_id(self) -> str: return self._comment_id
    @property
    def username(self) -> str: return self._username
    @property
    def nickname(self) -> str: return self._nickname
    @property
    def comment(self) -> str: return self._comment
    @property
    def create_time(self) -> str: return self._create_time
    @property
    def avatar(self) -> str: return self._avatar
    @property
    def total_reply(self) -> int: return self._total_reply
    @property
    def replies(self) -> List['Comment']: return self._replies

    @property
    def dict(self) -> Dict[str, Any]:
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
    def json(self) -> str:
        return json.dumps(self.dict, ensure_ascii=False) # FIXED: No infinite recursion

    def __str__(self) -> str:
        return self.json