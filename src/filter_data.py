import pandas as pd
import os

def filter_and_save_results(main_table_path, filter_table_path, output_dir):
    """
    根据筛选表中的条件过滤主表数据并生成子表
    :param main_table_path: 总表 CSV 文件路径
    :param filter_table_path: 筛选表 CSV 文件路径
    :param output_dir: 输出目录
    """
    try:
        # 读取总表和筛选表
        df_main = pd.read_csv(main_table_path)
        df_filter = pd.read_csv(filter_table_path)

        # 提取筛选条件和子表名称
        filter_conditions = df_filter[['子表名称', '年份', '品类']].drop_duplicates()

        # 分组生成子表
        for row in filter_conditions.itertuples(index=False):
            table_name, year, category = row
            # 过滤数据
            filtered_data = df_main[(df_main['年份'] == year) & (df_main['品类'] == category)]
            # 保存为子表
            output_path = os.path.join(output_dir, f"{table_name}.csv")
            filtered_data.to_csv(output_path, index=False)
            print(f"子表 {table_name}.csv 已生成")
            
            # 保存为子表
            output_path = os.path.join(output_dir, f"result{chr(64 + idx)}.csv")
            filtered_data.to_csv(output_path, index=False)
            print(f"子表 result{chr(64 + idx)}.csv 已生成")

    except Exception as e:
        print(f"处理失败: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python filter_data.py <总表路径> <筛选表路径> [输出目录]")
        sys.exit(1)
    
    main_path = sys.argv[1]
    filter_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else os.path.dirname(main_path)
    
    filter_and_save_results(main_path, filter_path, output_dir)