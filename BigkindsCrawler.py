
# coding: utf-8

# In[ ]:

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import random
import sys
import re
import datetime
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
import pymongo
from pymongo import MongoClient


# In[ ]:

result_list = []
client = MongoClient()
db = client["bigkinds_db"]
collection = db["bigkinds_collection"]

class Scrapper():
    counter = 0
    
    def setup(self):
        options = webdriver.ChromeOptions()
        options.add_argument("window-size=1920x1080")
        options.add_argument('headless')
        options.add_argument("disable-gpu")
        self.driver = webdriver.Chrome('C:/chromedriver/chromedriver.exe',chrome_options=options)

        self.driver.set_page_load_timeout(30)
        
    def test(self, keyword, year, start=1, end=None):
        result = []
        
        self.counter = int(start) - 1
        p = 0
        isContinue = False
        if (start != 0):
            p = int(start) / 100
            p = int(p)+1
            isContinue = True
        
        self.setup()
        self.driver.get("https://www.bigkinds.or.kr/v2/news/index.do")
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.find_element_by_css_selector("span.caret").click()
        self.driver.find_element_by_css_selector("button.btn.btn-sm.w-100.main-search-filters__dropdown__btn.date-select-btn").click()
        self.driver.find_element_by_css_selector("button#date-confirm-btn").click()
        sleep(random.randint(5, 20))
        self.driver.find_element_by_css_selector("input#total-search-key").send_keys(keyword)
        sleep(random.randint(5, 20))
        self.driver.find_element_by_css_selector("span.input-group-btn").click()
        sleep(random.randint(20, 30))
        self.driver.find_element_by_css_selector("input#filter-date-"+str(year)).click()
        sleep(random.randint(20, 30))
        for op in self.driver.find_elements_by_css_selector("option"):
            if op.get_attribute("value") == "100":
                op.click()
                sleep(random.randint(20, 30))
                break
        total = int(self.driver.find_element_by_css_selector("span#total-news-cnt").text.replace(",",""))
        page = int(total/100) +1
        if (isContinue): count = (p-1) * 100
        else: count = 0
        #count = 0
        #fdup_cnt = 0
        
        for i in range(1,page+1):#page 수 만큼
            
            print('i is', i)
            
            if (isContinue):
                if ((i//7) < (p//7)): continue
                elif (i < p) and (i%7 == 0):
                    self.driver.find_element_by_css_selector('#news-results-pagination > ul > li:nth-child(10) > a').click()
                    sleep(random.randint(20, 30))
                    continue
                elif (i < p): continue
            for pnum in self.driver.find_elements_by_css_selector("a.page-link"):
                print('pnum:', pnum.text)
                if (str(i) == pnum.text) or (pnum.text == '다음'):
                    print('str(i):', str(i))
                    pnum.click()
                    sleep(random.randint(20, 30))
                    break
                    
                    
            #articles =  self.driver.find_elements_by_css_selector("h4.news-item__title.news-detail")
            #for i in articles :
            #    print(i)  
            
            
            
            
            
            for article in self.driver.find_elements_by_css_selector("#news-results > div > div > h4"):
                count+=1
                if(isContinue):
                    if(count < int(start)):
                        continue
                id = article.get_attribute("data-newsid")
                title = article.text
                print(id,title)

                article.click()
                sleep(random.randint(5, 20))
                temp = ""
                for hitem in self.driver.find_elements_by_css_selector("span.news-detail__header-item"):
                    temp += hitem.text + "\t"
                headline = temp
                try:
                    written_at = re.findall('\d\d\d\d-\d\d-\d\d', headline)[0]
                except Exception as e:
                    written_at = None
                category = self.driver.find_element_by_css_selector("#news-detail-modal > div > div > div.modal-header > div.pull-left > span:nth-child(2)").text
                #print(category)
                content = self.driver.find_element_by_css_selector("div.news-detail__content").text

                ##scrapped_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.counter += 1
                if (end == None): pass
                elif (self.counter > end):
                    print('Counter reaches the endpoint. Goodbye!')
                    self.tearDown()
                    return 0
                result.append([id,category,title,written_at,content])
                values = {"id":id,
                          "category":category,
                          "title":title,
                          "written_at":written_at,
                          "content":content}
                while(True):
                    try:
                        values_id = collection.insert_one(values)
                        break
                    except Exception as e:
                        print(e)
                        self.counter-=1
                        sleep(3)
                print(str(int(self.counter)-int(start)+1),"article crawled ",values_id)
                #result_list.append([id,category,title,written_at,content])
                #print(result)
                for a in self.driver.find_elements_by_css_selector("button.btn.btn-default"):
                    if (a.text == "닫기"):
                        
                        a.click()
                        sleep(random.randint(5, 20))
            sleep(random.randint(60, 90))
                
            #except :
                #pass
            
        self.tearDown()
        
        #data = pd.DataFrame(result)
        #data.columns = ['id','category','title','written_at','content']
        #data.to_csv('result.csv',encoding='cp949')
    
    def tearDown(self):
        self.driver.close()
                
if __name__ == '__main__':
    s = Scrapper()
    keyword = "취업"
    s.test(keyword, 2020, 0)
            

    

