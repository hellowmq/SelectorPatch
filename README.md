# SelectorPatch 项目

## 概述
SelectorPatch 是一个用于处理Excel数据并生成筛选结果的工具。它从指定的Excel文件中提取数据总表和筛选条件，应用筛选后生成CSV文件和包含所有结果的XLSX文件。

## 功能
- 从Excel文件提取数据总表
- 从Excel文件提取筛选条件
- 应用筛选条件生成多个CSV文件
- 生成包含所有结果的XLSX文件

## 快速开始
### 1. 获取项目
```bash
git clone https://github.com/hellowmq/SelectorPatch.git
cd SelectorPatch
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 准备数据
将要处理的Excel文件命名为`mockdata.xlsx`并放在项目根目录

### 4. 运行程序
```bash
# Linux/macOS
python src/main.py

# Windows
python src\main.py
```

### 5. 查看结果
结果将输出到`outputs/`目录

### Windows平台注意事项
- 确保已安装Python 3.7或更高版本
- 如果遇到权限问题，请以管理员身份运行命令提示符
- 如果出现编码问题，在命令前设置编码：`chcp 65001`

## 文件结构
- `src/main.py`: 主程序入口
- `outputs/`: 结果输出目录
- `app.log`: 程序运行日志
- `docs/xlsx_processing_flow.md`: 详细处理流程文档
- `requirements.txt`: 项目依赖列表

## 详细流程
有关数据处理流程的详细信息，请参阅[流程文档](docs/xlsx_processing_flow.md)