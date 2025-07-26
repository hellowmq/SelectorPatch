#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os

class DataManager:
    """数据管理类，用于管理数据状态和配置"""
    
    def __init__(self):
        self.data_store = []
        self.filter_store = []
        self.filtered_data = {}
        self.output_dir = None
        self.logger = logging.getLogger(__name__)
    
    def set_output_dir(self, base_path: str):
        """设置输出目录"""
        self.output_dir = os.path.join(base_path, "outputs")
        os.makedirs(self.output_dir, exist_ok=True)
    
    def clear_data(self):
        """清理所有数据"""
        self.data_store.clear()
        self.filter_store.clear()
        self.filtered_data.clear()