import os
import subprocess

def set_wallpaper(path):
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    try:
        if "gnome" in desktop_env or "unity" in desktop_env:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{path}"], check=True)
        elif "kde" in desktop_env:
            subprocess.run(["plasma-apply-wallpaperimage", path], check=True)
        else:
            print(f"不支持的 Linux 桌面环境: {desktop_env}")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"设置 Linux 壁纸时发生错误: {e}")
        return False