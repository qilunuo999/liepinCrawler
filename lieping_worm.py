#coding=utf-8

from selenium import webdriver
from bs4 import BeautifulSoup
import pymysql
import time

def gain_company_info(webpage,soup,company):
    company.append(webpage)
    company.append(soup.select('section.clearfix img')[0]['alt'])
    if soup.select('div.name-and-welfare h1 i'):
        company.append(soup.select('div.name-and-welfare h1 i')[0].get_text())
    else:
        company.append("无")
    if soup.select('div.relative ul'):
        company.append(soup.select('div.relative ul')[0].get_text())
    else:
        company.append("无")
    if soup.select('p.profile'):
        company.append(soup.select('p.profile')[0].get_text())
    else:
        company.append("无")
    if soup.select('h2.product-title p'):
        company.append(soup.select('h2.product-title p')[0].get_text())
    else:
        company.append("无")
    if soup.select('p.rate-num'):
        company.append(soup.select('p.rate-num')[0].get_text())
    else:
        company.append("无")
    if soup.select('p.time-num'):
        company.append(soup.select('p.time-num')[0].get_text())
    else:
        company.append("无")
    if soup.select('ul.new-compintro li'):
        company.append(soup.select('ul.new-compintro li')[0].get_text())
        company.append(soup.select('ul.new-compintro li')[1].get_text())
        company.append(soup.select('ul.new-compintro li')[2].get_text())
    if soup.select('h2.job-title small'):
        company.append(soup.select('h2.job-title small')[0].get_text())

def gain_job_info(soup,job,i,company):
    i=i+1;
    for k in range(0,len(soup.select('div.job-info a.title'))):
        job[k].append(soup.select('div.name-and-welfare h1 a')[0]['data-uid']+str(i)+str(k))
        job[k].append(soup.select('div.job-info a.title')[k].get_text())
        job[k].append(company[0])
        job[k].append(company[1])
        job[k].append(soup.select('div.job-info span.text-warning')[k].get_text())
        job[k].append(soup.select('div.job-info p.condition span')[k+1].get_text())
        job[k].append(soup.select('div.job-info p.condition span')[k+2].get_text())
        job[k].append(soup.select('div.job-info p.condition span')[k+3].get_text())
        job[k].append(soup.select('div.job-info time')[k]['title'])
        job[k].append(soup.select('div.job-info p.time-info span')[k].get_text())

def gain_area(soup,area,company):
    j = 0
    for i in soup.select('div.selectui.job-address li')[1:]:
        area[j].append(i['title'])
        area[j].append(company[0])
        area[j].append(company[1])
        j+=1
    return j
    
def gain_field(hangye,field,company):
    field.append(hangye)
    field.append(company[0])
    field.append(company[1])

def insert_companytable(cursor,company):
    cursor.executemany("insert into Company(C_ID_Url,C_Name,Follower_Count,C_Welfare,C_Describe,C_Product_Describe,Resume_View_Rate,Resume_View_Time,C_Develop_Field,C_Scale,C_Address,Recruitment_Count)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[company])
    conn.commit()
    

def insert_jobtable(cursor,job):
    for i in range(0,15):
        if job[i]:
            cursor.executemany("insert into Job(J_ID,J_Name,C_ID_Url,C_Name,J_Salary,J_Region,J_Degree_Requirement,J_Experience_Requirement,J_Publish_Time,J_Feedback_Time)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",[job[i]])
    conn.commit()

def insert_areatable(num,cursor,area):
    for i in range(0,num):
        cursor.executemany("insert into Area(Area_Name,C_ID_Url,C_Name)values(%s,%s,%s)",[area[i]])
    conn.commit()

def insert_fieldtable(cursor,field):
    cursor.executemany("insert into Field(Field_Name,C_ID_Url,C_Name)values(%s,%s,%s)",[field])
    conn.commit()

webpage = input("请输入网址：")
hangye = input("请输入行业：")
driver = webdriver.Chrome()
driver.get(webpage)

soup = BeautifulSoup(driver.page_source,'lxml')
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='qaz12345', db='c_db', charset='utf8')
cursor = conn.cursor()

company = []
job = [[] for j in range(15)]
field = []
area = [[] for j in range(100)]

gain_company_info(webpage,soup,company)
gain_job_info(soup,job,0,company)
num=gain_area(soup,area,company)
gain_field(hangye,field,company)

#insert_companytable(cursor,company)
#insert_jobtable(cursor,job)
#insert_areatable(num,cursor,area)
#insert_fieldtable(cursor,field)

for i in range(0,int(soup.select('div.pager a.last')[0]['number'])):
    for j in range(0,15):
        job[j]=[]
    print("请点击招聘的下一页")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source,'lxml')
    gain_job_info(soup,job,i+1,company)
    insert_jobtable(cursor,job)

print("结束")
cursor.close()
conn.close()
driver.close()


