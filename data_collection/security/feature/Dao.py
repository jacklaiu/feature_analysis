from base import Dao as dao

def appendRecord(code, date, ye_chg, continuous_rise_day_count, ye_qrr, ye_tr, open_chg, close_chg, res):
    delRecord(code, date)
    dao.update("insert into security_feature_record(code, date, ye_chg, continuous_rise_day_count, ye_qrr, ye_tr, open_chg, close_chg, res) value(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
               (code, date, ye_chg, continuous_rise_day_count, ye_qrr, ye_tr, open_chg, close_chg, res))

def getRecord(code, date):
    ret = dao.select("select code, date, ye_chg, continuous_rise_day_count, ye_qrr, ye_tr, open_chg, close_chg, res from security_feature_record where code = %s and date = %s", (code, date))
    return ret[0]

def delRecord(code, date):
    dao.update("delete from security_feature_record where code = %s and date = %s", (code, date))

# appendRecord('002123', '2018-07-19', '7.89', '3', '2.1', '9.1', '-3.4', '4.6', '8.0')
# print(getRecord('002123', '2018-07-19'))