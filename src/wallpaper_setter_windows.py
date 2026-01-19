import ctypes
import time
import os

def set_wallpaper(path):
    try:
        # 确保文件存在
        if not os.path.exists(path):
            print(f"壁纸文件不存在: {path}")
            return False
            
        # 确保文件大小有效
        if os.path.getsize(path) == 0:
            print(f"壁纸文件为空: {path}")
            return False
        
        # 等待桌面环境完全加载
        time.sleep(2)
        
        # 使用绝对路径
        abs_path = os.path.abspath(path)
        
        # 设置壁纸，使用更完整的参数
        result = ctypes.windll.user32.SystemParametersInfoW(
            20,  # SPI_SETDESKWALLPAPER
            0,
            abs_path,
            3    # SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
        )
        
        if result:
            print(f"成功设置壁纸: {abs_path}")
            return True
        else:
            print(f"SystemParametersInfoW 返回失败")
            return False
            
    except Exception as e:
        print(f"设置 Windows 壁纸时发生错误: {e}")
        return False