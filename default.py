import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
import os
import re
import sys
import unicodedata
from t0mm0.common.addon import Addon
from t0mm0.common.net import Net
import xml.etree.ElementTree as ET


addon = Addon('plugin.video.livingstreams', sys.argv)
net = Net()
settings = xbmcaddon.Addon(id='plugin.video.livingstreams')
fanart = os.path.join(settings.getAddonInfo('path'), 'fanart.jpg')
streams_url = "http://lvstr.org/kodi-addon"
icon = os.path.join(settings.getAddonInfo('path'), 'icon.png')
play = addon.queries.get('play', None)


def MAIN():
        addDir('TV', streams_url, 1, '')
        addDir('Radio', streams_url, 2, '')
        addDir('Audio Bibles', streams_url, 3, '')
        addDir('Settings', '', 4, '', False)
##################################################################################################################################

def addLinks(link_type):
        root = ET.fromstring(getUrl(streams_url))
        language = settings.getSetting(link_type+"-language")
        region = settings.getSetting(link_type+"-region")
        # xbmc.log("region = "+region)
        quality = settings.getSetting("quality")
        quality = quality.lower()
        multilanguage_enabled = settings.getSetting("multilanguage-enabled")
        # xbmc.log("quality = "+quality)
        # i = 1
        for child in root:
                # i = i +1
                # xbmc.log(str(i))
                # xbmc.log(child.find('type').text)
                # xbmc.log(link_type)
                media_url = None
                if child.find('type').text == link_type:
                        # xbmc.log(str(i))
                        if child.find('type').text == 'video':
                                urls = child.find('url')
                                if urls.find('ss') != None:
                                        media_url = urls.find('ss').text
                                elif urls.find(quality) != None:
                                        media_url = urls.find(quality).text
                                elif len(urls) > 0:
                                        media_url = urls[len(urls)-1].text
                        elif child.find('type').text == 'audio' or child.find('type').text == 'audio-bible':
                                urls = child.find('url')
                                if urls.find('ss') != None:
                                        media_url = urls.find('ss').text
                        if media_url != None:
                                if language == "All" and region == "All":
                                        if multilanguage_enabled == "true" or len(child.find('languages')) == 1:
                                                addLink(child.get('name'), media_url, child.find('icon').text, child.find('fanart').text)
                                else:
                                        includes_language = False

                                        for stream_language in child.find('languages'):
                                                stream_language = stream_language.text
                                                if isinstance(stream_language, unicode):
                                                        stream_language = unicodedata.normalize('NFKD', stream_language).encode('ascii', 'ignore')
                                                if stream_language == language:
                                                        includes_language = True
                                                        break

                                        if (includes_language or language == "All") and (child.find('region').text == region or region == "All"):
                                                if multilanguage_enabled == "true" or len(child.find('languages')) == 1:
                                                        addLink(child.get('name'), media_url, child.find('icon').text, child.find('fanart').text)


def openSettings():
        updateSettings()
        xbmcaddon.Addon(id='plugin.video.livingstreams').openSettings()


def updateSettings():
        settings_file = os.path.join(settings.getAddonInfo('path'), 'resources', 'settings.xml')
        available = {'video-language': "All|English", 'audio-language': "All|English", 'audio-bible-language': "All|English", 'video-region': "All", 'audio-region': "All", 'audio-bible-region': "All"}
        array = {'video-language': [], 'audio-language': [], 'audio-bible-language': [], 'video-region': [], 'audio-region': [], 'audio-bible-region': []}
        settings_tree = ET.parse(settings_file)
        settings_category = settings_tree.getroot()[0]
        root = ET.fromstring(getUrl(streams_url))
        for stream in root:
                language_type = stream.find('type').text+'-language'
                region_type = stream.find('type').text+'-region'

                # Add the region to the array if necessary
                region = stream.find('region').text
                if isinstance(region, unicode):
                        region = unicodedata.normalize('NFKD', region).encode('ascii','ignore')

                already_exists = False
                for item in array[region_type]:
                        if item == region:
                                already_exists = True
                                break

                if not already_exists and region != None:
                        array[region_type].append(region)

                # Add the language to the array if necessary
                already_exists = False
                for language in stream.find('languages'):
                        language = language.text
                        if isinstance(language, unicode):
                                language = unicodedata.normalize('NFKD', language).encode('ascii','ignore')
                        for item in array[language_type]:
                                if item == language:
                                        already_exists = True
                                        break
                        if not already_exists and language != None and language != "English":
                                array[language_type].append(language)


        for option in array:
                array[option] = sorted(array[option], key=str.lower)
                for item in array[option]:
                        available[option] += '|'+item

        i = 0
        for setting in settings_category:
                for option in available:
                        if setting.get('id') == option:
                                settings_category[i].set('values', available[option])
                i = i + 1
        settings_tree.write(settings_file)

##################################################################################################################################

def getUrl(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        return link

##################################################################################################################################

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]

        return param


##################################################################################################################################

def Previous():
        xbmc.executebuiltin('Action(Back)')

##################################################################################################################################

def addDir(name, url, mode, iconimage, folder=True):
        u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok = True
        liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setProperty("Fanart_Image", fanart)
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=folder)
        return ok


##################################################################################################################################

def addLink(name,url,iconimage, fanart):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        liz.setArt({ 'fanart': fanart })
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


params = get_params()
url = None
name = None
iconimage = None
mode = None

try:
        url = urllib.unquote_plus(params["url"])
except:
        pass
try:
        name = urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage = urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode = int(params["mode"])
except:
        pass

# xbmc.log("Mode: "+str(mode))
# xbmc.log("URL: "+str(url))
# xbmc.log("Name: "+str(name))

if mode == None:
        MAIN()
elif mode == 1:
        addLinks("video")
elif mode == 2:
        addLinks("audio")
elif mode == 3:
        addLinks("audio-bible")
elif mode == 4:
        openSettings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
