#coding=utf-8

from selenium import webdriver
from bs4 import BeautifulSoup

webpage = input("请输入网址：")
driver = webdriver.Chrome()
driver.get(webpage)

soup = BeautifulSoup(driver.page_source,'lxml')
for i in soup.select('div.backdrop-area div.wrap ul a'):
    print(i['href'])
driver.close()

