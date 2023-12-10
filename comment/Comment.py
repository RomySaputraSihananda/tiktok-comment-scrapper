import requests
from requests import Response
from json import dumps
from datetime import datetime

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
            return datetime.fromtimestamp(milisecond/ 1000).strftime("%Y-%m-%dT%H:%M:%S")

    def __get_replies(self, commentid: str) -> list:
        print(commentid);
        res: Response = requests.get(f'https://www.tiktok.com/api/comment/list/reply/?aid=1988&comment_id={commentid}&count=9999999').json()
        return self.__filter_comments(res['comments'])

    def __filter_comments(self, comments: list) -> list:
        new_comments: list = []

        for comment in comments:
            try:
                new_comments.append({
                    "username": comment['user']['unique_id'],
                    "nickname": comment['user']['nickname'],
                    "comment": comment['text'],
                    'create_time': self.__format_date(comment['create_time']),
                    "avatar": comment['user']['avatar_thumb']['url_list'][0],
                    "total_reply": comment['reply_comment_total'],
                    "replies": self.__get_replies(comment['cid'])
                })

            except:
                new_comments.append({
                    "username": comment['user']['unique_id'],
                    "nickname": comment['user']['nickname'],
                    "comment": comment['text'],
                    'create_time': self.__format_date(comment['create_time']),
                    "avatar": comment['user']['avatar_thumb']['url_list'][0],
                })

        return new_comments

    def execute(self, videoid: str) -> None:
        res: Response = requests.get(f'https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={videoid}&count=9999999').json()

        if(res['status_code'] > 0): print('invalid id video');

        self.__result['caption']: str = res['comments'][0]['share_info']['title']
        self.__result['date_now']: str = self.__format_date(res['extra']['now'])
        self.__result['video_url']: str = res['comments'][0]['share_info']['url']
        self.__result['comments']:list = self.__filter_comments(res['comments'])

        with open('test.json', 'w') as file:
            file.write(dumps(self.__result, ensure_ascii=False))

if(__name__ == '__main__'):
    comment: Comment = Comment()
    # comment.execute('7170139292767882522')
    comment.execute('7308764254914628869')