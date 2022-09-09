from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import json
from models.syukuyo import Syukuyo
from models.g_calendar import GCalendar

class SyukuyoCalendar(object):

    #本命宿ごとのGoogleカレンダーID
    CALENDAR_IDS = {
            '尾' : 'elq5368slgqd7fudhp3106nr88@group.calendar.google.com'
        }

    def __init__(self):
        pass

    #本命宿ごとのGoogleカレンダーに宿曜運勢を予定として書き込む
    def create_events(self,honsyuku,y_from,m_from,y_to,m_to):

        #運勢を求める期間の開始年月の月初日
        dt_from = date(y_from, m_from, 1)
        #運勢を求める期間の開始年月の月末日
        dt_to = date(y_to,m_to,1) + relativedelta(months=1) - timedelta(days=1)
        #運勢を求める期間の日数
        dt_days_count = (dt_to - dt_from).days + 1

        if dt_days_count > 366:
            resp = "期間指定は1年以内にしてください"
        
        else:
            #本命宿から指定された期間の運勢リストを取得
            syukuyo = Syukuyo()
            ft_list = syukuyo.get_fortune(honsyuku,y_from,m_from,y_to,m_to)

            #本命宿に応じたカレンダーIDを取得
            #calendar_id = self.CALENDAR_IDS[honsyuku]
            calendar_id = self.CALENDAR_IDS['尾']

            gcal = GCalendar()

            for i in range(len(ft_list)):
                plan = {
                    'summary' : list(ft_list[i].values())[0],
                    'start' : {
                        #Googleカレンダーは日時をISOフォーマットで受け取る
                        'date' : list(ft_list[i].keys())[0].isoformat(),
                        #timeZoneはユーザーカレンダー側に設定してあればそちらを見る
                        #'timeZone' : 'Japan'   
                    },
                    'end':{
                        'date' : list(ft_list[i].keys())[0].isoformat(),
                        #'timeZone' : 'Japan'
                    },
                    'allDayEvent' : True,
                    'singleEvents' : True,
                    'colorId' : 5     
                }
                #event = self.service.events().insert(calendarId=calendar_id,body=plan).execute()
                event = gcal.gapi_events_insert(calendar_id,plan)

                #gapiのレスポンスボディが空でない場合
                if event:
                    #レスポンスボディにerror情報がある場合
                    if list(event.keys())[0] == 'error':
                        gapi_error_code = event['error']['code']
                        gapi_error_msg = event['error']['message']
                        resp = 'idx:{} gapi_error_code:{} gapi_error_msg:{}'.format(i,gapi_error_code,gapi_error_msg)
                        break
                    #レスポンスボディにerror情報が無い場合
                    resp = "Googleカレンダーに運勢を書き込みました"
                #gapiのレスポンスボディが空の場合（HTTPエラー）
                else:
                    resp = "GAPI HTTP Error"
                    break

        return resp


    #本命宿ごとのGoogleカレンダーの予定を削除する
    def delete_events(self,honsyuku,y_from,m_from,y_to,m_to):
        
        #本命宿に応じたカレンダーIDを取得
        #calendar_id = self.CALENDAR_IDS[honsyuku]
        calendar_id = self.CALENDAR_IDS['尾']

        gcal = GCalendar()

        #UTC時間をISOフォーマットで指定する（故に9時間引く） 
        #dateでなくdatetime（時間付き）でないと、gapiからの戻りがBad Request errorとなる
        #指定された年月の月初日
        time_from = (datetime(y_from,m_from,1,hour=0, minute=0, second=0, microsecond=0)-timedelta(hours=9)).isoformat()+'Z'
        #指定された年月の月末日
        time_to = ((datetime(y_to,m_to,1,hour=0, minute=0, second=0, microsecond=0)+relativedelta(months=1)-timedelta(days=1))-timedelta(hours=9)).isoformat()+'Z'

        # print(time_from)
        # print(time_to)

        event_list = gcal.gapi_events_list(calendar_id,time_from,time_to,500,True)
        print(len(event_list['items']))

        #取得された予定が1件以上ある場合、それらを削除
        if len(event_list['items']):
            i=0
            for i in range(len(event_list['items'])):
                event_id = event_list['items'][i]['id']
                result = gcal.gapi_events_delete(calendar_id,event_id)

                #レスポンスボディが空の場合
                if result == '':
                    resp = "Googleカレンダーの予定を削除しました"
                #レスポンスボディにerror情報がある場合
                elif list(result.keys())[0] == 'error':
                    gapi_error_code = result['error']['code']
                    gapi_error_msg = result['error']['message']
                    resp = 'idx:{} gapi_error_code:{} gapi_error_msg:{}'.format(i,gapi_error_code,gapi_error_msg)
                    break
        else:
            resp = '削除する予定が存在しないか、または他のエラーです'
        
        return resp

    




 

        


    

