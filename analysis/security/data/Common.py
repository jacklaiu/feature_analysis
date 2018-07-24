import base.Dao as dao
import base.FinanceDataSource as fd

#注意：要先把tushare的get_k_date数据爬取到db，再从db获取个股基本数据

def getQrr(code, date):
    today = dao.select("SELECT (volume/(60*4)) as today from security_data where code=%s and date=%s", (code, date))[0]['today']
    base = dao.select("select (sum(volume)/(4*60*5)) as base from (SELECT date, volume from security_data where date<%s and code=%s ORDER BY date DESC limit 5) as A", (date, code))[0]['base']
    ret = round(today/base, 2)
    return ret

def getChgPercent(code, date):
    res = dao.select("select `close` from security_data where code=%s and date<=%s order by date desc limit 2", (code, date))
    close = float(res[0]['close'])
    pre_close = float(res[1]['close'])
    ret = round(((close-pre_close)/pre_close)*100, 2)
    return ret

print(getChgPercent('600939', '2018-07-20'))

