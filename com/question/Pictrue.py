#coding=UTF-8

from selenium import webdriver
import time

import urllib.request
import re 
import os


from bs4 import BeautifulSoup

import html.parser
from asyncio.tasks import sleep

def main():
    #打开浏览器
    driver = webdriver.Chrome("E:/**/chromedriver.exe")
    #打开想要爬取的知乎页面
#     driver.get("https://www.zhihu.com/question/33602847") 
#     https://www.zhihu.com/question/34243513/answer/243042102
    driver.get("https://www.zhihu.com/question/19646643")
    
    #模拟用户操作
    
    def execute_times(times):
        
        for i in range(times):
            driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(1)
            try:
                driver.find_element_by_css_selector('button.QuestionMainAction').click()                
                print("page"+str(i))
                time.sleep(1)
            except:
                break
    execute_times(1000)
    
    print("60s倒计时")
    
    #这是原网页Html信息
    result_raw = driver.page_source
    
    #然后将其解析
    result_soup = BeautifulSoup(result_raw,'html.parser')
    
    #结构化Html文件
    result_bf = result_soup.prettify()
    
    #存储文件
    with open("E:/test/raw_result.txt",'w',encoding="utf-8") as girls:
        girls.write(result_bf)
    girls.close()
    print("爬取回答页面成功！")
#     title = result_soup.find_all('title')
    # 读取title内容
    title1 = result_soup.find_all('title')
    # 读取title内容
    title = str(title1[0])
    a = title[7:]
    b= str(a[:-14])
    print(b)
      
    with open("E:/test/noscript_meta.txt",'wb') as noscript_meta:
        #找到所有<noscript>node
        noscript_nodes = result_soup.find_all('noscript')
        noscript_inner_all=""
        for noscript in noscript_nodes:
            #获取<noscript>node内部内容
            noscript_inner = noscript.get_text()
                
            noscript_inner_all += noscript_inner+"\n"
                
        #将内部内容转码并存储
        #noscript_all = html.parser.unescape(noscript_inner_all).encode('utf-8')
        noscript_all = html.parser.unescape(noscript_inner_all).encode('utf-8')
            
        noscript_meta.write(noscript_all)
            
    noscript_meta.close()
    print("爬取noscript标签成功！！")
        
        
    img_soup = BeautifulSoup(noscript_all,'html.parser')
    img_nodes = img_soup.find_all('img')
        
    with open("E:/test/ZhihuImages/img_meta.txt",'w') as img_meta:
        count = 0
        for img in img_nodes:
            img_url = img.get('src')
                 
            line = str(count)+'\t'+img_url+'\n'
                 
            img_meta.write(line)
                 
            #下载图片
            path = "E:/test/ZhihuImages/"+b
            mkdir(path);
            urllib.request.urlretrieve(img_url, path+"/"+str(count)+'.jpg')
            count +=1
            print("第"+str(count)+"图片下载成功！")
    img_meta.close()
    print("共"+str(count)+"张图片")
        
    print("图片下载成功！")
    driver.quit()
def mkdir(path):
   
    folder = os.path.exists(path)
   
    if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
           
          
     
if __name__ == '__main__':
    main()