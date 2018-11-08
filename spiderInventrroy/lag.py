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
import random

timeformat = "%Y-%m-%d %H:%M:%S"
ReParticipantsUrl = re.compile('"url_token": "(.*?)", "id"')
Url = "https://www.zhihu.com/lives/978334089803231232"

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

initUrl = "http://www.zhihu.com"
#driver.get(initUrl)
#wait=WebDriverWait(driver,100)
#wait.until(EC.presence_of_element_located((By.CLASS_NAME, "GlobalSideBar-categoryList")))
#driver.get(initUrl)

conn =pymysql.connect(host='localhost',user='root',password='qq1997lzy0509',port=3306,db='zhihu',use_unicode=True,charset="utf8")
cursor=conn.cursor()

    
def GetFansIdList(LiveOwnerId): #传入live举办者的url 返回关注live主的人的url列表
    sqlFollow ="insert into Follow (peopleId,followingId) values(%s,%s)"
    Url ="https://www.zhihu.com/people/"+ LiveOwnerId+"/followers"
    driver.get(Url)
    #path = "E://Fans.txt"
    
    time.sleep(1)
    
    peopleId =str(driver.current_url)[29:-10]
    
    Bs = BeautifulSoup(driver.page_source, 'lxml')
    FansNum = Bs.findAll("strong", {"NumberBoard-itemValue"})[1].attrs["title"]
    

    a = int(int(FansNum) / 20)

    FansIdList = []

    for i in range(a + 1):
        FansPageUrl = "https://www.zhihu.com/people/"+ peopleId+"/followers" + "?page=" + str(i + 1)
        driver.get(FansPageUrl)
        time.sleep(1)

        FansPageBs = BeautifulSoup(driver.page_source, 'lxml')

        People = FansPageBs.findAll("a", {"class": "UserLink-link"})
        for y in People:
            FansId = str(re.split("/", str(y.attrs['href']))[-1])
            
            if FansId not in FansIdList:
                FansIdList.append(FansId)
                try:
                   GetPeople(FansId)
                except:
                   pass
                try:
                   cursor.execute(sqlFollow,(LiveOwnerId,FansId))
                   conn.commit()
                except:
                   print("fanId:"+FansId)
                    
    
        
    
    #return FansIdList

def GetFollowingIdList(LiveOwnerId):  # 传入live举办者的url 返回live主关注的人的url列表
    sqlFollow ="insert into Follow (peopleId,followingId) values(%s,%s)"
    Url = "https://www.zhihu.com/people/" + LiveOwnerId + "/following"
    driver.get(Url)

    time.sleep(1)

    peopleId = str(driver.current_url)[29:-10]

    Bs = BeautifulSoup(driver.page_source, 'lxml')
    FansNum = Bs.findAll("strong", {"NumberBoard-itemValue"})[0].attrs["title"]

    a = int(int(FansNum) / 20)

    FollowingIdList = []

    for i in range(a + 1):
        FansPageUrl = "https://www.zhihu.com/people/" + peopleId + "/following" + "?page=" + str(i + 1)
        driver.get(FansPageUrl)
        time.sleep(1)

        FansPageBs = BeautifulSoup(driver.page_source, 'lxml')

        People = FansPageBs.findAll("a", {"class": "UserLink-link"})
        for y in People:
            FansId = str(re.split("/", str(y.attrs['href']))[-1])

            if FansId not in FollowingIdList:
                FollowingIdList.append(FansId)
                try:
                   GetPeople(FansId)
                except:
                   pass
                try:
                   cursor.execute(sqlFollow, (FansId, LiveOwnerId))
                   conn.commit()
                except:
                   print("FollowingId:" + FansId)

    #return FollowingIdList


def GetLiveParticipantsIdList(LiveId, ParticipantsNum): #传入liveId live 参加人数 返回参加live所有人的URL
    sqlJoinLive ="insert into JoinLive (liveId,peopleId) values(%s,%s)"
    a = int(int(ParticipantsNum) / 3000)
    path ="E://participants.txt"
    ParticipantsIdList = []

    for i in range(a):
        ParticipantsUrl = "https://api.zhihu.com/lives/" + str(LiveId) + "/members?limit=" + str((i + 1) * 3000) + "&offset=" + str(i * 3000)
        html = urlopen(ParticipantsUrl)

        ParticipantsBs = BeautifulSoup(html.read(), 'lxml')

        IdList = re.split("}, {", ParticipantsBs.find("p").get_text())

        for i in IdList:
            if len(ReParticipantsUrl.findall(i)) > 0:
                Url =  ReParticipantsUrl.findall(i)[0]
                ParticipantsIdList.append(Url)

    ParticipantsUrl = "https://api.zhihu.com/lives/" + str(LiveId) + "/members?limit=" + str(ParticipantsNum) + "&offset=" + str(a * 3000)
    html = urlopen(ParticipantsUrl)

    ParticipantsBs = BeautifulSoup(html.read(), 'lxml')

    IdList = re.split("}, {", ParticipantsBs.find("p").get_text())

    for i in IdList:
        if len(ReParticipantsUrl.findall(i)) > 0:
            Url = ReParticipantsUrl.findall(i)[0]
            ParticipantsIdList.append(Url)
            
            try:
                GetPeople(Url)
            except:
                pass
            
            try:
               cursor.execute(sqlJoinLive,(LiveId,Url))
               conn.commit()
            except:
                print("participantId:"+Url)
    
    #return ParticipantsIdList

def GetLiveINI(Url): #方法传入参数为知乎Live Url
    sqlLive ="insert into live (liveId,liveName,organizerId,sTime,score,numOfReview,numOfMember,numOfAudio,numOfFile,numOfAnswer,price,introduction,WTimeStamp)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    #sqlJoinLive ="insert into JoinLive (liveId,peopleId) values(%s,%s)"
    #sqlFollow ="insert into Follow (peopleId,followingId) values(%s,%s)"
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    driver.get(Url)
    time.sleep(1)
    PageSource = driver.page_source

    bs = BeautifulSoup(PageSource, 'lxml')

    LiveId = Url[-18:]
    try:

        Name = bs.find("div", {"class": "LivePageHeader-line-SzR2 LivePageHeader-title-1RQL"}).string#Live名字
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


    #SoundMinute = int(INFList[0].findAll("div")[0].get_text()) #Live分钟语音数

    
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
    #driver.get("https://www.zhihu.com/people/"+ LiveOwner + "/answers")
    #time.sleep(random.randint(2,10))
    #LiveOwnerId = re.split("/",str(driver.current_url))[-2]
    LiveOwnerId= GetPeople(LiveOwner)
    WTimeStamp = time.strftime(timeformat,time.localtime(time.time()))
    try:
        cursor.execute(sqlLive,(LiveId,Name,LiveOwnerId,Date,Star,str(EvaluationNum),str(LiveParticipantsNum),str(SoundMinute),str(FileNum),str(AswerNum),str(Price),str(Intro),WTimeStamp))
        conn.commit()
    except:
        print("liveId:"+LiveId)
        
    
     

    
    #ParticipantsIdList = GetLiveParticipantsIdList(LiveId, LiveParticipantsNum) #Live听众的Id
    GetLiveParticipantsIdList(LiveId, LiveParticipantsNum)

   
            
                

    #FansIdList = GetFansIdList(LiveOwnerId)#关注Live主的用户的Id
    GetFansIdList(LiveOwnerId)
    
            
           
                
    #FollowingIdList = GetFollowingIdList(LiveOwnerId)
    GetFollowingIdList(LiveOwnerId)
    
           
                
    GetReview(LiveId,EvaluationNum)
    
def GetQuestion(peopleId,Num):
    sql ="insert into Question (questionId,questionName,qTime,qPeople,numOfFollow,numOfAnswer,WTimeStamp)values(%s,%s,%s,%s,%s,%s,%s)"
    peopleUrl="https://www.zhihu.com/people/" + peopleId + "/asks"
    a = int(int(Num)/20)
    for i in range(a+1):
        questionUrl = peopleUrl + "?page="+str(i+1)
        driver.get(questionUrl)
        time.sleep(1)

        askbs = BeautifulSoup(driver.page_source, 'lxml')
        askList = askbs.findAll("div",{"class":"List-item"})
        for j in askList:
            mid= j.find("a",{"data-za-detail-view-name":"Title"}).attrs["href"]
            name=j.find("a",{"data-za-detail-view-name":"Title"}).string
            href = re.search("\d+$",str(mid)).group()
            detail = j.findAll("span",{"class":"ContentItem-statusItem"})
            askdate = detail[0].string
            Year = int(str(askdate)[:4])
            Month = int(str(askdate)[5:7])
            Day = int(str(askdate)[8:10])

            Date = datetime.datetime(Year, Month, Day)
            numOfAnswer =int(re.search("\d*", detail[1].string).group())
            numOfFocus =int(re.search("\d*",detail[2].string).group())
            WTimeStamp = time.strftime(timeformat,time.localtime(time.time()))
            try:
                cursor.execute(sql,(href,name,Date,peopleId,str(numOfFocus),str(numOfAnswer),WTimeStamp))
                conn.commit()
            except:
                pass
            
        
    
def GetAnswer(peopleId,Num):
    sql = "insert into Answer (answerId,question,numOfAgree,numOfReview,aTime,aPeople,WTimeStamp) values (%s,%s,%s,%s,%s,%s,%s)"
    peopleUrl ="https://www.zhihu.com/people/"+ peopleId + "/answers"
    a = int(int(Num)/20)
    for i in range(a+1):
        answerPageUrl = peopleUrl + "?page="+str(i+1)
        driver.get(answerPageUrl)
        time.sleep(1)

        answerPagebs = BeautifulSoup(driver.page_source, 'lxml')
        answerList = answerPagebs.findAll("div",{"class":"List-item"})
      
        for j in answerList:
            mid=str(j.find("a",{"data-za-detail-view-element_name":"Title"}).attrs["href"])
            aquestion=re.sub("/","",str(re.search("/\d+/",mid).group()))
            answerId =re.sub("/answer/","",str(re.search("/answer/\d+",mid).group()))
            answerUrl = "https://www.zhihu.com" + mid
            try:
                up = j.find("button",{"aria-label":"赞同"}).get_text()
            except:
                up = 0
            try:
                
                html0 = s.get(answerUrl,headers=headers)
                answerbs = BeautifulSoup(html0.text, 'lxml').find("div",{"class":"QuestionAnswer-content"})
            except:
                driver.get(answerUrl)
                answerbs = BeautifulSoup(driver.page_source, 'lxml').find("div",{"class":"QuestionAnswer-content"})
            
            try:
                if up == "0":
                   numOfAgree = 0
                else:
                   numOfAgree = int(re.search("\d*",str(answerbs.find("button",{"class","Button Button--plain"}).get_text())).group())
            except:
                numOfAgree = 0


            try:
                try:
                    mid = re.search("发布于 昨天" ,str(answerbs.find("div",{"class":"ContentItem-time"}))).group()
                except:
                    mid =re.search("发布于 \d+-\d+-\d+" ,str(answerbs.find("div",{"class":"ContentItem-time"}))).group()
            except:
                print(answerbs)
                continue
           

            contentTime = re.sub("(发布于| )","",str(mid))
            

            if str(contentTime)[:4] == '昨天':
                Year = 2018
                Month = 4
                Day = 17
            else:
                Year = int(str(contentTime)[:4])
                Month = int(str(contentTime)[5:7])
                Day = int(str(contentTime)[8:10])
        
            Date = datetime.datetime(Year, Month, Day)
            try:
                
                mid =str(answerbs.findAll("div",{"class":"ContentItem-actions"})[0])
                numOfReview=int(re.sub("( |条评论)","",str(re.search("\d 条评论",mid).group())))
            except:
                numOfReview =0

            WTimeStamp = time.strftime(timeformat,time.localtime(time.time()))   
            try:
                cursor.execute(sql,(answerId,aquestion,str(numOfAgree),str(numOfReview),Date,peopleId,WTimeStamp))
                conn.commit()
            except:
                pass

            
def GetPeople(peopleId):
    peopleUrl ="https://www.zhihu.com/people/"+ peopleId
    sql="insert into people(peopleId,peopleName,numOfQuestion,numOfAnswer,numOfFollowing,numOfFollowed,numOfAgree,numOfThanks,numOfcollected,numOfShareEditing,numOfArticle,numOfColumn,numOfThought,numOfFollowTheme,numOfFollowColumn,numOfFollowQuestion,numOfFollowFavorite,numOfLive,numOfJoinLive,WTimeStamp)values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    driver.get(peopleUrl)
    time.sleep(random.randint(2,30))
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
    try:
        Have_live=re.search("举办的 Live",str(bs)).group()
        numOfLive = int(re.sub(",","",lightList[0].get_text()))
        print(numOfLive)
        numOfJoinLive = GetLiveNum(oldPeopleId) - numOfLive
        numOfFollowTheme = int(re.sub(",","",lightList[1].get_text()))
        numOfFollowColumn = int(re.sub(",","",lightList[2].get_text()))
        numOfFollowQuestion = int(re.sub(",","",lightList[3].get_text()))
    
        try:
            numOfFollowFavorite = int(re.sub(",","",lightList[4].get_text()))
        except:
            numOfFollowFavorite =0
    except:
        numOfLive = 0
        try:
            Have_live=re.search("赞助的 Live",str(bs)).group()
            numOfJoinLive = int(re.sub(",","",lightList[0].get_text()))
            numOfFollowTheme = int(re.sub(",","",lightList[1].get_text()))
            numOfFollowColumn = int(re.sub(",","",lightList[2].get_text()))
            numOfFollowQuestion = int(re.sub(",","",lightList[3].get_text()))
    
            try:
                numOfFollowFavorite = int(re.sub(",","",lightList[4].get_text()))
            except:
                numOfFollowFavorite =0
        except:
            numOfJoinLive=0
            numOfFollowTheme = int(re.sub(",","",lightList[0].get_text()))
            numOfFollowColumn = int(re.sub(",","",lightList[1].get_text()))
            numOfFollowQuestion = int(re.sub(",","",lightList[2].get_text()))
    
            try:
                numOfFollowFavorite = int(re.sub(",","",lightList[3].get_text()))
            except:
                numOfFollowFavorite =0

    card = bs.find("div",{"class":"Profile-sideColumn"})
    
    try:
        mid= re.search(">[\d,]+<",str(re.search("获得.*?次赞同",str(card)).group())).group()
        
        numOfAgree=int(re.sub("(<|>|,)","",mid))
    except:
        numOfAgree = 0
    
        
    try:
        mid=re.search("获得 \d.*?\d 次感谢",str(card)).group()
        
        numOfThanks =int(re.sub("(获得|,|次感谢)","",mid))     
    except:
        numOfThanks = 0
       
    try:
        mid =re.split(">",re.search(">.*?次收藏",str(card)).group())[-1]
        
        numOfCollected =int(re.sub("(>|,|次收藏)","",mid))
    except:
        numOfCollected = 0
       
    try:
        mid = re.search(">[\d,]+<",str(re.search("参与.*?次公共编辑",str(card)).group())).group()
        
        numOfShareEditing =int(re.sub("(,|>|<)","",mid))
    except:
        numOfShareEditing = 0
   
    WTimeStamp = time.strftime(timeformat,time.localtime(time.time()))  
    try:
        cursor.execute(sql,(peopleId,peopleName,str(numOfAsk),str(numOfAnswer),str(numOfFollowing),str(numOfFollowed),str(numOfAgree),str(numOfThanks),str(numOfCollected),str(numOfShareEditing),str(numOfArticle),str(numOfColumn),str(numOfThought),str(numOfFollowTheme),str(numOfFollowColumn),str(numOfFollowQuestion),str(numOfFollowFavorite),str(numOfLive),str(numOfJoinLive),WTimeStamp))
        conn.commit()
    except:
        print(peopleId)
        
        
    #GetQuestion(peopleId,numOfAsk)
    #GetAnswer(peopleId,numOfAnswer)

    return peopleId

def GetLiveNum(PeopleId):
    LiveNumURL = "https://www.zhihu.com/lives/users/" + PeopleId
    driver.get(LiveNumURL)
    for i in range(10):
        driver.execute_script("window.scrollBy(0,5000)")
        time.sleep(0.05)

    page = driver.page_source
    bs = BeautifulSoup(page, "lxml")

    LiveList = bs.findAll("a",{"data-za-module": "LiveItem"})
    TotalLiveNum = len(LiveList)
    return TotalLiveNum

def GetReview(liveId,Num):
    sql ="insert into LiveReview(liveId,peopleId,liveReview,reply,reviewStar,reviewDate,WTimeStamp) values (%s,%s,%s,%s,%s,%s,%s)"
    
    Url ="https://www.zhihu.com/lives" + liveId + "/reviews"
    driver.get(Url)
    time.sleep(random.randint(2,10))
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
           time.sleep(1)
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
       except:
           pass
       WTimeStamp = time.strftime(timeformat,time.localtime(time.time()))
       try:
           cursor.execute(sql,(liveId,UserId,UserComment,Reply,UserCommentStar,Date,WTimeStamp))
           conn.commit()
       except:
           pass
          








GetLiveINI(Url)
conn.close()
driver.close()


