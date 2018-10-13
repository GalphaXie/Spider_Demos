# coding=utf-8
from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://mail.qq.com/")

driver.switch_to.frame("login_frame")  # 查看网页源码,有三种写法
driver.find_element_by_id("u").send_keys("123456@qq.com")

time.sleep(5)
driver.quit()
