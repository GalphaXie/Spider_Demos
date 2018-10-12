# coding=utf-8
import time

import requests
from selenium import webdriver

from yundama import indetify


# 1.实例化deriver
driver = webdriver.Chrome()

# 2.请求url地址
url = 'https://www.douban.com/'
# 发送请求
driver.get(url)

# 输入用户名密码进行登录
driver.find_element_by_id('form_email').send_keys('user name')  # 需要配置自己的用户名
driver.find_element_by_id('form_password').send_keys('pass_word')  # 配置自己的密码

# 请求验证码
img_src = driver.find_element_by_id('captcha_image').get_attribute('src')
response = requests.get(img_src)  #请求验证码的地址
captcha_code = indetify(response.content)  #验证码识别

# 输入验证码
driver.find_element_by_id('captcha_field').send_keys(captcha_code)

time.sleep(2)

driver.find_element_by_class_name('bn-submit').click()

# 退出
time.sleep(10)
driver.quit()