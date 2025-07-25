#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog
import logging
import os
import sys
from pathlib import Path

# 导入自定义模块
from modules.data_manager import DataManager
from modules.data_extractor import extract_schema, extract_data, extract_filters
from modules.filter_processor import apply_filters
from modules.output_generator import export_to_xlsx
from modules.config import Config
from clean_output import clean_output_directory

def setup_logging(config):
    """
    设置日志系统
    
    Args:
        config: 配置对象
    """
    log_config = config.get('logging')
    log_level = getattr(logging, log_config.get('level', 'INFO'))
    log_format = log_config.get('format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file = log_config.get('file', 'app.log')
    
    # 配置日志
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), log_file)),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def select_excel_file() -> str:
    """
    打开文件选择对话框，让用户选择Excel文件
    
    Returns:
        str: 选择的文件路径
    """
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="选择 Excel 文件",
        filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")]
    )
    if not file_path:
        logging.error("未选择文件，程序终止")
        exit(1)
    return file_path

def main() -> None:
    """主程序入口，协调整个数据处理流程"""
    # 加载配置
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    config = Config(config_path)
    
    # 设置日志
    logger = setup_logging(config)
    
    try:
        # 清理上次运行的结果
        logger.info("清理上次运行的结果...")
        clean_output_directory()
        
        # 初始化数据管理器
        data_manager = DataManager()
        data_manager.set_output_dir(os.path.dirname(os.path.abspath(__file__)))
        
        # 获取命令行参数
        if len(sys.argv) > 1:
            input_xlsx = sys.argv[1]
        else:
            input_xlsx = select_excel_file()
        
        logger.info("=== 开始处理 XLSX 文件 ===")
        
        # 检查输入文件是否存在
        if not Path(input_xlsx).exists():
            logger.error(f"输入文件不存在: {input_xlsx}")
            return
        
        # 执行流程
        extract_schema(input_xlsx, data_manager)
        extract_data(input_xlsx, data_manager)
        extract_filters(input_xlsx, data_manager)
        apply_filters(data_manager)
        output_path = export_to_xlsx(input_xlsx, data_manager)
        
        logger.info(f"=== 处理完成，结果保存在: {output_path} ===")
        
    except FileNotFoundError as e:
        logger.error(f"文件错误: {str(e)}")
        print(f"错误: {str(e)}")
    except ValueError as e:
        logger.error(f"数据错误: {str(e)}")
        print(f"错误: {str(e)}")
    except Exception as e:
        logger.error(f"处理过程中发生错误: {str(e)}", exc_info=True)
        print(f"发生未预期的错误: {str(e)}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        logging.info("程序被用户中断")
    except Exception as e:
        logging.critical(f"程序发生严重错误: {str(e)}", exc_info=True)
        print(f"程序发生严重错误: {str(e)}")
    finally:
        # 程序结束时不清理日志文件，因为可能需要查看日志
        pass