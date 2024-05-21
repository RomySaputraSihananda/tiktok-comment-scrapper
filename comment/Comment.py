import requests
import logging
import aiohttp
import asyncio

from requests import Response
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s [ %(levelname)s ]\t:: %(message)s', datefmt="%Y-%m-%dT%H:%M:%S")

async def fetch(url, session):
    try:
        async with session.get(url) as response:
            if(response.status != 200): return logging.error(f'invalid url: {url}');
            return await response.json();
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")
        return None;

async def getComments(videoid_list: list):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(f'https://www.tiktok.com/api/comment/list/?aid=1988&aweme_id={videoid}&count=9999999', session) for videoid in videoid_list]
        responses = await asyncio.gather(*tasks)
        return responses

class Comment:
    def __init__(self) -> None:
        self.__result: dict             = {}
        self.__result["caption"]: str   = None
        self.__result["date_now"]: str  = None
        self.__result["video_url"]: str = None
        self.__result["comments"]: list = []

    def __format_date(self, milisecond: int) -> str:
        try:
            return datetime.fromtimestamp(milisecond).strftime("%Y-%m-%dT%H:%M:%S")
        except:
            return datetime.fromtimestamp(milisecond / 1000).strftime("%Y-%m-%dT%H:%M:%S")

    def __get_replies(self, commentid: str) -> list:
        [data, i] = [[], 0]

        while(True):
            res: Response = requests.get(f'https://www.tiktok.com/api/comment/list/reply/?aid=1988&comment_id={commentid}&count=9999999&cursor={i * 50}').json()
            
            if(not res['comments']): break

            data += res['comments']
            i += 1

        return self.__filter_comments(data)

    def __filter_comments(self, comments: list) -> list:
        new_comments: list = []

        for comment in comments:
            if(comment['share_info']['desc']): logging.info(comment['share_info']['desc'])

            new_comment = {
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

    def execute(self, res: str) -> None:
        try:
            self.__result['caption']: str = res['comments'][0]['share_info']['title']
            self.__result['date_now']: str = self.__format_date(res['extra']['now'])
            self.__result['video_url']: str = res['comments'][0]['share_info']['url']
            self.__result['comments']:list = self.__filter_comments(res['comments'])

        except:
            return logging.error('comments are over')

        return self.__result

# testing
if(__name__ == '__main__'):
    comment: Comment = Comment()
    comment.execute('7170139292767882522')