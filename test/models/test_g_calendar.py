import unittest
from unittest import mock
from models.g_calendar import GCalendar
from models.syukuyo import Syukuyo

class GCalendarTest(unittest.TestCase):

    #各テストメソッド実行前に呼ばれる
    def setUp(self):
        self.cal = GCalendar()
    
    #各テストメソッド実行後に呼ばれる
    def tearDown(self):
        del self.cal

    @mock.patch('models.g_calendar.GCalendar.gapi_events_insert')
    def test_create_events_gapi_http_error(self,mock):
        mock.return_value = ''
        #本来はSyukuyoもmockにすべき？だが、ft_listを手作りするのが面倒なためUnittest済の実物を呼ぶ
        syukuyo = Syukuyo()
        ft_list = syukuyo.get_fortune('尾',1)
        
        self.assertEqual(self.cal.create_events(ft_list,'尾'),"GAPI HTTP error")

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
        syukuyo = Syukuyo()
        ft_list = syukuyo.get_fortune('尾',1)

        self.assertEqual(self.cal.create_events(ft_list,'尾'),"idx:0 gapi_error_code:400 gapi_error_msg:The specified time range is empty.")
    


if __name__ == '__main__':
    unittest.main()