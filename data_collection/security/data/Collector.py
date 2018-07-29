import base.FinanceDataSource as fd
import tushare as ts
import base.Dao as dao

def caculateMarketAnd2DB():
    openDates = fd.getOpenDates()
    openDates.reverse()
    max_date = dao.select("select max(date) max_date from security_data", ())[0]['max_date']
    min_date = dao.select("select min(date) min_date from security_data", ())[0]['min_date']
    startDate = min_date
    endDate = max_date
    pdv = None
    for date in openDates:
        if date == '' or date > endDate or date < fd.nextOpenDate(startDate, 10): continue

        arr = dao.select("select code, date, open, close, high, low, volume from "
                   "security_data where date=%s", (date))

        ye_arr = dao.select("select code, date, open, close, high, low, volume from "
                   "security_data where date=(select max(date) from security_data where date<%s) ", (date))

        ty_arr = dao.select("select code, date, open, close, high, low, volume from "
                            "security_data where date=(select max(date) from security_data where date<%s) ", (fd.preOpenDate(date, 1)))

        pre_ty_arr = dao.select("select code, date, open, close, high, low, volume from "
                            "security_data where date=(select max(date) from security_data where date<%s) ", (fd.preOpenDate(date, 2)))

        code_item = {}
        code_ye_item = {}
        code_ty_item = {}
        code_pre_ty_item = {}
        for item in arr: code_item[item['code']] = item
        for ye_item in ye_arr: code_ye_item[ye_item['code']] = ye_item
        for ty_item in ty_arr: code_ty_item[ty_item['code']] = ty_item
        for pre_ty_item in pre_ty_arr: code_pre_ty_item[pre_ty_item['code']] = pre_ty_item
        yzzt_count = 0
        yzdt_count = 0
        dt = 0
        zrzt = 0

        zt_count= 0
        zt_high_count = 0
        _1bzt_count = 0
        _1bzt_high_count = 0
        _2bzt_count = 0
        _2bzt_high_count = 0
        _3bzt_count = 0
        _3bzt_high_count = 0
        _4bzt_count = 0
        _4bzt_high_count = 0
        _5bzt_count = 0
        _5bzt_high_count = 0
        _6bzt_count = 0
        _6bzt_high_count = 0
        sum_chg = 0
        ye_zt_count = 0

        for item in arr:
            code = item['code']
            # if code != '000760': continue
            try:
                ye_item = code_ye_item[code]
            except:
                _date = item['date']
                ye_items = dao.select("select code, date, open, close, high, low, volume from security_data "
                                     "where code=%s and date=(select max(date) from security_data where date<%s and code=%s) ",
                                     (code, _date, code))
                if ye_items is None or ye_items.__len__() == 0:
                    continue
                else:
                    ye_item = ye_items[0]
            try:
                ty_item = code_ty_item[code]
            except:
                _date = ye_item['date']
                ty_items = dao.select("select code, date, open, close, high, low, volume from security_data "
                                     "where code=%s and date=(select max(date) from security_data where date<%s and code=%s) ",
                                     (code, _date, code))
                if ty_items is None or ty_items.__len__() == 0: continue
                else: ty_item = ty_items[0]

            try:
                pre_ty_item = code_pre_ty_item[code]
            except:
                _date = ty_item['date']
                pre_ty_items = dao.select("select code, date, open, close, high, low, volume from security_data "
                                     "where code=%s and date=(select max(date) from security_data where date<%s and code=%s) ",
                                     (code, _date, code))
                if pre_ty_items is None or pre_ty_items.__len__() == 0: continue
                else: pre_ty_item = pre_ty_items[0]

            if(_is_yzzt(item, ye_item) == True): yzzt_count = yzzt_count + 1
            if (_is_yzdt(item, ye_item) == True): yzdt_count = yzdt_count + 1
            if (_is_dt(ye_item, ty_item) == True): dt = dt + 1
            if (_is_zrzt(ye_item, ty_item) == True): zrzt = zrzt + 1
            lb = _is_lb(code, date, item, ye_item, ty_item)
            if (lb == 6): _6bzt_count = _6bzt_count + 1
            elif (lb == 5): _5bzt_count = _5bzt_count + 1
            elif (lb == 4): _4bzt_count = _4bzt_count + 1
            elif (lb == 3): _3bzt_count = _3bzt_count + 1
            elif (lb == 2): _2bzt_count = _2bzt_count + 1
            elif (lb == 1): _1bzt_count = _1bzt_count + 1

            if is_zt(item, ye_item) == True: zt_count = zt_count + 1
            if is_high_zt(item, ye_item) == True: zt_high_count = zt_high_count + 1

            pre_lb = _is_ye_lb(code, date, ye_item, ty_item, pre_ty_item)

            if pre_lb == 0 and is_high_zt(item, ye_item):
                _1bzt_high_count = _1bzt_high_count + 1
            if pre_lb == 1 and is_high_zt(item, ye_item) == True:
                _2bzt_high_count = _2bzt_high_count + 1
            if pre_lb == 2 and is_high_zt(item, ye_item) == True:
                _3bzt_high_count = _3bzt_high_count + 1
            if pre_lb == 3 and is_high_zt(item, ye_item) == True:
                _4bzt_high_count = _4bzt_high_count + 1
            if pre_lb == 4 and is_high_zt(item, ye_item) == True:
                _5bzt_high_count = _5bzt_high_count + 1
            if pre_lb == 5 and is_high_zt(item, ye_item) == True:
                _6bzt_high_count = _6bzt_high_count + 1

            if is_ye_zt(ye_item, ty_item) == True:
                today_chg = get_chg(item, ye_item)
                sum_chg = sum_chg + today_chg
                ye_zt_count = ye_zt_count + 1

            print("Code: " + code + " Date: " + date)

        zt_success = None
        if zt_high_count > 0: zt_success = round((zt_count/zt_high_count), 2)
        _1bzt_success = -1
        if _1bzt_high_count > 0: _1bzt_success = round((_1bzt_count/_1bzt_high_count), 2)
        _2bzt_success = -1
        if _2bzt_high_count > 0: _2bzt_success = round((_2bzt_count / _2bzt_high_count), 2)
        _3bzt_success = -1
        if _3bzt_high_count > 0: _3bzt_success = round((_3bzt_count / _3bzt_high_count), 2)
        _4bzt_success = -1
        if _4bzt_high_count > 0: _4bzt_success = round((_4bzt_count / _4bzt_high_count), 2)
        _5bzt_success = -1
        if _5bzt_high_count > 0: _5bzt_success = round((_5bzt_count / _5bzt_high_count), 2)
        _6bzt_success = -1
        if _6bzt_high_count > 0: _6bzt_success = round((_6bzt_count / _6bzt_high_count), 2)

        today_avg_chg_when_yezt = round((sum_chg/ye_zt_count), 2)

        print('Date: ' + date + ' yzzt_count: ' + str(yzzt_count) + ' yzdt_count: ' + str(yzdt_count) + ' dt: ' + str(dt) + ' zrzt:' + str(zrzt))

        dao.update("delete from market_environment where date=%s", (date))

        if pdv is None:

            dao.update("insert into market_environment(date, yzzt_count, yzdt_count, dt_count, zrzt_count, "
                       
                       "1bzt_count, 2bzt_count, 3bzt_count, 4bzt_count, 5bzt_count, 6bzt_count, "
                       
                       "1bzt_success, 2bzt_success, 3bzt_success, 4bzt_success, 5bzt_success, 6bzt_success, "
                       
                       "zt_success, today_avg_chg_when_yezt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

                       (date, yzzt_count, yzdt_count, dt, zrzt,

                        _1bzt_count, _2bzt_count, _3bzt_count, _4bzt_count, _5bzt_count, _6bzt_count,

                        _1bzt_success, _2bzt_success, _3bzt_success, _4bzt_success, _5bzt_success, _6bzt_success, zt_success,

                        today_avg_chg_when_yezt))
        else:

            dao.update("insert into market_environment(date, yzzt_count, ye_yzzt_count, yzdt_count, ye_yzdt_count, dt_count, ye_dt_count, zrzt_count, ye_zrzt_count, "

                       "1bzt_count, ye_1bzt_count, 2bzt_count, ye_2bzt_count, 3bzt_count, ye_3bzt_count, 4bzt_count, ye_4bzt_count, 5bzt_count, ye_5bzt_count, 6bzt_count, ye_6bzt_count, "
                       
                       "1bzt_success, ye_1bzt_success, 2bzt_success, ye_2bzt_success, 3bzt_success, ye_3bzt_success, 4bzt_success, ye_4bzt_success, 5bzt_success, ye_5bzt_success, 6bzt_success, ye_6bzt_success, "

                       "zt_success, ye_zt_success, today_avg_chg_when_yezt, ye_today_avg_chg_when_yezt) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,"
                       
                       "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",

                       (date, yzzt_count, pdv[1], yzdt_count, pdv[2], dt, pdv[3], zrzt, pdv[4],

                        _1bzt_count, pdv[5], _2bzt_count, pdv[6], _3bzt_count, pdv[7], _4bzt_count, pdv[8], _5bzt_count, pdv[9], _6bzt_count, pdv[10],

                        _1bzt_success, pdv[11], _2bzt_success, pdv[12], _3bzt_success, pdv[13], _4bzt_success, pdv[14], _5bzt_success, pdv[15], _6bzt_success, pdv[16],

                        zt_success, pdv[17],

                        today_avg_chg_when_yezt, pdv[18]))

        pdv = (date, yzzt_count, yzdt_count, dt, zrzt,

                    _1bzt_count, _2bzt_count, _3bzt_count, _4bzt_count, _5bzt_count, _6bzt_count,

                    _1bzt_success, _2bzt_success, _3bzt_success, _4bzt_success, _5bzt_success, _6bzt_success, zt_success,

                    today_avg_chg_when_yezt)


def crawlSecurityData_AtFront(daysCount):
    securities = fd.get_all_securities()
    min_date = dao.select("select min(date) min_date from security_data",())[0]['min_date']
    if min_date is not None:
        endDate = fd.preOpenDate(min_date, 1)
    else:
        endDate = fd.getLastestOpenDate()
    startDate = fd.preOpenDate(endDate, daysCount)
    if startDate > endDate: return
    for code in securities:
        count = 0
        df = ts.get_k_data(code, startDate, endDate)
        arr_values = []
        while count < df.index.__len__():
            open = str(df['open'].values[count])
            close = str(df['close'].values[count])
            high = str(df['high'].values[count])
            low = str(df['low'].values[count])
            volume = str(df['volume'].values[count])
            date = str(df['date'].values[count])
            arr_values.append((code, date, open, close, high, low, volume))
            count = count + 1
            print("Date: " + date + " Code: " + code)

        #dao.update("delete from security_data where code=%s", (code,))
        dao.updatemany(
            "insert into security_data(code, date, open, close, high, low, volume) values(%s,%s,%s,%s,%s,%s,%s)",
            arr_values)

def crawlSecurityData_AtRear(dayCount):
    securities = fd.get_all_securities()
    max_date = dao.select("select max(date) max_date from security_data", ())[0]['max_date']
    endDate = fd.getLastestOpenDate()
    if max_date is not None:
        startDate = fd.nextOpenDate(max_date, 1)
    else:
        startDate = fd.preOpenDate(endDate, dayCount)
    if startDate > endDate: return
    for code in securities:
        count = 0
        df = ts.get_k_data(code, startDate, endDate)
        arr_values = []
        while count < df.index.__len__():
            open = str(df['open'].values[count])
            close = str(df['close'].values[count])
            high = str(df['high'].values[count])
            low = str(df['low'].values[count])
            volume = str(df['volume'].values[count])
            date = str(df['date'].values[count])
            arr_values.append((code, date, open, close, high, low, volume))
            count = count + 1
            print("Date: " + date + " Code: " + code)

        dao.update("delete from security_data where code=%s and date=%s", (code, date))
        dao.updatemany(
            "insert into security_data(code, date, open, close, high, low, volume) values(%s,%s,%s,%s,%s,%s,%s)",
            arr_values)

#------------------------------------------------------------------------------------------------------------------------------


















#获取今日涨跌幅
def get_chg(item, ye_item):
    close = float(item['close'])
    pre_close = float(ye_item['close'])
    rate = round(float((close - pre_close) / pre_close) * 100, 2)
    return rate

#最高价涨停
def is_high_zt(item, ye_item):
    high = float(item['high'])
    pre_close = float(ye_item['close'])
    rate = round(float((high - pre_close) / pre_close) * 100, 2)
    return rate >= 9.89

#涨停
def is_zt(item, ye_item):
    close = float(item['close'])
    pre_close = float(ye_item['close'])
    rate = round(float((close - pre_close) / pre_close) * 100, 2)
    return rate >= 9.89

#昨日涨停
def is_ye_zt(ye_item, ty_item):
    pre_close = float(ye_item['close'])
    ty_close = float(ty_item['close'])
    rate = round(float((pre_close - ty_close) / ty_close) * 100, 2)
    return rate >= 9.89

def getLbSuccess(date, num2Lb):
    return ''

def _is_lb(code, date, item, ye_item, ty_item):
    close = float(item['close'])
    pre_close = float(ye_item['close'])
    ty_close = float(ty_item['close'])
    rate = round(float((close - pre_close) / pre_close) * 100, 2)
    ye_rate = round(float((pre_close - ty_close) / ty_close) * 100, 2)
    if rate >= 9.89 and ye_rate < 9.89: return 1
    if rate < 9.89 or ye_rate < 9.89: return 0
    count = 0
    df = ts.get_k_data(code, fd.preOpenDate(date, 30), date)
    len = df['close'].values.__len__()
    while True:
        try:
            close = df['close'].values[len-count-1]
        except:
            return 2
        try:
            pre_close = df['close'].values[len-count-2]
        except:
            return 2
        rate = round(float((close - pre_close)/pre_close)*100, 2)
        if rate >= 9.89:
            count = count + 1
            if count >=6:
                break
            continue
        else:
            break
    return count

def _is_ye_lb(code, date, ye_item, ty_item, pre_ty_item):

    pre_close = float(ye_item['close'])
    ty_close = float(ty_item['close'])
    pre_ty_close = float(pre_ty_item['close'])

    ye_rate = round(float((pre_close - ty_close) / ty_close) * 100, 2)
    ty_rate = round(float((ty_close - pre_ty_close) / pre_ty_close) * 100, 2)

    if ye_rate >= 9.89 and ty_rate < 9.89: return 1
    if ye_rate < 9.89 or ty_rate < 9.89: return 0
    count = 0
    df = ts.get_k_data(code, fd.preOpenDate(date, 30), fd.preOpenDate(date, 1))
    len = df['close'].values.__len__()
    while True:
        try:
            pre_close = df['close'].values[len-count-1]
        except:
            return 2
        try:
            ty_close = df['close'].values[len-count-2]
        except:
            return 2
        rate = round(float((pre_close - ty_close)/ty_close)*100, 2)
        if rate >= 9.89:
            count = count + 1
            if count >=6:
                break
            continue
        else:
            break
    return count

def _is_yzzt(item, ye_item):
    open = float(item['open'])
    pre_close = float(ye_item['close'])
    open_rate = round(float((open - pre_close)/pre_close)*100, 2)
    if open_rate >= 9.89:
        return True
    else:
        return False

def _is_yzdt(item, ye_item):
    open = float(item['open'])
    pre_close = float(ye_item['close'])
    open_rate = round(float((open - pre_close)/pre_close)*100, 2)
    if open_rate <= -9.89:
        return True
    else:
        return False

def _is_dt(item, ye_item):
    pre_close = float(item['close'])
    ty_close = float(ye_item['close'])
    open_rate = round(float((pre_close - ty_close)/ty_close)*100, 2)
    if open_rate <= -9.89:
        return True
    else:
        return False

def _is_zrzt(item, ye_item):
    pre_close = float(item['close'])
    ty_close = float(ye_item['close'])
    pre_open = item['open']
    pre_high = item['high']
    open_rate = round(float((pre_close - ty_close)/ty_close)*100, 2)
    if open_rate >= 9.89 and pre_open != pre_high:
        return True
    else:
        return False

# caculateMarketAnd2DB()
#crawlSecurityData('2018-07-25', 100)
#crawlSecurityData_AtFront(100)
crawlSecurityData_AtRear(200)
#caculateMarketAnd2DB()