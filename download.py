import requests
import datetime
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
    pass

def mediafire(url):
    pass

def ggdrive(url):
    pass

def onedrive(url):
    pass

def facebook(url):
    pass

def download(url):
    pass

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
