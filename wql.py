import requests
import json

f = open("nicknames.config","r")
nicknames = json.loads(f.read())
f.close()

class device:
	name = ""
	ipaddr = ""
	macaddr = ""
	connection = ""
	nickname = ""
	def __init__(self, n, i, m, c):
		self.name = n
		self.ipaddr = i
		self.macaddr = m
		self.connection = c
		try:
			self.nickname = nicknames[m]			#
		except:
			self.nickname = "Unknown"
	def printDev(self):						# this is for CLI usage
		print("[{}]\t{}\t[IP: {},\tMAC: {}]".format(self.connection, self.nickname, self.ipaddr, self.macaddr))

class httpHandler:
	session = None
	loginURL = ""
	queryURL = ""
	user=""
	pwd=""
	HEADER = {}
	deviceLst = []
	def __init__(self):
		self.session = requests.Session()
	def setData(self, log, qur, use, pas):
		self.loginURL = log
		self.queryURL = qur
		self.user = use
		self.pwd = pas
	def constructHeader(self, uuid):
		self.HEADER = {'userid':uuid}
	def login(self):
		PARAMS = {
		'user':self.user,
		'pwd':self.pwd,
		'rememberMe':"0",
		'pwdCookieFlag':"0"
		}
		resp = self.session.post(url=self.loginURL, data=PARAMS)
	def reqData(self):
		self.login()
		self.constructHeader(self.session.cookies['userid'])
		self.deviceLst = []
		PARAMS = {
			'_':'1581557043808'
			}
		resp = self.session.get(url=self.queryURL, params=PARAMS, headers=self.HEADER)
		content = json.loads(resp.text)
		for i in range(len(content)):
			self.deviceLst.append(device(content[i]['hostName'],content[i]['ipAddr'],content[i]['macAddr'],content[i]['interface']))
		return self.deviceLst


