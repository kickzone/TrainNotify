#!C:\Python34\python.exe

def notify(target):
    retDict = {}

    import lxml.html
    import requests
    try:
        target_url = 'http://www.yomiuri.co.jp/'
        target_html = requests.get(target_url).content
        root = lxml.html.fromstring(target_html.decode('utf-8'))
        top = root.cssselect('.headline')[0].text_content()
        dict = {}
        dict['time'] = top[-6:-1]
        dict['contents'] = top[0:-7]
        retDict['読売新聞'] = dict
    except Exception as ex:
        print(ex + " from yomiuritop")
    
    return retDict
