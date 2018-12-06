import requests
from requests.exceptions import RequestException
import time
import random
import os
from login import get_cookies


class UserListSpider():
    def __init__(self, headers, cookies):
        self.headers = headers
        self.cookies = cookies

    # 通过一名用户获取n名用户列表
    def get_more_users(self, n, user, users):
        new_users = [user]
        i = 0
        while i < len(new_users) <= n:
            followee_list = self.get_followees(new_users[i])
            for user in followee_list:
                if user not in users:
                    new_users.append(user)
                    users.append(user)
                    with open('data/users.txt', 'a', encoding='utf-8') as f:
                        f.write(user + '\n')
                if len(new_users) > n:
                    break
            i += 1

    # 获取关注者列表
    def get_followees(self, user):
        url = 'https://www.zhihu.com/api/v4/members/' + user + '/followees?offset=0&limit=20'
        followees = []
        time.sleep(3)
        try:
            res = requests.get(url, headers=self.headers, cookies=self.cookies, timeout=20)
            if res.status_code != 200:
                self.write_to_log('爬取用户 %s 的关注者时发生异常，代码：%d' % (user, res.status_code), 'log.txt')
                return followees
            d = res.json()
            followees.extend([i['url_token'] for i in d['data']])
        except RequestException as e:
            self.write_to_log('爬取用户 %s 的关注者时发生异常：%s' % (user,e), 'log.txt')
            return followees

        return followees

    # 写入日志
    def write_to_log(self, msg, file):
        with open(file, 'a', encoding='utf-8') as f:
            t = time.asctime(time.localtime(time.time()))
            f.write(t + '\t' + msg + '\n')

    def start(self, number):
        if os.path.exists('data/users.txt'):
            with open('data/users.txt', 'r', encoding='utf-8') as f:
                start_list = [line.strip() for line in f.readlines()]
                start_user = random.choice(start_list)
        else:
            start_list = []
            start_user = ''  # 起始用户
        self.get_more_users(number, start_user, start_list)


def main():
    user = ''     # 用户名
    passwd = ''    # 密码
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    cookies = get_cookies(user, passwd)
    number = 10000
    spider = UserListSpider(headers, cookies)
    spider.start(number)


if __name__ == "__main__":
    main()
