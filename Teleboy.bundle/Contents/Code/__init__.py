# PMS plugin framework
from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *

####################################################################################################

VIDEO_PREFIX = "/video/teleboy"
VIDEO_URL_BASE = "http://www.teleboy.ch"

NAME = L('Title')

# make sure to replace artwork with what you want
# these filenames reference the example files in
# the Contents/Resources/ folder in the bundle
ART           = 'art-default.png'
ICON          = 'icon-default.png'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('VideoTitle'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def VideoMainMenu():
    dir = MediaContainer(viewGroup="InfoList")
    
    response = XML.ElementFromURL(VIDEO_URL_BASE + "/tv/player/includes/ajax.php", isHTML=True, values={'cmd': 'getStations', 'category': 'de'}, cacheTime=5*60)
    #Log(XML.StringFromElement(response))
    i=0
    part = 0
    summary = ""
    name = ""
    thumb = ""
    for channel in response.xpath('//div[@class="epgdetail_content"]/table/tr'):
        #Log(XML.StringFromElement(channel))
        if part == 0:
            part = 1
            if i > 2:
                break
            summary = channel.findtext('.//span[@class="begintime"]') + " - " + channel.findtext('.//span[@class="endtime"]')
        
        elif part == 1:
            part = 2
            summary += " " + channel.findtext('td[@class="title"]') + ": "
            thumbElement = channel.find('td[@class="logo"]')
            name = thumbElement.find('img').get('title')
            thumb = thumbElement.find('img').get('src')

        
        elif part == 2:
            part = 0
            summary += channel.findtext('.//p[@class="info_long"]') if channel.findtext('.//p[@class="info_long"]') else ""
            stationId = int(thumb.split('/')[3])
            dir.Append(WebVideoItem(VIDEO_URL_BASE + "/tv/player/player.php?station_id=%d" % stationId, title=name, thumb=thumb, summary=summary))

    # ... and then return the container
    return dir
