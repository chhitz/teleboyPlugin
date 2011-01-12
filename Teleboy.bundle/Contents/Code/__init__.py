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
    Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, L('Title'), ICON, ART)

    Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
    Plugin.AddViewGroup("List", viewMode="List", mediaType="items")

    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    DirectoryItem.thumb = R(ICON)

def languagePrefs():
    lang = list()
    if Prefs['channels_de']:
        lang.append('de')
    if Prefs['channels_fr']:
        lang.append('fr')
    if Prefs['channels_it']:
        lang.append('it')
    if Prefs['channels_en']:
        lang.append('en')
    return lang

def VideoMainMenu():
    dir = MediaContainer(viewGroup="InfoList")
    
    response = HTTP.Request(VIDEO_URL_BASE + "/layer/login.php", values={'login': Prefs['username'], 'password': Prefs['password']})
    #Log(response)
    #Log(Prefs['channels'])
    #Log(mapLanguagePrefs(Prefs['channels']))
    
    for lang in languagePrefs():
        response = HTML.ElementFromURL(VIDEO_URL_BASE + "/tv/player/includes/ajax.php", values={'cmd': 'getStations', 'category': lang})
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
                summary += " - " + channel.findtext('td[@class="title"]') + "\n"
                thumbElement = channel.find('td[@class="logo"]')
                name = thumbElement.find('img').get('title')
                thumb = thumbElement.find('img').get('src')
            
            elif part == 2:
                part = 0
                summary += channel.findtext('.//p[@class="info_long"]') if channel.findtext('.//p[@class="info_long"]') else ""
                stationId = int(thumb.split('/')[3])
                staticThumb = R("Logos/%d.png" % stationId)
                if staticThumb:
                    thumb = staticThumb
                else:
                    thumb = VIDEO_URL_BASE + thumb
                dir.Append(WebVideoItem(VIDEO_URL_BASE + "/tv/player/player.php?station_id=%d" % stationId, title=name, thumb=thumb, summary=summary))

    dir.Append(
        PrefsItem(
            title=L('Preferences'),
            summary=L('Set your login credentials'),
            thumb=R("icon-prefs.png")
        )
    )

    # ... and then return the container
    return dir
