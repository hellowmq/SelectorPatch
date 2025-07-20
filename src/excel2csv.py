import pandas as pd
import os
import sys

def excel_to_csv(input_excel_path, output_dir=None):
    """
    将 Excel 文件中的所有 Sheet 转换为 CSV 文件
    :param input_excel_path: 输入的 Excel 文件路径
    :param output_dir: 输出的 CSV 文件目录（可选，默认为输入文件同目录）
    :return: None
    """
    try:
        # 设置默认输出目录
        if output_dir is None:
            output_dir = os.path.dirname(input_excel_path)
        
        # 读取 Excel 文件中的所有 Sheet
        excel_file = pd.ExcelFile(input_excel_path)
        sheet_names = excel_file.sheet_names
        
        # 遍历所有 Sheet
        for sheet_name in sheet_names:
            try:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                output_path = os.path.join(output_dir, f"{sheet_name}.csv")
                df.to_csv(output_path, index=False)
                print(f"Sheet '{sheet_name}' 转换成功！CSV 文件已保存到: {output_path}")
            except Exception as e:
                print(f"Sheet '{sheet_name}' 转换失败: {e}", file=sys.stderr)
    
    except FileNotFoundError:
        print(f"错误：文件未找到 - {input_excel_path}", file=sys.stderr)
    except Exception as e:
        print(f"转换过程中发生错误: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python excel2csv.py <input_excel_path> [output_dir]", file=sys.stderr)
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    excel_to_csv(input_path, output_dir)