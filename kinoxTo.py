from imports import *
from decrypt import *

def kxListEntry(entry):
	png = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/%s.png" % entry[4]
	flag = LoadPixmap(png)
	return [entry,
		(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 20, 5, 16, 11, flag),
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
def kxStreamListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 230, 25, 0, RT_HALIGN_LEFT, entry[0]),
		(eListboxPythonMultiContent.TYPE_TEXT, 270, 0, 120, 25, 0, RT_HALIGN_LEFT, entry[2]),
		(eListboxPythonMultiContent.TYPE_TEXT, 390, 0, 130, 25, 0, RT_HALIGN_LEFT, entry[3]),
		(eListboxPythonMultiContent.TYPE_TEXT, 520, 0, 150, 25, 0, RT_HALIGN_LEFT, entry[4])
		]
def kxMainListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 20, 0, 860, 25, 0, RT_HALIGN_CENTER, entry[0])
		]
def kxPartsListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_CENTER, entry[0])
		]
def kxList2Entry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
def kxWatchedListEntry(entry):
	if entry[2]:
		png = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/watched.png"
		watched = LoadPixmap(png)
		return [entry,
			(eListboxPythonMultiContent.TYPE_PIXMAP_ALPHATEST, 39, 3, 100, 22, watched),
			(eListboxPythonMultiContent.TYPE_TEXT, 100, 0, 700, 25, 0, RT_HALIGN_LEFT, entry[0])
			]
	else:
		return [entry,
			(eListboxPythonMultiContent.TYPE_TEXT, 100, 0, 700, 25, 0, RT_HALIGN_LEFT, entry[0])
			]
def kxLetterEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_CENTER, entry)
		]
def kxWatchSeriesListEntry(entry):
	return [entry,
		(eListboxPythonMultiContent.TYPE_TEXT, 50, 0, 830, 25, 0, RT_HALIGN_LEFT, entry[0])
		]
class kxMain(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("M e n u")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("Genre auswahl")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = False
		self.onLayoutFinish.append(self.layoutFinished)
		
	def layoutFinished(self):
		lt = localtime()
		self.currentdatum = strftime("%d.%m.%Y", lt)
		self.neuste_kino = "Frisches aus dem Kino vom %s" % self.currentdatum
		self.neuste_online = "Neue Filme online vom %s" % self.currentdatum
		self.keyLocked = True
		self.streamList.append((self.neuste_kino, "http://kinox.to"))
		self.streamList.append((self.neuste_online, "http://kinox.to"))
		self.streamList.append(("Kinofilme", "http://kinox.to/Cine-Films.html"))
		self.streamList.append(("Filme A-Z", "dump"))
		self.streamList.append(("Serien A-Z","dump"))
		self.streamList.append(("Neuste Serien", "http://kinox.to/Latest-Series.html"))
		self.streamList.append(("Watchlist","dump"))
		self.streamMenuList.setList(map(kxMainListEntry, self.streamList))
		self.keyLocked = False
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0][0]
		url = self['streamlist'].getCurrent()[0][1]
		print auswahl
		if auswahl == "Kinofilme":
			self.session.open(kxKino, url)
		elif auswahl == self.neuste_kino:
			self.session.open(kxNeusteKino, url)
		elif auswahl == self.neuste_online:
			self.session.open(kxNeusteOnline, url)
		elif auswahl == "Filme A-Z":
			self.session.open(kxABC, url)
		elif auswahl == "Serien A-Z":
			self.session.open(kxSerienABC, url)
		elif auswahl == "Neuste Serien":
			self.session.open(kxNeusteSerien, url)
		elif auswahl == "Watchlist":
			self.session.open(kxWatchlist)
			
	def keyCancel(self):
		self.close()

class kxKino(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, kxGotLink):
		self.kxGotLink = kxGotLink
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("KinoFilme")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		#self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		getPage(self.kxGotLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		kxMovies = re.findall('<div class="Opt leftOpt Headlne"><a title=".*?" href="(.*?)"><h1>(.*?)</h1></a></div>.*?<div class="Thumb"><img style="width: 70px; height: 100px" src="(.*?)" /></div>.*?<div class="Descriptor">(.*?)</div>.*?src="/gr/sys/lng/(.*?).png"', data, re.S)
		if kxMovies:
			for (kxUrl,kxTitle,kxImage,kxHandlung,kxLang) in kxMovies:
				kxUrl = "http://kinox.to" + kxUrl
				self.streamList.append((decodeHtml(kxTitle),kxUrl,kxImage,kxHandlung,kxLang))
				self.streamMenuList.setList(map(kxListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		filmName = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(filmName)
		coverUrl = self['streamlist'].getCurrent()[0][2]
		handlung = self['streamlist'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(handlung))
		if coverUrl:
			downloadPage(coverUrl, "/tmp/kxIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/kxIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kxIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(kxStreams, auswahl, stream_name)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()
		
	def keyCancel(self):
		self.close()

class kxNeusteKino(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, kxGotLink):
		self.kxGotLink = kxGotLink
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Kinox.to")
		lt = localtime()
		self.currentdatum = strftime("%d.%m.%Y", lt)
		self['leftContentTitle'] = Label("Frisches aus dem Kino vom %s" % self.currentdatum)
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		print self.kxGotLink
		getPage(self.kxGotLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		neuste = re.findall('<div class="Opt leftOpt Headlne"><h1>.*?aus dem Kino vom.*?</h1></div>(.*?)</table>', data, re.S)
		if neuste:
			movies = re.findall('td class="Title"><a href="(.*?)" title=".*?" class="OverlayLabel">(.*?)</a></td>', neuste[0], re.S)
			if movies:
				for (kxUrl,kxTitle) in movies:
					kxUrl = "http://kinox.to" + kxUrl
					print kxTitle, kxUrl
					self.streamList.append((decodeHtml(kxTitle),kxUrl))
					self.streamMenuList.setList(map(kxList2Entry, self.streamList))
				self.keyLocked = False
				self.showInfos()

	def showInfos(self):
		filmName = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(filmName)
		url = self['streamlist'].getCurrent()[0][1]
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getDetails).addErrback(self.dataError)
		
	def getDetails(self, data):
		details = re.findall('<div class="Grahpics">.*?<img src="(.*?)".*?<div class="Descriptore">(.*?)</div>', data, re.S)
		if details:
			for (image, handlung) in details:
				print image
				self['handlung'].setText(decodeHtml(handlung))
				downloadPage(image, "/tmp/kxIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/kxIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kxIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(kxStreams, auswahl, stream_name)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()
		
	def keyCancel(self):
		self.close()
		
class kxNeusteOnline(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, kxGotLink):
		self.kxGotLink = kxGotLink
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Kinox.to")
		lt = localtime()
		self.currentdatum = strftime("%d.%m.%Y", lt)
		self['leftContentTitle'] = Label("Neue Filme online vom %s" % self.currentdatum)
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		print self.kxGotLink
		getPage(self.kxGotLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		neuste = re.findall('<div class="Opt leftOpt Headlne"><h1>.*?Neue Filme online.*?</h1></div>(.*?)</table>', data, re.S)
		if neuste:
			print neuste[0]
			movies = re.findall('td class="Title"><a href="(.*?)" title=".*?" class="OverlayLabel">(.*?)</a></td>', neuste[0], re.S)
			if movies:
				for (kxUrl,kxTitle) in movies:
					kxUrl = "http://kinox.to" + kxUrl
					print kxTitle, kxUrl
					self.streamList.append((decodeHtml(kxTitle),kxUrl))
					self.streamMenuList.setList(map(kxList2Entry, self.streamList))
				self.keyLocked = False
				self.showInfos()

	def showInfos(self):
		filmName = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(filmName)
		url = self['streamlist'].getCurrent()[0][1]
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getDetails).addErrback(self.dataError)
		
	def getDetails(self, data):
		details = re.findall('<div class="Grahpics">.*?<img src="(.*?)".*?<div class="Descriptore">(.*?)</div>', data, re.S)
		if details:
			for (image, handlung) in details:
				print image
				self['handlung'].setText(decodeHtml(handlung))
				downloadPage(image, "/tmp/kxIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/kxIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kxIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(kxStreams, auswahl, stream_name)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()
		
	def keyCancel(self):
		self.close()

class kxABC(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, kxGotLink):
		self.kxGotLink = kxGotLink
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Filme A-Z")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		abc = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
		for letter in abc:
			self.streamList.append((letter))
		self.streamMenuList.setList(map(kxLetterEntry, self.streamList))
		self.keyLocked = False
					
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0]
		print auswahl
		self.session.open(kxABCpage, auswahl)
		
	def keyCancel(self):
		self.close()
		
class kxABCpage(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="850,420" size="45,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />			
			</screen>
		"""
		
	def __init__(self, session, letter):
		self.letter = letter
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Movies #%s" % self.letter)
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("1")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		url = "http://kinox.to/aGET/List/Page="+str(self.page)+"&Per_Page=10&url=%2FaGET%2FList%2F&dir=desc&sort=title&per_page=10&ListMode=cover&additional=%7B%22fType%22%3A%22movie%22%2C%22fLetter%22%3A%22"+self.letter+"%22%7D&iDisplayStart=0&iDisplayLength=10"
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		kxMovies = re.findall('title=."(.*?)" href=."(.*?)".*?<img.*?src=."(.*?)".*?<div class=."Descriptor.">(.*?)<./div>.*?src=.".*?lng.*?/(.*?).pn.*?" alt=."language.">', data, re.S)
		if kxMovies:
			for (kxTitle,kxUrl,kxImage,kxHandlung,kxLang) in kxMovies:
				kxUrl = "http://kinox.to" + kxUrl.replace('\\','')
				self.streamList.append((decodeHtml(kxTitle.replace('\\','')),kxUrl,kxImage.replace('\\',''),kxHandlung,kxLang))
				self.streamMenuList.setList(map(kxListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()
		else:
			self['page'].setText("END")

	def showInfos(self):
		filmName = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(filmName)
		self['page'].setText(str(self.page))
		coverUrl = self['streamlist'].getCurrent()[0][2]
		handlung = self['streamlist'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(handlung))
		if coverUrl:
			downloadPage(coverUrl, "/tmp/kxIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/kxIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kxIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(kxStreams, auswahl, stream_name)
		
	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadPage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
		self.loadPage()
		
	def keyCancel(self):
		self.close()

class kxNeusteSerien(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, kxGotLink):
		self.kxGotLink = kxGotLink
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"green" : self.keyAdd
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Neuste Serien")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		self.keckse = {}
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		#self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		url = "http://kinox.to/aSET/ListMode/cover"
		getPage(url, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.getKeckse).addErrback(self.dataError)
		
	def getKeckse(self, data):
		print self.keckse
		getPage(self.kxGotLink, cookies=self.keckse, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		kxMovies = re.findall('<div class="Opt leftOpt Headlne"><a title=".*?" href="(.*?)"><h1>(.*?)</h1></a></div>.*?<div class="Thumb"><img style="width: 70px; height: 100px" src="(.*?)" /></div>.*?<div class="Descriptor">(.*?)</div>.*?src="/gr/sys/lng/(.*?).png"', data, re.S)
		if kxMovies:
			for (kxUrl,kxTitle,kxImage,kxHandlung,kxLang) in kxMovies:
				kxUrl = "http://kinox.to" + kxUrl
				self.streamList.append((decodeHtml(kxTitle),kxUrl,kxImage,kxHandlung,kxLang))
				self.streamMenuList.setList(map(kxListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()

	def showInfos(self):
		filmName = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(filmName)
		coverUrl = self['streamlist'].getCurrent()[0][2]
		handlung = self['streamlist'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(handlung))
		if coverUrl:
			downloadPage(coverUrl, "/tmp/kxIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/kxIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kxIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(kxEpisoden, auswahl, stream_name)

	def keyAdd(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		muTitle = self['streamlist'].getCurrent()[0][0]
		muID = self['streamlist'].getCurrent()[0][1]
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/kx_watchlist"
		if fileExists(path):
			writePlaylist = open(path,"a")
			writePlaylist.write('"%s" "%s"\n' % (muTitle, muID))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("Serie wurde zur watchlist hinzugefuegt."), MessageBox.TYPE_INFO, timeout=3)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()
		
	def keyCancel(self):
		self.close()
		
class kxSerienABC(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, kxGotLink):
		self.kxGotLink = kxGotLink
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Serien A-Z")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		abc = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","0","1","2","3","4","5","6","7","8","9"]
		for letter in abc:
			self.streamList.append((letter))
		self.streamMenuList.setList(map(kxLetterEntry, self.streamList))
		self.keyLocked = False
					
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		auswahl = self['streamlist'].getCurrent()[0]
		print auswahl
		self.session.open(kxSerienABCpage, auswahl)
		
	def keyCancel(self):
		self.close()
		
class kxSerienABCpage(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
			<eLabel text="Page" position="750,420" size="100,25" backgroundColor="#00101214" transparent="1" foregroundColor="#00555556" font="Regular;20" valign="top" />
			<widget name="page" position="850,420" size="45,25" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />			
			</screen>
		"""
		
	def __init__(self, session, letter):
		self.letter = letter
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft,
			"nextBouquet" : self.keyPageUp,
			"prevBouquet" : self.keyPageDown,
			"green" : self.keyAdd
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Serien #%s" % self.letter)
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		self['page'] = Label("1")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.page = 1
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		url = "http://kinox.to/aGET/List/?ListMode=cover&Page="+str(self.page)+"&Per_Page=10&additional=%7B%22fType%22%3A%22series%22%2C%22fLetter%22%3A%22"+self.letter+"%22%7D&dir=desc&iDisplayLength=10&iDisplayStart=0&per_page=10&sort=title&url=%2FaGET%2FList%2F"
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		kxMovies = re.findall('title=."(.*?)" href=."(.*?)".*?<img.*?src=."(.*?)".*?<div class=."Descriptor.">(.*?)<./div>.*?src=.".*?lng.*?/(.*?).pn.*?" alt=."language.">', data, re.S)
		if kxMovies:
			for (kxTitle,kxUrl,kxImage,kxHandlung,kxLang) in kxMovies:
				kxUrl = "http://kinox.to" + kxUrl.replace('\\','')
				self.streamList.append((decodeHtml(kxTitle.replace('\\','')),kxUrl,kxImage.replace('\\',''),kxHandlung,kxLang))
				self.streamMenuList.setList(map(kxListEntry, self.streamList))
			self.keyLocked = False
			self.showInfos()
		else:
			self['page'].setText("END")

	def showInfos(self):
		filmName = self['streamlist'].getCurrent()[0][0]
		self['name'].setText(filmName)
		self['page'].setText(str(self.page))
		coverUrl = self['streamlist'].getCurrent()[0][2]
		handlung = self['streamlist'].getCurrent()[0][3]
		self['handlung'].setText(decodeHtml(handlung))
		if coverUrl:
			downloadPage(coverUrl, "/tmp/kxIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/kxIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kxIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		#self.session.open(kxStreams, auswahl)
		self.session.open(kxEpisoden, auswahl, stream_name)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		self.showInfos()

	def keyPageDown(self):
		print "PageDown"
		if self.keyLocked:
			return
		if not self.page < 2:
			self.page -= 1
			self.loadPage()
		
	def keyPageUp(self):
		print "PageUP"
		if self.keyLocked:
			return
		self.page += 1
		self.loadPage()

	def keyAdd(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		muTitle = self['streamlist'].getCurrent()[0][0]
		muID = self['streamlist'].getCurrent()[0][1]
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/kx_watchlist"
		if fileExists(path):
			writePlaylist = open(path,"a")
			writePlaylist.write('"%s" "%s"\n' % (muTitle, muID))
			writePlaylist.close()
			message = self.session.open(MessageBox, _("Serie wurde zur watchlist hinzugefuegt."), MessageBox.TYPE_INFO, timeout=3)
			
	def keyCancel(self):
		self.close()

class kxEpisoden(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />		
			</screen>
		"""
		
	def __init__(self, session, url, stream_name):
		self.url = url
		self.stream_name = stream_name
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"up" : self.keyUp,
			"down" : self.keyDown,
			"right" : self.keyRight,
			"left" : self.keyLeft
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Season - Episode")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.plugin_path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal"
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		getPage(self.url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
	
		self.watched_liste = []
		self.mark_last_watched = []
		if not fileExists(self.plugin_path+"/kx_watched"):
			os.system("touch "+self.plugin_path+"/kx_watched")
		if fileExists(self.plugin_path+"/kx_watched"):
			leer = os.path.getsize(self.plugin_path+"/kx_watched")
			if not leer == 0:
				self.updates_read = open(self.plugin_path+"/kx_watched" , "r")
				for lines in sorted(self.updates_read.readlines()):
					line = re.findall('"(.*?)"', lines)
					if line:
						self.watched_liste.append("%s" % (line[0]))
				self.updates_read.close()
				
		MirrorByEpisode = "http://kinox.to/aGET/MirrorByEpisode/"
		if re.match('.*rel="\?Addr=', data, re.S):
			id = re.findall('rel="(\?Addr=.*?)"', data, re.S)
			if id:
				staffeln2 = re.findall('<option value="(.*\d)" rel="(.*\d)"', data, re.M)
				if staffeln2:
					for each in staffeln2:
						(staffel, epsall) = each
						eps = re.findall('(\d+)', epsall, re.S)
						#print staffel, eps
						#http://kinox.to/aGET/MirrorByEpisode/?Addr=The_Vampire_Diaries&SeriesID=2403&Season=1&Episode=2
						for episode in eps:
							url_to_streams = "%s%s&Season=%s&Episode=%s" % (MirrorByEpisode, id[0], staffel, episode)
							#print staffel, episode, url_to_streams
							if int(staffel) < 10:
								staffel3 = "S0"+str(staffel)
							else:
								staffel3 = "S"+str(staffel)
								
							if int(episode) < 10:
								episode3 = "E0"+str(episode)
							else:
								episode3 = "E"+str(episode)
								
							self.staffel_episode = "%s%s" % (staffel3, episode3)
							if self.staffel_episode:
								streamname = "%s - %s" % (self.stream_name, self.staffel_episode)
								#check = ("%s %s" % (self.stream_name, streamname))
								if streamname in self.watched_liste:
									self.streamList.append((streamname,url_to_streams,True))
									self.mark_last_watched.append(streamname)
								else:
									self.streamList.append((streamname,url_to_streams,False))
									
						self.streamMenuList.setList(map(kxWatchedListEntry, self.streamList))

						if len(self.mark_last_watched) != 0:
							counting_watched = 0
							for (name,url,watched) in self.streamList:
								counting_watched += 1
								if self.mark_last_watched[-1] == name:
									counting_watched = int(counting_watched) - 1
									print "[kinox] last watched episode: %s" % counting_watched
									break
							self["streamlist"].moveToIndex(int(counting_watched))
							self.keyLocked = False
						else:
							if len(self.streamList) != 0:
								jump_last = len(self.streamList) -1
							else:
								jump_last = 0
							print "[kinox] last episode: %s" % jump_last
							self["streamlist"].moveToIndex(int(jump_last))
							self.keyLocked = False
						

		details = re.findall('<div class="Grahpics">.*?<img src="(.*?)".*?<div class="Descriptore">(.*?)</div>', data, re.S)
		if details:
			for (image, handlung) in details:
				print image
				self['handlung'].setText(decodeHtml(handlung))
				downloadPage(image, "/tmp/kxIcon.jpg").addCallback(self.showCover)
		
	def showCover(self, picData):
		if fileExists("/tmp/kxIcon.jpg"):
			self['stationIcon'].instance.setPixmap(None)
			self.scale = AVSwitch().getFramebufferScale()
			self.picload = ePicLoad()
			size = self['stationIcon'].instance.size()
			self.picload.setPara((size.width(), size.height(), self.scale[0], self.scale[1], False, 1, "#FF000000"))
			if self.picload.startDecode("/tmp/kxIcon.jpg", 0, 0, False) == 0:
				ptr = self.picload.getData()
				if ptr != None:
					self['stationIcon'].instance.setPixmap(ptr.__deref__())
					self['stationIcon'].show()
					del self.picload
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		episode = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		streamname = "%s" % episode
		self.session.open(kxStreams, auswahl, streamname)

	def keyLeft(self):
		if self.keyLocked:
			return
		self['streamlist'].pageUp()
		#self.showInfos()
		
	def keyRight(self):
		if self.keyLocked:
			return
		self['streamlist'].pageDown()
		#self.showInfos()
		
	def keyUp(self):
		if self.keyLocked:
			return
		self['streamlist'].up()
		#self.showInfos()
		
	def keyDown(self):
		if self.keyLocked:
			return
		self['streamlist'].down()
		#self.showInfos()
		
	def keyCancel(self):
		self.close()

class kxWatchlist(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />		
			</screen>
		"""
		
	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel,
			"red" : self.keyDel
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Watchlist")
		self['stationIcon'] = Pixmap()
		self['handlung'] = Label("")
		self['name'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPlaylist)

	def loadPlaylist(self):
		self.streamList = []
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/kx_watchlist"	
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink) = data[0]
					self.streamList.append((stationName, stationLink))
			print "Reload Playlist"
			self.streamList.sort()
			self.streamMenuList.setList(map(kxWatchSeriesListEntry, self.streamList))
			readStations.close()
			self.keyLocked = False
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		stream_name = self['streamlist'].getCurrent()[0][0]
		auswahl = self['streamlist'].getCurrent()[0][1]
		print auswahl
		self.session.open(kxEpisoden, auswahl, stream_name)
			
	def keyDel(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		
		selectedName = self['streamlist'].getCurrent()[0][0]
		pathTmp = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/kx_watchlist.tmp"
		writeTmp = open(pathTmp,"w")	
		path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/kx_watchlist"
		if fileExists(path):
			readStations = open(path,"r")
			for rawData in readStations.readlines():
				data = re.findall('"(.*?)" "(.*?)"', rawData, re.S)
				if data:
					(stationName, stationLink) = data[0]
					if stationName != selectedName:
						writeTmp.write('"%s" "%s"\n' % (stationName, stationLink))
			readStations.close()
			writeTmp.close()
			shutil.move(pathTmp, path)
			self.loadPlaylist()
				
	def keyCancel(self):
		self.close()
		
class kxStreams(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, kxGotLink, stream_name):
		self.kxGotLink = kxGotLink
		self.stream_name = stream_name
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Streams")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.plugin_path = "/usr/lib/enigma2/python/Plugins/Extensions/mediaportal"
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		getPage(self.kxGotLink, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		hosterdump = re.findall('<li id="Hoster(.*?)/li>', data, re.S)
		if hosterdump:
			self.streamList = []
			self.streamList.append(("Hoster", "nix", "Mirror", "Hits", "Date"))
			for each in hosterdump:
				if re.match('.*?Mirror', each):
					hosters = re.findall('rel="(.*?)".*?<div class="Named">(.*?)</div>.*?<div class="Data"><b>Hits</b>\:.(.*?)<b>Mirror</b>\:.(.*?)<br /><b>Vom</b>\:.(.*\d+)</div>',each, re.S)
					if hosters:
						(get_stream_url, hostername, hits, mirror, date)= hosters[0]
						get_stream_url = "http://kinox.to/aGET/Mirror/%s" % get_stream_url.replace('&amp;','&')
						print get_stream_url, hostername, mirror, hits.replace(',','').replace(' ',''), date
						if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx)', hostername, re.S|re.I):
							self.streamList.append((hostername, get_stream_url, mirror, hits.replace(',','').replace(' ',''), date))
				else:
					hosters = re.findall('rel="(.*?)".*?<div class="Named">(.*?)</div>.*?<div class="Data"><b>Hits</b>\:.(.*\d+)<br /><b>Vom</b>\:.(.*\d+)</div>',each, re.S)
					if hosters:
						(get_stream_url, hostername, hits, date)= hosters[0]
						get_stream_url = "http://kinox.to/aGET/Mirror/%s" % get_stream_url.replace('&amp;','&')
						print get_stream_url, hostername, "1", hits, date
						if re.match('.*?(putlocker|sockshare|streamclou|xvidstage|filenuke|movreel|nowvideo|xvidstream|uploadc|vreer|MonsterUploads|Novamov|Videoweed|Divxstage|Ginbig|Flashstrea|Movshare|yesload|faststream|Vidstream|PrimeShare|flashx)', hostername, re.S|re.I):
							self.streamList.append((hostername, get_stream_url, "1", hits, date))
							
			self.streamMenuList.setList(map(kxStreamListEntry, self.streamList))
			self.keyLocked = False
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		url = self['streamlist'].getCurrent()[0][1]
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseStream, url).addErrback(self.dataError)
		
	def parseStream(self, data, url):
		print url
		if re.match('.*?Part', data, re.S):
			print "more parts.."
			urls = []
			urls.append(("Part 1", url+"&Part=1"))
			urls.append(("Part 2", url+"&Part=2"))
			print urls
			self.session.open(kxParts, urls, self.stream_name)
		else:
			print "one parts only.."
			extern_stream_url = re.findall('<a href=."(.*?)"', data, re.S)
			if extern_stream_url:
				stream = extern_stream_url[0].replace('\\','')
				if stream:
					print stream
					get_stream_link(self.session).check_link(stream, self.playfile)

	def playfile(self, stream_url):
		if stream_url != None:
			print stream_url
			if not fileExists(self.plugin_path+"/kx_watched"):
				os.system("touch "+self.plugin_path+"/kx_watched")
				
			self.update_liste = []
			leer = os.path.getsize(self.plugin_path+"/kx_watched")
			if not leer == 0:
				self.updates_read = open(self.plugin_path+"/kx_watched" , "r")
				for lines in sorted(self.updates_read.readlines()):
					line = re.findall('"(.*?)"', lines)
					if line:
						print line[0]
						self.update_liste.append("%s" % (line[0]))
				self.updates_read.close()
				
				updates_read2 = open(self.plugin_path+"/kx_watched" , "a")
				check = ("%s" % self.stream_name)
				if not check in self.update_liste:
					print "[kinox] update add: %s" % (self.stream_name)
					updates_read2.write('"%s"\n' % (self.stream_name))
					updates_read2.close()
				else:
					print "[kinox] dupe %s" % (self.stream_name)
			else:
				updates_read3 = open(self.plugin_path+"/kx_watched" , "a")
				print "[kinox] update add: %s" % (self.stream_name)
				updates_read3.write('"%s"\n' % (self.stream_name))
				updates_read3.close()

			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(self.stream_name)
			self.session.open(MoviePlayer, sref)

	def keyCancel(self):
		self.close()
		
class kxParts(Screen):
	skin = 	"""
		<screen name="Kinox.to" position="center,center" size="900,630" backgroundColor="#00060606" flags="wfNoBorder">
			<eLabel position="0,0" size="900,60" backgroundColor="#00242424" />
			<widget name="title" position="30,10" size="500,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="left" />
			<widget source="global.CurrentTime" render="Label" position="700,00" size="150,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;24" valign="center" halign="right">
				<convert type="ClockToText">Format:%-H:%M</convert>
			</widget>
			<widget source="global.CurrentTime" render="Label" position="450,20" size="400,55" backgroundColor="#18101214" transparent="1" zPosition="1" font="Regular;16" valign="center" halign="right">
				<convert type="ClockToText">Format:%A, %d.%m.%Y</convert>
			</widget>
			<widget name="leftContentTitle" position="0,60" size="900,25" backgroundColor="#00aaaaaa" zPosition="5" foregroundColor="#00000000" font="Regular;22" halign="center"/>
			<widget name="streamlist" position="0,85" size="900,325" backgroundColor="#00101214" scrollbarMode="showOnDemand" transparent="0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/sel.png"/>
			<eLabel position="215,460" size="675,2" backgroundColor="#00555556" />
			<widget name="stationIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/mediaportal/images/no_coverArt.png" position="20,420" size="145,200" transparent="1" alphatest="blend" />
			<widget name="name" position="230,420" size="520,30" foregroundColor="#00e5b243" backgroundColor="#00101214" transparent="1" font="Regular;26" valign="top" />
			<widget name="handlung" position="205,473" size="680,140" backgroundColor="#00101214" transparent="1" font="Regular;20" valign="top" />
	        </screen>
		"""
		
	def __init__(self, session, parts, stream_name):
		self.parts = parts
		self.stream_name = stream_name
		self.session = session
		Screen.__init__(self, session)

		self["actions"]  = ActionMap(["OkCancelActions", "ShortcutActions", "EPGSelectActions", "WizardActions", "ColorActions", "NumberActions", "MenuActions", "MoviePlayerActions", "InfobarSeekActions"], {
			"ok"    : self.keyOK,
			"cancel": self.keyCancel
		}, -1)
		
		self['title'] = Label("Kinox.to")
		self['leftContentTitle'] = Label("Parts")
		self['stationIcon'] = Pixmap()
		self['name'] = Label("")
		self['handlung'] = Label("")
		
		self.streamList = []
		self.streamMenuList = MenuList([], enableWrapAround=True, content=eListboxPythonMultiContent)
		self.streamMenuList.l.setFont(0, gFont('Regular', 24))
		self.streamMenuList.l.setItemHeight(25)
		self['streamlist'] = self.streamMenuList
		
		self.keyLocked = True
		self.onLayoutFinish.append(self.loadPage)
		
	def loadPage(self):
		self.streamList = []
		for (partName, partUrl) in self.parts:
			self.streamList.append((partName, partUrl))
		self.streamMenuList.setList(map(kxPartsListEntry, self.streamList))
		self.keyLocked = False
					
	def dataError(self, error):
		print error
			
	def keyOK(self):
		exist = self['streamlist'].getCurrent()
		if self.keyLocked or exist == None:
			return
		url = self['streamlist'].getCurrent()[0][1]
		print url
		getPage(url, headers={'Content-Type':'application/x-www-form-urlencoded'}).addCallback(self.parseData).addErrback(self.dataError)
		
	def parseData(self, data):
		extern_stream_url = re.findall('<a href=."(.*?)"', data, re.S)
		if extern_stream_url:
			stream = extern_stream_url[0].replace('\\','')
			if stream:
				print stream
				get_stream_link(self.session).check_link(stream, self.playfile)

	def playfile(self, stream_url):
		if stream_url != None:
			part = self['streamlist'].getCurrent()[0][0]
			streamname = "%s - %s" % (self.stream_name ,part)
			print stream_url, streamname
			sref = eServiceReference(0x1001, 0, stream_url)
			sref.setName(streamname)
			self.session.open(MoviePlayer, sref)
			
	def keyCancel(self):
		self.close()