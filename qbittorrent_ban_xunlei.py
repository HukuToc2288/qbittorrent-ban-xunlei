#!/usr/bin/python3
import requests
import json
import time
import random
import math
import string

from requests import RequestException

# Change lines below with your settings

# File to store banned IPs
# IDK for what is the purpose of it as banned IPs goes directly to qbittorrent settings
fileAddress = r'./blacklist.txt'
# webUI URL
Root_url = 'http://127.0.0.1:8080'
# webUI credentials
# WARNING: CLEARTEXT PASSWORD
# Make sure that the file is unreadable for others that torrent user
data = {
    'username': 'admin',
    'password': 'adminadmin'
}

def getDownloadItem(url, cookie):
    # random number
    rid = random.random() * 1000
    rid = math.floor(rid)

    param = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    content = {'rid': rid, param: ''}
    rsp = requests.get(url, params=content, headers=def_headers, cookies=cookie)
    return json.loads(str(rsp.content, 'utf-8'))['torrents']


def getTorrentHashAndStatus(torrentVal, value):
    status = value.get('state')
    if status is not None:
        status = status.lower()
        if "uploading" == status or "downloading" == status:
            return torrentVal


def queryTorrentClient(url, cookie, hashVal):
    blockList = []
    rid = random.random() * 1000
    rid = math.floor(rid)

    param = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    content = {'rid': rid, 'hash': hashVal, param: ''}

    rsp = requests.get(url, params=content, headers=def_headers, cookies=cookie)
    PeersInfo = json.loads(str(rsp.content, 'utf-8'))['peers']

    for peer in PeersInfo:
        if isNeedBlockClient(PeersInfo[peer]):
            blockList.append(PeersInfo[peer])
    return blockList


def reloadIpFilter(url, bannedIps, cookie):
    reload = {'ip_filter_enabled': True, 'banned_IPs': bannedIps}
    content = {'json': json.dumps(reload, ensure_ascii=False)}

    requests.post(url, content, headers=headers, cookies=cookie)


def getAllFilerClient(itemsHash, url, cookie):
    blockAllList = []
    for item in itemsHash:
        blockList = queryTorrentClient(url, cookie, item)
        if blockList is not None:
            blockAllList.append(blockList)
    return blockAllList


def isNeedBlockClient(peer):
    client = peer.get('client')
    if client is None:
        return False

    for deFilter in filterClient:
        if deFilter['findType'] == 1 and client.find(deFilter['name']) > -1:
            return True
        elif deFilter['findType'] == 2 and client.startswith(deFilter['name']):
            return True

    return False


def writeToFile(newAddList):
    with open(fileAddress, 'a+') as f:
        for writeIp in newAddList:
            f.write(writeIp + '\n')
        f.close()


def readExistIp():
    with open(fileAddress, 'r') as f1:
        existFilerClient = f1.readlines()
    f1.close()
    return existFilerClient


def notExistIp(existFilerClient, ipsCollect):
    newAddList = []
    for ip in ipsCollect:
        if ''.join(existFilerClient).strip('\n').find(ip['ip']) == -1:
            newAddList.append(ip['ip'])
            print("find new client: " + ip['ip'] + '\t\t' + ip['client'])
    return newAddList


# IDK what the purpose of this method
# It gets trackers from github but for what?
def loadTrackerByGithubAndSetting(url, cookie):
    github_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3 ',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.108 Safari/537.36 ',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    # 10秒超时设置
    rsp = requests.get(github_user_content_url, headers=github_headers, timeout=10)
    trackers = str(rsp.content, 'utf-8')
    # print(trackers)

    reload = {'add_trackers_enabled': True, 'add_trackers': trackers}
    content = {'json': json.dumps(reload, ensure_ascii=False)}

    requests.post(url, content, headers=headers, cookies=cookie)


if __name__ == "__main__":
    # Client names to be filtered, case sensitive
    # findType 1 means contains, findType 2 - startWith
    filterClient = [
        {'name': '-XL0012', 'findType': 1},
        {'name': 'Xunlei', 'findType': 1},
        {'name': 'Xfplay', 'findType': 1},
        {'name': 'QQDownload', 'findType': 1},
        {'name': '7.', 'findType': 2}
    ]
    github_user_content_url = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt'
    
    # Login method
    login_url = Root_url + '/api/v2/auth/login'
    # Get the item being downloaded or uploaded
    mainData_url = Root_url + '/api/v2/sync/maindata'
    # Get the user who downloaded the file connection
    peers_url = Root_url + '/api/v2/sync/torrentPeers'
    # Update preferences
    filter_url = Root_url + '/api/v2/app/setPreferences'

    headers = {
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.70 Safari/537.36 '
    }

    def_headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/78.0.3904.70 Safari/537.36 '
    }
    
    response = requests.post(login_url, data, headers=headers)

    # login error
    if response.text != 'Ok.':
        exit(0)

    cookie_jar = response.cookies
    
    # Uncomment line below, if you know what you do
    
    #try:
    #    loadTrackerByGithubAndSetting(filter_url, cookie_jar)
    #except RequestException:
    #    print('Loading tracker list failed')
    #else:
    #    print('Trackers successfully loaded')
    
    print('Filter running successfully')
    # Main loop
    while True:
        downItem = getDownloadItem(mainData_url, cookie_jar)
        downloadList = []
        for torrent in downItem:
            hashKey = getTorrentHashAndStatus(torrent, downItem[torrent])
            if hashKey is not None:
                downloadList.append(hashKey)

        allFilerClientList = getAllFilerClient(downloadList, peers_url, cookie_jar)
        clients = [y for x in allFilerClientList for y in x]

        existIps = readExistIp()
        newList = notExistIp(existIps, clients)

        if len(newList) > 0:
            writeToFile(newList)
            ips = ''.join(existIps) + '\n'.join(newList)
            # print(ips)
            reloadIpFilter(filter_url, ips, cookie_jar)

        # Execute every 30 seconds
        time.sleep(30)
