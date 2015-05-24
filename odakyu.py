#!C:\Python34\python.exe

import lxml.html
import requests

#<BR>タグを改行文字に変換して文字列化
def repBR(element):
    rawstr = lxml.html.tostring(element)
    repstr = rawstr.decode('utf-8').replace("<br>", "\n")
    return lxml.html.fromstring(repstr).text_content()

def notify(target):
    retDict = {}
    try:
        target_url = 'http://www.odakyu.jp/cgi-bin/user/emg/emergency_bbs.pl'
        target_html = requests.get(target_url).content
        root = lxml.html.fromstring(target_html)
        time = root.cssselect('.date')[0]
        left = root.cssselect('div.left_dotline_b')
        #div.left_dotline_bがあれば運行状況が出ている
        if len(left) > 0:
            str = left[0].text_content()
            str += "\n"
            if len(left) > 1:
                if len(left[1].cssselect('img[alt="ロマンスカーの運転状況"]')) == 0:
                    str += "\n詳細情報\n"
                else:
                    str += "\nロマンスカーの運転状況\n"
                str += repBR(left[1])
            if len(left) > 2 and len(left[2].cssselect('img[alt="ロマンスカーの運転状況"]')):
                str += "\nロマンスカーの運転状況\n" + repBR(left[2])
            dict = {}
            dict['time'] = time.text_content()
            dict['contents'] = str
            retDict['小田急小田原線'] = dict
    except Exception as ex:
        print(ex + " from odakyu")

    return retDict

