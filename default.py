#WSHH - by r0tt 2013. V0.0.1

import urllib,urllib2,re,string,xbmcaddon,xbmcplugin,xbmcgui,socket,sys,os

if sys.version_info < (2, 7):
    import json as simplejson
else:
    import simplejson

timeout = 25
socket.setdefaulttimeout(timeout)
pluginhandle = int(sys.argv[1])

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer
 
addon=xbmcaddon.Addon('plugin.video.wshh')
scriptpath=addon.getAddonInfo('path')
q=scriptpath+'/icon.png'
ua='Mozilla/5.0 (X11; Linux x86_64; rv:18.0) Gecko/18.0 Firefox/18.0'
base = 'http://www.worldstarhiphop.com/videos/index.php?start='
x='0'
p='&limit=15'
        
def INDEX():
		url=base+x+p
		req=urllib2.Request(url)
		req.add_header('User-Agent', ua)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		page=str(re.compile('<strong>(\d{1,3})</strong>&').findall(link)).strip("['']")
		if int(page) == 1:
			pageurl = base + str((int(page)+1)*15-15) + p
			addDir("Next Page >>>>> " + str(int(page)+1), pageurl, 1, "")
		else:
			pageurl = base + str((int(page)+1)*15-15) + p
			addDir("Next Page >>>>> " + str(int(page)+1), pageurl, 1, "")
			pageurl1 = base + str((int(page)-1)*15-15) + p
			addDir(str(int(page)-1) + " <<<<< Previous Page", pageurl, 1, "")
		title=re.compile('\">(.+?)</b></a>').findall(link)
		video1=re.compile('<td align=\"center\" valign=\"top\"><a href=\"(.+?)\">').findall(link)
		video=['http://www.worldstarhiphop.com'+li for li in video1]
		thumb=re.compile('<img src=\"(.+?)\" width=\"200\" height=\"151\" vspace=\"5\" />').findall(link)
		match=zip(title, video, thumb)
		for name,url,thumb in match:
			name = name.replace("&#39;","'").replace("&#039;","'").replace("&amp;","&").replace('&quot;','"')
			addDir(name,url,2,thumb)
		xbmcplugin.endOfDirectory(pluginhandle)

def VIDEOLINKS(url,name):
		req = urllib2.Request(url)
		req.add_header('User-Agent', ua)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		match=re.compile('so\.addVariable\(\"file\"\,\"(.+?)\"\);').findall(link)
		video3=str(re.compile('http://(.+?)/').findall(str(match))).strip("[']")
		video4=re.compile('http://www.youtube.com/v/(.*)').findall(str(match))
		if video3 in ['www.youtube.com']:
			Vid=str(video4).strip('["\']')
			url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=%s' % Vid
			addLink(name,url,'')
			action = ''
			xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		else:
			for url in match:
				addLink(name,url,'')
				xbmc.executebuiltin("xbmc.PlayMedia("+url+")")
		xbmcplugin.endOfDirectory(pluginhandle)

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

def addLink(name,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok

def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
                  
params=get_params()
url=None
name=None
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
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
		print ""
		INDEX()
       
elif mode==1:
		print ""+url
		INDEX(url)
        
elif mode==2:
		print ""+url
		VIDEOLINKS(url,name)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

