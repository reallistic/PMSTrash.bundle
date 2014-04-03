####################################################################################################

PREFIX  = '/video/pmstrash'
NAME    = 'PMS Trash'

ART     = 'art-default.jpg'
ICON    = 'icon-default.png'
PMS_URL = 'http://%s/library/sections/'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler(PREFIX, MainMenu, NAME, ICON, ART)
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
    
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = 'List'
    DirectoryItem.thumb = R(ICON)
    PopupDirectoryItem.thumb = R(ICON)

####################################################################################################

def MainMenu():
    dir = MediaContainer(noCache=True)

    try:
      sections = XML.ElementFromURL(GetPmsHost(), errors='ignore').xpath('//Directory')
      for section in sections:
          key = section.get('key')
          title = section.get('title')
          dir.Append(Function(DirectoryItem(ViewTrash, title=title, subtitle="subtitle", summary="this is a summary", thumb=R(ICON), art=R(ART)), title=title, key=key))

    except:
      dir.header = 'Couldn\'t find PMS instance'
      dir.message = 'Add or update the address of PMS in the plugin\'s preferences'

    dir.Append(PrefsItem('Preferences', thumb=R('icon-prefs.png')))

    return dir

####################################################################################################

def ViewTrash(sender, title, key):
    dir = MediaContainer(viewGroup='InfoList',noCache=True)

    try:
      trashvideos = XML.ElementFromURL(GetPmsHost() + key + '/all', errors='ignore').xpath('//Video[@deletedAt]')
      for trashvideo in trashvideos:
          trashkey = trashvideo.get('key')
          trashtitle = trashvideo.get('title')
          trashthumb = trashvideo.get('thumb')
          trashpaths = trashvideo.xpath('.//Part')
          trashfiles = ''
          for trashpath in trashpaths:
              trashfiles = trashfiles + trashpath.get('file') + '\n'
          
          dir.Append(DirectoryItem(trashkey, title=trashtitle, summary=trashfiles, thumb=trashthumb))

    except:
      dir.header = title + ' trash empty'
      dir.message = 'Section [' + title + '] is empty and does not contain any items'

    if len(dir) == 0:
      dir.header = title + ' trash empty'
      dir.message = 'Section [' + title + '] is empty and does not contain any items'
 
    return dir

####################################################################################################

def GetPmsHost():
  host = Prefs['host']

  if host.find(':') == -1:
    host += ':32400'

  return PMS_URL % (host)
