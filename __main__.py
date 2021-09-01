from twse import twt49u
from twse import twt48u
import time

def main():
    service_48 = twt48u.TWT48_Service()
    service_48.collection()

def dividend_history():
    service_49 = twt49u.TWT49_Service()
    # 458
    service_49.collection("2003", "5", "5", "2004", "1", "1")
    time.sleep(1)
    # 508
    service_49.collection("2004", "1", "1", "2005", "1", "1")
    time.sleep(1)
    # 555
    service_49.collection("2005", "1", "1", "2006", "1", "1")
    time.sleep(1)
    # 523
    service_49.collection("2006", "1", "1", "2007", "1", "1")
    time.sleep(1)
    # 538
    service_49.collection("2007", "1", "1", "2008", "1", "1")
    time.sleep(1)
    # 609
    service_49.collection("2008", "1", "1", "2009", "1", "1")
    time.sleep(1)
    # 511
    service_49.collection("2009", "1", "1", "2010", "1", "1")
    time.sleep(1)
    # 627
    service_49.collection("2010", "1", "1", "2011", "1", "1")
    time.sleep(1)
    # 729
    service_49.collection("2011", "1", "1", "2012", "1", "1")
    time.sleep(1)
    # 674
    service_49.collection("2012", "1", "1", "2013", "1", "1")
    time.sleep(1)
    # 691
    service_49.collection("2013", "1", "1", "2014", "1", "1")
    time.sleep(1)
    # 732
    service_49.collection("2014", "1", "1", "2015", "1", "1")
    time.sleep(1)
    # 747
    service_49.collection("2015", "1", "1", "2016", "1", "1")
    time.sleep(1)
    # 734
    service_49.collection("2016", "1", "1", "2017", "1", "1")
    time.sleep(1)
    # 781
    service_49.collection("2017", "1", "1", "2018", "1", "1")
    time.sleep(1)
    # 825
    service_49.collection("2018", "1", "1", "2019", "1", "1")
    time.sleep(1)
    # 880
    service_49.collection("2019", "1", "1", "2020", "1", "1")
    time.sleep(1)
    # 888
    service_49.collection("2020", "1", "1", "2021", "1", "1")
    time.sleep(1)
    # 740
    service_49.collection("2021", "1", "1", "2021", "9", "2")


if __name__ == '__main__':
    print("==================== main ====================")
    main()
    print("==================== main ====================")