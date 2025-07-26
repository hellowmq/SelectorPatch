#!/bin/bash

# 构建脚本 - 用于跨平台打包

# 检查参数
if [ "$#" -ne 1 ]; then
    echo "用法: $0 [macos|windows]"
    echo "示例: $0 macos"
    exit 1
fi

# 获取平台参数
PLATFORM=$1

# 打包 MacOS 平台
function build_macos() {
    echo "构建 MacOS 版本..."
    python -m PyInstaller --onefile --name=app_macos \
        --add-data="src/config.yaml:." \
        --add-data="src/modules:modules" \
        --hidden-import=yaml \
        --collect-all=yaml \
        --exclude-module=tkinter \
        --console \
        src/main.py
    echo "MacOS 构建完成。"
    echo ""
    echo "===== 使用说明 ====="
    echo "1. 直接运行（使用默认测试文件）:"
    echo "   ./dist/app_macos"
    echo ""
    echo "2. 指定输入文件运行:"
    echo "   ./dist/app_macos <Excel文件路径>"
    echo "   例如: ./dist/app_macos templates/全维度筛选.xlsx"
    echo ""
    echo "3. 输出文件将保存在 outputs/ 目录中"
    echo "===================="
}

# 打包 Windows 平台
function build_windows() {
    echo "构建 Windows 版本..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # 在 macOS 上构建 Windows 版本
        python -m PyInstaller --onefile --name=app_windows \
            --add-data="src/config.yaml:." \
            --add-data="src/modules:modules" \
            --hidden-import=yaml \
            --collect-all=yaml \
            --exclude-module=tkinter \
            --console \
            src/main.py
        echo "Windows 构建完成。"
        echo ""
        echo "===== 使用说明 ====="
        echo "1. 直接运行（使用默认测试文件）:"
        echo "   dist\\app_windows.exe"
        echo ""
        echo "2. 指定输入文件运行:"
        echo "   dist\\app_windows.exe <Excel文件路径>"
        echo "   例如: dist\\app_windows.exe templates\\全维度筛选.xlsx"
        echo ""
        echo "3. 输出文件将保存在 outputs\\ 目录中"
        echo "===================="
        echo ""
        echo "===== 使用说明 ====="
        echo "1. 直接运行（使用默认测试文件）:"
        echo "   dist\\app_windows.exe"
        echo ""
        echo "2. 指定输入文件运行:"
        echo "   dist\\app_windows.exe <Excel文件路径>"
        echo "   例如: dist\\app_windows.exe templates\\全维度筛选.xlsx"
        echo ""
        echo "3. 输出文件将保存在 outputs\\ 目录中"
        echo "===================="
        echo "注意：在 Windows 环境中构建时，请使用以下命令："
        echo "python -m PyInstaller --onefile --name=app_windows --add-data=\"src/config.yaml;.\" --add-data=\"src/modules;modules\" --hidden-import=yaml --collect-all=yaml --exclude-module=tkinter --console src/main.py"
    else
        # 在 Windows 上构建 Windows 版本
        python -m PyInstaller --onefile --name=app_windows \
            --add-data="src/config.yaml;." \
            --add-data="src/modules;modules" \
            --exclude-module=tkinter \
            --console \
            src/main.py
        echo "Windows 构建完成。"
    fi
}

# 根据平台参数执行相应的构建函数
case $PLATFORM in
    macos)
        build_macos
        ;;
    windows)
        build_windows
        ;;
    *)
        echo "错误: 不支持的平台 '$PLATFORM'"
        echo "支持的平台: macos, windows"
        exit 1
        ;;
esac

exit 0