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
sql ="SELECT liveId FROM liveInfo"
sql0="SELECT liveId FROM liveTheme"
url_list=[]
url_list0=[]

cursor.execute(sql)
for i in cursor:
    mild = str(re.search("\d+",str(i)).group())
    url_list.append(mild)
    
cursor.execute(sql0)
for i in cursor:
    mi = str(re.search("\d+",str(i)).group())
    url_list0.append(mi)


def GetLiveINI(Url): #方法传入参数为知乎Live Url
    sqlLive ="insert into liveInfo (liveId,liveName,organizerId,sTime,score,numOfReview,numOfMember,numOfAudio,numOfFile,numOfAnswer,price)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    driver.get(Url)
    time.sleep(2)
    PageSource = driver.page_source

    bs = BeautifulSoup(PageSource, 'lxml')

    LiveId = Url[-18:]
    try:

        Name = str(bs.find("div", {"class": "LivePageHeader-line-SzR2 LivePageHeader-title-1RQL"}).string).translate(non_bmp_map)#Live名字
    except:
        Name =""
    try:
       date = bs.find("div", {"class": "LivePageHeader-timeNumber-3dX8"}).get_text()
       Year = int(str(date)[:4])
       Month = int(str(date)[5:7])
       Day = int(str(date)[8:10])
       hour = int(str(date)[11:13])
       minute = int(str(date)[14:16])
       
    except:
       date = bs.find("div", {"class": "LivePageHeader-timeNumber-3dX8"}).get_text()
       Year = int(str(date)[:5])
       Month = int(str(date)[6:8])
       Day = int(str(date)[9:11])
       hour = int(str(date)[12:14])
       minute = int(str(date)[15:17])
    Date = datetime.datetime(Year, Month, Day,hour,minute)#Live举办时间

    try:
        Star = bs.find("span", {"class": "LiveContentInfo-scoreNum-Qa-K"}).get_text()#Live星级数
    except:
        Star = 0
    try :
       EvaluationNum = int(str(bs.find("div", {"class": "LiveContentInfo-reviewText-1ncS"}).get_text())[:-9])#Live评论数
    except:
       EvaluationNum = 0

    INFList = bs.findAll("div", {"class": "LiveContentInfo-item-w7BI"})

    mid =""
    for i in INFList:
        mid=mid+str(i)
    
    try:
        Aswer = str(re.search("问答",mid).group())
        
    except:
        Aswer = ""
    try:
        File = str(re.search("文件",mid).group())
        
    except:
        File =""

    try:
        Sound = str(re.search("语音",mid).group())
        SoundMinute = int(INFList[0].findAll("div")[0].get_text()) #Live分钟语音数
        
    except:
        SoundMinute = 0
        
    if SoundMinute == 0:
        
        if Aswer == "问答" :
            AswerNum = int(INFList[0].findAll("div")[0].get_text()) #Live文件数
            if File == "文件":
                FileNum = int(INFList[1].findAll("div")[0].get_text())
            else:
                FileNum = 0
        
        else:
            AswerNum =0
            if File == "文件":
                FileNum = int(INFList[0].findAll("div")[0].get_text())
            else:
                FileNum = 0

    else:
        if Aswer == "问答" :
            AswerNum = int(INFList[1].findAll("div")[0].get_text()) #Live文件数
            if File == "文件":
                FileNum = int(INFList[2].findAll("div")[0].get_text())
            else:
                FileNum = 0
        
        else:
            AswerNum =0
            if File == "文件":
                FileNum = int(INFList[1].findAll("div")[0].get_text())
            else:
                FileNum = 0
    
    try:
        LiveParticipantsNum = str(bs.find("span", {"class": "Participants-text--jB3"}).get_text())[:-5]
    except:
        LiveParticipantsNum = 0
    try:
        Price = str(re.sub("（|）|¥","",re.search("（¥.*?\d）",str(bs.find("div",{"class":"LiveActions-buttonWrapper-3mOE"}))).group()))
    except:
        Price = 0
    
    LiveOwner =  str(bs.find("a", {"class": "LiveSpeakers-link-6dN8 UserLink-root-1ogW"})['href'])[13:] #Live举办人个人信息主页ID
    driver.get("https://www.zhihu.com/people/"+ LiveOwner + "/answers")
    time.sleep(1)
    LiveOwnerId = re.split("/",str(driver.current_url))[-2]
    

    
   
    try:
        cursor.execute(sqlLive,(LiveId,Name,LiveOwnerId,Date,Star,str(EvaluationNum),str(LiveParticipantsNum),str(SoundMinute),str(FileNum),str(AswerNum),str(Price)))
        conn.commit()
    except:
        print("liveId:"+LiveId)
        print(Name)
        print(LiveOwnerId)
        print(Date)
        print(Star)
        print(str(EvaluationNum))
        print(str(LiveParticipantsNum))
        print(str(SoundMinute))
        print(str(FileNum))
        print(str(AswerNum))
        print(str(Price))
        

   
                  

def gethtml(Url):
         
 
       
    
                url_list.append(Url)
                GetLiveINI("https://www.zhihu.com/lives/"+Url)
                print(len(url_list))
  


def main():

    for i in url_list0:
       try:
         if i not in url_list:
            gethtml(i)
       except:
           pass
       print(i)
      
main()
