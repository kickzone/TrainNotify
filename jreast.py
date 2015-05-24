#!C:\Python34\python.exe

def notify(lines):
    retDict = {}
    import lxml.html
    import requests
    try:
        target_url = 'http://traininfo.jreast.co.jp/train_info/kanto.aspx'
        target_html = requests.get(target_url).content
        root = lxml.html.fromstring(target_html)
        TblInfo = root.cssselect('#TblInfo')[0]
        trs = TblInfo.cssselect('.px12')
        for tr in trs:
            for line in lines:
                if tr.text_content() == line:
                    time = tr.xpath('../../following::tr')[0]
                    content = tr.xpath('../../following::tr/following::tr')[0]
                    dict = {}
                    dict['time'] = time.text_content().rstrip()
                    dict['content'] = content.text_content().rstrip()
                    retDict[line] = dict
    except Exception as ex:
        print(ex + " from jreast")
    return retDict