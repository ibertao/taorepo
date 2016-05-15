# -*- coding: utf-8 -*-

""" plexus-streams  (c)  2014 enen92 fightnight

    This file contains parser utilities

    Functions:

    parser_resolver(name,url,icon) -> Process an URL to reproduce Sopcast or AceStream content

"""

import requests
import acestream as ace
import sopcast as sop
from utils.pluginxbmc import *
from utils.webutils import *

def parser_resolver(name,url,icon,depth=0):
    if "sop://" not in url and "acestream://" not in url:
        if "http://" not in url:
            url="http://"+url

        if 'arenavision' in url:
            headers = {
                "Cookie" : "beget=begetok; has_js=1;"
            }
            try:
                source = requests.get(url,headers=headers).text
            except: source="";xbmcgui.Dialog().ok(translate(40000),translate(40128))
        else:
            try:
                source = get_page_source(url)
            except: source = "";xbmcgui.Dialog().ok(translate(40000),translate(40128))

        patternList = ['(sop://[^ "\']+)',                   # Sopcast
                       '(?:acestream://|this.loadPlayer\(["\'])([^"\']+)["\']', # AceStream
                       '<i?frame[^>]+src=["\']([^>]+?)["\']' # iframes
                      ]

        allPatterns = "|".join(patternList)

        matchs = re.findall(allPatterns, source, re.IGNORECASE)
        iframes = []
        for match in matchs:
            if match[0]:
                sop.sopstreams(name,icon,match[0])
                return match[0]
            elif match[1]:
                ace.acestreams(name,icon,match[1])
                return match[1]
            else:
                iframes.append(match[2])

        for iframe in iframes:
            redirect_url = iframe if '/' in iframe else url + '/' + iframe
            if depth < 2:
                found = parser_resolver(name,redirect_url,icon,depth+1)
                if found: return found

        if depth == 0:
            xbmcgui.Dialog().ok(translate(40000),translate(40022))

        return None

    elif "sop://" in url: sop.sopstreams(name,icon,url)
    else: ace.acestreams(name,icon,url)

    return url

# http://stackoverflow.com/a/14173535/1344260
def russianTransliterate(string):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

    tr = dict( [ (ord(a), ord(b)) for (a, b) in zip(*symbols) ] )

    return string.decode("utf-8").translate(tr)
