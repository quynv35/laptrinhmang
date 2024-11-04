import requests
from gdown import download_folder
import sys
import re
import json
import os
from clint.textui import progress

ggdrive_api = "AIzaSyAPAHH0LPdbBaYoB0ecqVJtLdnf8E5xcDs"

def get_fileId(text):
    if "https:" in text:
        fileId = text.split('/')[5].split('?')[0]
        return fileId
    return text

def isFile(fileId):
    global ggdrive_api
    url = f"https://www.googleapis.com/drive/v3/files/{fileId}?key={ggdrive_api}"
    res = requests.get(url).text
    if "application/vnd.google-apps.folder" in res:
        return False
    return True

def get_filename(fileId):
    global ggdrive_api
    url = f"https://www.googleapis.com/drive/v3/files/{fileId}?key={ggdrive_api}&fields=name,mimeType,size"
    res = json.loads(requests.get(url).text)
    name,mimeType = res["name"],res["mimeType"]
    if mimeType == "application/vnd.google-apps.folder":
        size = 0
    else:
        size = int(res["size"])
    mime_to_extension = {
        'application/pdf': '.pdf',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': '.xlsx',
        'application/vnd.openxmlformats-officedocument.presentationml.presentation': '.pptx',
        'text/plain': '.txt',
        'text/csv': '.csv',
        'image/jpeg': '.jpg',
        'image/png': '.png',
        'image/gif': '.gif',
        'audio/mpeg': '.mp3',
        'audio/wav': '.wav',
        'video/mp4': '.mp4',
        'application/zip': '.zip',
        'application/vnd.rar': '.rar',
        'application/vnd.google-apps.script+json': '.json',
        'application/vnd.google-apps.folder':''
    }
    extension = mime_to_extension[mimeType]
    if not name.endswith(extension) and mimeType!='application/vnd.google-apps.folder':
        name = name + extension
    return name,size

def get_linkdownload(fileId):
    global ggdrive_api
    url = f"https://www.googleapis.com/drive/v3/files/{fileId}/download?key={ggdrive_api}"
    res = requests.post(url)
    data = json.loads(res.text)
    downloadUri = data["response"]["downloadUri"]
    return downloadUri

def rename(name):
    if not os.path.exists(name):
        return name
    else:
        base, extension = os.path.splitext(name)
        counter = 1
        newname = f"{base}_{counter}{extension}"
        while os.path.exists(newname):
            counter += 1
            newname = f"{base} ({counter}){extension}"
        return newname

def download(fileId, folder='.'):
    url = get_linkdownload(fileId)
    filename,size = get_filename(fileId)
    filename  = rename(filename)
    response = requests.get(url)
    print(f"Downloading file {folder}/{filename}")
    with open(f"{folder}/{filename}", "wb") as f:
        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(size/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()

def extract_domain(url):
    pattern = r'^(?:http[s]?://)?(?:www\.)?([^/]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        exit(1)

def main():
    # print('Chương trình download file/folder từ google driver')
    if len(sys.argv) == 1:
        print(f"python {sys.argv[0]} <url>")
        sys.exit(1)

    url = sys.argv[1]
    if "drive.google.com" not in url:
        print("Chỉ hỗ trợ download từ google driver")
        sys.exit(1)

    try:
        fileId = get_fileId(url)
    except:
        print("Khong tim thay file/folder can tai")
        exit(1)

    if isFile(fileId):
        download(fileId)
    else:
        download_folder(url)

if __name__ == '__main__':
    main()
