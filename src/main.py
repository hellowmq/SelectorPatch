import csv
import logging
import os
import pandas as pd
from pathlib import Path
import glob
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 写死的输入文件路径
INPUT_XLSX = "mockdata.xlsx"


def extract_schema(input_file: str) -> None:
    """提取表结构（保留为未来版本扩展）"""
    logger.info(f"表结构提取功能预留: {input_file}")


def extract_data(input_file: str) -> None:
    """
    从输入文件中提取数据总表

    Args:
        input_file (str): 输入文件路径，应为 XLSX 格式

    Returns:
        None: 无返回值，但会将提取的数据存储在全局变量或类属性中

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
            logger.error(f"输入文件缺少 '总表' Sheet，现有Sheet: {excel_file.sheet_names}")
            return
        
        # 读取数据并打印原始样例
        df = pd.read_excel(input_file, sheet_name="总表")
        logger.debug(f"原始数据前3行:\n{df.head(3).to_string()}")

        # 保存总表到 CSV 文件
        os.makedirs("outputs", exist_ok=True)
        output_path = os.path.join("outputs", f"总表.csv")
        df.to_csv(output_path, index=False)
        
        # 转置数据，将第一列作为表头
        df = df.T
        df.columns = df.iloc[0]
        df = df[1:]
        
        # 提取数据并转换为字典列表
        global data_store
        data_store = df.to_dict(orient="records")
        
        logger.info(f"成功加载 {len(data_store)} 条数据，首条样例: {data_store[0] if data_store else {}}")
        logger.info(f"成功提取数据总表，共 {len(data_store)} 条记录")
    except ValueError as e:
        raise ValueError(f"XLSX 文件中不存在名为 '总表' 的 Sheet: {input_file}") from e


def extract_filters(input_file: str) -> None:
    """
    从输入文件中提取筛选标签

    Args:
        input_file (str): 输入文件路径，应为 XLSX 格式

    Returns:
        None: 无返回值，但会将提取的筛选标签存储在全局变量或类属性中

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
        
        global filter_store
        filter_store = df.to_dict(orient="records")
        logger.info(f"成功提取筛选标签，共 {len(filter_store)} 条记录")
        
        # 保存筛选条件到 CSV 文件
        os.makedirs("outputs", exist_ok=True)
        
        # 添加 condition_group 列
        filter_df = pd.DataFrame(filter_store)
        filter_df['condition_group'] = [f"条件_{i+1}" for i in range(len(filter_df))]
        
        filter_df.to_csv("outputs/filter_conditions.csv", index=False, encoding='utf-8-sig')
        logger.info(f"已将筛选条件保存到 outputs/filter_conditions.csv")
    except ValueError as e:
        raise ValueError(f"XLSX 文件中不存在名为 '总表筛选' 的 Sheet: {input_file}") from e


def apply_filters() -> None:
    """
    应用筛选任务，根据 filter_store 中的条件对 data_store 进行筛选。
    每个筛选条件生成独立的筛选结果并输出到 CSV 文件。

    Returns:
        None: 无返回值，但会将筛选结果存储在全局变量并输出到文件。

    Raises:
        ValueError: 如果 data_store 或 filter_store 未加载。
    """
    try:
        data_store
        filter_store
    except NameError:
        raise ValueError("数据未加载，请先调用 extract_data 和 extract_filters 方法")
    
    global filtered_data
    filtered_data = {}
    
    # 确保输出目录存在
    os.makedirs("outputs", exist_ok=True)
    
    # 为每个筛选条件生成独立的筛选结果和CSV文件
    for idx, filter_item in enumerate(filter_store):
        condition_name = f"条件_{idx + 1}"
        filtered_data[condition_name] = []
        
        # 执行筛选
        logger.debug(f"开始应用筛选条件 {condition_name}: {filter_item}")
        if not data_store:
            logger.warning("数据总表为空，请检查输入文件格式和Sheet名称")
        else:
            logger.info(f"成功加载 {len(data_store)} 条数据，首条样例: {data_store[0]}")
        
        for data_item in data_store:
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
            
            if match:
                filtered_data[condition_name].append(data_item)
            else:
                if idx == 0:  # 只记录第一个条件的详细不匹配信息
                    logger.debug(f"数据不匹配: {condition_name} - {', '.join(mismatch_fields)}")
        
        logger.info(f"筛选完成 {condition_name}: 匹配 {len(filtered_data[condition_name])} 条记录")
        
        # 输出到CSV - 使用正常格式（非转置）
        output_path = os.path.join("outputs", f"{condition_name}.csv")
        with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
            # 写入UTF-8 BOM头确保Excel兼容
            f.write("\ufeff")
            # 写入筛选条件作为注释（确保不换行）
            f.write(f"# 筛选条件: {' '.join(f'{k}={v}' for k, v in filter_item.items())}\n")
            
            if filtered_data[condition_name]:
                # 创建 DataFrame 并直接写入
                df = pd.DataFrame(filtered_data[condition_name])
                df.to_csv(f, index=False, encoding="utf-8-sig")
            else:
                # 即使没有数据也创建带表头的空文件
                if data_store:
                    fieldnames = [f for f in data_store[0].keys() if f != '序号']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
        
        logger.info(f"{condition_name} 筛选完成，共 {len(filtered_data[condition_name])} 条记录，已保存到 {output_path}")


def export_to_xlsx(input_file: str) -> None:
    """
    生成新的 XLSX 文件，包含总表、总表筛选和每个筛选条件的结果。
    
    Returns:
        None: 无返回值，但会生成一个新的XLSX文件。
    
    Raises:
        ValueError: 如果 data_store 或 filter_store 未加载。
    """
    try:
        data_store
        filter_store
    except NameError:
        raise ValueError("数据未加载，请先调用 extract_data 和 extract_filters 方法")
    
    # 生成输出文件名
    input_filename = os.path.splitext(INPUT_XLSX)[0]
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{input_filename}_筛选结果_{timestamp}.xlsx"
    output_path = os.path.join("outputs", output_filename)
    
    # 确保输出目录存在
    os.makedirs("outputs", exist_ok=True)

    # 读取源文件表头
    source_excel_file = pd.ExcelFile(input_file)
    source_df = pd.read_excel(input_file, sheet_name="总表")
    export_column_header = source_df.iloc[:, 0].tolist()  # 转换为列表
    
    # 使用 ExcelWriter 写入多个Sheet
    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # 写入总表
        if data_store:
            df_total = pd.DataFrame(data_store)
            # 转置数据
            df_total = df_total.T
            # 插入原始的第一列数据作为新列
            df_total.insert(0, "原始第一列", export_column_header)
            df_total.to_excel(writer, sheet_name="总表", header=False, index=False)
        
        # 写入总表筛选
        if filter_store:
            df_filters = pd.DataFrame(filter_store)
            df_filters.to_excel(writer, sheet_name="总表筛选", index=False)
        
        # 写入每个筛选条件的结果
        for idx, filter_item in enumerate(filter_store):
            condition_name = f"条件_{idx + 1}"
            if condition_name in filtered_data and filtered_data[condition_name]:
                df_filtered = pd.DataFrame(filtered_data[condition_name])
                # 转置数据
                df_filtered = df_filtered.T
                # 插入原始的第一列数据作为新列
                df_filtered.insert(0, "原始第一列", export_column_header)
                # 转置数据
                df_filtered = df_filtered.T

                sheet_name = f"{condition_name}_{'_'.join(f'{k}={v}' for k, v in filter_item.items())}"
                df_filtered.T.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    
    logger.info(f"成功生成XLSX文件: {output_path}")


def main() -> None:
    """主函数入口"""
    logger.info("=== 开始处理 XLSX 文件 ===")
    
    # 检查输入文件是否存在
    if not Path(INPUT_XLSX).exists():
        logger.error(f"输入文件不存在: {INPUT_XLSX}")
        return
    
    # 执行流程
    extract_schema(INPUT_XLSX)  # 恢复调用
    extract_data(INPUT_XLSX)
    extract_filters(INPUT_XLSX)
    apply_filters()
    export_to_xlsx(INPUT_XLSX)
    
    logger.info("=== 处理完成 ===")


if __name__ == "__main__":
    main()