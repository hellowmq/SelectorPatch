#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import pandas as pd
import os
from .data_manager import DataManager

def _match_data_item(data_item: dict, filter_item: dict) -> tuple[bool, list]:
    """
    检查数据项是否匹配筛选条件
    
    Args:
        data_item: 单个数据项
        filter_item: 筛选条件
        
    Returns:
        tuple: (是否匹配, 不匹配字段列表)
    """
    match = True
    mismatch_fields = []
    
    for field, value in filter_item.items():
        # 获取数据项中的字段值
        data_value = data_item.get(field)
        
        # 如果筛选条件值为空，视为通配符（匹配任何值）
        if value == '':
            continue  # 跳过这个条件，匹配任何值
        
        # 如果数据项中的字段值为空，但筛选条件值不为空，则不匹配
        if pd.isna(data_value) or data_value == '':
            match = False
            mismatch_fields.append(f"{field}(期望:{value},实际:空值)")
            break
        
        # 比较值（字符串比较）
        if str(data_value) != str(value):
            match = False
            mismatch_fields.append(f"{field}(期望:{value},实际:{data_value})")
            break
            
    return match, mismatch_fields


def _save_filtered_data_to_csv(filtered_items: list, filter_item: dict, 
                              condition_name: str, output_path: str, 
                              data_mgr: DataManager) -> None:
    """
    将筛选结果保存到CSV文件
    
    Args:
        filtered_items: 筛选后的数据项列表
        filter_item: 筛选条件
        condition_name: 条件名称
        output_path: 输出文件路径
        data_mgr: 数据管理器
    """
    with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
        # 写入UTF-8 BOM头确保Excel兼容
        f.write("\ufeff")
        # 写入筛选条件作为注释（确保不换行）
        f.write(f"# 筛选条件: {' '.join(f'{k}={v}' for k, v in filter_item.items())}\n")
        
        if filtered_items:
            # 创建 DataFrame 并直接写入
            df = pd.DataFrame(filtered_items)
            df.to_csv(f, index=False, encoding="utf-8-sig")
        else:
            # 即使没有数据也创建带表头的空文件
            if data_mgr.data_store:
                fieldnames = [f for f in data_mgr.data_store[0].keys() if f != '序号']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()


def apply_filters(data_mgr: DataManager) -> None:
    """
    应用筛选任务，根据筛选条件对数据进行筛选。
    每个筛选条件生成独立的筛选结果并输出到CSV文件。

    Args:
        data_mgr: 数据管理器实例

    Returns:
        None: 无返回值，但会将筛选结果存储在数据管理器中并输出到文件。

    Raises:
        ValueError: 如果数据未加载。
    """
    try:
        # 检查数据是否已加载
        if not data_mgr.data_store or not data_mgr.filter_store:
            raise ValueError("数据未加载，请先提取数据和筛选条件")
        
        # 初始化筛选结果字典
        data_mgr.filtered_data = {}
        
        # 为每个筛选条件生成独立的筛选结果和CSV文件
        for idx, filter_item in enumerate(data_mgr.filter_store):
            condition_name = f"条件_{idx + 1}"
            data_mgr.filtered_data[condition_name] = []
            
            # 执行筛选
            data_mgr.logger.debug(f"开始应用筛选条件 {condition_name}: {filter_item}")
            if not data_mgr.data_store:
                data_mgr.logger.warning("数据总表为空，请检查输入文件格式和Sheet名称")
                continue
                
            data_mgr.logger.info(f"成功加载 {len(data_mgr.data_store)} 条数据，首条样例: {data_mgr.data_store[0]}")
            
            # 筛选数据
            for data_item in data_mgr.data_store:
                match, mismatch_fields = _match_data_item(data_item, filter_item)
                
                if match:
                    data_mgr.filtered_data[condition_name].append(data_item)
                elif idx == 0:  # 只记录第一个条件的详细不匹配信息
                    data_mgr.logger.debug(f"数据不匹配: {condition_name} - {', '.join(mismatch_fields)}")
            
            data_mgr.logger.debug(f"筛选完成 {condition_name}: 匹配 {len(data_mgr.filtered_data[condition_name])} 条记录")
            
            # 输出到CSV
            output_path = os.path.join(data_mgr.output_dir, f"{condition_name}.csv")
            _save_filtered_data_to_csv(
                data_mgr.filtered_data[condition_name], 
                filter_item, 
                condition_name, 
                output_path, 
                data_mgr
            )
            
            data_mgr.logger.info(f"{condition_name} 筛选完成，共 {len(data_mgr.filtered_data[condition_name])} 条记录，已保存到 {output_path}")
    
    except Exception as e:
        data_mgr.logger.error(f"应用筛选条件时发生错误: {str(e)}")
        raise