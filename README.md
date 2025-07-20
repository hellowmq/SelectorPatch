# Pillar2 项目数据转换工具

## 项目概述
本工具用于将 Excel 文件中的不同表格转换为多个 CSV 文件，方便后续数据处理和分析。

## 技术栈
- Python 3.x
- 虚拟环境（推荐使用 `venv` 或 `conda`）
- 依赖管理：`requirements.txt`

## 快速开始
1. 克隆项目并进入项目目录：
   ```bash
   git clone <项目地址>
   cd PiliarSelectorPatch
   ```

2. 创建并激活虚拟环境：
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

4. 运行工具：
   ```bash
   python main.py
   ```

## 代码示例
以下是一个简单的代码片段，展示如何读取 Excel 文件并导出为 CSV：

```python
import pandas as pd

# 读取 Excel 文件
excel_file = pd.ExcelFile("input.xlsx")

# 遍历每个表格并导出为 CSV
for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    df.to_csv(f"output_{sheet_name}.csv", index=False)

print("转换完成！")
```

## 依赖列表
以下是 `requirements.txt` 的内容：
```
pandas>=1.3.0
openpyxl>=3.0.0
```

## 注意事项
- 确保输入的 Excel 文件格式正确。
- 导出的 CSV 文件会保存在当前目录下。