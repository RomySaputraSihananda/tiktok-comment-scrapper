import re
import time
import requests
import os
import asyncio

import pandas as pd

from json import dumps
from argparse import ArgumentParser
from comment import Comment, logging
from comment import getComments

def json2csv(json):
    # Pars to a Dataframe
    df = pd.DataFrame(columns=['date','text'])

    # Parse comments and replies to a csv
    for c in json:
        df = df._append({'date':c['create_time'],'text':c['comment']}, ignore_index=True)
        if len(c['replies'])>0:
            for r in c['replies']:
                df = df._append({'date':c['create_time'],'text':r['comment']}, ignore_index=True)
    else:
        return df

    return

if(__name__ == '__main__'):
    # Arguments
    argp: ArgumentParser = ArgumentParser()
    argp.add_argument("--url", '-u', type=str, default='7329272740622372139')
    argp.add_argument("--csv", '-c', action="store_true")
    argp.add_argument("--nojson", '-nj', action="store_true", default=False)
    argp.add_argument("--merge", '-m', action="store_true")
    argp.add_argument("--output", '-o', type=str, default='data')
    args = argp.parse_args()

    # Delete spaces from url
    url = (args.url).replace(' ', '')

    # Split by ','
    urls = url.split(',')

    videoid_list = []
    for url in urls:
        # Parse Url
        if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            videoid = requests.head(url, stream=True, allow_redirects=True, timeout=5).url.split("/")[5].split("?", 1)[0]
        elif re.match(r"^\d+$", url):
            videoid = url
        else:
            videoid = url.split("/")[5].split("?", 1)[0]

        # Append videoids
        videoid_list.append(videoid)

    json_full = []

    init = time.time();

    logging.info(f'Starting Scrapping for videos with id {videoid_list}')

    responses = asyncio.run(getComments(videoid_list))
    for i, response in enumerate(responses):
        comment: Comment = Comment()
        json = []
        data: dict = comment.execute(response)

        output: str = args.output

        if (not os.path.exists(output)):
            os.makedirs(output)

        if(data):
            json = data['comments']

        # Avoid merge
        if (args.merge):
            json_full += json
            continue

        # JSON
        if (not args.nojson):
            fileName = f'{output}/{videoid_list[i]}.json';
            with open(fileName, 'w') as file:
                file.write(dumps(json, ensure_ascii=False, indent=2))
                logging.info(f'Output data from video with id {videoid_list[i]} in {fileName}')
        # CSV
        if (args.csv):
            df = json2csv(json)
            if (not df.empty):
                df.to_csv(f'{output}/{videoid_list[i]}.csv')
                logging.info(f'Output {len(df.index)} comments csv data from video with id {videoid_list[i]} in {output}/{videoid_list[i]}.csv')
    if (args.merge):
        # JSON
        if (not args.nojson):
            fileName = f'{output}/full.json';
            with open(fileName, 'w') as file:
                file.write(dumps(json_full, ensure_ascii=False, indent=2))
                logging.info(f'Output merged json: {fileName}')
        # CSV
        if (args.csv):
            df = json2csv(json_full)
            if (not df.empty):
                df.to_csv(f'{output}/full.csv')
                logging.info(f'Output {len(df.index)} comments merged csv data: {output}/full.csv')

    print('Time: ' + str(time.time() - init));