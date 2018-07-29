# -*- coding: gbk -*-

import tushare as ts
import base.HtmlGetter as hg
import base.FinanceDataSource as fd
import base.Dao as dao

def getZhangTingCodeConceptAnd2DB(date):
    # codes = fd.get_all_securities()
    # code_item = {}
    # code_ye_item = {}
    # items = dao.select("select code, close from security_data where date=%s", (date))
    # ye_items = dao.select("select code, close from security_data where date=%s", (fd.preOpenDate(date, 1)))
    # for item in items: code_item[item['code']] = item
    # for ye_item in ye_items: code_ye_item[ye_item['code']] = ye_item
    # ret = []
    # arr2db = []
    # for code in codes:
    #     if code not in code_item.keys() or code not in code_ye_item.keys():
    #         continue
    #     item = code_item[code]
    #     ye_item = code_ye_item[code]
    #     close = float(item['close'])
    #     pre_close = float(ye_item['close'])
    #     rate = round(((close - pre_close)/pre_close)*100,2)
    #     if rate < 9.89:
    #         continue
    #     reason = hg.getZhangTingReasonWords(code, date)
    #     ret.append(code)
    #     arr2db.append((code, date, reason))

    soup = hg.getSoupFromWencai(date + "����ͣ����ͣԭ�򣻰�"+date+"���״���ͣʱ������")
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


    dao.update("delete from zhangting_concept where date=%s", (date))
    dao.updatemany("insert into zhangting_concept(code, date, concept) values(%s,%s,%s)", arr2db)
    return ret


# date = "2018-07-27"
# codes = getZhangTingCodeConcept(date)
# reasons = []
# for code in codes:
#     reason = hg.getZhangTingReasonWords(code, date)
#     reasons.append(reason)
#     print(reason)






# concepts = ['���ڹ���ĸ�', '�ͼ۳���', '����ĸ�', 'ʵ��������', '�ͼ۳���', '��Ȩת��', '����ĸ�', '��Ȩת��', '����ĸ�', 'ǩ��������Э��', 'ϡ�н���', '����ĸ�', None, '����ĸ�', 'ʵ���˱��', '����ĸ�', '�ͼ۳���', '�ͼ۳���', '��������', '�ͼ۳���', '���ؽ���', '����תԤ��+���¹�', '�¹�', '������Ʒ', '�ͼ۳���', 'ʳƷҽҩ��ȫ', '����תԤ��', '����תԤ��+���¹�', '�ͼ۳���', '�����', '�ͼ۳���', '���ؽ���', '�Ϻ�����ĸ�', '�Ϻ�����ĸ�', '�Ϻ�����ĸ�', '����ĸ�', '�ͼ۳���', '������ĸ�', '����ĸ�', '�¹�', '�¹�']
# map = {}
# for c in concepts:
#     if c in map.keys():
#         map[c] = map[c] + 1
#     else:
#         map.setdefault(c, 1)

getZhangTingCodeConceptAnd2DB("2018-07-27")

date = "2018-07-27"
len = 10
while len > 0:
    getZhangTingCodeConceptAnd2DB(date)
    date = fd.preOpenDate(date)
    len = len - 1