from data_collection.security.feature import Dao as dao
from base import FinanceDataSource as fds
from base import HtmlGetter as hg
import tushare as ts
import base.FinanceDataSource as fd
DateCount = 200

# 在交易后的晚上执行
def getWencaiCodesForGettingDataAndSave2DB(date=fd.getLastestOpenDate()):
    count = 0
    while True:
        if count < 151:
            count = count + 1
            ye_date = fds.preOpenDate(date, 1)
            date = ye_date
            continue
        if count > DateCount:
            break
        ye_date = fds.preOpenDate(date, 1)
        w = "非st；" + ye_date + "日均线角度>30；" + ye_date + "日涨跌幅>0；((" + date + "日开盘价-" + ye_date + "日收盘价)/" + ye_date + "日收盘价)<-0.03"
        codes = hg.getCodesFromWencai(w)
        print(w)
        for code in codes:
            df = ts.get_k_data(code, start=fds.preOpenDate(date, 20), end=date)
            # 过滤问句因除权数据产生的杂音
            open_chg = fds.get_open_chg(df, date)
            if open_chg > -3:
                continue
            print("Date: " + str(date) + " ye_Date: "+ ye_date + " Code: " + str(code))
            print("(1)getting df: ")
            ye_chg = fds.get_ye_chg(df, date)
            print("(2)getting ye_chg: " + str(ye_chg))
            continuous_rise_day_count = fds.get_continuous_rise_day_count(df, date)
            print("(3)getting continuous_rise_day_count: " + str(continuous_rise_day_count))
            ye_qrr = fds.get_ye_qrr(df, date)
            print("(4)getting ye_qrr: " + str(ye_qrr))
            open_chg = fds.get_open_chg(df, date)
            print("(5)getting open_chg: " + str(open_chg))
            close_chg = fds.get_close_chg(df, date)
            print("(6)getting close_chg: " + str(close_chg))

            continuous_z_day_count = fds.get_continuous_z_day_count(df, date)
            print("(7)getting continuous_z_day_count: " + str(continuous_z_day_count))

            print("(8)storing 2 DB")
            dao.appendRecord(df, date, ye_chg, continuous_rise_day_count, ye_qrr, 0, open_chg, close_chg, close_chg-open_chg)
            print("-------------------------------------------------------")
        count = count + 1
        date = ye_date

#getWencaiCodesForGettingDataAndSave2DB("2018-07-20")