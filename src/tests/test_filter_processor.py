#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
from modules.data_manager import DataManager
from modules.filter_processor import _match_data_item

class TestFilterProcessor(unittest.TestCase):
    """筛选处理器测试类"""
    
    def test_match_data_item_exact_match(self):
        """测试精确匹配"""
        data_item = {"年份": 2024, "品类": "A", "Value1": 100}
        filter_item = {"年份": 2024, "品类": "A"}
        
        match, _ = _match_data_item(data_item, filter_item)
        self.assertTrue(match)
    
    def test_match_data_item_no_match(self):
        """测试不匹配"""
        data_item = {"年份": 2024, "品类": "A", "Value1": 100}
        filter_item = {"年份": 2024, "品类": "B"}
        
        match, mismatch_fields = _match_data_item(data_item, filter_item)
        self.assertFalse(match)
        self.assertEqual(len(mismatch_fields), 1)
    
    def test_match_data_item_empty_filter(self):
        """测试空筛选条件（通配符）"""
        data_item = {"年份": 2024, "品类": "A", "Value1": 100}
        filter_item = {"年份": 2024, "品类": ""}
        
        match, _ = _match_data_item(data_item, filter_item)
        self.assertTrue(match)
    
    def test_match_data_item_empty_data(self):
        """测试数据项为空但筛选条件不为空"""
        data_item = {"年份": 2024, "品类": "", "Value1": 100}
        filter_item = {"年份": 2024, "品类": "A"}
        
        match, mismatch_fields = _match_data_item(data_item, filter_item)
        self.assertFalse(match)
        self.assertEqual(len(mismatch_fields), 1)

if __name__ == "__main__":
    unittest.main()