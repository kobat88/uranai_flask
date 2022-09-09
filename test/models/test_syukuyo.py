import unittest
from datetime import datetime, date 
from models.syukuyo import Syukuyo

class SyukuyoTest(unittest.TestCase):

    #各テストメソッド実行前に呼ばれる
    def setUp(self):
        self.syukuyo = Syukuyo()
    
    #各テストメソッド実行後に呼ばれる
    def tearDown(self):
        del self.syukuyo

    def test_get_honsyuku(self):
        self.assertEqual(self.syukuyo.get_honsyuku(1930,1,1),"危")
        self.assertEqual(self.syukuyo.get_honsyuku(2000,2,29),"女")
        self.assertEqual(self.syukuyo.get_honsyuku(2021,12,31),"斗")
        self.assertEqual(self.syukuyo.get_honsyuku(2022,12,31),"畢")

    def test_get_honsyuku_err(self):
        with self.assertRaises(ValueError):
            self.syukuyo.get_honsyuku(2021,12,50)

    def test_get_honsyuku_err2(self):
        with self.assertRaises(TypeError):
            self.syukuyo.get_honsyuku(2021,12,"23")

    def test_get_fortune_count(self):
        self.assertEqual(len(self.syukuyo.get_fortune("尾",2022,9,2022,9)),30)

    def test_get_fortune_ryohan(self):
        self.assertIn({date(2023,1,10):"【凌】危"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,1,9):"(再)安"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,1,18):"意"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,1,21):"【凌】壊"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,1,22):"(活)壊"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,2,21):"事"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,2,24):"克"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,2,27):"聚"},self.syukuyo.get_fortune("尾",2023,1,2023,3))
        self.assertIn({date(2023,3,3):"同"},self.syukuyo.get_fortune("尾",2023,1,2023,3))

    def test_get_fortune_err(self):
        with self.assertRaises(ValueError):
            self.syukuyo.get_fortune("あ",2022,9,2022,9)

    def test_get_fortune_err2(self):
        with self.assertRaises(ValueError):
            self.syukuyo.get_fortune("",2022,9,2022,9)

if __name__ == '__main__':
    unittest.main()

