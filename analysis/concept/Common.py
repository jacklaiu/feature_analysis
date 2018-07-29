# -*- coding: gbk -*-
import base.HtmlGetter as hg
import base.FinanceDataSource as fd
import base.Dao as dao

def getZhangTingCodeConceptAnd2DB(date):
    soups = hg.getSoupsFromWencai(date + "����ͣ����ͣԭ�򣻰�"+date+"���״���ͣʱ������")
    for soup in soups:
        eles_codes = soup.select('#resultWrap .static_con_outer .tbody_table tr td.item div.em')
        index = 0
        codes = []
        while index < eles_codes.__len__():
            o_str = eles_codes[index].text.strip()
            if (o_str.isdigit()):
                codes.append(o_str)
            index = index + 1
        eles_reason = soup.select('#resultWrap .scroll_tbody_con .tbody_table tr td[colnum="5"] div.em')
        reasons = []
        for elem in eles_reason:
            o_str = elem.text.strip()
            reasons.append(o_str)
        count = 0
        for code in codes:
            r = reasons[count]
            dao.update("delete from zhangting_concept where date=%s and code=%s", (date, code))
            dao.update("insert into zhangting_concept(code, date, concept) values(%s,%s,%s)", (code, date, r))
            count = count + 1

def get_zhangtingconcept_countMap(dayCount):
    endDate = fd.getLastestOpenDate()
    startDate = fd.preOpenDate(endDate, dayCount)
    nowDate = startDate
    ret = {}
    while nowDate <= endDate:
        arr = dao.select("select code, date, concept from zhangting_concept where date = %s", (nowDate))
        if arr.__len__() == 0:
            nowDate = fd.nextOpenDate(nowDate, 1)
            continue
        map = {}
        for it in arr:
            date = it['date']
            concept = it['concept']
            print("Date: " + date + " Concept: " + concept)
            if concept in map.keys():
                map[concept] = map[concept] + 1
            else:
                map.setdefault(concept, 1)
        ret[nowDate] = map
        nowDate = fd.nextOpenDate(nowDate, 1)
    return ret
# concepts = ['���ڹ���ĸ�', '�ͼ۳���', '����ĸ�', 'ʵ��������', '�ͼ۳���', '��Ȩת��', '����ĸ�', '��Ȩת��', '����ĸ�', 'ǩ��������Э��', 'ϡ�н���', '����ĸ�', None, '����ĸ�', 'ʵ���˱��', '����ĸ�', '�ͼ۳���', '�ͼ۳���', '��������', '�ͼ۳���', '���ؽ���', '����תԤ��+���¹�', '�¹�', '������Ʒ', '�ͼ۳���', 'ʳƷҽҩ��ȫ', '����תԤ��', '����תԤ��+���¹�', '�ͼ۳���', '�����', '�ͼ۳���', '���ؽ���', '�Ϻ�����ĸ�', '�Ϻ�����ĸ�', '�Ϻ�����ĸ�', '����ĸ�', '�ͼ۳���', '������ĸ�', '����ĸ�', '�¹�', '�¹�']
# map = {}
# for c in concepts:
#     if c in map.keys():
#         map[c] = map[c] + 1
#     else:
#         map.setdefault(c, 1)
# date = "2018-07-24"

#map = get_zhangtingconcept_countMap(10)
