#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import os
import tempfile
import sys

# 尝试导入Config，如果失败则跳过测试
try:
    from modules.config import Config
    SKIP_CONFIG_TESTS = False
except ImportError:
    SKIP_CONFIG_TESTS = True
    print("警告: 无法导入Config模块，相关测试将被跳过")

@unittest.skipIf(SKIP_CONFIG_TESTS, "Config模块不可用")
class TestConfig(unittest.TestCase):
    """配置模块测试类"""
    
    def setUp(self):
        """测试前准备"""
        if SKIP_CONFIG_TESTS:
            self.skipTest("Config模块不可用")
        # 创建临时配置文件
        self.temp_dir = tempfile.TemporaryDirectory()
        self.config_file = os.path.join(self.temp_dir.name, "test_config.yaml")
    
    def tearDown(self):
        """测试后清理"""
        if hasattr(self, 'temp_dir'):
            # 删除临时目录
            self.temp_dir.cleanup()
    
    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        self.assertEqual(config.get("sheets", "data_sheet"), "总表")
        self.assertEqual(config.get("sheets", "filter_sheet"), "总表筛选")
        self.assertEqual(config.get("output", "directory"), "outputs")
        self.assertEqual(config.get("output", "condition_prefix"), "条件_")
    
    def test_save_and_load_config(self):
        """测试保存和加载配置"""
        # 创建并保存配置
        config1 = Config()
        config1.set("test", "key", "value")
        config1.save(self.config_file)
        
        # 加载配置
        config2 = Config(self.config_file)
        self.assertEqual(config2.get("test", "key"), "value")
    
    def test_merge_config(self):
        """测试配置合并"""
        # 创建默认配置
        config = Config()
        
        # 修改配置
        config.set("sheets", "data_sheet", "新总表")
        config.set("new_section", "new_key", "new_value")
        
        # 验证修改
        self.assertEqual(config.get("sheets", "data_sheet"), "新总表")
        self.assertEqual(config.get("sheets", "filter_sheet"), "总表筛选")  # 未修改的保持默认值
        self.assertEqual(config.get("new_section", "new_key"), "new_value")

if __name__ == "__main__":
    unittest.main()