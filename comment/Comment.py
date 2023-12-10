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

    def __filter_comments(self, comments: list):
        for comment in comments:
            self.__result['comments'].append(comment['text'])

    def execute(self, id: str) -> None:
        res: Response = requests.get(f'https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={id}&count=9999999&cursor=0').json()
        
        if(res['status_code'] > 0): print('invalid id video');

        self.__result['caption']: str = res['comments'][0]['share_info']['title']
        self.__result['date_now']: str = self.__format_date(res['extra']['now'])
        self.__result['video_url']: str = res['comments'][0]['share_info']['url']

        self.__filter_comments(res['comments'])

        print(self.__result);

if(__name__ == '__main__'):
    comment: Comment = Comment()
    comment.execute('7170139292767882522')