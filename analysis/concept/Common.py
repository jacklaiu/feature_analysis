# -*- coding: gbk -*-
import base.HtmlGetter as hg
import base.FinanceDataSource as fd
import base.Dao as dao

def getZhangTingCodeConceptAnd2DB(date=fd.getLastestOpenDate()):
    soups = hg.getSoupsFromWencai(date + "���ǵ���>=9.89��" + date +"��ͣԭ�򣻰�"+date+"���״���ͣʱ������")
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
    nowDate = fd.getLastestOpenDate()
    #��1����ȡ����concept�ļ���(����1)
    startDate = fd.preOpenDate(nowDate, dayCount)
    rows = dao.select("select concept from zhangting_concept where date>=%s group by concept", (startDate))
    concepts = []
    for row in rows:
        concept = row['concept']
        concepts.append(concept)

    #��2������concept����ȡcount�����ض���date
    # date = nowDate
    # while date > startDate:
    #     rows = dao.select("select concept, count(0) count from zhangting_concept where date=%s group by concept", (date))
    #     for row in rows:
    #         concept = row['concept']
    #         count = row['count']
    date = startDate
    ret = {}
    concept_count_rel = {}


    for concept in concepts:
        countsArr = []
        _date = date
        while _date <= nowDate:
            row = dao.select("select count(0) count from zhangting_concept where date=%s and concept=%s", (_date, concept))
            count = str(row[0]['count'])
            countsArr.append(count)
            _date = fd.nextOpenDate(_date, 1)
        concept_count_rel.setdefault(concept, countsArr)
    ret.setdefault('concept_count_rel', concept_count_rel)
    ret.setdefault('concepts', concepts)
    #��3������ͼ����ܵ�����model

    # endDate = fd.getLastestOpenDate()
    # startDate = fd.preOpenDate(endDate, dayCount)
    # nowDate = startDate
    # ret = {}
    # while nowDate <= endDate:
    #     try:
    #         arr = dao.select("select count(0) count, concept from zhangting_concept where date = %s GROUP BY concept", (nowDate))
    #     except Exception as e:
    #         return "get_zhangtingconcept_countMap mysql error"
    #     map = {}
    #     for it in arr:
    #         count = it['count']
    #         concept = it['concept']
    #         map.setdefault(concept, count)
    #     ret[nowDate] = map
    #     nowDate = fd.nextOpenDate(nowDate, 1)
    dates = []
    _date = date
    while _date <= nowDate:
        dates.append(_date)
        _date = fd.nextOpenDate(_date, 1)
    ret.setdefault('dates', dates)
    return ret






# concepts = ['���ڹ���ĸ�', '�ͼ۳���', '����ĸ�', 'ʵ��������', '�ͼ۳���', '��Ȩת��', '����ĸ�', '��Ȩת��', '����ĸ�', 'ǩ��������Э��', 'ϡ�н���', '����ĸ�', None, '����ĸ�', 'ʵ���˱��', '����ĸ�', '�ͼ۳���', '�ͼ۳���', '��������', '�ͼ۳���', '���ؽ���', '����תԤ��+���¹�', '�¹�', '������Ʒ', '�ͼ۳���', 'ʳƷҽҩ��ȫ', '����תԤ��', '����תԤ��+���¹�', '�ͼ۳���', '�����', '�ͼ۳���', '���ؽ���', '�Ϻ�����ĸ�', '�Ϻ�����ĸ�', '�Ϻ�����ĸ�', '����ĸ�', '�ͼ۳���', '������ĸ�', '����ĸ�', '�¹�', '�¹�']
# map = {}
# for c in concepts:
#     if c in map.keys():
#         map[c] = map[c] + 1
#     else:
#         map.setdefault(c, 1)
# date = "2018-07-24"

