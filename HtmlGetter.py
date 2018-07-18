from time import clock
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import execjs
import time

def getCodesFromWencai(w):
    url = 'https://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=3&qs=pc_~soniu~stock~stock~history~query&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=' + w
    browser = None
    try:
        browser = webdriver.Chrome(os.path.abspath('.') + '\driver\chromedriver.exe')
        browser.get(url)
        time.sleep(4)
        browser.implicitly_wait(1)
        try:
            isClicked = False
            elem70 = browser.find_element_by_css_selector('#resultWrap #showPerpage select option[value="70"]')
            if elem70 is not None and isClicked == False:
                elem70.click()
                isClicked = True
            elem50 = browser.find_element_by_css_selector('#resultWrap #showPerpage select option[value="50"]')
            if elem50 is not None and isClicked == False:
                elem50.click()
                isClicked = True
            elem30 = browser.find_element_by_css_selector('#resultWrap #showPerpage select option[value="30"]')
            if elem30 is not None and isClicked == False:
                elem30.click()
            time.sleep(5)
        except:
            print("")
        html = browser.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        eles = soup.select('#resultWrap .static_con_outer .tbody_table tr td.item div.em')
        index = 0
        arr = []
        while index < eles.__len__():
            o_str = eles[index].text.strip()
            if (o_str.isdigit()):
                arr.append(o_str)
            index = index + 1
        return arr
    except Exception as e:
        browser.quit()
        return None
    finally:
        browser.quit()

codes = getCodesFromWencai("按昨日涨跌幅降序排序前10")
print(codes)