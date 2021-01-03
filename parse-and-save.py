import json
import requests
import re


def get_playlist(url: str):
    resp = requests.get(url, allow_redirects=True)
    content = resp.content
    matches = re.search('file:[^"]*"([^"]+)"', str(content))
    playlist_url = matches.groups()[0]

    headers = {
        'referer': 'https://audio-knigi.org/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36',
    }
    resp = requests.get(playlist_url, allow_redirects=True, headers=headers)
    playlist = str(resp.content, encoding='utf-8')
    playlist_object = json.loads(playlist)

    return playlist_object


def get_files_by_playlist(playlist: json):
    headers = {
        'referer': 'https://audio-knigi.org/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/87.0.4280.88 Safari/537.36',
    }

    for item in playlist:
        title = item['title']
        file_url = item['file']
        r = requests.get(file_url, allow_redirects=True, headers=headers)
        open(title + '.mp3', 'wb').write(r.content)


def main(url: str):
    playlist = get_playlist(url)
    get_files_by_playlist(playlist)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Parse and save audio book')
    parser.add_argument('--url', required=True,
                        help='the url to book')
    args = parser.parse_args()
    main(url=args.url)
