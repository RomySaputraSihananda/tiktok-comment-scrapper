import re
import os
import requests
import math
import pandas as pd
import numpy as np

from json import dumps
from argparse import ArgumentParser
from comment import Comment, logging

if(__name__ == '__main__'):
    # Arguments
    argp: ArgumentParser = ArgumentParser()
    argp.add_argument("--url", '-u', type=str, default='7329272740622372139')
    argp.add_argument("--csv", '-c', action="store_true")
    argp.add_argument("--size", '-s', type=int, default=50)
    argp.add_argument("--output", '-o', type=str, default='data')
    args = argp.parse_args()

    # Delete spaces from url
    url = (args.url).replace(' ', '')

    # Check if url is a list
    if "," in args.url:
        urls = url.split(',')
    else:
        urls = [url]

    videoids = []
    for url in urls:
        # Parse Url
        if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            videoid = requests.head(url, stream=True, allow_redirects=True, timeout=5).url.split("/")[5].split("?", 1)[0]
        elif re.match("^\d+$", url):
            videoid = url
        else:
            videoid = url.split("/")[5].split("?", 1)[0]

        # Append videoids
        videoids.append(videoid)

    json_full_csv = []

    for videoid in videoids:
        comment: Comment = Comment()
        [json_full, dummy] = [[], {}];

        for i in range(math.ceil(args.size / 50)):
            data: dict = comment.execute(videoid, i * 50)

            if (args.csv):
                output: str = args.output
            else:
                output: str = f'{args.output}/{videoid}'

            if (not os.path.exists(output)):
                os.makedirs(output)

            if(data):
                dummy = data
                json_full += data['comments']

                if (not args.csv):
                    with open(f'{output}/{i * 50}-{(i + 1) * 50}.json', 'w') as file:
                        file.write(dumps(data, ensure_ascii=False, indent=2))
                        logging.info(f'Output data : {output}/{i * 50}-{(i + 1) * 50}.json')

        dummy['comments'] = json_full
        json_full_csv += json_full

        if (not args.csv):
            with open(f'{output}/full.json', 'w') as file:
                file.write(dumps(dummy, ensure_ascii=False, indent=2))
                logging.info(f'Output data : {output}/full.json')
        
            logging.info(f'Scrapping Success, Output all data : {output}')
    # Convert to csv
    if (args.csv):
        df  = pd.DataFrame(columns=['date','text'])

        for c in json_full_csv:
            df = df._append({'date':c['create_time'],'text':c['comment']}, ignore_index=True)
            if len(c['replies'])>0:
                for r in c['replies']:
                    df = df._append({'date':c['create_time'],'text':r['comment']}, ignore_index=True)

        if (len(urls) > 1):
            df.to_csv(f'{output}/full.csv')
        else:
            df.to_csv(f'{output}/{videoid}.csv')

        logging.info(f'Scrapping Success, Output all data : {output}/{videoid}.csv')
