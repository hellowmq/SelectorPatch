import tkinter as tk
from tkinter import filedialog
import csv
import logging
import os
import pandas as pd
from pathlib import Path
from clean_output import clean_output_directory

print("HIHIHI")
print(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("FUFUFU")

# 首先配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 清理上次运行的结果
logger.info("清理上次运行的结果...")
clean_output_directory()

# 默认输入文件路径
DEFAULT_INPUT_XLSX = "mockdata.xlsx"

def select_excel_file() -> str:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="选择 Excel 文件",
        filetypes=[("Excel 文件", "*.xlsx"), ("所有文件", "*.*")]
    )
    if not file_path:
        logger.error("未选择文件，程序终止")
        exit(1)
    return file_path



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
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"总表.csv")
        df.to_csv(output_path, index=False)
        logger.info(f"已将总表保存到 {output_path}")
        
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
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
        os.makedirs(output_dir, exist_ok=True)
        
        # 添加 condition_group 列
        filter_df = pd.DataFrame(filter_store)
        filter_df['condition_group'] = [f"条件_{i+1}" for i in range(len(filter_df))]
        
        filter_output_path = os.path.join(output_dir, "filter_conditions.csv")
        filter_df.to_csv(filter_output_path, index=False, encoding='utf-8-sig')
        logger.info(f"已将筛选条件保存到 {filter_output_path}")
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
        # 尝试访问全局变量
        global data_store, filter_store, filtered_data
        if 'data_store' not in globals() or 'filter_store' not in globals():
            raise NameError("全局变量未定义")
    except NameError:
        raise ValueError("data_store 或 filter_store 未加载")
    
    filtered_data = {}
    
    # 确保输出目录存在
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    os.makedirs(output_dir, exist_ok=True)
    
    # 为每个筛选条件生成独立的筛选结果和CSV/XLSX文件
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
        logger.debug(f"筛选完成 {condition_name}: 匹配 {len(filtered_data[condition_name])} 条记录")
        
        # 输出到CSV - 使用正常格式（非转置）
        output_path = os.path.join(output_dir, f"{condition_name}.csv")
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
    
    Args:
        input_file (str): 输入文件路径，用于确定输出文件的保存位置
        
    Returns:
        None: 无返回值，但会生成一个新的XLSX文件。
    
    Raises:
        ValueError: 如果 data_store 或 filter_store 未加载。
    """
    try:
        # 尝试访问全局变量
        global data_store, filter_store, filtered_data
        if 'data_store' not in globals() or 'filter_store' not in globals():
            raise NameError("全局变量未定义")
    except NameError:
        raise ValueError("数据未加载，请先调用 extract_data 和 extract_filters 方法")
    
    # 生成输出文件名
    input_filename = os.path.splitext(os.path.basename(input_file))[0]
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"{input_filename}_筛选结果_{timestamp}.xlsx"
    
    # 使用 output 目录作为输出目录
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "outputs")
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    
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
                
                # 简化工作表名称：只使用筛选值的序列作为标识
                value_sequence = '_'.join([str(v) for v in filter_item.values() if v != ''])
                if not value_sequence:
                    value_sequence = "空值"
                
                # 确保工作表名称不超过31个字符（Excel限制）
                sheet_name = f"{condition_name}_{value_sequence}"
                if len(sheet_name) > 31:
                    sheet_name = sheet_name[:31]
                
                df_filtered.to_excel(writer, sheet_name=sheet_name, index=True)
    
    logger.info(f"成功生成XLSX文件: {output_path}")


def extract_schema(input_file: str) -> None:
    """提取表结构（保留为未来版本扩展）"""
    logger.info(f"表结构提取功能预留: {input_file}")


def main() -> None:
    # 日志初始化已在文件顶部完成，不需要在这里清理
    
    import sys
    
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
    extract_schema(input_xlsx)  # 恢复调用
    extract_data(input_xlsx)
    extract_filters(input_xlsx)
    apply_filters()
    export_to_xlsx(input_xlsx)
    
    logger.info("=== 处理完成 ===")


if __name__ == "__main__":
    try:
        main()
    finally:
        # 程序结束时不清理日志文件，因为可能需要查看日志
        # 如果需要清理日志，可以取消下面的注释
        pass
        # clean_output_directory()