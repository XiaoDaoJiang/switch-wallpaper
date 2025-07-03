import os
import sys
from datetime import datetime

from wallpaper_downloader import download_bing_wallpaper
from wallpaper_setter import set_wallpaper

def get_wallpaper_folder():
    # 检测是否为打包后的可执行文件
    if getattr(sys, 'frozen', False):
        # 打包后的可执行文件：使用可执行文件所在目录
        base_dir = os.path.dirname(sys.executable)
        print(f"检测到打包环境，使用可执行文件目录: {base_dir}")
    else:
        # 直接运行Python脚本：使用当前工作目录
        base_dir = os.getcwd()
        print(f"检测到脚本环境，使用当前工作目录: {base_dir}")
    
    wallpaper_folder = os.path.join(base_dir, "Bing_Wallpapers")
    try:
        if not os.path.exists(wallpaper_folder):
            os.makedirs(wallpaper_folder)
            print(f"创建壁纸目录: {wallpaper_folder}")
    except Exception as e:
        print(f"创建壁纸目录失败: {e}")
        # 如果创建失败，尝试使用临时目录
        import tempfile
        wallpaper_folder = os.path.join(tempfile.gettempdir(), "Bing_Wallpapers")
        os.makedirs(wallpaper_folder, exist_ok=True)
        print(f"使用临时目录: {wallpaper_folder}")
    
    return wallpaper_folder

def change_wallpaper():
    wallpaper_folder = get_wallpaper_folder()
    print(f"壁纸存储目录: {wallpaper_folder}")
    file_name = f"bing_wallpaper_{datetime.now().strftime('%Y%m%d')}.jpg"
    file_path = os.path.join(wallpaper_folder, file_name)

    if download_bing_wallpaper(file_path):
        if set_wallpaper(file_path):
            print(f"壁纸已更新: {file_path}")
        else:
            print("设置壁纸失败")
    else:
        print("下载壁纸失败")

if __name__ == "__main__":
    change_wallpaper()
