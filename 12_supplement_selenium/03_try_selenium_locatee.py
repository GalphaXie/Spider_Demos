# coding=utf-8
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://movie.douban.com/top250")

# find_element和find_elements的取舍
# ret2 = driver.find_elements_by_xpath("//div[@class='item111']")
# print(ret2)
# print("*"*100)
#
# ret1 = driver.find_element_by_xpath("//div[@class='item111']")
# print(ret1)

# #获取文本
# ret3 = driver.find_elements_by_xpath("//span[@class='title']")
# # print(ret3)
# ret3 = [i.text for i in ret3]
# # print(ret3)
#
# #获取属性的值
# ret4 = driver.find_elements_by_xpath("//span[@class='title']/..")
# print(ret4[0].get_attribute("href"))
# ret4 = [i.get_attribute("href") for i in ret4]
# print(ret4)


# 根据标签的文本定位元素
ret5 = driver.find_element_by_link_text("后页>").get_attribute("href")
print(ret5)

# 根据标签包含的文本定位元素
ret6 = driver.find_element_by_partial_link_text("后页").get_attribute("href")
print(ret6)

driver.quit()
