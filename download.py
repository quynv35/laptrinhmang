import requests
from datetime import datetime
import argparse
import sys

def support():
    print("Chương trình hỗ trợ download file trên các trang web:")
    print("youtube.com")
    print("mediafire")
    print("google drive")
    print("facebook")
    print("onedrive")

def youtube(url):
    # from pytube import YouTube
    pass

def mediafire(url):
    pass

def ggdrive(url):
    pass

def onedrive(url):
    pass

def facebook(url_video):
    url = "https://facebook-videos-reels-downloader.p.rapidapi.com/get-video-info"
    querystring = {"url": url_video}
    headers = {
        "x-rapidapi-key": "0cc733e278mshc6dfccfbf2203f6p16914djsnc108e3d901f5",
        "x-rapidapi-host": "facebook-videos-reels-downloader.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()["video"]["hd_video_url"]


def download(url):
    now = datetime.now()
    filename = now.strftime("%Y_%m_%d_%H_%M_%S")
    with open(filename, "wb") as f:
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
        print("Download thanh cong")

def main():
    parser = argparse.ArgumentParser(description='Chương trình download file trên 1 số trang web thông dụng')
    parser.add_argument('--support' ,action='store_true', help='Danh sách các website hỗ trợ')
    parser.add_argument('-u','--url', type=str, help='Đường dẫn file cần download')
    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.support:
        support()

    if args.url:
        url = args.url
        download(url)

if __name__ == '__main__':
    main()
