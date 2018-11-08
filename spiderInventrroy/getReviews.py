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
sys.setrecursionlimit(1000000)

driver=webdriver.Firefox()

initUrl = "http://www.zhihu.com"
driver.get(initUrl)
wait=WebDriverWait(driver,100)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "GlobalSideBar-categoryList")))
driver.get(initUrl)

conn =pymysql.connect(host='localhost',user='root',password='qq1997lzy0509',port=3306,db='zhihulive',use_unicode=True,charset="utf8")
cursor=conn.cursor()
sql ="SELECT liveId FROM liveReview group by liveId"
sql0="SELECT liveId,numOfReview  FROM liveInfo"
url_list=[]
url_list0=[]
num_list=[]

cursor.execute(sql)
for i in cursor:
    mild = str(re.search("\d+",str(i)).group())
    url_list.append(mild)
    
cursor.execute(sql0)
for i in cursor:
    mi = str(re.search("\d+",str(i[0])).group())
    url_list0.append(mi)
    num_list.append(i[1])

def GetReview(liveId,Num):
    sql ="insert into LiveReview(liveId,peopleId,liveReview,reply,reviewStar,reviewDate) values (%s,%s,%s,%s,%s,%s)"
    
    Url ="https://www.zhihu.com/lives" + liveId + "/reviews"
    driver.get(Url)
    time.sleep(1)
    Comment=[]
  
    while(len(Comment)<int(Num)):
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        driver.execute_script("window.scrollBy(0,5000)")
        PageSource = driver.page_source

        bs = BeautifulSoup(PageSource, 'lxml')
        Comment = bs.findAll("div",{"data-za-module":"CommentItem"})
        
    for i in Comment:
       UserName = i.find("img",{"class":"Avatar-image-uu3z"}).attrs["alt"]
       try:
           UserId = str(i.find("a",{"class":"UserLink-root-1ogW"}).attrs["href"])[-32:]
           peopleUrl ="https://www.zhihu.com/people/"+ UserId
           driver.get(peopleUrl)
           time.sleep(0.05)
           UserId =str(driver.current_url)[29:-11]
       except:
           UserId ="00000000000000000000000000000000"
           
       UserCommentStar = re.search("[1-5]",str(i.find("div",{"class":""}).attrs['aria-label'])).group()
       try:
           UserComment = str(i.find("div",{"class":"ReviewItem-text-22Wg"}).string).translate(non_bmp_map)
           
       except:
           UserComment =""
       try:
           Reply = i.find("div",{"class":"ReviewItem-reply-1_lH"}).get_text()
       except:
           Reply =""
       try:
           CommentDate =re.sub("编辑于","",i.find("div",{"class":"ReviewItem-date-2XBc"}).find("span").string)
           Year = int(str(CommentDate)[:4])
           Month = int(str(CommentDate)[5:7])
           Day = int(str(CommentDate)[8:10])
           hour = int(str(CommentDate)[11:13])
           minute = int(str(CommentDate)[14:16])

           Date = datetime.datetime(Year, Month, Day,hour,minute)
       except:
           print(re.sub("编辑于","",i.find("div",{"class":"ReviewItem-date-2XBc"}).find("span").string))
       try:
           cursor.execute(sql,(liveId,UserId,UserComment,Reply,UserCommentStar,Date))
           conn.commit()
       except:
           print(liveId,UserId,UserComment,Reply,UserCommentStar,Date)
           pass

def main():
    for i in range(len(url_list0)):
        if i not in url_list or i >50:
            GetReview(url_list0[i],num_list[i])
            url_list.append(url_list0[i])
            print(len(url_list))
        else:
            pass


main()
