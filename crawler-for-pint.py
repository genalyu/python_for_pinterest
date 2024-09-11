from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

# 指定 msedgedriver.exe 的路径
edge_driver_path = 'C:/Users/文静的宇/Downloads/Compressed/msedgedriver.exe'

# 创建 Edge Service
service = Service(executable_path=edge_driver_path)

# 配置 Edge 浏览器的选项
edge_options = Options()

# 启动 Edge 浏览器
driver = webdriver.Edge(service=service, options=edge_options)

# 获取用户输入
want = input("你想要的图片类型：")

# 打开目标页面
url = f'https://www.pinterest.com/search/pins/?q={want}&rs=typed'
driver.get(url)

# 等待页面加载完成
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'img'))
    )
except Exception as e:
    print(f"Error while waiting for page to load: {e}")

n = 0

# 滚动页面，加载更多图片
for _ in range(10):  # 滚动10次，视需要调整
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(4)  # 等待页面加载更多图片

    # 获取页面源代码并解析
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    # 创建保存图片的本地目录
    save_dir = f'{want}'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

   

    # 查找并下载图片
    def download_images(soup):
        global n
        images = soup.find_all('img')
        for idx,img in enumerate(images):
            img_url = img.get('src')

            if not "60x" in img_url:
                for p in range(200,900):
                    img_url = img_url.replace(f"{p}x", "originals")
                img_url = urljoin(url, img_url)
                print(f'Image URL: {img_url}')
                try:
                    img_data = requests.get(img_url, timeout=10).content
                    n = n+1
                    img_name = f'{want}_{n}.jpg'
                    img_path = os.path.join(save_dir, img_name)

                    with open(img_path, 'wb') as img_file:
                        img_file.write(img_data)

                    print(f'Downloaded {img_name}')
                    time.sleep(1)  # 延迟，避免过快请求
                except Exception as e:
                    print(f"Failed to download image {img_url}: {e}")

    # 调用下载函数
    download_images(soup)

# 关闭浏览器
driver.quit()

print("Finished downloading images.")
