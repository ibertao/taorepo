# -*- coding: utf-8 -*-

"""
This plugin is 3rd party and not part of plexus-streams addon

sport7.ru

"""
import sys,os
current_dir = os.path.dirname(os.path.realpath(__file__))
basename = os.path.basename(current_dir)
core_dir =  current_dir.replace(basename,'').replace('parsers','')
sys.path.append(core_dir)
from utils.webutils import *
from utils.pluginxbmc import *
from utils.directoryhandle import *
from utils.parsers import *

base_url = 'http://sport7.ru'

def module_tree(name,url,iconimage,mode,parser,parserfunction):
	if not parserfunction: sport7_main()
	elif parserfunction == 'list_streams': list_streams(url)

def sport7_main():
	html_source = get_page_source(base_url+"/onlain_sopcast")

	matches = {}
	matchesOrder = []
	matchedLines = [line for line in html_source.split('\n') if "grey-bl col-gr1" in line]
	for line in matchedLines:
		onlineMatches=re.findall('<img class="v-bt"[^>]+src="(.+?)".+?<a.+?/match/(\d+?)">([^<]+)</a>(.*?)(?:div class="match-ln"|$)', line)
		for img, mid, teams, data in onlineMatches:
			match = matches.setdefault(mid, {"img" : img, "teams": teams, "links" : set()})
			if not match in matchesOrder:
				matchesOrder.append(match)
			links=re.findall('<a[^>]+href="([^"]+)[^>]*>((?:sopcast|acestream)[^<]+)', data)
			match["links"].update([linkID for linkID in links])

	if len(matchesOrder) == 0:
		addLink('[B][COLOR white]No sopcast or acestream links found at this moment[/COLOR][/B]', '', os.path.join(current_dir,'icon.png'))
	else:
		for match in matchesOrder:
			addDir('[B][COLOR orange]{0}[/COLOR][/B]'.format(russianTransliterate(match["teams"])), str(match), 401, match["img"], len(matchesOrder), False, parser="sport7",parserfunction="list_streams")

def list_streams(matchData):
	match = eval(matchData)

	links = []
	names = []
	for link, name in match["links"]:
		links.append(link)
		names.append(name + ": " + link)

	if len(links) > 0:
		dialog = xbmcgui.Dialog()
		index = dialog.select(translate(40021), names)

		if index>-1:
			name=names[index]
			url=links[index]
			parser_resolver(name, url, os.path.join(current_dir,'icon.png'))
