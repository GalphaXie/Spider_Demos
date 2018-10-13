# coding=utf-8
from selenium import webdriver
import time

driver = webdriver.Chrome()  # 实例化dirver

# 调整浏览器窗口 的大小
driver.maximize_window()  # 最大化
# driver.set_window_size(1920,1080)

driver.get("http://www.baidu.com")

# 在input标签输入内容
driver.find_element_by_id("kw").send_keys("渣渣辉")  # 输入内容
driver.find_element_by_id("su").click()  # 点击元素

# 页面截屏
# driver.save_screenshot("./baidu.png")

# 获取页面源码
# print(driver.page_source)

# 获取当前的url地址
# print(driver.current_url)

# 获取cookie
print(driver.get_cookies())
print("*" * 100)
print({i["name"]: i["value"] for i in driver.get_cookies()})

time.sleep(3)
driver.quit()  # 退出浏览器
