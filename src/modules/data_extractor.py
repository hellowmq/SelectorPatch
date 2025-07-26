#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from .data_manager import DataManager

def extract_schema(input_file: str, data_mgr: DataManager) -> None:
    """
    提取表结构（保留为未来版本扩展）
    
    Args:
        input_file (str): 输入文件路径
        data_mgr (DataManager): 数据管理器实例
    """
    data_mgr.logger.info(f"表结构提取功能预留: {input_file}")


def extract_data(input_file: str, data_mgr: DataManager) -> None:
    """
    从输入文件中提取数据总表

    Args:
        input_file (str): 输入文件路径，应为 XLSX 格式
        data_mgr (DataManager): 数据管理器实例

    Returns:
        None: 无返回值，但会将提取的数据存储在数据管理器中

    Raises:
        FileNotFoundError: 如果输入文件不存在
        ValueError: 如果 XLSX 文件中不存在名为 "总表" 的 Sheet
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    
    try:
        # 检查Sheet是否存在
        excel_file = pd.ExcelFile(input_file)
        if "总表" not in excel_file.sheet_names:
            data_mgr.logger.error(f"输入文件缺少 '总表' Sheet，现有Sheet: {excel_file.sheet_names}")
            return
        
        # 读取数据并打印原始样例
        df = pd.read_excel(input_file, sheet_name="总表")
        data_mgr.logger.debug(f"原始数据前3行:\n{df.head(3).to_string()}")
        
        # 保存总表到 CSV 文件
        output_path = os.path.join(data_mgr.output_dir, "总表.csv")
        df.to_csv(output_path, index=False)
        data_mgr.logger.info(f"已将总表保存到 {output_path}")
        
        # 转置数据，将第一列作为表头
        df = df.T
        df.columns = df.iloc[0]
        df = df[1:]
        
        # 提取数据并转换为字典列表
        data_mgr.data_store = df.to_dict(orient="records")
        
        data_mgr.logger.info(f"成功加载 {len(data_mgr.data_store)} 条数据，首条样例: {data_mgr.data_store[0] if data_mgr.data_store else {}}")
        data_mgr.logger.info(f"成功提取数据总表，共 {len(data_mgr.data_store)} 条记录")
    except ValueError as e:
        raise ValueError(f"XLSX 文件中不存在名为 '总表' 的 Sheet: {input_file}") from e
    except Exception as e:
        data_mgr.logger.error(f"提取数据时发生错误: {str(e)}")
        raise


def extract_filters(input_file: str, data_mgr: DataManager) -> None:
    """
    从输入文件中提取筛选标签

    Args:
        input_file (str): 输入文件路径，应为 XLSX 格式
        data_mgr (DataManager): 数据管理器实例

    Returns:
        None: 无返回值，但会将提取的筛选标签存储在数据管理器中

    Raises:
        FileNotFoundError: 如果输入文件不存在
        ValueError: 如果 XLSX 文件中不存在名为 "总表筛选" 的 Sheet
    """
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    
    try:
        # 读取筛选标签表，将所有列作为字符串处理
        # 注意：dtype=str 确保所有值被读取为字符串，但不会处理空值
        df = pd.read_excel(input_file, sheet_name="总表筛选", dtype=str)
        
        # 处理空值：将 NaN 转换为空字符串
        # 即使指定了 dtype=str，空单元格仍会被读取为 NaN
        df = df.fillna('')
        data_mgr.filter_store = df.to_dict(orient="records")
        data_mgr.logger.info(f"成功提取筛选标签，共 {len(data_mgr.filter_store)} 条记录")
        
        # 添加 condition_group 列
        filter_df = pd.DataFrame(data_mgr.filter_store)
        filter_df['condition_group'] = [f"条件_{i+1}" for i in range(len(filter_df))]
        
        filter_output_path = os.path.join(data_mgr.output_dir, "filter_conditions.csv")
        filter_df.to_csv(filter_output_path, index=False, encoding='utf-8-sig')
        data_mgr.logger.info(f"已将筛选条件保存到 {filter_output_path}")
    except ValueError as e:
        raise ValueError(f"XLSX 文件中不存在名为 '总表筛选' 的 Sheet: {input_file}") from e
    except Exception as e:
        data_mgr.logger.error(f"提取筛选条件时发生错误: {str(e)}")
        raise