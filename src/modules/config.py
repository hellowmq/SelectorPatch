#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import yaml
import logging
from pathlib import Path

class Config:
    """配置管理类，用于管理应用程序配置"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        "sheets": {
            "data_sheet": "总表",
            "filter_sheet": "总表筛选"
        },
        "output": {
            "directory": "outputs",
            "condition_prefix": "条件_"
        },
        "logging": {
            "level": "INFO",
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "file": "app.log"
        }
    }
    
    def __init__(self, config_file=None):
        """
        初始化配置
        
        Args:
            config_file: 配置文件路径，如果为None则使用默认配置
        """
        self.config = self.DEFAULT_CONFIG.copy()
        self.config_file = config_file
        
        if config_file and os.path.exists(config_file):
            self._load_config()
    
    def _load_config(self):
        """从配置文件加载配置"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                
            # 合并配置
            if user_config:
                self._merge_config(self.config, user_config)
        except Exception as e:
            logging.error(f"加载配置文件失败: {str(e)}")
    
    def _merge_config(self, default_config, user_config):
        """递归合并配置"""
        for key, value in user_config.items():
            if key in default_config and isinstance(value, dict) and isinstance(default_config[key], dict):
                self._merge_config(default_config[key], value)
            else:
                default_config[key] = value
    
    def get(self, section, key=None, default=None):
        """
        获取配置值
        
        Args:
            section: 配置节
            key: 配置键，如果为None则返回整个节
            default: 默认值，如果配置不存在则返回此值
            
        Returns:
            配置值
        """
        if section not in self.config:
            return default
            
        if key is None:
            return self.config[section]
            
        return self.config[section].get(key, default)
    
    def set(self, section, key, value):
        """
        设置配置值
        
        Args:
            section: 配置节
            key: 配置键
            value: 配置值
        """
        if section not in self.config:
            self.config[section] = {}
            
        self.config[section][key] = value
    
    def save(self, config_file=None):
        """
        保存配置到文件
        
        Args:
            config_file: 配置文件路径，如果为None则使用初始化时的路径
        """
        save_path = config_file or self.config_file
        
        if not save_path:
            logging.warning("未指定配置文件路径，无法保存配置")
            return
            
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
                
            logging.info(f"配置已保存到: {save_path}")
        except Exception as e:
            logging.error(f"保存配置文件失败: {str(e)}")
    
    @staticmethod
    def create_default_config(config_file):
        """
        创建默认配置文件
        
        Args:
            config_file: 配置文件路径
        """
        config = Config()
        config.save(config_file)
        return config