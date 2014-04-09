####################################################################################################

PREFIX  = '/applications/pmstrash'
NAME    = 'PMS Trash'

ART     = 'art-default.jpg'
ICON    = 'icon-default.png'
PMS_URL = 'http://%s/library/sections/'
PMS_BASEURL = 'http://%s'

####################################################################################################

def Start():
    Plugin.AddPrefixHandler(PREFIX, MainMenu, NAME, ICON, ART)
    Plugin.AddViewGroup('List', viewMode='List', mediaType='items')
    Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')
    
    MediaContainer.art = R(ART)
    MediaContainer.title1 = NAME
    MediaContainer.viewGroup = 'List'
    DirectoryItem.thumb = R(ICON)
    DirectoryObject.thumb = R(ICON)
    PopupDirectoryItem.thumb = R(ICON)
    ObjectContainer.title1 = L(NAME)
    ObjectContainer.art = R(ART)
    DirectoryObject.thumb = R(ICON)
    DirectoryObject.art = R(ART)

####################################################################################################
@handler(PREFIX, NAME, thumb=ICON, art=ART)
def MainMenu(view_group="InfoList"):
   dir = ObjectContainer()

    #try:
   sections = XML.ElementFromURL(GetPmsHost(), errors='ignore').xpath('//Directory')
   for section in sections:
       key = section.get('key')
       title = section.get('title')
       type = section.get('type')
       summary = "Check the trash for section %s" % title
       if type == "show":
           dir.add(DirectoryObject(key=Callback(ViewTvTrash, title=title, key=key), title=title, summary=summary, thumb=R(ICON), art=R(ART)))
       elif type == "artist":
           dir.add(DirectoryObject(key=Callback(ViewMusicTrash, title=title, key=key), title=title, summary=summary, thumb=R(ICON), art=R(ART)))
       elif type == "movie":
           dir.add(DirectoryObject(key=Callback(ViewMovieTrash, title=title, key=key), title=title, summary=summary, thumb=R(ICON), art=R(ART)))
       else:
           dir.add(DirectoryObject(key=Callback(NotAvailable), title=title, summary=summary, thumb=R(ICON), art=R(ART)))

    #except:
    #  dir.header = 'Couldn\'t find PMS instance'
    #  dir.message = 'Add or update the address of PMS in the plugin\'s preferences'

    #dir.add(PrefsObject('Preferences', thumb=R('icon-prefs.png')))
   dir.add(PrefsObject(title="Preferences", summary="Set PMS Trash preferences", thumb=R('icon-prefs.png')))

   return dir

####################################################################################################
@route(PREFIX + '/MovieTrash')
def ViewMovieTrash(title, key):
    dir = ObjectContainer(title2="Movie Trash")

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
          
          dir.add(DirectoryObject(key=trashkey, title=trashtitle, summary=trashfiles, thumb=trashthumb))

    except:
      dir.header = title + ' trash empty'
      dir.message = 'Trash for section [' + title + '] is empty'

    if len(dir) == 0:
      dir.header = title + ' trash empty'
      dir.message = 'Trash for section [' + title + '] is empty'
 
    return dir

####################################################################################################
@route(PREFIX + '/TVTrash')
def ViewTvTrash(title, key):
   dir = ObjectContainer(title2="TV Trash", no_cache=True)
    #try:
   trashvideos = XML.ElementFromURL(GetPmsHost() + key + '/all', errors='ignore').xpath('//Directory[@deletedAt]')
   for trashvideo in trashvideos:
       trashkey = trashvideo.get('key')
       trashtitle = trashvideo.get('title')
       Log("Found Show %s" % trashtitle)
       trashseasons = XML.ElementFromURL(GetBasePmsHost() + trashkey, errors='ignore').xpath('//Directory[@deletedAt]')
       Log("[debug] Requesting - %s" % GetBasePmsHost() + trashkey)
       for trashseason in trashseasons:
           trashskey = trashseason.get('key')
           trashstitle = trashseason.get('title')
           #trasheps = XML.ElementFromURL(GetBasePmsHost() + trashskey, errors='ignore').xpath('//Video[@deletedAt]')
           trasheps = XML.ElementFromURL(GetBasePmsHost() + trashskey, errors='ignore').xpath('//Video')
           Log("[debug] Requesting - %s" % GetBasePmsHost() + trashskey)
           for trashep in trasheps:
               if len(trashep.xpath('./Media[@deletedAt]')) == 0 and len(trashep.xpath('.[@deletedAt]')) ==0:
                  continue
               trasheptitle = trashep.get('title')
               trashepkey = trashep.get('key')
               trashepsumm = trashep.get('summary')
               trashepthumb = trashep.get('thumb')
               Log("[debug] Adding - %s" % trasheptitle)
               dirtitle = trashtitle + " - " + trashstitle + " - " + trasheptitle
               dir.add(DirectoryObject(key=trashepkey, title=dirtitle, summary=trashepsumm,
                  thumb=Resource.ContentsOfURLWithFallback(url=trashepthumb, fallback=R(ICON))))
   if len(dir) == 0:
      dir.add(DirectoryObject(key=Callback(DirectoryEmpty), title="Empty", summary="There are no items to display", thumb=R(ICON)))
    #except:
    #  Log("[debug] Error in for loop")
    #  dir.header = title + ' trash empty'
    #  dir.message = 'Error - Trash for section [' + title + '] is empty'
 
   return dir

####################################################################################################
@route(PREFIX + '/MusicTrash')
def ViewMusicTrash(title, key):
   dir = ObjectContainer(title2="Music Trash", no_cache=True)
    #try:
   trashvideos = XML.ElementFromURL(GetPmsHost() + key + '/all', errors='ignore').xpath('//Directory[@deletedAt]')
   for trashvideo in trashvideos:
       trashkey = trashvideo.get('key')
       trashtitle = trashvideo.get('title')
       Log("Found Artist %s" % trashtitle)
       trashseasons = XML.ElementFromURL(GetBasePmsHost() + trashkey, errors='ignore').xpath('//Directory[@deletedAt]')
       Log("[debug] Requesting - %s" % GetBasePmsHost() + trashkey)
       for trashseason in trashseasons:
           trashskey = trashseason.get('key')
           trashstitle = trashseason.get('title')
           trasheps = XML.ElementFromURL(GetBasePmsHost() + trashskey, errors='ignore').xpath('//Track')
           Log("[debug] Requesting - %s" % GetBasePmsHost() + trashskey)
           for trashep in trasheps:
               try:
                  deldate = trashep.get("deletedAt")
               except:
                  deldate = None

               if deldate != None or len(trashep.xpath('./Media[@deletedAt]')) > 0:
                  trasheptitle = trashep.get('title')
                  trashepkey = trashep.get('key')
                  trashepsumm = trashep.get('summary')
                  trashepthumb = trashep.get('thumb')
                  Log("[debug] Adding - %s" % trasheptitle)
                  dirtitle = trashtitle + " - " + trashstitle + " - " + trasheptitle
                  dir.add(DirectoryObject(key=trashepkey, title=dirtitle, summary=trashepsumm,
                     thumb=Resource.ContentsOfURLWithFallback(url=trashepthumb, fallback=R(ICON))))
   if len(dir) == 0:
      dir.add(DirectoryObject(key=Callback(DirectoryEmpty), title="Empty", summary="There are no items to display", thumb=R(ICON)))
    #except:
    #  Log("[debug] Error in for loop")
    #  dir.header = title + ' trash empty'
    #  dir.message = 'Error - Trash for section [' + title + '] is empty'
 
   return dir


####################################################################################################

def NotAvailable():
    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

    return MessageContainer(
        "Not Available",
        "This type of section is not yet implemented"
    )
####################################################################################################

def DirectoryEmpty():
    ## you might want to try making me return a MediaContainer
    ## containing a list of DirectoryItems to see what happens =)

    return MessageContainer(
        "This is empty",
        "There are no items to display here"
    )

####################################################################################################

def GetBasePmsHost():
  host = Prefs['host']
  if host.find(':') == -1:
    host += ':32400'
  return PMS_BASEURL % (host)

####################################################################################################

def GetPmsHost():
  host = Prefs['host']

  if host.find(':') == -1:
    host += ':32400'
  return PMS_URL % (host)