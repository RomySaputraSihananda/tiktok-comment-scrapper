[![Twitter: romy](https://img.shields.io/twitter/follow/RomySihananda)](https://twitter.com/RomySihananda)

# tiktok-comment-scrapper

![](https://raw.githubusercontent.com/RomySaputraSihananda/RomySaputraSihananda/main/images/GA-U-u2bsAApmn9.jpeg)
Get all comments and replies from a TikTok video by URL or ID.

## Key Features & Updates

- **Bypass Bot Detection**: Replaced `requests` with `curl-cffi` (impersonating Chrome) to bypass TikTok's TLS/JA3 fingerprinting and Cloudflare protections.
- **Robust Networking**: Enforced IPv4 and added automatic retries to prevent DNS timeouts and network hiccups.
- **Modern Packaging**: Migrated from `main.py` + `requirements.txt` to standard PEP 621 `pyproject.toml` for easy installation via `pip`.
- **Smart URL Parsing**: You can now pass a full TikTok video URL directly; no need to manually extract the ID.
- **Memory Efficient**: Added `--format jsonl` support to stream comments to disk, preventing RAM crashes on viral videos.
- **Bug Fixes**: Fixed infinite recursion in JSON serialization, mutable default arguments, and `NoneType` errors from TikTok's API.

## Requirements

- **Python >= 3.11**

## Installation

### Option 1: Using `pip` (Standard)

```sh
git clone https://github.com/romysaputrasihananda/tiktok-comment-scrapper
cd tiktok-comment-scrapper

# Optional but recommended: virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\\Scripts\\activate`

# Install the CLI tool globally in your environment
pip install .
```

### Option 2: Using `uv` (Fast & Modern)

```sh
git clone https://github.com/romysaputrasihananda/tiktok-comment-scrapper
cd tiktok-comment-scrapper
uv sync
```

## Example Usages

```sh
# Scrape using a full URL
comment-scraper --aweme_id "https://www.tiktok.com/@user/video/7170139292767882522"

# Scrape using an ID, limit to 50 comments, and save as JSONL
comment-scraper --aweme_id 7170139292767882522 --limit 50 --format jsonl
```

### Flags

| Flag         | Alias | Description                                                  | Example            | Default |
| :----------- | :---: | :----------------------------------------------------------- | :----------------- | :------ |
| `--aweme_id` | `-id` | TikTok video URL or ID **(Required)**                        | `--aweme_id=url`   | `None`  |
| `--output`   | `-o`  | Output directory                                             | `--output=my_data` | `data`  |
| `--format`   |       | Output format (`json`/`jsonl`)                               | `--format=jsonl`   | `json`  |
| `--limit`    | `-l`  | Maximum number of comments (does not include reply comments) | `--limit=100`      | `All`   |

## Sample Output

```json
{
  "caption": "makk aku jadi animee🤩#faceplay #faceplayapp #anime #harem #xysryo ",
  "date_now": "2023-12-10T22:06:04",
  "video_url": "https://t.tiktok.com/i18n/share/video/7170139292767882522/?_d=0&comment_author_id=6838487455625479169&mid=7157599449395496962&preview_pb=0&region=ID&share_comment_id=7310977412674093829&share_item_id=7170139292767882522&sharer_language=en&source=h5_t&u_code=0",
  "comments": [
    {
      "username": "user760722966",
      "nickname": "rehan",
      "comment": "testing 😁😁",
      "create_time": "2023-12-10T21:46:36",
      "avatar": "https://p16-sign-useast2a.tiktokcdn.com/tos-useast2a-avt-0068-giso/f64f2c7df8a16098d3b3c80e958ffc52~c5_100x100.jpg?x-expires=1702306800&x-signature=KhUeuGmPAVij9A8gbgh7wK6rn98%3D",
      "total_reply": 0,
      "replies": []
    }
  ]
}
```

## License

This project is licensed under the [MIT License](LICENSE).
