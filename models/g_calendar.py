import googleapiclient.discovery
import google.auth

#Google Calendar APIをwrapするクラス
class GCalendar(object):

    #CALENDER_ID = 'elq5368slgqd7fudhp3106nr88@group.calendar.google.com'
    
    #Googleの認証情報ファイルパス　相対パス指定だとうまくいかない
    CRED_FILE_PATH = 'C:\\Users\\kobat88\\Desktop\\uranai_flask\\json\\turnkey-aleph-343401-a0a6dd2b750d.json'
    #認証スコープ
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        #Google APIの準備
        gapi_creds = google.auth.load_credentials_from_file(self.CRED_FILE_PATH,self.SCOPES)[0]
        #APIと対話するためのResourceオブジェクトを構築する
        self.service = googleapiclient.discovery.build('calendar','v3',credentials=gapi_creds)

    def gapi_events_insert(self,calendar_id,plan):
        event = self.service.events().insert(calendarId=calendar_id,body=plan).execute()
        return event

    def gapi_events_list(self,calendar_id,time_from,time_to,max_results,single_events):
        event_list = self.service.events().list( 
            calendarId = calendar_id, 
            timeMin = time_from, 
            timeMax = time_to, 
            maxResults = max_results, 
            singleEvents = single_events  #これを指定しないと全ての予定が取れない（省略値はFalse）
        ).execute()
        return event_list

    def gapi_events_delete(self,calendar_id,event_id):
        result = self.service.events().delete(calendarId = calendar_id,eventId = event_id).execute()
        return result




 

        


    

