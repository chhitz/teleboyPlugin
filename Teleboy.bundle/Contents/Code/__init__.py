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

def mapLanguagePrefs(languageSelection):
    if languageSelection == 'All channels':
        return 'all'
    elif languageSelection == 'German channels':
        return 'de'
    elif languageSelection == 'French channels':
        return 'fr'
    elif languageSelection == 'Italien channels':
        return 'it'
    elif languageSelection == 'English channels':
        return 'en'
    else:
        return ''

def VideoMainMenu():
    dir = MediaContainer(viewGroup="InfoList")
    
    response = HTTP.Request(VIDEO_URL_BASE + "/layer/login.php", values={'login': Prefs['username'], 'password': Prefs['password']})
    #Log(response)
    #Log(Prefs['channels'])
    #Log(mapLanguagePrefs(Prefs['channels']))
    
    response = HTML.ElementFromURL(VIDEO_URL_BASE + "/tv/player/includes/ajax.php", values={'cmd': 'getStations', 'category': mapLanguagePrefs(Prefs['channels'])})
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
            dir.Append(WebVideoItem(VIDEO_URL_BASE + "/tv/player/player.php?station_id=%d" % stationId, title=name, thumb=R("Logos/%d.png" % stationId), art=R("Logos/%d.png" % stationId), summary=summary))

    dir.Append(
        PrefsItem(
            title=L('Preferences'),
            summary=L('Set your login credentials'),
            thumb=R(ICON)
        )
    )

    # ... and then return the container
    return dir
