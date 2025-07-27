#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
import sys
from pathlib import Path

# 检查是否有命令行参数
has_cmd_args = len(sys.argv) > 1

# 只有在没有命令行参数时才尝试导入 tkinter
if not has_cmd_args:
    try:
        import tkinter as tk
        from tkinter import filedialog
        GUI_AVAILABLE = True
    except ImportError:
        GUI_AVAILABLE = False
        tk = None
        filedialog = None
else:
    # 有命令行参数时不需要 tkinter
    GUI_AVAILABLE = False
    tk = None
    filedialog = None

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
    if not GUI_AVAILABLE:
        print("错误: GUI 模式不可用")
        print("使用默认测试文件: templates/全维度筛选.xlsx")
        return "templates/全维度筛选.xlsx"
        
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
    # 记录启动时间
    import time
    start_time = time.time()
    print(f"程序启动... [时间: {time.strftime('%H:%M:%S', time.localtime())}]")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"脚本目录: {os.path.dirname(os.path.abspath(__file__))}")
    
    # 加载配置
    import time
    print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 开始加载配置...")
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.yaml")
    print(f"配置文件路径: {config_path}")
    print(f"配置文件是否存在: {os.path.exists(config_path)}")
    
    try:
        config = Config(config_path)
        print("配置加载成功")
    except Exception as e:
        print(f"配置加载失败: {str(e)}")
        return
    
    # 设置日志
    try:
        logger = setup_logging(config)
        print("日志设置成功")
    except Exception as e:
        print(f"日志设置失败: {str(e)}")
        return
    
    try:
        import time
        # 清理上次运行的结果
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 开始清理上次运行的结果...")
        logger.info("清理上次运行的结果...")
        clean_output_directory()
        
        # 初始化数据管理器
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 开始初始化数据管理器...")
        data_manager = DataManager()
        # 设置输出目录为项目根目录下的outputs目录，而不是src目录
        data_manager.set_output_dir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # 获取命令行参数
        import time
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 开始获取输入文件...")
        if len(sys.argv) > 1:
            input_xlsx = sys.argv[1]
            print(f"使用命令行参数指定的文件: {input_xlsx}")
        else:
            print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 开始选择文件对话框...")
            input_xlsx = select_excel_file()
            print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 文件选择完成: {input_xlsx}")
        
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] === 开始处理 XLSX 文件 ===")
        logger.info("=== 开始处理 XLSX 文件 ===")
        
        # 检查输入文件是否存在
        if not Path(input_xlsx).exists():
            logger.error(f"输入文件不存在: {input_xlsx}")
            return
        
        # 执行流程
        import time
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 1. 提取表结构...")
        extract_schema(input_xlsx, data_manager)
        
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 2. 提取数据总表...")
        extract_data(input_xlsx, data_manager)
        
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 3. 提取筛选条件...")
        extract_filters(input_xlsx, data_manager)
        
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 4. 应用筛选条件...")
        apply_filters(data_manager)
        
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 5. 导出结果到 XLSX...")
        output_path = export_to_xlsx(input_xlsx, data_manager)
        
        # 获取绝对路径，确保用户能找到输出文件
        import time
        abs_output_path = os.path.abspath(output_path)
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] === 处理完成，结果保存在: {abs_output_path} ===")
        logger.info(f"=== 处理完成，结果保存在: {abs_output_path} ===")
        
        # 如果输出路径包含临时目录，提示用户并复制到更合适的位置
        if "/var/folders/" in abs_output_path or "/tmp/" in abs_output_path:
            print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 开始复制文件到永久位置...")
            import shutil
            
            # 尝试以下位置（按优先级排序）：
            # 1. 被处理文件所在的目录
            # 2. 工具（二进制文件）所在的目录
            # 3. 当前工作目录
            
            # 获取被处理文件所在的目录
            input_file_dir = os.path.dirname(os.path.abspath(input_xlsx))
            input_file_output_path = os.path.join(input_file_dir, "outputs", os.path.basename(output_path))
            
            # 获取工具所在的目录
            tool_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            tool_output_path = os.path.join(tool_dir, "outputs", os.path.basename(output_path))
            
            # 获取当前工作目录
            cwd_output_path = os.path.join(os.getcwd(), "outputs", os.path.basename(output_path))
            
            # 按优先级尝试复制
            target_paths = [
                (input_file_dir, input_file_output_path, "被处理文件所在目录"),
                (tool_dir, tool_output_path, "工具所在目录"),
                (os.getcwd(), cwd_output_path, "当前工作目录")
            ]
            
            copied = False
            for base_dir, target_path, location_desc in target_paths:
                try:
                    # 创建输出目录
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    # 复制文件
                    shutil.copy2(abs_output_path, target_path)
                    print(f"已自动复制结果文件到{location_desc}: {target_path}")
                    copied = True
                    break
                except Exception as e:
                    print(f"无法复制到{location_desc}，尝试下一个位置: {str(e)}")
            
            if not copied:
                print(f"警告: 无法复制结果文件到任何可访问的位置，原始文件保留在: {abs_output_path}")
        
        # 强制退出程序，确保所有线程都被终止
        import time
        print(f"[时间: {time.strftime('%H:%M:%S', time.localtime())}] 程序执行完成，准备退出...")
        import os
        os._exit(0)
        
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
        # 强制退出程序，确保所有线程都被终止
        import os
        os._exit(0)
