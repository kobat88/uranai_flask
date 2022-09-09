import unittest
from unittest import mock
from models.syukuyo_calendar import SyukuyoCalendar
from models.g_calendar import GCalendar

class SyukuyoCalendarTest(unittest.TestCase):

    #各テストメソッド実行前に呼ばれる
    def setUp(self):
        self.cal = SyukuyoCalendar()
    
    #各テストメソッド実行後に呼ばれる
    def tearDown(self):
        del self.cal

    @mock.patch('models.g_calendar.GCalendar.gapi_events_insert')
    def test_create_events_gapi_http_error(self,mock):
        mock.return_value = ''
        
        self.assertEqual(self.cal.create_events("尾",2022,9,2022,9),"GAPI HTTP Error")

    @mock.patch('models.g_calendar.GCalendar.gapi_events_insert')
    def test_create_events_gapi_error(self,mock):
        mock.return_value = {
            "error": {
                "errors": [
                    {
                        "domain": "calendar",
                        "reason": "timeRangeEmpty",
                        "message": "The specified time range is empty.",
                        "locationType": "parameter",
                        "location": "timeMax",
                    }
                ],
                "code": 400,
                "message": "The specified time range is empty."
            }
        }

        self.assertEqual(self.cal.create_events("尾",2022,9,2022,9),"idx:0 gapi_error_code:400 gapi_error_msg:The specified time range is empty.")
    

if __name__ == '__main__':
    unittest.main()