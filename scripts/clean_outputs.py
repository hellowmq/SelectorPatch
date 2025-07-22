import os
import shutil

# 清理 outputs 目录
def clean_outputs():
    """
    清理 outputs 目录中的所有文件和子目录
    """
    outputs_dir = os.path.join(os.path.dirname(__file__), "../outputs")
    outputs_dir = os.path.normpath(outputs_dir)
    
    print(f"清理目录: {outputs_dir}")
    
    # 确保 outputs 目录存在
    if not os.path.exists(outputs_dir):
        print("outputs 目录不存在，无需清理")
        return
    
    # 删除 outputs 目录中的所有内容
    for filename in os.listdir(outputs_dir):
        file_path = os.path.join(outputs_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"已删除文件: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"已删除目录: {file_path}")
        except Exception as e:
            print(f"删除失败 {file_path}: {e}")
    
    print("清理完成")

if __name__ == "__main__":
    clean_outputs()