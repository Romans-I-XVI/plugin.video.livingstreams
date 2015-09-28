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
import urlresolver


addon = Addon('plugin.video.livingstreams', sys.argv)
net = Net()
settings = xbmcaddon.Addon( id = 'plugin.video.creationtoday_org' )
fanart = os.path.join( settings.getAddonInfo( 'path' ), 'fanart.jpg' )
icon = os.path.join( settings.getAddonInfo( 'path' ), 'icon.png' )
play = addon.queries.get('play', None)


def MAIN():
	addDir('Title', 'URL',Mode As Int,'')
##################################################################################################################################


if play:
	url = addon.queries.get('url', '')
	host = addon.queries.get('host', '')
	media_id = addon.queries.get('media_id', '')
	stream_url = urlresolver.HostedMediaFile(url=url, host=host, media_id=media_id).resolve()
	addon.resolve_url(stream_url)

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

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
	liz.setProperty( "Fanart_Image", fanart )
        xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

##################################################################################################################################
        
              
params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

xbmc.log("Mode: "+str(mode))
xbmc.log("URL: "+str(url))
xbmc.log("Name: "+str(name))

if mode==None or url==None or len(url)<1:
        xbmc.log ("")
        MAIN()



xbmcplugin.endOfDirectory(int(sys.argv[1]))





