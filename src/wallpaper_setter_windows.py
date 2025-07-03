import ctypes

def set_wallpaper(path):
    try:
        ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)
        return True
    except Exception as e:
        print(f"设置 Windows 壁纸时发生错误: {e}")
        return False