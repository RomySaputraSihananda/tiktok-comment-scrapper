import re
import os
import requests

from json import dumps
from argparse import ArgumentParser
from comment import Comment, logging

if(__name__ == '__main__'):
    argp: ArgumentParser = ArgumentParser()
    argp.add_argument("--url", '-u', type=str, default='7170139292767882522')
    argp.add_argument("--size", '-s', type=int, default=50)
    argp.add_argument("--output", '-o', type=str, default='data')
    args = argp.parse_args()

    if "vm.tiktok.com" in args.url or "vt.tiktok.com" in args.url:
        videoid = requests.head(args.url, stream=True, allow_redirects=True, timeout=5).url.split("/")[5].split("?", 1)[0]
    elif re.match("^\d+$", args.url):
        videoid = args.url
    else:
        videoid = args.url.split("/")[5].split("?", 1)[0]
    
    comment: Comment = Comment()

    for i in range(round(args.size / 50)):
        data: dict = comment.execute(videoid, i * 50)

        output: str = f'{args.output}/{videoid}'

        if(not os.path.exists(output)):
                os.makedirs(output)

        with open(f'{output}/{args.size}.json', 'w') as file:
            file.write(dumps(data, ensure_ascii=False))
            logging.info(f'Output data : {output}/{args.size}.json')
    
    logging.info('Scrapping Success...')

    

