# -*- coding: gbk -*-
import base.HtmlGetter as hg
import base.FinanceDataSource as fd
import base.Dao as dao

def getZhangTingCodeConceptAnd2DB(date=fd.getLastestOpenDate()):
    soups = hg.getSoupsFromWencai(date + "日涨停；涨停原因；按"+date+"日首次涨停时间排序")
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

    #（1）获取所有concept的集合
    #（2）迭代concept，获取count，在特定的date
    #（3）返回图标接受的数据model

    endDate = fd.getLastestOpenDate()
    startDate = fd.preOpenDate(endDate, dayCount)
    nowDate = startDate

    concepts = dao.select("select concept from zhangting_concept where date >= %s and date <= %s group by concept", (startDate, endDate))
    print()


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
    return None






# concepts = ['深圳国企改革', '低价超跌', '国企改革', '实控人拟变更', '低价超跌', '股权转让', '国企改革', '股权转让', '国企改革', '签署合作框架协议', '稀有金属', '国企改革', None, '国企改革', '实控人变更', '国企改革', '低价超跌', '低价超跌', '技术改造', '低价超跌', '西藏建设', '高送转预期+次新股', '新股', '生物制品', '低价超跌', '食品医药安全', '高送转预期', '高送转预期+次新股', '低价超跌', '地天板', '低价超跌', '西藏建设', '上海国企改革', '上海国企改革', '上海国企改革', '国企改革', '低价超跌', '天津国企改革', '国企改革', '新股', '新股']
# map = {}
# for c in concepts:
#     if c in map.keys():
#         map[c] = map[c] + 1
#     else:
#         map.setdefault(c, 1)
# date = "2018-07-24"

map = get_zhangtingconcept_countMap(10)
