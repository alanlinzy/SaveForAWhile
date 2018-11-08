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
timeformat = "%Y-%m-%d %H:%M:%S"

#profile = webdriver.FirefoxProfile()
#profile.set_preference('network.proxy.type', 1)
#profile.set_preference('network.proxy.http', '113.86.222.32')
#profile.set_preference('network.proxy.http_port', 808)  # int
#profile.update_preferences()
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
url_list1=[]
cursor.execute(sql)
url_list.append("https://www.zhihu.com/lives")
url_list0.append("https://www.zhihu.com/lives")
url_list1.append("https://www.zhihu.com/lives")
for i in cursor:
    mild = str(re.search("\d+",str(i)).group())
    url_list.append(mild)
    url_list0.append(mild)

cursor.execute(sql0)
for i in cursor:
    mi = str(re.search("\d+",str(i)).group())
    url_list1.append(mi)

def GetLiveINI(Url): #方法传入参数为知乎Live Url
    sqlLive ="insert into liveInfo (liveId,liveName,organizerId,sTime,score,numOfReview,numOfMember,numOfAudio,numOfFile,numOfAnswer,price,introduction,WTimeStamp)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    driver.get(Url)
    time.sleep(1)
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
       Year = 2000
       Month = 1
       Day = 1
       hour = 0
       minute = 0
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
        LiveParticipantsNum = int(str(bs.find("span", {"class": "Participants-text--jB3"}).get_text())[:-5])
    except:
        LiveParticipantsNum = 0
    try:
        try:
           Price = str(re.sub("赞助并参与活动|（|）|¥","",re.search("赞助并参与活动（.*?）",str(bs.find("div",{"class":"LiveActions-buttonWrapper-3mOE"}))).group()))
        except:
           Price = str(re.sub(">|<|¥","",re.search(">¥.*?<",str(bs.find("div",{"class":"LiveActions-buttonWrapper-3mOE"}))).group()))
    except:
        Price =0
    try:
        Intro = str(bs.find("div",{"class":"LiveDescription-content-1d92 Summary-isClickable-1n5n"}).get_text()).translate(non_bmp_map)
    except:
        Intro = str(bs.find("div",{"class":"LiveDescription-content-1d92"}).get_text()).translate(non_bmp_map)
    
    LiveOwner =  str(bs.find("a", {"class": "LiveSpeakers-link-6dN8 UserLink-root-1ogW"})['href'])[13:] #Live举办人个人信息主页ID
    driver.get("https://www.zhihu.com/people/"+ LiveOwner + "/answers")
    time.sleep(1)
    LiveOwnerId = re.split("/",str(driver.current_url))[-2]
    
    WTimeStamp = time.strftime(timeformat,time.localtime(time.time()))
   
    try:
        cursor.execute(sqlLive,(LiveId,Name,LiveOwnerId,Date,Star,str(EvaluationNum),str(LiveParticipantsNum),str(SoundMinute),str(FileNum),str(AswerNum),str(Price),str(Intro),WTimeStamp))
        conn.commit()
    except:
        print("liveId:"+LiveId)
        

   
                  

def gethtml(Url):
    
        
    driver.get(Url)
    sqlLiveTheme ="insert into liveTheme (liveId,liveTheme) values(%s,%s)"
    try:
            time.sleep(1)
           
            #driver.find_element_by_class_name('LiveRelatedLives-viewMore-ebUQ').click()
            if Url != "https://www.zhihu.com/lives":
                driver.get(Url+"/related")
            else:
                pass
    except:
            time.sleep(1)
    for i in range(20):
           driver.execute_script("window.scrollBy(0,5000)")
           time.sleep(1)
       
    pageSource = driver.page_source
    bs = BeautifulSoup(pageSource, 'lxml')
    list = bs.findAll("a", {"data-za-module": "LiveItem"})
    
    for i in list:
        herf = i['href']
        liveID =str(re.split("/",str(i['href']))[-1])
        
        try:
            theme = str(re.sub("<|>|/","",re.split("span",str(i))[2]))
            cursor.execute(sqlLiveTheme,(liveID,str(theme)))
            conn.commit()
        except:
           
           pass 
        
            
        URL = "https://www.zhihu.com" + i['href']
        if (liveID not in url_list):
            try:
               url_list.append(liveID)
               GetLiveINI(URL)
               print(len(url_list))
               gethtml(URL)
            except:
               pass
        else:
            continue
        
def fromOwner(url):
    sqlLiveTheme ="insert into liveTheme (liveId,liveTheme) values(%s,%s)"
    driver.get(url)
    handle = driver.current_window_handle
    list =[]
    try:
        time.sleep(1)
           
        driver.find_element_by_partial_link_text("举办的 Live").click()
        time.sleep(1)
        handles = driver.window_handles
        driver.switch_to_window(handles[1])
        
        for i in range(4):
           driver.execute_script("window.scrollBy(0,5000)")
           time.sleep(1)
        pageSource = driver.page_source
        bs = BeautifulSoup(pageSource, 'lxml')
        list = bs.findAll("a", {"data-za-module": "LiveItem"})
        
    
        for i in list:
            herf = i['href']
            liveID =str(re.split("/",str(i['href']))[-1])
        
            try:
               theme = str(re.sub("<|>|/","",re.split("span",str(i))[2]))
               
               cursor.execute(sqlLiveTheme,(liveID,str(theme)))
               conn.commit()
            except:
               pass 
        
            
            URL = "https://www.zhihu.com" + i['href']
            if (liveID not in url_list):
                try:
                   url_list.append(liveID)
                   GetLiveINI(URL)
                   print(len(url_list))
                except:
                   pass
            else:
                continue
        driver.close()
        driver.switch_to_window(handle)
    except:
       pass

def main():
    
    for i in url_list0:
         if i == "https://www.zhihu.com/lives":
             gethtml(i)
         else:
             url = "https://www.zhihu.com/lives/"+ re.sub(",|'|\(|\)","",i)
             gethtml(url)
       
      
    

def ma():
    people_list=[]
    sql3 ="select organizerId from liveInfo group by organizerId"
    cursor.execute(sql3)
    for i in cursor:
        mild = str(re.sub("\'","",re.search("\'.*?\'",str(i)).group()))
        people_list.append(mild)
    for j in people_list:
        fromOwner("https://www.zhihu.com/people/"+j)

def fromTheme():

    for i in url_list1:
        
        if i not in url_list:
              
              urlT = "https://www.zhihu.com/lives/"+ re.sub(",|'|\(|\)","",i)
              GetLiveINI(urlT)
              gethtml(urlT)
        
              
        print(len(url_list))


       
#main()
#ma()
fromTheme()
