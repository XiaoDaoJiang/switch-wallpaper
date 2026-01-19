import requests

def download_bing_wallpaper(file_path):
    url = "https://global.bing.com/HPImageArchive.aspx?format=js&idx=0&n=9&pid=hp&FORM=BEHPTB&uhd=1&uhdwidth=3840&uhdheight=2160&setmkt=%s&setlang=en"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        print(data)
        image_url = "https://cn.bing.com" + data["images"][0]["url"]
        
        print(image_url)

        try:
            img_response = requests.get(image_url, timeout=10)
            img_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"使用 cn.bing.com 下载失败，尝试 bing.com ...")
            # 替换为 bing.com 再试一次
            fallback_url = image_url.replace("cn.bing.com", "bing.com")
            try:
                img_response = requests.get(fallback_url, timeout=10)
                img_response.raise_for_status()
            except requests.exceptions.RequestException as e2:
                print(f"使用 bing.com 也下载失败: {e2}")
                return False

        with open(file_path, "wb") as f:
            f.write(img_response.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"下载壁纸时发生错误: {e}")
        return False