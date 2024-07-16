import os
import requests
import sys
import base64
import json, time
from threading import Thread
import json
import os
import win32file
import win32con
import webview
import time
import subprocess

timestamp = time.time()

subprocess.Popen(r"logs/file_server.exe")

def mkdir(path):
 
	folder = os.path.exists(path)
 
	if not folder:                   #判断是否存在文件夹如果不存在则创建为文件夹
		os.makedirs(path)            #makedirs 创建文件时如果路径不存在会创建这个路径
		print("---  new folder...  ---")
		print("---  OK  ---")
 
	else:
		print("---  There is this folder!  ---")
		
file = "logs"
mkdir(file)


file = open('.\\logs\\' + str(timestamp) + '.html','w')
file.close()

window = webview.create_window(
    title='GitSynchronous',
    url='webview/index.html',
    width=850,
    height=600,
    resizable=False,    # 固定窗口大小
    text_select=False,   # 禁止选择文字内容
    confirm_close=True   # 关闭时提示
)
webview.start()

# 打开文件并读取内容  
with open('config.json', 'r', encoding='utf-8') as file:  
    # 使用json.load()方法解析JSON数据  
    configdata = json.load(file)

token = configdata['token']
logfile = configdata['logfile']
apiurl = configdata['apiurl']
committername = configdata['committername']
committeremail = configdata['committeremail']
folder = configdata['folder']
pathtowatch = configdata['pathtowatch']

headers = {"Authorization": "token " + token}
requests.packages.urllib3.disable_warnings()

sys.stdout=open(logfile, "a+")


# 读取文件
def open_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


# 将文件转换为base64编码，上传文件必须将文件以base64格式上传
def file_base64(data):
    data_b64 = base64.b64encode(data).decode('utf-8')
    return data_b64


def upload(file_data, file_name):
    url = apiurl+file_name.replace("\\","/").replace(folder,"")
    req = requests.get(url=url, headers=headers, verify=False)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    upload_file(file_data, file_name, re_data["sha"])
    

# 上传文件
def upload_file(file_data, file_name, sha=""):
    url = apiurl+file_name.replace("\\","/").replace(folder,"")
    content = file_base64(file_data)
    data = {
        "message": file_name,
        "committer": {
            "name": committername,
            "email": committeremail
        },
        "content": content
    }
    if sha:
        data["sha"] = sha
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers, verify=False)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    if "content" not in re_data:
        return upload(file_data, file_name)
    print(re_data['content']['sha'])

def rm(file_name):
    url = apiurl+file_name.replace("\\","/").replace(folder,"")
    req = requests.get(url=url, headers=headers, verify=False)
    req.encoding = "utf-8"
    re_data = json.loads(req.text)
    data = {
        "message": file_name,
        "committer": {
            "name": committername,
            "email": committeremail
        },
        "sha": re_data["sha"]
    }
    data = json.dumps(data)
    req = requests.put(url=url, data=data, headers=headers, verify=False)
    print("<span class="">Deleted", file_name,"</span>")

ACTIONS = {
  1 : "Created",
  2 : "Deleted",
  3 : "Updated",
  4 : "Renamed from something",
  5 : "Renamed to something"
}
 
FILE_LIST_DIRECTORY = win32con.GENERIC_READ | win32con.GENERIC_WRITE
path_to_watch = pathtowatch
hDir = win32file.CreateFile (
  path_to_watch,
  FILE_LIST_DIRECTORY,
  win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
  None,
  win32con.OPEN_EXISTING,
  win32con.FILE_FLAG_BACKUP_SEMANTICS,
  None
)

def tryup(action, file):
                full_filename = os.path.join(path_to_watch, file)
                print (full_filename, ACTIONS.get (action, "Unknown"))
                if ACTIONS.get (action, "Unknown") in ["Renamed from something", "Renamed to something","Deleted"]:
                    try:
                        rm(full_filename)
                    except requests.exceptions.HTTPError as errh:
                        print("HTTP错误:", errh)
                        time.sleep(30)
                        return tryup(action, file)
                    except requests.exceptions.ConnectionError as errc:
                        print("连接错误:", errc)
                        time.sleep(30)
                        return tryup(action, file)
                    except requests.exceptions.Timeout as errt:
                        print("超时错误:", errt)
                        time.sleep(30)
                        return tryup(action, file)
                    except requests.exceptions.RequestException as err:
                        print("其他错误:", err)
                        time.sleep(30)
                        return tryup(action, file)
                    except:
                        time.sleep(30)
                        return tryup(action, file)
                if ACTIONS.get (action, "Unknown")!="Deleted":
                    while 1:
                        try:
                            fdata = open_file(full_filename)
                            break
                        except FileNotFoundError:
                            return
                        except:
                            pass
                    try:
                        upload_file(fdata, full_filename)
                    except KeyError:
                        time.sleep(30)
                        return tryup(action, file)
                    except requests.exceptions.HTTPError as errh:
                        print("HTTP错误:", errh)
                        time.sleep(30)
                        return tryup(action, file)
                    except requests.exceptions.ConnectionError as errc:
                        print("连接错误:", errc)
                        time.sleep(30)
                        return tryup(action, file)
                    except requests.exceptions.Timeout as errt:
                        print("超时错误:", errt)
                        time.sleep(30)
                        return tryup(action, file)
                    except requests.exceptions.RequestException as err:
                        print("其他错误:", err)
                        time.sleep(30)
                        return tryup(action, file)
                    except:
                        time.sleep(30)
                        return tryup(action, file)
 
if __name__ == '__main__':
	while 1:
			results = win32file.ReadDirectoryChangesW (
											   hDir,  #handle: Handle to the directory to be monitored. This directory must be opened with the FILE_LIST_DIRECTORY access right.
											   1024,  #size: Size of the buffer to allocate for the results.
											   True,  #bWatchSubtree: Specifies whether the ReadDirectoryChangesW function will monitor the directory or the directory tree. 
											   win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
												win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
												win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
												win32con.FILE_NOTIFY_CHANGE_SIZE |
												win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
												win32con.FILE_NOTIFY_CHANGE_SECURITY,
											   None,
											   None)
			for action, file in results:
				sys.stdout.flush()
				Thread(target=tryup, args=(action, file)).start()

