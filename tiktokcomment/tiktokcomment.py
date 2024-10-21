import jmespath

from typing import Any, Dict, Iterator
from requests import Session, Response
from loguru import logger
from typing import Optional
from datetime import datetime
from tiktokcomment.typing import Comments, Comment

class TiktokComment:
    BASE_URL: str = 'https://www.tiktok.com'
    API_URL: str = '%s/api' % BASE_URL

    def __init__(
        self: 'TiktokComment'
    ) -> None:
        self.__session: Session = Session()
    
    def __parse_comment(
        self: 'TiktokComment',
        data: Dict[str, Any]
    ) -> Comment:
        data: Dict[str, Any] = jmespath.search(
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
            """ ,
            data
        )
    
        comment: Comment = Comment(
            **data,
            replies=list(
                self.get_all_replies(data.get('comment_id'))
            ) if data.get('total_reply') else []
        )

        logger.info('%s - %s : %s' % (
                comment.create_time,
                comment.username, 
                comment.comment
            )
        )

        return comment

    def get_all_replies(
        self: 'TiktokComment',
        comment_id: str
    ) -> Iterator[Comment]:
        page: int = 1
        while True:
            if(
                not (replies := self.get_replies(
                    comment_id=comment_id,
                    page=page
                ))
            ): break
            for reply in replies:
                yield reply
            
            page += 1

    def get_replies(
        self: 'TiktokComment',
        comment_id: str,
        size: Optional[int] = 50,
        page: Optional[int] = 1
    ):
        response: Response = self.__session.get(
            '%s/comment/list/reply/' % self.API_URL,
            params={
                'aid': 1988,
                'comment_id': comment_id,
                'item_id': self.aweme_id,
                'count': size,
                'cursor': (page - 1) * size
            }
        )

        return [
            self.__parse_comment(
                comment
            ) for comment in response.json().pop('comments')
        ]
    
    def get_all_comments(
        self: 'TiktokComment',
        aweme_id: str
    ) -> Comments:
        page: int = 1
        data: Comments = self.get_comments(
            aweme_id=aweme_id,
            page=page   
        )
        while(True):
            page += 1
            
            comments: Comments = self.get_comments(
                aweme_id=aweme_id,
                page=page
            )
            if(not comments.has_more): break

            data.comments.extend(
                comments.comments
            )

        return data

    def get_comments(
        self: 'TiktokComment',
        aweme_id: str,
        size: Optional[int] = 50,
        page: Optional[int] = 1
    ) -> Comments:
        self.aweme_id: str = aweme_id

        response: Response = self.__session.get(
            '%s/comment/list/' % self.API_URL,
            params={
                'aid': 1988,
                'aweme_id': aweme_id,
                'count': size,
                'cursor': (page - 1) * size
            }
        )

        data: Dict[str, Any] = jmespath.search(    
            """
            {
                caption: comments[0].share_info.title,
                video_url: comments[0].share_info.url,
                comments: comments,
                has_more: has_more
            }
            """,
            response.json()
        )

        return Comments(
            comments=[
                self.__parse_comment(
                    comment
                ) for comment in data.pop('comments')
            ],
            **data,
        )
    
    def __call__(
        self: 'TiktokComment',
        aweme_id: str
    ) -> Comments:
        return self.get_all_comments(
            aweme_id=aweme_id
        )
