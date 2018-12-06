import requests
from requests.exceptions import RequestException
import time
import os
import json
from login import get_cookies


class UserTopicSpider():

    def __init__(self, headers, cookies):
        self.headers = headers
        self.cookies = cookies

    # 解析每名用户数据
    def parse_user(self, user):
        user_url = 'https://www.zhihu.com/api/v4/members/' + user + '?include=following_topic_count'
        time.sleep(3)
        try:
            res = requests.get(user_url, headers=self.headers, cookies=self.cookies, timeout=20)
            if res.status_code != 200:
                self.write_to_log('爬取用户 %s 时发生异常，代码：%d' % (user, res.status_code), 'log.txt')
                return None
            d = res.json()
            one_user = {
                'id': user,
                'name': d['name'],
                'type': d['user_type'],
                'following_topic_count': d['following_topic_count'],
                'following_topics': self.get_topics(user, d['following_topic_count'])
                }
        except RequestException as e:
            self.write_to_log('爬取用户 %s 时发生异常：%s' % (user, e), 'log.txt')
            return None
        return one_user

    # 爬取用户关注话题
    def get_topics(self, user, count):
        detail = []
        for i in range(count//20+1):
            url = 'https://www.zhihu.com/api/v4/members/' + user + '/following-topic-contributions?limit=20&offset=' + str(i*20)
            retry = 3
            while retry > 0:
                time.sleep(3)
                try:
                    res = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=20)
                    if res.status_code != 200:
                        self.write_to_log('爬取用户 %s 关注的话题时发生异常，代码：%d' % (user, res.status_code), 'log.txt')
                        retry -= 1
                        continue
                    d = res.json()
                    detail.extend([{'id': i['topic']['id'] , 'title': i['topic']['name']} for i in d['data']])
                    retry = 0
                except RequestException as e:
                    self.write_to_log('爬取用户 %s 关注的话题时发生异常: %s' % (user,e),'log.txt')
                    retry -= 1
                    continue
    
        return detail

    # 写入日志
    def write_to_log(self, msg, file):
        with open(file, 'a', encoding='utf-8') as f:
            t = time.asctime( time.localtime(time.time()))
            f.write(t+'\t' + msg + '\n')

    def start(self, position):
        p = position
        while True:
            with open('data/users.txt', 'r', encoding='utf-8') as f:
                f.seek(p)
                user = f.readline().strip()
                p = f.tell()
            if not user:
                break
            else:
                data = self.parse_user(user)
                if data:
                    with open('data/user_following_topics.txt', 'a', encoding='utf-8') as f:
                        f.write(json.dumps(data) + '\n')
                    with open('data/end_position_uft.txt', 'w') as f:
                        f.write(str(p))


def main():
    user = ''  # 用户名
    passwd = ''  # 密码
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    cookies = get_cookies(user, passwd)
    if os.path.exists('data/end_position_uft.txt'):
        with open('data/end_position_uft.txt', 'r') as f:
            position = int(f.readline().strip())
    else:
        position = 0
    spider = UserTopicSpider(headers, cookies)
    spider.start(position)


if __name__ == "__main__":
    main()

