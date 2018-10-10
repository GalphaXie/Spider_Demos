from retrying import retry
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
}


@retry(stop_max_attempt_number=3)
def _parse_url(url):
    print("*" * 50)
    resp = requests.get(url, headers=headers, timeout=3)
    print(type(resp.status_code))
    assert resp.status_code == 200  # 这里是 int 类型
    return resp.content.decode(encoding='utf-8')  # 这里的写法是 encoding='utf-8'


def parse_url(url):
    try:
        html_str = _parse_url(url)
    except Exception as e:
        print(e)
        html_str = None
    return html_str


if __name__ == '__main__':
    url = 'http://www.baidu.com'
    html_str = parse_url(url)
    print(html_str[:20])
