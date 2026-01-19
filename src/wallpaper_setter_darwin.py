import subprocess

def set_wallpaper(path):
    script = f'''
    tell application "Finder"
    set desktop picture to POSIX file "{path}"
    end tell
    '''
    try:
        subprocess.run(["osascript", "-e", script], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"设置 macOS 壁纸时发生错误: {e}")
        return False