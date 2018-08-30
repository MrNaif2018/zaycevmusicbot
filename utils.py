# -*- coding: UTF-8 -*-
from urllib.request import Request, urlopen 
from bs4 import BeautifulSoup
from urllib.parse import quote
def main(in_):
    def get_soup(url,header):
        return BeautifulSoup(urlopen(Request(url,headers=header)),'html.parser')
    query = quote(in_)
    query= query.split()
    query='+'.join(query)
    url="http://zaycev.net/search.html?query_search="+query
    header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"}
    soup = get_soup(url,header)
    title=soup.findAll( 'div', {"class":'musicset-track__title track-geo__title'})
    if len(title) > 10:
        title=title[0:10]
    performer = soup.findAll('div',{"class":"musicset-track__artist"})
    if len(performer) > 10:
        performer=performer[0:10]
    for i in range(0,len(performer)):
        performer[i]=performer[i].find('a')['href'].replace("/artist/","")+"/"
    track=soup.findAll('div',{"class":"musicset-track__track-name"})
    if len(track) > 10:
        track=track[0:10]
    for i in range(0,len(track)):
        track[i]=track[i].find('a')['href'].replace("/pages/","").replace(".shtml","").split("/")[1]+"/"
    lst=[]
    names=[]
    try:
        for i in range(0,len(track)):
            audio="http://cdndl.zaycev.net/"+performer[i]+track[i]+title[i].text.replace('–','-').replace(" ","_")+".mp3"
            lst.append(audio)
            names.append(title[i].text)
    except IndexError:
        return
    return lst, names
