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
video_streams = os.path.join(settings.getAddonInfo('path'), 'video_streams.xml')
audio_streams = os.path.join(settings.getAddonInfo('path'), 'audio_streams.xml')
icon = os.path.join(settings.getAddonInfo('path'), 'icon.png')
play = addon.queries.get('play', None)


def MAIN():
        addDir('Video Streams', video_streams, 1, '')
        addDir('Audio Streams', audio_streams, 1, '')
        addDir('Settings', '', 2, '', False)
##################################################################################################################################

def addLinks():
        tree = ET.parse(url)
        root = tree.getroot()
        media_type = root.get('type')
        language = settings.getSetting("language")
        region = settings.getSetting("region")
        xbmc.log("region = "+region)
        quality = settings.getSetting("quality")
        quality = quality.lower()
        xbmc.log("quality = "+quality)
        for child in root:
                if media_type == 'video':
                        urls = child.find('url')
                        media_url = urls.find(quality).text
                elif media_type == 'audio':
                        media_url = child.find('url').text
                if language == "All" and region == "All":
                        addLink(child.get('name'), media_url, child.find('icon').text)
                else:
                        if (child.find('language').text == language or language == "All") and (child.find('region').text == region or region == "All"):
                                addLink(child.get('name'), media_url, child.find('icon').text)




def openSettings():
        xbmcaddon.Addon(id='plugin.video.livingstreams').openSettings()
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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
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

xbmc.log("Mode: "+str(mode))
xbmc.log("URL: "+str(url))
xbmc.log("Name: "+str(name))

if mode == None:
        xbmc.log("")
        MAIN()
elif mode == 1:
        addLinks()
elif mode == 2:
        openSettings()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
