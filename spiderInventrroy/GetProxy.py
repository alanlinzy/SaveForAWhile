#encoding=utf8
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import socket

User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
header = {}
header['User-Agent'] = User_Agent

url = 'http://www.xicidaili.com/nn/1'
req = requests.get(url,headers=header)

soup = BeautifulSoup(req.text,"html.parser")
ips = soup.findAll('tr')
f = open("../Proxy","w")

for x in range(1,len(ips)):
    ip = ips[x]
    tds = ip.findAll("td")
    ip_temp = tds[1].contents[0]+"\t"+tds[2].contents[0]+"\n"
    #print (tds[1].contents[0]+"\t"+tds[2].contents[0])
    
    f.write(ip_temp)
    



socket.setdefaulttimeout(3)
f = open("../Proxy")
lines = f.readlines()
proxys = []
for i in range(0,len(lines)):
    ip = lines[i].strip("\n").split("\t")
    proxy_host = "http://"+ip[0]+":"+ip[1]
    proxy_temp = {"http":proxy_host}
    proxys.append(proxy_temp)
#url = "http://ip.chinaz.com/getip.aspx"
url = "http://www.zhihu.com"
for proxy in proxys:
    try:
        res = requests.get(url,proxies=proxy).text
        print (res)
        
    except Exception:
        print (proxy)
        continue


