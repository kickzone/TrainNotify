#!C:\Python34\python.exe

import configparser
import time
import datetime
from email.mime.text import MIMEText
import smtplib
#plugins.iniの読み込み
conf = configparser.ConfigParser()
conf.read('plugins.ini')
pluginDict = {}
for item in conf.items('plugins'):
    vals = item[1].split('|')
    pluginDict[item[0]] = vals
        

#settings.iniの読み込み
conf.read('settings.ini')
sendList = []
for to in conf.get('settings', 'to').split('|'):
    sendList.append(to)
notifyList = []
for notify in conf.get('settings', 'notify').split('|'):
    notifyList.append(notify)

#使用するpluginと引数を決定する
targetPlugins = {}
for plugin in pluginDict.keys():
    lines = pluginDict[plugin]
    for notify in notifyList:
        if notify in lines:
            if plugin not in targetPlugins:
                targetPlugins[plugin] = []
            targetPlugins[plugin].append(notify)


smtpFrom = conf.get('smtp', 'from')
smtpServer = conf.get('smtp', 'server')
smtpPass = conf.get('smtp', 'pass')
smtpPort = conf.get('smtp', 'port')

#1分ごとにnotifyListを対象にpluginを実行、内容に変化があればメール送信

contentsDict = {}
d = datetime.datetime.today()
print("処理開始 %s時%s分" % (d.hour, d.minute))
while True:
    for plugin in targetPlugins.keys():
        module = __import__(plugin)
        result = module.notify(targetPlugins[plugin])
        for val in targetPlugins[plugin]:
            strNotify = ""
            #メモリ中のcontentDictに保存された内容と比較
            #内容が変わった場合、カラに変わった場合にはメール送信
            if val in result.keys():
                #内容あり
                item = result[val]
                if (val in contentsDict.keys() and contentsDict[val] != item["contents"]) or val not in contentsDict.keys():
                    #メモリがカラ or 内容に変更有
                    strNotify = item["time"] + "\n" + item["contents"]
                    contentsDict[val] = item["contents"]
            else:
                #内容無し
                #メモリがカラでない場合のみメール送信
                if val in contentsDict.keys():
                    strNotify = "平常通り運行しています。"
                    #メモリ内容を消す
                    del contentsDict[val]
            if strNotify != "":
                #メール送信
                print("[" + val + "]\n" + strNotify)
                for to in sendList:
                    try:
                        msg = MIMEText(strNotify)
                        msg['Subject'] = val
                        msg['From'] = smtpFrom
                        msg['To'] = to

                        # Send the message via our own SMTP server.
                        s = smtplib.SMTP(smtpServer, smtpPort)
                        s.ehlo()
                        s.login(smtpFrom, smtpPass)
                        s.send_message(msg)
                        s.close()
                    except Exception as ex:
                        print(ex)
    #1分ごとに反復
    time.sleep(60)