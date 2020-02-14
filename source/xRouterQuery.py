import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import wql
import json
import os
 
dirpath = os.path.dirname(os.path.abspath(__file__))
dirpath = dirpath + "/config/routerinfo.config"

######################	 WQL	 ######################

wifi = wql.httpHandler()

###################### LOAD CONFIG ######################
def load(location):
	f = open(dirpath, 'r')
	contents = json.loads(f.read())
	f.close()
	for i in contents:
		if i['location']==location:
			wifi.setData(i['loginurl'],i['connectionurl'],i['user'],i['pass'])

def loadData():
	root = tk.Tk()
	root.title("Choose what location to load")
	f = open(dirpath, 'r')
	contents = json.loads(f.read())
	f.close()
	listbox = tk.Listbox(root)
	for i in range(len(contents)):
		listbox.insert(tk.END, contents[i]['location'])
	button = tk.Button(root, text ="Load", command = lambda:[load(listbox.get(listbox.curselection())),changeWindow(root)])
	button.pack()
	listbox.pack()
	root.mainloop()
	
###################### SAVE CONFIG ######################
def editLocation(data):
	f = open(dirpath,"w+")
	contents = json.loads(f.read())
	for i in contents:
		if i['location']==data['location']:
			i = data
	f.close()

def newLocation(data):
	f = open(dirpath,"w+")
	contents = json.loads(f.read())
	contents.append(data)
	f.write(contents)
	f.close()
###################### HTTP  QUERY ######################
def query(mcl):
	try:
		deviceList = wifi.reqData()
		dlst = []
		for i in deviceList:
			dlst.append((i.nickname, i.connection, i.ipaddr, i.macaddr))
		mcl.addDevices(dlst)
	except:
		pass

def doNothing():
	pass
	
def changeWindow(rt):
	slaves = rt.pack_slaves()
	for l in slaves:
		l.destroy()
	main(rt)
	

######################  TK   HERE  ######################


class MultiColumnListbox(object):
	header = ["Name", "Connection", "IP Address", "MAC Address"]
	deviceLst = []
	def __init__(self):
		self.tree = None

	def _setup_widgets(self):
		container = ttk.Frame()
		container.pack(fill='both', expand=True)
		self.tree = ttk.Treeview(columns=self.header, show="headings")
		vsb = ttk.Scrollbar(orient="vertical",
			command=self.tree.yview)
		hsb = ttk.Scrollbar(orient="horizontal",
			command=self.tree.xview)
		self.tree.configure(yscrollcommand=vsb.set,
			xscrollcommand=hsb.set)
		self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
		vsb.grid(column=1, row=0, sticky='ns', in_=container)
		hsb.grid(column=0, row=1, sticky='ew', in_=container)
		container.grid_columnconfigure(0, weight=1)
		container.grid_rowconfigure(0, weight=1)
	def addDevices(self, devices):
		self.deviceLst = devices
		self._setup_widgets()
		self._build_tree()

	def _build_tree(self):
		for col in self.header:
			self.tree.heading(col, text=col.title(),
				command=lambda c=col: sortby(self.tree, c, 0))
			self.tree.column(col,
				width=tkFont.Font().measure(col.title()))

		for item in self.deviceLst:
			self.tree.insert('', 'end', values=item)
			for ix, val in enumerate(item):
				col_w = tkFont.Font().measure(val)
				if self.tree.column(self.header[ix],width=None)<col_w:
					self.tree.column(self.header[ix], width=col_w)

def sortby(tree, col, descending):
	data = [(tree.set(child, col), child) for child in tree.get_children('')]
	data.sort(reverse=descending)
	for ix, item in enumerate(data):
		tree.move(item[1], '', ix)
	tree.heading(col, command=lambda col=col: sortby(tree, col, int(not descending)))

def main(window):
	window.title("Wifi Scanner")

	## Menu Bar ###
	menubar = tk.Menu(window)

	filemenu = tk.Menu(menubar, tearoff=0)
	filemenu.add_command(label="New", command=doNothing)
	filemenu.add_command(label="Reload", command=doNothing)
	filemenu.add_command(label="Edit", command=doNothing)
	filemenu.add_separator()
	filemenu.add_command(label="Exit", command=window.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	helpmenu = tk.Menu(menubar, tearoff=0)
	helpmenu.add_command(label="Help Index", command=doNothing)
	helpmenu.add_command(label="About...", command=doNothing)
	menubar.add_cascade(label="Help", menu=helpmenu)

	window.config(menu=menubar)

	## Listbox ##
	listbox = MultiColumnListbox()
	
	## Button ##
	query(listbox)
	window.mainloop()


loadData()
