from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time


# 浏览器模拟登陆
def get_cookies(username, password):
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_headless()
    browser = webdriver.Firefox(firefox_options=firefox_options)
    try:
        browser.get("https://www.zhihu.com/signin")
        input_name = browser.find_element_by_name('username')
        input_passwd = browser.find_element_by_name('password')
        input_name.send_keys(username)
        input_passwd.send_keys(password)
        button = browser.find_element_by_xpath('//button[@type="submit"]')
        button.click()
        time.sleep(2)
        # 保存cookies
        cookies_list = browser.get_cookies()
        cookies = {}
        for i in range(len(cookies_list)):
            cookies[cookies_list[i]['name']] = cookies_list[i]['value']
    except WebDriverException as e:
        print('登录失败：%s' % e)
        return None
    browser.close()
    return cookies
