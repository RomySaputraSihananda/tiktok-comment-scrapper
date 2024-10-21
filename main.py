import re
import os
import click
import json

from loguru import logger

from tiktokcomment import TiktokComment
from tiktokcomment.typing import Comments

__title__ = 'TikTok Comment Scrapper'
__version__ = '2.0.0'

@click.command(
    help=__title__
)
@click.version_option(
    version=__version__,
    prog_name=__title__
)
@click.option(
    "--aweme_id",
    help='id video tiktok',
    callback=lambda _, __, value: match.group(0) if(match := re.match(r"^\d+$", value)) else None
)
@click.option(
    "--output",
    default='data/',
    help='directory output data'
)
def main(
    aweme_id: str,
    output: str
): 
    if(not aweme_id):
        raise ValueError('example id : 7418294751977327878')      
    
    logger.info(
        'start scrap comments %s' % aweme_id
    )

    comments: Comments = TiktokComment()(
        aweme_id=aweme_id
    )

    if not (
        os.path.exists(
            dir := os.path.dirname(output)
        )
    ):
        os.makedirs(dir)

    json.dump(
        comments.dict,
        open(
            (final_path := '%s%s.json' % (output, aweme_id)),
            'w'
        ),
        ensure_ascii=False
    )

    logger.info(
        'save comments %s on %s' % (aweme_id, final_path)
    )


if(__name__ == '__main__'):
    main()