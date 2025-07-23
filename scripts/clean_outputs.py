import os
import shutil

# 清理 outputs 目录和 app.log 文件
def clean_outputs():
    """
    清理 outputs 目录中的所有文件和子目录，以及 app.log 文件
    """
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 清理 outputs 目录
    outputs_dir = os.path.join(project_root, "outputs")
    print(f"清理目录: {outputs_dir}")
    
    if os.path.exists(outputs_dir):
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
    else:
        print("outputs 目录不存在，无需清理")
    
    # 清理 app.log 文件
    app_log_path = os.path.join(project_root, "app.log")
    print(f"清理日志文件: {app_log_path}")
    
    if os.path.exists(app_log_path):
        try:
            os.unlink(app_log_path)
            print(f"已删除日志文件: {app_log_path}")
        except Exception as e:
            print(f"删除日志文件失败: {e}")
    else:
        print("app.log 文件不存在，无需清理")
    
    print("清理完成")

if __name__ == "__main__":
    clean_outputs()