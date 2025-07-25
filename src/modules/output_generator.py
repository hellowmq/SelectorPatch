#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pandas as pd
from .data_manager import DataManager

def export_to_xlsx(input_file: str, data_mgr: DataManager) -> str:
    """
    生成新的 XLSX 文件，包含总表、总表筛选和每个筛选条件的结果。
    
    Args:
        input_file (str): 输入文件路径，用于确定输出文件的保存位置
        data_mgr (DataManager): 数据管理器实例
        
    Returns:
        str: 生成的XLSX文件路径
    
    Raises:
        ValueError: 如果数据未加载。
    """
    try:
        # 检查数据是否已加载
        if not data_mgr.data_store or not data_mgr.filter_store:
            raise ValueError("数据未加载，请先提取数据和筛选条件")
        
        # 生成输出文件名
        input_filename = os.path.splitext(os.path.basename(input_file))[0]
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"{input_filename}_筛选结果_{timestamp}.xlsx"
        
        # 确保输出路径存在
        output_path = os.path.join(data_mgr.output_dir, output_filename)
        
        # 读取源文件表头
        source_df = pd.read_excel(input_file, sheet_name="总表")
        export_column_header = source_df.iloc[:, 0].tolist()  # 转换为列表
        
        # 使用 ExcelWriter 写入多个Sheet
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            # 写入总表
            if data_mgr.data_store:
                df_total = pd.DataFrame(data_mgr.data_store)
                # 转置数据
                df_total = df_total.T
                # 插入原始的第一列数据作为新列
                df_total.insert(0, "原始第一列", export_column_header)
                df_total.to_excel(writer, sheet_name="总表", header=False, index=False)
            
            # 写入总表筛选
            if data_mgr.filter_store:
                df_filters = pd.DataFrame(data_mgr.filter_store)
                df_filters.to_excel(writer, sheet_name="总表筛选", index=False)
            
            # 写入每个筛选条件的结果
            for idx, filter_item in enumerate(data_mgr.filter_store):
                condition_name = f"条件_{idx + 1}"
                if condition_name in data_mgr.filtered_data and data_mgr.filtered_data[condition_name]:
                    df_filtered = pd.DataFrame(data_mgr.filtered_data[condition_name])
                    # 转置数据
                    df_filtered = df_filtered.T
                    
                    # 简化工作表名称：只使用筛选值的序列作为标识
                    value_sequence = '_'.join([str(v) for v in filter_item.values() if v != ''])
                    if not value_sequence:
                        value_sequence = "空值"
                    
                    # 确保工作表名称不超过31个字符（Excel限制）
                    sheet_name = f"{condition_name}_{value_sequence}"
                    if len(sheet_name) > 31:
                        sheet_name = sheet_name[:31]
                    
                    df_filtered.to_excel(writer, sheet_name=sheet_name, index=True)
        
        data_mgr.logger.info(f"成功生成XLSX文件: {output_path}")
        return output_path
    except Exception as e:
        data_mgr.logger.error(f"生成XLSX文件时发生错误: {str(e)}")
        raise