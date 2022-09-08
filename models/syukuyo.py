from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import sys

#pip install git+https://github.com/fgshun/qreki_py.git@v0.5.1#egg=qreki
from qreki import Kyureki

class Syukuyo(object):
    
    __syuku12 = ["室","圭","胃","ひつ","参","鬼","張","角","底","心","斗","虚"]
    __syuku27 = ["室","壁","圭","ろう","胃","昂","ひつ","嘴","参","井","鬼","柳","星","張","翼","珍","角","抗","底","房","心","尾","筧","斗","女","虚","危"]
    __syuku_ft = ["命","(活)栄","(活)衰","(活)安","(活)危","(活)成","(活)壊","(活)友","(活)親","業","(破)栄","(破)衰","(破)安","(破)危","(破)成","(破)壊","(破)友","(破)親","胎","(再)栄","(再)衰","(再)安","(再)危","(再)成","(再)壊","(再)友","(再)親"]
    __ryohan_dict = {'1-5':'1-16','1-6':'17-30','2-0':'1-14','2-1':'15-30','3-2':'1-12','3-3':'13-30',
                '4-4':'1-10','4-5':'11-30','5-6':'1-8','5-0':'9-30','6-1':'1-6','6-2':'7-30',
                '7-4':'1-3','7-5':'4-30','8-1':'1-27','9-3':'1-25','9-4':'26-30',
                '10-5':'1-23','10-6':'24-30','11-1':'1-20','11-2':'21-30','12-3':'1-18','12-4':'19-30'}

    def __init__(self):
        pass

    #本宿を求める
    #仕様 https://www.timeless-edition.com/archives/11698, https://nakshatra.tokyo/pc/30.html
    def get_honsyuku(self,birthy,birthm,birthd):
        """
        Args:
            birthy(int): 誕生日の年
            birthm(int): 誕生日の月
            birthd(int): 誕生日の日
        Returns:
            string: 誕生日から求めた本宿名
        """
        #誕生日を旧暦に変換（kはDatetimeやDateオブジェクトではなくKyurekiオブジェクト）
        k = Kyureki.from_ymd(birthy,birthm,birthd)

        #誕生月（旧暦）の一日の宿を12宿リストから取得
        first_syuku = self.__syuku12[k.month-1]

        #本宿=誕生日（旧暦）の宿を27宿リストから取得
        syuku27_idx = self.__syuku27.index(first_syuku)  
        honsyuku = self.__syuku27[((syuku27_idx+k.day)%27)-1]
        return honsyuku


    #本宿から運勢リストを求める
    #仕様 https://uranai.blog/shukuyo-unsei/
    def get_fortune(self,honsyuku,months_num):

        #27宿リストに無い本宿値が渡されたらValueErrorを返す
        if honsyuku not in self.__syuku27:
            raise ValueError('入力された本宿が不正です')

        #今月月初日
        dt_first = date.today().replace(day=1)
        #本日からNヵ月後の日
        dt_month_to = date.today() + relativedelta(months=months_num-1)
        #本日からNヵ月後の月末日
        dt_last = dt_month_to + relativedelta(months=1) - timedelta(days=dt_month_to.day)
        #日数
        dt_days_count = (dt_last - dt_first).days + 1

        ft_list = []
        i=0
        for i in range(dt_days_count):
            ft_dict = {}
            dt = dt_first + timedelta(days=i)

            #指定日を旧暦変換
            k = Kyureki.from_ymd(dt.year,dt.month,dt.day)
            #指定日の旧暦月一日の宿を取得
            first_syuku = self.__syuku12[k.month-1]
            #上記宿の27宿リストでのインデックス番号を取得
            dt_first_idx = self.__syuku27.index(first_syuku)  
            #指定日の宿を取得
            dt_syuku = self.__syuku27[(dt_first_idx + k.day) % len(self.__syuku27) - 1 ]
            #上記宿の27宿リストでのインデックス番号を取得
            dt_idx = self.__syuku27.index(dt_syuku)

            #本宿の27宿リストでのインデックス番号を取得
            honsyuku_idx = self.__syuku27.index(honsyuku)

            if(dt_idx >= honsyuku_idx):
                diff = dt_idx - honsyuku_idx
            else:                           
                diff = 27 + (dt_idx - honsyuku_idx)
            
            #運勢宿リストから指定日の運勢を取得
            fortune = self.__syuku_ft[diff]

            #凌犯期間対応
            #仕様 https://yakumoin.net/about/ryouhan
            #指定日の旧暦月一日の曜日を取得（0=月曜～6=日曜）
            first_weekday = (dt.weekday() - (k.day-1)) % 7 

            ryohan_key = str(k.month) + '-' + str(first_weekday)
  
            if ryohan_key in self.__ryohan_dict:
                ryohan_val = self.__ryohan_dict[ryohan_key]
                ryohan_start = ryohan_val[:ryohan_val.find('-')]
                ryohan_end = ryohan_val[ryohan_val.find('-')+1:]

                #凌犯期間に相当すれば、運勢に【凌】を付加し、六害宿はその文字に置き換える
                if k.day>=int(ryohan_start) and k.day<=int(ryohan_end):
                    if fortune == "(活)安":
                        fortune = "意"
                    elif fortune == "業":
                        fortune = "事"
                    elif fortune == "(破)安":
                        fortune = "克"
                    elif fortune == "(破)壊":
                        fortune = "聚"
                    elif fortune == "(再)栄":
                        fortune = "同"
                    else:
                        fortune = fortune.replace('(活)','')
                        fortune = fortune.replace('(破)','')
                        fortune = fortune.replace('(再)','')
                        fortune = "【凌】" + fortune 

            #運勢を{日付(datetime.date)：運勢(str)}形式でリストへ追加
            ft_dict[dt]=fortune
            ft_list.append(ft_dict)

        return ft_list


        



   