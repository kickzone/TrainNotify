#!C:\Python34\python.exe

def notify(lines):
    retDict = {}
    import lxml.html
    import requests
    try:
        target_url = 'http://shinkansen.jr-central.co.jp/sep/pc/senku01/P02.html'
        target_html = requests.get(target_url).content
        root = lxml.html.fromstring(target_html)
        text = root.cssselect('.text')[3].text_content()
        time = root.cssselect('.date')[0].text_content()
        if len(text) > 30 :
            dict = {}
            dict['time'] = time
            dict['contents'] = text
            retDict[lines[0]] = dict
    except Exception as ex:
        print(ex + " from shinkansen")
    return retDict