#coding=utf-8

def gain_company_info(webpage,soup,company):
    company[0].append(webpage)
    company[1].append(soup.select('section.clearfix img')[0]['alt'])
    company[2].append(soup.select('section.clearfix div.name-and-welfare hq i')[0].get_text())
    company[3].append(soup.select('div.relative ul')[0].get_text())
    company[4].append(soup.select('p.profile')[0].get_text())
    company[5].append(soup.select('h2.product-title p')[0].get_text())
    company[6].append(soup.select('p.rate-num')[0].get_text())
    company[7].append(soup.select('time-num')[0].get_text())
    company[8].append(soup.select('ul.new-compintro ul')[0].get_text())
    company[9].append(soup.select('ul.new-compintro ul')[1].get_text())
    company[10].append(soup.select('ul.new-compintro ul')[2].get_text())
    company[11].append(soup.select('h2.job-title small')[0].get_text())

def gain_job_info(soup,job,i,company):
    i=i+1;
    job[0].append(soup.select('div.name-and-welfare h1')[0]['data-uid']+str(i))
    job[1].append(soup,select('div.job-info a.title')[0].get_text())
    job[2].append(company[0])
    job[3].append(company[1])
    job[4].append(soup.select('div.job-info span.text-warning')[0].get_text())
    job[5].append(soup.select('div.job-info p.condition')[1].get_text())
    job[6].append(soup.select('div.job-info p.condition')[2].get_text())
    job[7].append(soup.select('div.job-info p.condition')[3].get_text())
    job[8].append(soup.select('div.job-info time')[0]['title'])
    job[9].append(soup.select('div.job-info p.time-info span').get_text())

def gain_area(soup,area,company):
    j = 0
    for i in soup.select('div.selectui li'):
        area[j][0].append(i['title'])
        area[j][1].append(company[0])
        area[j][2].append(company[1])
        j+=1
    return j
    
def gain_field(hangye,field,company):
    field[0].append(hangye)
    field[1].append(company[0])
    field[2].append(company[1])

def insert_companytable(cursor,company):
    cursor.executemany("insert into Company(C_ID_Url,C_Name,Follower_Count,C_Welfare,C_Describe,C_Product_Describe,Resume_View_Rate,Resume_View_Time,C_Develop_Field,C_Scale,C_Address)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",company)
    num=int(re.sub("\D"," ",company[11]))
    cursor.execute("update Company set Recruitment_Count=%d where C_Name = %s",num,company[1])

def insert_jobtable(cursor,job):
    cursor.executemany("insert into Job(J_ID,J_Name,C_ID_Url,C_Name,J_Salary,J_Region,J_Degree_Requirement,J_Experience_Requirement,J_Publish_Time,J_Feedback_Time)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",job)

def insert_areatable(num,cursor,area):
    for i in range(0,num):
        cursor,executemany("insert into Area(Area_Name,C_ID_Url,C_Name)values(%s,%s,%s)",area[i])

def insert_fieldtable(cursor,field):
    cursor.executemany("insert into Field(Field_Name,C_ID_Url,C_Name)")

