from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time

def getCodesFromWencai(w):
    soup = getSoupsFromWencai(w)
    eles = soup.select('#resultWrap .static_con_outer .tbody_table tr td.item div.em')
    index = 0
    arr = []
    while index < eles.__len__():
        o_str = eles[index].text.strip()
        if (o_str.isdigit()):
            arr.append(o_str)
        index = index + 1
    return arr

def getZhangTingReasonWords(code, date):
    soup = getSoupsFromWencai(code + "；" + date + "；" + "涨停原因")
    eles = soup.select('#doctorPick .dp_pointonline_block_con .dp_pointonline_con .reason_con .reason_list .reason_item a')
    elem = None
    for e in eles:
        title = e.get("title")
        if date in title:
            elem = e
            break
    kw = elem.text.strip()
    kw = kw[1: elem.text.strip().__len__()]
    return kw

def getSoupsFromWencai(w):
    url = 'https://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=3&qs=pc_~soniu~stock~stock~history~query&selfsectsn=&querytype=stock&searchfilter=&tid=stockpick&w=' + w
    browser = None
    ret = []
    try:
        browser = webdriver.Chrome(
            os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\driver\chromedriver.exe')
        browser.get(url)
        browser.implicitly_wait(1)
        time.sleep(2)
        try:
            isClicked = False
            elem70 = browser.find_element_by_css_selector('#table_foot_bar select option[value="70"]')
            if elem70 is not None and isClicked == False:
                elem70.click()
                time.sleep(4)
        except Exception as e:
            print("")

        html = browser.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html, "html.parser")
        ret.append(soup)
        try:
            next = browser.find_element_by_css_selector("#pageBar #next")
        except:
            next = None
        if next is not None and next.tag_name is not None:
            try:
                next.click()
            except:
                return ret
            browser.implicitly_wait(1)
            time.sleep(4)
            html = browser.execute_script("return document.documentElement.outerHTML")
            soup = BeautifulSoup(html, "html.parser")
            ret.append(soup)
        else:
            return ret
    except Exception as e:
        return None
    finally:
        browser.close()
    return ret

def getElemsFromWencai(w, selector):
    soup = getSoupsFromWencai(w)
    eles = soup.select(selector)
    return eles

def getArrayFromWencai(w, selector):
    elems = getElemsFromWencai(w, selector)
    arr = []
    for elem in elems:
        str = elem.text.strip()
        arr.append(str)
    return arr

def isElemExist(browser, css):
    try:
        browser.find_element_by_css_selector(css)
    except Exception as e:
        return False

# codes = getCodesFromWencai("按昨日涨跌幅降序排序前10")
# print(codes)

