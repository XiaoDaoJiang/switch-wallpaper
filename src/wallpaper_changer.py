import os
import sys
import logging
import re
from datetime import datetime, timedelta

from wallpaper_downloader import download_bing_wallpaper
from wallpaper_setter import set_wallpaper

RETENTION_DAYS = 30


def cleanup_old_wallpapers(wallpaper_folder, current_wallpaper, today=None):
    """保留含今天在内的最近30天图片，以及当前正在使用的壁纸。"""
    cutoff = (today or datetime.now().date()) - timedelta(days=RETENTION_DAYS - 1)
    current_path = os.path.normcase(os.path.abspath(current_wallpaper))
    logger = logging.getLogger(__name__)
    try:
        with os.scandir(wallpaper_folder) as entries:
            for entry in entries:
                match = re.fullmatch(r"bing_wallpaper_(\d{8})\.jpg", entry.name)
                if not match or not entry.is_file(follow_symlinks=False):
                    continue
                if os.path.normcase(os.path.abspath(entry.path)) == current_path:
                    continue
                try:
                    image_date = datetime.strptime(match.group(1), '%Y%m%d').date()
                except ValueError:
                    continue
                if image_date < cutoff:
                    try:
                        os.remove(entry.path)
                        logger.info("已清理过期壁纸: %s", entry.path)
                    except OSError as exc:
                        logger.warning("清理壁纸失败: %s: %s", entry.path, exc)
    except OSError as exc:
        logger.warning("读取壁纸目录失败，跳过清理: %s", exc)

def setup_logging():
    """设置日志记录"""
    log_dir = get_wallpaper_folder()
    log_file = os.path.join(log_dir, "wallpaper_changer.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

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
    import time
    
    wallpaper_folder = get_wallpaper_folder()
    print(f"壁纸存储目录: {wallpaper_folder}")
    file_name = f"bing_wallpaper_{datetime.now().strftime('%Y%m%d')}.jpg"
    file_path = os.path.join(wallpaper_folder, file_name)

    # 检查是否已有今天的壁纸
    if os.path.exists(file_path):
        print(f"发现今天的壁纸文件: {file_path}")
        if set_wallpaper(file_path):
            print(f"使用已存在的壁纸: {file_path}")
            cleanup_old_wallpapers(wallpaper_folder, file_path)
            return
        else:
            print("设置已存在的壁纸失败，尝试重新下载")

    # 等待网络连接稳定（开机后可能需要时间）
    print("等待网络连接...")
    time.sleep(10)
    
    # 尝试下载新壁纸
    download_success = False
    for attempt in range(3):  # 重试3次
        print(f"尝试下载壁纸 (第{attempt + 1}次)")
        if download_bing_wallpaper(file_path):
            download_success = True
            break
        else:
            print(f"下载失败，等待{5 * (attempt + 1)}秒后重试...")
            time.sleep(5 * (attempt + 1))
    
    if download_success:
        # 确保文件存在且有效
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            if set_wallpaper(file_path):
                print(f"壁纸已更新: {file_path}")
                cleanup_old_wallpapers(wallpaper_folder, file_path)
            else:
                print("设置新下载的壁纸失败")
                # 尝试使用备用壁纸
                use_fallback_wallpaper(wallpaper_folder)
        else:
            print("下载的文件无效")
            use_fallback_wallpaper(wallpaper_folder)
    else:
        print("下载壁纸失败，使用备用壁纸")
        use_fallback_wallpaper(wallpaper_folder)

def use_fallback_wallpaper(wallpaper_folder):
    """使用最近的壁纸作为备用"""
    try:
        # 查找最近的壁纸文件
        wallpaper_files = [f for f in os.listdir(wallpaper_folder) if f.endswith('.jpg')]
        if wallpaper_files:
            # 按文件名排序，获取最新的
            wallpaper_files.sort(reverse=True)
            latest_wallpaper = os.path.join(wallpaper_folder, wallpaper_files[0])
            if set_wallpaper(latest_wallpaper):
                print(f"使用备用壁纸: {latest_wallpaper}")
                cleanup_old_wallpapers(wallpaper_folder, latest_wallpaper)
            else:
                print("设置备用壁纸也失败")
        else:
            print("没有找到备用壁纸文件")
    except Exception as e:
        print(f"使用备用壁纸时发生错误: {e}")

if __name__ == "__main__":
    logger = setup_logging()
    logger.info("=== 壁纸更换程序启动 ===")
    try:
        change_wallpaper()
    except Exception as e:
        logger.error(f"程序执行出错: {e}", exc_info=True)
    logger.info("=== 壁纸更换程序结束 ===\n")
