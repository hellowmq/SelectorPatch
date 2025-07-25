# PiliarSelectorPatch 项目

## 概述
PiliarSelectorPatch 是一个专业的Excel数据筛选工具，用于从Excel文件中提取数据总表和筛选条件，智能应用筛选规则后生成多格式的筛选结果文件。

## 核心功能
- 📊 **智能数据提取**：从Excel文件自动提取"总表"和"总表筛选"数据
- 🔍 **灵活筛选规则**：支持精确匹配和空值通配符筛选
- 📁 **多格式输出**：同时生成CSV和XLSX格式的筛选结果
- 🧹 **自动清理**：智能清理上次运行结果，保持输出目录整洁
- 🖱️ **交互式操作**：提供GUI文件选择界面，操作简便
- 📝 **详细日志**：完整的操作日志记录，便于问题追踪

## 项目状态

### ⚠️ 当前版本状态
- **功能状态**：✅ 核心功能完整可用
- **代码质量**：✅ 已完成重构优化
- **生产就绪**：⚠️ 需要性能优化后可用于生产环境

### 🔧 待修复问题
详细问题列表请查看 [问题归档](docs/问题归档.md)

**已完成改进**：
- ✅ 清理调试代码
- ✅ 重构全局变量
- ✅ 完善错误处理
- ✅ 函数职责分离
- ✅ 模块化重构
- ✅ 配置系统实现
- ✅ 单元测试添加

**待改进项**：
- ⚠️ 性能优化

## 快速开始

### 环境要求
- Python 3.7+
- 支持的操作系统：Windows、macOS、Linux

### 1. 环境准备
```bash
# 克隆项目
git clone <repository-url>
cd PiliarSelectorPatch

# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 准备数据文件
确保你的Excel文件包含以下Sheet：
- **总表**：包含原始数据，每列代表一个属性
- **总表筛选**：包含筛选条件，每行代表一组筛选规则

参考模板文件：
- `templates/全维度筛选.xlsx`
- `templates/支持空筛选.xlsx`

### 4. 运行程序
```bash
# 交互式运行（推荐）
python src/main.py

# 命令行指定文件
python src/main.py path/to/your/file.xlsx
```

### 5. 查看结果
程序运行完成后，结果文件将保存在 `outputs/` 目录：
- `总表.csv`：原始数据表
- `filter_conditions.csv`：筛选条件表
- `条件_1.csv`, `条件_2.csv`, ...：各筛选条件的结果
- `{文件名}_筛选结果_{时间戳}.xlsx`：包含所有结果的Excel文件

## 项目结构
```
PiliarSelectorPatch/
├── src/                    # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── clean_output.py    # 输出清理模块
│   ├── config.yaml        # 配置文件
│   ├── run_tests.py       # 测试运行器
│   ├── modules/           # 功能模块目录
│   │   ├── __init__.py    # 模块初始化文件
│   │   ├── data_manager.py       # 数据管理模块
│   │   ├── data_extractor.py     # 数据提取模块
│   │   ├── filter_processor.py   # 筛选处理模块
│   │   ├── output_generator.py   # 输出生成模块
│   │   └── config.py             # 配置管理模块
│   └── tests/             # 测试目录
│       ├── __init__.py    # 测试初始化文件
│       ├── test_config.py        # 配置模块测试
│       └── test_filter_processor.py  # 筛选处理器测试
├── docs/                  # 文档目录
│   ├── 问题归档.md         # 问题跟踪文档
│   └── xlsx_processing_flow.md  # 处理流程文档
├── instructions/          # 使用指南
│   ├── user_guide.md      # 用户指南
│   └── agent_guide.md     # 开发指南
├── templates/             # 模板文件
│   ├── 全维度筛选.xlsx     # 全维度筛选模板
│   └── 支持空筛选.xlsx     # 空值筛选模板
├── outputs/               # 输出目录（自动创建）
├── requirements.txt       # 项目依赖
├── CHANGELOG.md          # 更新日志
├── app.log               # 运行日志
└── README.md             # 项目说明
```

## 使用说明

### 数据格式要求
1. **总表Sheet**：
   - 第一行为列标题
   - 每列代表一个数据属性
   - 支持文本、数字等各种数据类型

2. **总表筛选Sheet**：
   - 每行代表一组筛选条件
   - 列名必须与总表的列名对应
   - 空值表示该条件不参与筛选（通配符）

### 筛选规则
- **精确匹配**：筛选条件值与数据值完全相等
- **空值通配**：筛选条件为空时，匹配该字段的任意值
- **混合筛选**：可以组合精确匹配和通配符筛选

## 开发指南

### 代码贡献
在提交代码前，请确保：
1. 遵循 [开发指南](instructions/agent_guide.md)
2. 查看 [问题归档](docs/问题归档.md) 了解当前待修复问题
3. 运行测试确保功能正常

### 技术栈
- **数据处理**：pandas, openpyxl
- **用户界面**：tkinter
- **日志系统**：logging
- **文件操作**：pathlib, os

## 平台兼容性

### Windows
```cmd
# 设置编码（如遇到中文问题）
chcp 65001

# 设置执行策略（如虚拟环境激活失败）
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### macOS/Linux
```bash
# 确保Python版本
python3 --version

# 使用python3命令
python3 src/main.py
```

## 故障排除

### 常见问题
1. **文件找不到**：确保Excel文件包含"总表"和"总表筛选"Sheet
2. **编码问题**：Windows用户设置 `chcp 65001`
3. **权限问题**：以管理员身份运行或检查文件权限
4. **依赖问题**：确保所有依赖包已正确安装

### 日志查看
程序运行日志保存在 `app.log` 文件中，包含详细的操作记录和错误信息。

## 版本历史
- **当前版本**：功能完整，待代码优化
- **下一版本计划**：代码重构、性能优化、测试覆盖

## 许可证
[待添加许可证信息]

## 联系方式
如有问题或建议，请查看 [问题归档](docs/问题归档.md) 或提交Issue。
