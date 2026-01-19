import platform
import wallpaper_setter_windows as wallpaper_setter_windows
import wallpaper_setter_darwin as wallpaper_setter_darwin
import wallpaper_setter_linux as wallpaper_setter_linux

def set_wallpaper(path):
    system = platform.system().lower()
    if system == 'windows':
        return wallpaper_setter_windows.set_wallpaper(path)
    elif system == 'darwin':
        return wallpaper_setter_darwin.set_wallpaper(path)
    elif system == 'linux':
        return wallpaper_setter_linux.set_wallpaper(path)
    else:
        print(f"不支持的操作系统: {system}")
        return False