# Anime-Serifu-Downloader

## 简介

本工具是方便广大日语学习者在动漫中学习日语的工具，你可以搜索日漫台词并导出为 txt 格式的文本供学习使用。开发者不对使用该工具造成的一切后果负责。

日文网站 [anicobin.ldblog.jp](http://anicobin.ldblog.jp/) 收集了许多动漫的日文台词原文，特此制作该工具爬取日文台词。



## 准备工作
* 如果你没有安装` Python 3`  请自行安装  
[Python 3.8.10 下载地址](https://www.python.org/ftp/python/3.8.10/python-3.8.10-amd64.exe)
* 安装好 Pyhton 后 到源码文件夹下，执行以下命令。  
```
pip install -r requirements.txt
```
* 如果你使用的是 `Anaconda` 环境, 则请执行以下命令。
```
while read requirement; do conda install --yes $requirement || pip install $requirement; done < requirements.txt
```
## 使用方法
python 运行 `serifu.py` 文件, 按照命令提示操作。需要注意的是，搜索动漫名只能使用日文。
## 原理
日文网站 [anicobin.ldblog.jp](http://anicobin.ldblog.jp/) 收集了许多动漫的日文台词原文。
其中 `http://anicobin.ldblog.jp/search?` 接口是搜索动漫台词的接口  
其中 HTTP请求中的 params 为搜索的关键词。
(更多内容，敬请期待)