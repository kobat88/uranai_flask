import unittest
#import sys
#import os
#sys.path.append(os.path.abspath("...")) #c:\Users\kobat88\Desktop\uranai_flask\test.pthにパス定義した
from models.doubutsu_uranai import DoubutsuUranai

class DoubutsuUranaiTest(unittest.TestCase):

    #各テストメソッド実行前に呼ばれる
    def setUp(self):
        self.db = DoubutsuUranai()
    
    #各テストメソッド実行後に呼ばれる
    def tearDown(self):
        del self.db

    def test_get_doubutsu(self):
        #db = DoubutsuUranai()
        self.assertEqual(self.db.get_doubutsu(1921,1,1),"1.イエローのチーター")
        self.assertEqual(self.db.get_doubutsu(1921,1,13),"13.レッドのオオカミ")
        self.assertEqual(self.db.get_doubutsu(1921,3,13),"12.グリーンのゾウ")
        self.assertEqual(self.db.get_doubutsu(1974,10,18),"29.ブルーのヒツジ")
        self.assertEqual(self.db.get_doubutsu(2000,2,29),"54.オレンジのトラ")
        self.assertEqual(self.db.get_doubutsu(2021,12,31),"50.パープルのクロヒョウ")
        self.assertEqual(self.db.get_doubutsu(2022,12,31),"55.ブラウンのトラ")
        self.assertEqual(self.db.get_doubutsu(1920,12,31),"60.パープルのトラ")
        self.assertEqual(self.db.get_doubutsu(1900,1,1),"11.イエローのコジカ")

    def test_get_doubutsu_err(self):
        #db = DoubutsuUranai()
        with self.assertRaises(ValueError):
            self.db.get_doubutsu(2021,12,50)

    def test_get_doubutsu_err2(self):
        #db = DoubutsuUranai()
        with self.assertRaises(TypeError):
            self.db.get_doubutsu(2021,12,'23')

if __name__ == '__main__':
    unittest.main()