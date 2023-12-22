import re
import os
import requests
import math

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

    [json_full, dummy] = [[], {}];

    for i in range(math.ceil(args.size / 50)):
        data: dict = comment.execute(videoid, i * 50)

        output: str = f'{args.output}/{videoid}'

        if(not os.path.exists(output)):
                os.makedirs(output)

        if(data):
            dummy = data
            json_full += data['comments']

            with open(f'{output}/{i * 50}-{(i + 1) * 50}.json', 'w') as file:
                file.write(dumps(data, ensure_ascii=False, indent=2))
                logging.info(f'Output data : {output}/{i * 50}-{(i + 1) * 50}.json')
        
    dummy['comments'] = json_full

    with open(f'{output}/full.json', 'w') as file:
        file.write(dumps(dummy, ensure_ascii=False, indent=2))
        logging.info(f'Output data : {output}/full.json')
    

    logging.info(f'Scrapping Success, Output all data : {output}')
