#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import logging
from pathlib import Path

# 获取日志记录器但不配置 basicConfig，避免覆盖主程序的日志配置
logger = logging.getLogger('clean_output')
# 添加 NullHandler 防止未配置日志时的警告
logger.addHandler(logging.NullHandler())

def clean_output_directory():
    """
    清理 output 目录中的所有文件
    如果目录不存在则创建它
    同时清理项目根目录下的 app.log 文件
    """
    # 获取 output 目录的路径（相对于脚本所在目录的上一级）
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    
    # 确保路径是绝对路径
    output_dir = os.path.abspath(output_dir)
    
    logger.info(f"清理输出目录: {output_dir}")
    
    # 检查目录是否存在
    if os.path.exists(output_dir):
        # 如果存在，删除目录中的所有文件和子目录
        for item in os.listdir(output_dir):
            item_path = os.path.join(output_dir, item)
            try:
                if os.path.isfile(item_path):
                    os.unlink(item_path)
                    logger.debug(f"已删除文件: {item}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    logger.debug(f"已删除目录: {item}")
            except Exception as e:
                logger.error(f"删除 {item_path} 时出错: {e}")
        logger.info("输出目录已清理完成")
    else:
        # 如果目录不存在，创建它
        os.makedirs(output_dir)
        logger.info(f"输出目录不存在，已创建: {output_dir}")
    
    # 不再删除项目根目录下的 app.log 文件，因为它正在被主程序使用
    # 如果需要清理旧日志，应该在日志系统初始化前进行，或者使用日志轮转机制
    logger.info("日志文件保留，不进行清理")

if __name__ == "__main__":
    clean_output_directory()