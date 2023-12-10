import requests
import logging

from requests import Response
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ] :: %(message)s', datefmt="%Y-%m-%dT%H:%M:%S")

class Comment:
    def __init__(self) -> None:
        self.__result: dict = {}
        self.__result["caption"]: str = None
        self.__result["date_now"]: str = None
        self.__result["video_url"]: str = None
        self.__result["comments"]: list = []

    def __format_date(self, milisecond: int) -> str:
        try:
            return datetime.fromtimestamp(milisecond).strftime("%Y-%m-%dT%H:%M:%S")
        except:
            return datetime.fromtimestamp(milisecond / 1000).strftime("%Y-%m-%dT%H:%M:%S")

    def __get_replies(self, commentid: str) -> list:
        res: Response = requests.get(f'https://www.tiktok.com/api/comment/list/reply/?aid=1988&comment_id={commentid}&count=9999999').json()
        return self.__filter_comments(res['comments'])

    def __filter_comments(self, comments: list) -> list:
        new_comments: list = []

        for comment in comments:
            if(comment['share_info']['desc']): logging.info(comment['share_info']['desc'])

            new_comment = {
                "username": comment['user']['unique_id'],
                "nickname": comment['user']['nickname'],
                "comment": comment['text'],
                'create_time': self.__format_date(comment['create_time']),
                "avatar": comment['user']['avatar_thumb']['url_list'][0]
            }

            try:
                new_comment.update({
                    "total_reply": comment['reply_comment_total'],
                    "replies": self.__get_replies(comment['cid']) if comment['reply_comment_total'] > 0 else [] 
                })

            except:
                pass

            new_comments.append(new_comment)

        return new_comments

    def execute(self, videoid: str, size: int) -> None:
        logging.info(f'Starting Scrapping for video with id {videoid}.....')

        res: Response = requests.get(f'https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={videoid}&count=9999999&cursor={size}').json()

        if(res['status_code'] > 0): return logging.error('invalid id video');

        self.__result['caption']: str = res['comments'][0]['share_info']['title']
        self.__result['date_now']: str = self.__format_date(res['extra']['now'])
        self.__result['video_url']: str = res['comments'][0]['share_info']['url']
        self.__result['comments']:list = self.__filter_comments(res['comments'])

        return self.__result

# testing
if(__name__ == '__main__'):
    comment: Comment = Comment()
    comment.execute('7170139292767882522')
    # comment.execute('7308764254914628869')