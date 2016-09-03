import urllib
import urllib2
import xbmcplugin
import xbmcgui
import xbmcaddon
import os
import re
import sys
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
        addDir('Video Streams', streams_url, 1, '')
        addDir('Audio Streams', streams_url, 2, '')
        addDir('Settings', '', 3, '', False)
##################################################################################################################################

def addLinks(link_type):
        root = ET.fromstring(getUrl(streams_url))
        language = settings.getSetting("language")
        region = settings.getSetting("region")
        # xbmc.log("region = "+region)
        quality = settings.getSetting("quality")
        quality = quality.lower()
        # xbmc.log("quality = "+quality)
        i = 1
        for child in root:
                i = i +1
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
                        elif child.find('type').text == 'audio':
                                urls = child.find('url')
                                if urls.find('ss') != None:
                                        media_url = urls.find('ss').text
                        if media_url != None:
                                if language == "All" and region == "All":
                                        addLink(child.get('name'), media_url, child.find('icon').text, child.find('fanart').text)
                                else:
                                        if (child.find('language').text == language or language == "All") and (child.find('region').text == region or region == "All"):
                                                addLink(child.get('name'), media_url, child.find('icon').text, child.find('fanart').text)


def openSettings():
        updateSettings()
        xbmcaddon.Addon(id='plugin.video.livingstreams').openSettings()


def updateSettings():
        settings_file = os.path.join(settings.getAddonInfo('path'), 'resources', 'settings.xml')
        available = {'language': "All", 'region': "All"}
        array = {'language': [], 'region': []}
        language_array = []
        region_array = []
        settings_tree = ET.parse(settings_file)
        settings_category = settings_tree.getroot()[0]
        root = ET.fromstring(getUrl(streams_url))
        for stream in root:
                options = {'language': stream.find('language').text, 'region': stream.find('region').text}
                for option in options:
                        already_exists = False
                        for item in array[option]:
                                if item == options[option]:
                                        already_exists = True
                                        break
                        if not already_exists and options[option] != None:
                                array[option].append(options[option])

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
        openSettings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
