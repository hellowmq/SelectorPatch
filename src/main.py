import csv
import logging
import os
import pandas as pd
from pathlib import Path

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
    """提取表结构（空方法，暂用日志占位）"""
    logger.info(f"正在提取表结构: {input_file}")


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
        df = pd.read_excel(input_file, sheet_name="总表筛选")
        global filter_store
        filter_store = df.to_dict(orient="records")
        logger.info(f"成功提取筛选标签，共 {len(filter_store)} 条记录")
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
                if str(data_item.get(field)) != str(value):
                    match = False
                    mismatch_fields.append(f"{field}(期望:{value},实际:{data_item.get(field)})")
                    break
            if match:
                filtered_data[condition_name].append(data_item)
            else:
                logger.debug(f"数据不匹配: {condition_name} - {', '.join(mismatch_fields)}")
        logger.debug(f"筛选完成 {condition_name}: 匹配 {len(filtered_data[condition_name])} 条记录")
        
        # 输出到CSV
        output_path = os.path.join("outputs", f"{condition_name}.csv")
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            # 写入UTF-8 BOM头确保Excel兼容
            f.write("\ufeff")
            # 写入筛选条件作为注释（确保不换行）
            f.write(f"# 筛选条件: {' '.join(f'{k}={v}' for k, v in filter_item.items())}\n")
            if filtered_data[condition_name]:
                clean_data = [dict(row) for row in filtered_data[condition_name]]
                writer = csv.DictWriter(f, fieldnames=clean_data[0].keys())
                writer.writeheader()
                writer.writerows(clean_data)
            else:
                # 即使没有数据也创建带表头的空文件
                fieldnames = [f for f in (data_store[0].keys() if data_store else []) 
                             if f != '序号']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
        
        logger.info(f"{condition_name} 筛选完成，共 {len(filtered_data[condition_name])} 条记录，已保存到 {output_path}")


def export_to_xlsx() -> None:
    """生成新的 XLSX 文件（空方法，暂用日志占位）"""
    logger.info("正在生成新的 XLSX 文件")


def main() -> None:
    """主函数入口"""
    logger.info("=== 开始处理 XLSX 文件 ===")
    
    # 检查输入文件是否存在
    if not Path(INPUT_XLSX).exists():
        logger.error(f"输入文件不存在: {INPUT_XLSX}")
        return
    
    # 执行流程
    extract_schema(INPUT_XLSX)
    extract_data(INPUT_XLSX)
    extract_filters(INPUT_XLSX)
    apply_filters()
    export_to_xlsx()
    
    logger.info("=== 处理完成 ===")


if __name__ == "__main__":
    main()