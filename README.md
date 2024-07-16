# GSR
GSR，全称GitSynchronous，是一个本地文件自动同步到Git仓库的Python程序。

## 功能清单
- [x] 使用pywin32自动监听本地文件变化，并自动提交到Git仓库
- [x] 自定义监听文件夹和提交仓库
- [x] 多线程同时上传
- [x] 自动将日志保存到指定文件中
- [x] 用户界面窗口
- [x] 窗口查看日志
- [ ] 使用计数器，限制线程数，避免过高的内存占用
- [ ] 开机自启动

## 开箱即用
[Release Page 下载页](https://github.com/ning0818/GSR/releases)

## 使用教程
1.从Release页面下载对应系统版本所需的程序，解压到任意文件夹

2.修改`config.json`,注释如下表所示：
```
{  
    "token": "ghp_xxxxxxx", // github token
    "logfile": "E:/logs.log",  // 指定日志文件
    "apiurl": "https://api.github.com/repos/oblivionocean/gsr/contents/",  // github上传文件apiurl，格式https://api.github.com/repos/用户名/仓库名/contents/
    "committername": "ning0818", // github用户名
    "committeremail": "yuanning0818@foxmail.com",  // github绑定邮箱
    "folder": "E:/gitrepotest/", // 监听目录
    "pathtowatch": "E:\\gitrepotest" // 监听目录
  }
```
4.保存配置文件
5.运行`gitsynchronous.exe`

## Bug反馈
[议题](https://github.com/ning0818/GSR/issues)

## 拉取请求
[拉取请求](https://github.com/ning0818/GSR/pulls)

## 社区讨论
[社区讨论](https://github.com/ning0818/GSR/discussions)

## 鸣谢
- [@Fgaoxing](https://github.com/fgaoxing)
