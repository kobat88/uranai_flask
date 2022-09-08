import datetime 
import json
import googleapiclient.discovery
import google.auth

class GCalendar:

    #CALENDER_ID = 'elq5368slgqd7fudhp3106nr88@group.calendar.google.com'
    #本宿ごとのカレンダーを用意する
    CALENDAR_IDS = {
            '尾' : 'elq5368slgqd7fudhp3106nr88@group.calendar.google.com'
        }
    #Googleの認証情報ファイルパス　相対パス指定だとうまくいかない
    CRED_FILE_PATH = 'C:\\Users\\kobat88\\Desktop\\uranai_flask\\json\\turnkey-aleph-343401-a0a6dd2b750d.json'
    SCOPES = ['https://www.googleapis.com/auth/calendar']


    def __init__(self):
        #Google APIの準備
        gapi_creds = google.auth.load_credentials_from_file(self.CRED_FILE_PATH,self.SCOPES)[0]
        #APIと対話するためのResourceオブジェクトを構築する
        self.service = googleapiclient.discovery.build('calendar','v3',credentials=gapi_creds)


    #本宿ごとのカレンダーに運勢リストを予定として書き込む
    def create_events(self,plan_list,honsyuku):
        """
        Args:
            plan_list: {日付(datetime.date):予定名(str)}形式の要素が入ったリスト
        """
        #本宿ごとのカレンダーIDを取得
        calendar_id = self.CALENDAR_IDS['尾']

        for i in range(len(plan_list)):
            plan = {
                'summary':list(plan_list[i].values())[0],
                'start':{
                    #Googleカレンダーは日時をISOフォーマットで受け取る
                    'date' : list(plan_list[i].keys())[0].isoformat(),
                    #'timeZone':'Japan'
                },
                'end':{
                    'date' : list(plan_list[i].keys())[0].isoformat(),
                    #'timeZone':'Japan'
                },
                'allDayEvent':True,
                'singleEvents':True,
                'colorId':5     #予定の色を指定
            }
            #event = self.service.events().insert(calendarId=calendar_id,body=plan).execute()
            #Unittestでmockにするため、Google API呼び出しは別メソッドにする
            event = self.gapi_events_insert(calendar_id,plan)

            #gapiのレスポンスボディが空でない場合
            if event:
                #レスポンスボディにerror情報がある場合
                if list(event.keys())[0] == 'error':
                    gapi_error_code = event['error']['code']
                    gapi_error_msg = event['error']['message']
                    resp = 'idx:{} gapi_error_code:{} gapi_error_msg:{}'.format(i,gapi_error_code,gapi_error_msg)
                    break
                #レスポンスボディにerror情報が無い場合
                resp = 'success'
            #gapiのレスポンスボディが空の場合（HTTPエラー）
            else:
                resp = "GAPI HTTP error"
                break

        return resp


    #本宿ごとのカレンダーの予定を削除する
    def delete_events(self,honsyuku):
        
        #本宿ごとのカレンダーIDを取得
        calendar_id = self.CALENDAR_IDS['尾']

        #予定を削除する期間を指定
        TIME_FROM = '2022/08/31'
        TIME_TO = '2022/12/31'

        #UTC（協定世界時）で指定する
        # dt=datetime.datetime.utcnow().isoformat()+'Z' #nowの場合
        time_from = datetime.datetime.strptime(TIME_FROM, '%Y/%m/%d').isoformat()+'Z'
        time_to = datetime.datetime.strptime(TIME_TO, '%Y/%m/%d').isoformat()+'Z'
       
       #指定したカレンダーIDと期間の予定リストを取得
        # event_list = self.service.events().list(
        #     calendarId = calendar_id,
        #     timeMin = time_from,
        #     timeMax = time_to,
        #     maxResults=500,
        #     singleEvents=True   #これを指定しないと全ての予定が取れない
        # ).execute()
        #Unittestでmockにするため、Google API呼び出しは別メソッドにする
        event_list = self.gapi_events_list(calendar_id,time_from,time_to,500,True)
        print(len(event_list['items']))

        #取得された予定が1件以上ある場合、それらを削除
        if len(event_list['items']):
            i=0
            for i in range(len(event_list['items'])):
                event_id = event_list['items'][i]['id']
                # result = self.service.events().delete(
                #     calendarId = calendar_id,
                #     eventId = event_id
                # ).execute()
                #Unittestでmockにするため、Google API呼び出しは別メソッドにする
                result = self.gapi_events_delete(calendar_id,event_id)

                #レスポンスボディが空の場合
                if result == '':
                    resp = 'success'
                #レスポンスボディにerror情報がある場合
                elif list(result.keys())[0] == 'error':
                    gapi_error_code = result['error']['code']
                    gapi_error_msg = result['error']['message']
                    resp = 'idx:{} gapi_error_code:{} gapi_error_msg:{}'.format(i,gapi_error_code,gapi_error_msg)
                    break
        else:
            resp = '削除する予定が存在しないか、またはエラー'
        
        return resp

    #Google Calendar API wrapper 
    def gapi_events_insert(self,calendar_id,plan):
        event = self.service.events().insert(calendarId=calendar_id,body=plan).execute()
        return event

    #Google Calendar API wrapper 
    def gapi_events_list(self,calendar_id,time_from,time_to,max_results,single_events):
        event_list = self.service.events().list( 
            calendarId = calendar_id, 
            timeMin = time_from, 
            timeMax = time_to, 
            maxResults = max_results, 
            singleEvents = single_events  #これを指定しないと全ての予定が取れない（省略値はFalse）\
        ).execute()
        return event_list

    #Google Calendar API wrapper 
    def gapi_events_delete(self,calendar_id,event_id):
        result = self.service.events().delete(calendarId = calendar_id,eventId = event_id).execute()
        return result




 

        


    

