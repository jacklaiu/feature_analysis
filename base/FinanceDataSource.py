import tushare as ts
from base import DateUtil as du
import os

def get_all_securities():
    f = open(os.path.dirname(__file__) + "/all_securities.txt", "r")
    str = f.read()
    return str.split("_")

def initOpenDateTempFile():
    OpenList = ts.trade_cal()
    rows = OpenList[OpenList.isOpen == 1].values[-888:]
    f = open("temp_OpenDate.txt", "w")
    f.write("")
    f.close()
    f = open("temp_OpenDate.txt", "a")
    for row in rows:
        date = row[0]
        f.write(date + ";")
    f.close()

def readOpenDatesFromTempFile():
    f = open(os.path.dirname(__file__) + "/temp_OpenDate.txt", "r")
    str = f.read()
    if str != "":
        dates = str.split(";")
    else: return None
    return dates

def getOpenDates():
    OpenList = ts.trade_cal()
    dates = []
    rows = OpenList[OpenList.isOpen == 1].values[-888:]
    for row in rows:
        dates.append(row[0])
    return dates

OpenDates = readOpenDatesFromTempFile()

def get_k_data(df, start, end):
    ret = df[(df['date'] >= start) & (df['date'] <= end)]
    return ret

def isOpen(date):
    #OpenList = ts.trade_cal()
    # try:
    #     isOpen = OpenList[OpenList.calendarDate == date].values[0][1]
    # except:
    #     return None
    # if (isOpen == 1):
    #     return True
    # return False
    str = ";".join(OpenDates)
    return date in str

def preOpenDate(date, leftCount=1):
    index = 0
    for d in OpenDates:
        if d == date:
            return OpenDates[index - leftCount]
        index = index + 1
    return None

def getLastestOpenDate(date=du.getYMD()):
    count = 0
    while True:
        count = count + 1
        if isOpen(date) == False:
            date = preOpenDate(date, count)
            continue
        else:
            break
    return date

def nextOpenDate(date, rightCount=1):
    index = 0
    for d in OpenDates:
        if d == date:
            if index + rightCount < OpenDates.__len__() -1:
                return OpenDates[index + rightCount]
            else:
                break
        index = index + 1
    return None

def get_today_open2close_chg(code, date=du.getYMD()):
    try :
        start = preOpenDate(date, 1)
        end = start
        if isinstance(code, str):
            d = ts.get_k_data(code=code, start=start, end=end)
        else:
            d = get_k_data(df=code, start=start, end=end)
        dc = d['close']
        do = d['open']
        ye_open = do.values[0]
        ye_close = dc.values[0]
        ret = round(((float(ye_close) - float(ye_open)) / float(ye_open)), 4) * 100
    except Exception as e:
        print(e)
        return None
    return ret

def get_ye_chg(code, date=du.getYMD()):
    try:
        start = preOpenDate(date, 2)
        end = preOpenDate(date, 1)
        if isinstance(code, str):
            d = ts.get_k_data(code=code, start=start, end=end)
        else:
            d = get_k_data(df=code, start=start, end=end)
        dd = d['close']
        ty_close = dd.values[0]
        ye_close = dd.values[1]
        ret = round(((float(ye_close) - float(ty_close)) / float(ty_close)), 4) * 100
    except Exception as e:
        print(e)
        return None
    return ret

def get_ty_chg(code, date=du.getYMD()):
    try:
        start = preOpenDate(date, 3)
        end = preOpenDate(date, 2)
        if isinstance(code, str):
            d = ts.get_k_data(code=code, start=start, end=end)
        else:
            d = get_k_data(df=code, start=start, end=end)
        dd = d['close']
        ty_close = dd.values[0]
        ye_close = dd.values[1]
        ret = round(((float(ye_close) - float(ty_close)) / float(ty_close)), 4) * 100
    except Exception as e:
        print(e)
        return None
    return ret

def get_continuous_rise_day_count(code, date=du.getYMD()):
    count = 0
    try:
        #chg = get_ye_chg(code, preOpenDate(date, count))
        chg = get_today_open2close_chg(code, preOpenDate(date, count))
        while chg >= 0:
            if count > 10:
                break
            count = count + 1
            #chg = get_ye_chg(code, preOpenDate(date, count))
            chg = get_today_open2close_chg(code, preOpenDate(date, count))
            if chg is None:
                break
    except Exception as e:
        print(e)
        return None
    return count

def get_continuous_z_day_count(code, date=du.getYMD()):
    count = 0
    try:
        chg = get_ye_chg(code, preOpenDate(date, count))
        #chg = get_today_open2close_chg(code, preOpenDate(date, count))
        while chg >= 0:
            if count > 10:
                break
            count = count + 1
            chg = get_ye_chg(code, preOpenDate(date, count))
            #chg = get_today_open2close_chg(code, preOpenDate(date, count))
            if chg is None:
                break
    except Exception as e:
        print(e)
        return None
    return count

def get_ye_qrr(code, date=du.getYMD()):
    try:
        start = preOpenDate(date, 6)
        end = preOpenDate(date, 1)
        if isinstance(code, str):
            d = ts.get_k_data(code=code, start=start, end=end)
        else:
            d = get_k_data(df=code, start=start, end=end)
        dd = d['volume']
        len = dd.values.__len__()
        total_volume = 0
        ye_volume = 0
        count = 0
        for row in dd.values:
            if count == len - 1:
                ye_volume = row
            else:
                total_volume = total_volume + row
            count = count + 1
        base = total_volume / (4*60*5)
        today = ye_volume / (4*60)
        if base == 0:
            return None
        ret = round(float(today/base), 2)
    except Exception as e:
        print(e)
        return None
    return ret

# def get_ye_tr(code, date=du.getYMD()):
#     start = preOpenDate(date, 1)
#     end = preOpenDate(date, 1)
#     if isinstance(code, str):
#         d = ts.get_k_data(code=code, start=start, end=end)
#     else:
#         d = get_k_data(df=code, start=start, end=end)
#         code = d['code'].values[0]
#         d = ts.get_hist_data(code, start, end)
#     dd = d['turnover']
#     print()

def get_open_chg(code, date=du.getYMD()):
    try:
        start = preOpenDate(date, 1)
        end = date
        if isinstance(code, str):
            d = ts.get_k_data(code=code, start=start, end=end)
        else:
            d = get_k_data(df=code, start=start, end=end)
        pre_close = d['close'].values[0]
        open = d['open'].values[1]
        ret = round(((float(open) - float(pre_close)) / float(pre_close)), 4) * 100
    except Exception as e:
        print(e)
    return ret

def get_close_chg(code, date=du.getYMD()):
    try:
        start = preOpenDate(date, 1)
        end = date
        if isinstance(code, str):
            d = ts.get_k_data(code=code, start=start, end=end)
        else:
            d = get_k_data(df=code, start=start, end=end)
        pre_close = d['close'].values[0]
        close = d['close'].values[1]
        ret = round(((float(close) - float(pre_close)) / float(pre_close)), 4) * 100
    except Exception as e:
        print(e)
    return ret

# dataf = ts.get_k_data('000565', start="2018-07-06", end="2018-07-20")
# print("open_chg: " + str(get_open_chg(dataf, "2018-07-20")))
# print("close_chg: " + str(get_close_chg(dataf, "2018-07-20")))

#initOpenDateTempFile()
# print(isOpen("2018-07-21"))
# print(os.path.dirname(__file__))