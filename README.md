# banned-xunlei-for-qbittorrent
Script, which finds IP addresses of Xunlei (Thunder) users and adds them to blacklist
This is English-translated fork of (originqtum/banned-xunlei-for-qbittorrent)[https://github.com/originqtum/banned-xunlei-for-qbittorrent]
Hovewer, I added some minor changes from my preferences

## Blocked clients names
* -XL0012-***  
* Xunlei/***  
* 7.x.x.x
* Xfplay
* QQDownload

## Requirements
1. Python 3 (tested with python 3.8.10)
2. qbittorrent or qbittorrent-nox v4.1.9.1
3. enabled webui

## How to use
1. download qbittorrent_ban_xunlei.py
2. change URL, login and password to yours
3. on linux, simply run qbittorrent_ban_xunlei.py
4. also, you can run it as plain python script using "python3 qbittorrent_ban_xunlei.py"

## When a new connection is found
```
find new client: *.*.*.*		Xunlei 0.0.1.8
find new client: *.*.*.*		-XL0012-#�����Q���
find new client: *.*.*.*		-XL0012-^ȕ�Dm�[ǏW
find new client: *.*.*.*		-XL0012-����d+5ۆ�t
find new client: *.*.*.*		-XL0012-�_���c�`F݋
find new client: *.*.*.*		-XL0012-}[���W�Q��
find new client: *.*.*.*		-XL0012-,���|�����2�
...
```
