import threading
import os
from userlist import UserListSpider
from usertopic import UserTopicSpider
from login import get_cookies
import time


class GetUsers(threading.Thread):

    def __init__(self, name, headers=None, cookies=None):
        threading.Thread.__init__(self)
        self.name = name
        self.headers = headers
        self.cookies = cookies

    def run(self):
        number = 10000
        spider = UserListSpider(self.headers, self.cookies)
        spider.start(number)


class GetTopic(threading.Thread):

    def __init__(self, name, headers=None, cookies=None):
        threading.Thread.__init__(self)
        self.name = name
        self.headers = headers
        self.cookies = cookies

    def run(self):
        if os.path.exists('data/end_position_uft.txt'):
            with open('data/end_position_uft.txt', 'r') as f:
                position = int(f.readline().strip())
        else:
            position = 0
        spider = UserTopicSpider(self.headers, self.cookies)
        spider.start(position)


class Check(threading.Thread):

    def __init__(self, name, t1, t2, duration, headers=None, cookies=None):
        threading.Thread.__init__(self)
        self.name = name
        self.t1 = t1
        self.t2 = t2
        self.duration = duration
        self.headers = headers
        self.cookies = cookies

    def run(self):
        for i in range(self.duration//300):
            if not self.t1.isAlive():
                self.t1 = GetUsers('get_users_thread', self.headers, self.cookies)
                self.t1.start()
            if not self.t2.isAlive():
                self.t2 = GetTopic('get_topic_thread', self.headers, self.cookies)
                self.t2.start()
            time.sleep(300)


def main():
    user = ''  # 用户名
    passwd = ''  # 密码
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    cookies = get_cookies(user, passwd)
    thread1 = GetUsers('get_users_thread', headers, cookies)
    thread2 = GetTopic('get_topic_thread', headers, cookies)
    thread3 = Check('check_thread', thread1, thread2, 40000, headers, cookies)
    thread3.start()


if __name__ == "__main__":
    main()
