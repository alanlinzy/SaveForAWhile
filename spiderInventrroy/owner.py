from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import time
import lxml
import datetime
import re
import sys
import pymysql

ReParticipantsUrl = re.compile('"url_token": "(.*?)", "id"')

headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
s = requests.Session()

_xsrf='30d4a23b-6557-4fc8-9ff9-f943ea4995bd'

loginurl = 'https://www.zhihu.com/login/email'
formdata={
  'email':'lzy19970509@qq.com',
  'password':'qq1997lzy0509',
  '_xsrf':'_xsrf'
  
  }
z5 = s.post(url=loginurl,data=formdata,headers=headers)
mylog='https://www.zhihu.com/people/lin-yang-72-83/logs'
s.get(url=mylog)


driver = webdriver.Firefox()

#initUrl = "http://www.zhihu.com"
#driver.get(initUrl)
#wait=WebDriverWait(driver,100)
#wait.until(EC.presence_of_element_located((By.CLASS_NAME, "GlobalSideBar-categoryList")))
#driver.get(initUrl)

conn =pymysql.connect(host='localhost',user='root',password='qq1997lzy0509',port=3306,db='zhihulive',use_unicode=True,charset="utf8")
cursor=conn.cursor()
sql = "select organizerId from liveInfo"
cursor.execute(sql)
ownerlist =[]
for i in cursor:
    mild = str(re.sub("\'","",re.search("\'.*?\'",str(i)).group()))
    ownerlist.append(mild)

sql1 = "select peopleId from liveowner"
cursor.execute(sql1)
ownerlist1 =[]
for i in cursor:
    mild = str(re.sub("\'","",re.search("\'.*?\'",str(i)).group()))
    ownerlist1.append(mild)
            
            
def GetPeople(peopleId):
    peopleUrl ="https://www.zhihu.com/people/"+ peopleId
    sql="insert into liveowner(peopleId,peopleName,numOfQuestion,numOfAnswer,numOfFollowing,numOfFollowed,numOfAgree,numOfThanks,numOfcollected,numOfShareEditing,numOfArticle,numOfColumn,numOfThought,numOfFollowTheme,numOfFollowColumn,numOfFollowQuestion,numOfFollowFavorite,numOfLive)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    driver.get(peopleUrl)
    time.sleep(1)
    peopleId =re.split("/",str(driver.current_url))[-2]
    page = driver.page_source
    bs = BeautifulSoup(page,"lxml")
    peopleName =bs.find("span",{"class":"ProfileHeader-name"}).string
    follow = bs.findAll("strong", {"class":"NumberBoard-itemValue"})
    numOfFollowing = int(follow[0].attrs["title"])
    numOfFollowed = int(follow[1].attrs["title"])
    numOfAnswer = int(re.sub(",","",bs.find("li",{"aria-controls":"Profile-answers"}).span.string))
    numOfAsk = int(re.sub(",","",bs.find("li",{"aria-controls":"Profile-asks"}).span.string))
    numOfArticle = int(re.sub(",","",bs.find("li",{"aria-controls":"Profile-posts"}).span.string))
    
    numOfColumn = int(re.sub(",","",bs.find("li",{"aria-controls":"Profile-columns"}).span.string))
    try:
        numOfThought=int(re.sub(",","",bs.find("li",{"aria-controls":"Profile-pins"}).span.string))
    except:
        numOfThought=0
    lightList = bs.findAll("span",{"class":"Profile-lightItemValue"})
    numOfLive = int(re.sub(",","",lightList[0].get_text()))
    numOfFollowTheme = int(re.sub(",","",lightList[1].get_text()))
    numOfFollowColumn = int(re.sub(",","",lightList[2].get_text()))
    numOfFollowQuestion = int(re.sub(",","",lightList[3].get_text()))
    
    try:
        numOfFollowFavorite = int(re.sub(",","",lightList[4].get_text()))
    except:
        numOfFollowFavorite =0
    card = bs.find("div",{"class":"Profile-sideColumn"})
    print(card)
    
    try:
        mid= str(re.search("获得 .*? 次赞同",str(card)).group())
        
        numOfAgree=int(re.sub("(<|>|,|获得|次赞同)","",mid))
        
    except:
        numOfAgree = 0
    
        
    try:
        mid=re.search("\">获得 .*? 次感谢",str(card)).group()
        numOfThanks =int(re.sub("(获得|,|次感谢|\"|>)","",mid))
        
    except:
        numOfThanks = 0
       
    try:
        mid =re.split("，",re.search(".*?次收藏",str(card)).group())[-1]
        
        numOfCollected =int(re.sub("(>|，|次收藏)","",mid))
        print(numOfCollected)
    except:
        numOfCollected = 0
       
    try:
        mid = str(re.search("参与 .*? 次公共编辑",str(card)).group())
        
        numOfShareEditing =int(re.sub("(,|>|<|参与|次公共编辑)","",mid))
        
    except:
        numOfShareEditing = 0
   
    
    try:
        cursor.execute(sql,(peopleId,peopleName,str(numOfAsk),str(numOfAnswer),str(numOfFollowing),str(numOfFollowed),str(numOfAgree),str(numOfThanks),str(numOfCollected),str(numOfShareEditing),str(numOfArticle),str(numOfColumn),str(numOfThought),str(numOfFollowTheme),str(numOfFollowColumn),str(numOfFollowQuestion),str(numOfFollowFavorite),str(numOfLive)))
        conn.commit()
    except:
        print(peopleId)
        
    
          

def main():
    for i in ownerlist:
        if i not in ownerlist1:
            GetPeople(i)
            ownerlist1.append(i)
            print(len(ownerlist1))




#main()
GetPeople("niu-du-du-46")
conn.close()
driver.close()


