# Bing Wallpaper Changer

## 项目简介
本项目是一个自动下载并设置Bing每日壁纸为桌面背景的工具，适合开机自启、定时任务或一键更换壁纸。

## 主要功能
- 自动从Bing获取下载最新高清壁纸
- 支持Windows一键设置桌面背景

## 运行环境
- Python 3.7 及以上
- 依赖库：requests

## 推荐：使用虚拟环境
建议在虚拟环境中安装依赖和运行项目，避免与全局Python环境冲突。

### 创建并激活虚拟环境（Windows）
```bash
python -m venv .venv
.venv\Scripts\activate
```

### 创建并激活虚拟环境（Linux/macOS）
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 安装依赖
```bash
pip install -r requirements.txt
```

## 源码运行
```bash
python src/wallpaper_changer.py
```

## build
本项目使用PyInstaller命令行方式打包

```bash
pyinstaller --onefile --name BingWallpaperChanger src/wallpaper_changer.py
```
- 生成的可执行文件在`dist/`目录下
- 如需隐藏控制台窗口（仅限Windows），可加`--noconsole`

## 其他说明
- 壁纸图片默认保存在`Bing_Wallpapers/`目录。