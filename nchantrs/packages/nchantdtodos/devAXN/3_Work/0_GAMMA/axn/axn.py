#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
<(meta)>:
	DOCid: <^[uuid]^>
	name: Ecosystems Level TODO Module Python Document
	description: >

		Initate action against daily TODOs load schedule for the actor
		generate new operations from daily operations
		set a todo to follow up with said research topics

		#Generate Standard tasks for all processes with a determinate
		#rating greater than 0.5 and maturity level of ???

		Review all ToDo's and break down as is feasible
		then need to have a script that runs over this and
		continous breaking down and creating actions as it can

		Also create a list of used actions that don't have processes
		should these be created or added as matches

		How to draw boundaries around this but still keep it
		highly useable and potentially facilitiate a crawler

		a system to ask questions to user allowing the system to
		leverage the knowledge of humans

		highly good at fuzzy decisions with various data points but
		low response rate or calculatory power

		launch mobile note organization

		retrieve yesterdays notes and distribute accordingly
		distribute todays notes
			schedule
			sam notes
			market notes
		use schedule to define various file distributions
			travel entertainment
			travel itenary documents
		disposition based on naming convention?
		would like to have a trigger from cherrytree that would
		then read the cherry tree file for any P: and then trigger
		creation of the project filles as needed....master project control document

		review xml document used by cherry tree see if i can easily pick ou the note headings
		Analyze project for creating Loci method of memory based in a
		program/app that reinforces internal memory with external memories
		value of memory in an external memory world?
		Retrieve calendar items for the next 24 hours after the given date time
		Get schedule from JDB GMail
		take a process id argument
		check on that pid periodically and if it fails
		restart the service
		.speakeasy - to access encrypted areas
		build this to trim various automatically created cherrytree
		also trim a fs tree or any other type of tree based file and/or directory structure
		how to populate information onto agenda?  write it on the background and then assign that background to the first page???

	expirary: <[expiration]>
	Version: <[Version]>
	path: <[LEXIvrs]>pheonix/ecosystems/oprm/z_tools_creOP.py
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import os, datetime as dt, shutil#										||
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class act:
	'Complete Action Events from Operations, Quests and Projects'#		||
	version = '0.0.0.0.0.0'#											||=>Set version
	def __init__(self, given=None):#									||
		pass
	def request(self):
		return self
	def do(self):
		if given == None:#												||
			dolist = here+'/'+given
		else:
			dolist = given
		self.doid = calcgen.thing().uuid
		self.action = 'Waiting On'
		self.do = 'Disposition eMail'
	def schedule(self, timeframe='day'):
		planrng = '10days'
		timetmp = config.load(timeframe).code(timeframe).text
		cal = calendar.box(today).to(planrng)
		for day in cal.days:
			newday = calendar.plan(today).time(timetmp)
		return self
	def new(self):
		self.name = name
		self.taskid = genid()
		self.tasktype = 'eMail' #need a way to analyze the object and determine the type
		self.concern = 'SAM' #need to look at all stored concerns and determine
		if 'X' in message.Categories:
			self.action = 'Action'
			self.do = ''
		elif 'NX' in message.Categories:
			self.action = 'Need Action'
			if 'Notes' in message.Categories:
				self.do = 'Transcribe'
			if 'ToRead' in message.Categories:
				pass
			if 'ToReview' in message.Categories:
				pass
		elif 'WO' in message.Categories:
			self.action = 'Waiting On'
		else:
			self.action = 'Action'
			self.do = 'Disposition eMail'
	def collect(self, profile):
		self.profile = profile
		self.action_model = profile['ActionModel']
	def email(self):
		self.emails = self.profile['Emails']
		for email in emails:
			pass
class notdo:
	''
	def __init__(self):
		pass
#==========================Source Materials=============================||
#============================:::DNA:::==================================||
'''
<(DNA)>:
	<@[datetime]@>:
		<[class]>:
			version: <[active:.version]>
			test:
			description: >
				<[description]>
			work:
				- <@[work_datetime]@>
	<[datetime]>:
		here:
			version: <[active:.version]>
			test:
			description: >
				<[description]>
			work:
				- <@[work_datetime]@>
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||








'''
meta:
	DOCid: <^[uuid]^>
	version: 0.0.0.0.0.0
	here: <^[here]^>
	outline:
'''
# -*- coding: utf-8 -*-
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
#enter new todos
#schedule todos to be completed
#break down entries to completable chunks
#completeing a truly independant step or task will get logged under a daily workorder activity only which becomes a basic log
#other workorders will link off this based on objective priorities
#accept an operation sequence from a primePOV
#run the operation
#A Task Group has a Schedule Group of Steps
#-> The Schedule gives the Task Group Sequence and Timing
#A Task Group Sequence May or May Not be Linear
#A Task Group Sequence May or May Not be Consecutive
#A Task can take no longer than 15minutes to complete
#A Task can interact with no more than 3 entities
#A Task can have no more than 20 steps
#A Task must advance at least 1 goal
#A Task cannot have a decision point
#Generate Standard tasks for all processes with a determinate
#rating greater than 0.5 and maturity level of ???
#Review all ToDo's and break down as is feasible then need to have
#a script that runs over this and continous breaking down and
#creating actions as it can
#Also create a list of used actions that don't have processes
#	should these be created or added as matches
#	How to draw boundaries around this but still keep it
#highly useable and potentially facilitiate a crawler
#a system to ask questions to user allowing the system to
#leverage the knowledge of humans
#highly good at fuzzy decisions with various data points but
#low response rate or calculatory power
#A large part of a companies direction and performance revolves
#around handling legacy items - employee loyalty, poorly engineered products,
#How quickly and on what items are new technologies developed?
#Example of spacex due to NASA legacy from previous investment bias
#But on the other end continually jumping to the newest tech will
#diminish interchangeability over time as well the creation and
#dissemination of standards and the ability to
#"stand on the shoulders of giants"
#Develop QUDO System:
#	Research, Investigate, RnD, R&D
#Need to code a system for TODOs that allows for
#easy division of a todo into others
#	create mytosis by procrastination
#(why can't you complete this right now?)
#Need to integrate tasks with a research modifier
#to denote major uknown needs, time, etc.
#Scriptables: setup cleanup of WTx/FTx every sunday at the
#same time as backups
#what is control mechanism
#would like to have a trigger from cherrytree that would
#then read the cherry tree file for any P: and then trigger
#creation of the project filles as needed
#review xml document used by cherry tree see if i can
#easily pick ou the note headings
#OfI: Opportunity for Improvment - improvements are targeted
#in an intentioned direction and can include less or more
#OfG: Opportunity for Growth - Growth is just more not always good,
#wanted or directed....much growth has to be pruned
#Analyze project for creating Loci method of memory based in a
#program/app that reinforces internal memory with external memories
#value of memory in an external memory world?
#need to get exchange feed to trigger this script to run
#when a document is added or changed
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
import os, datetime as dt, shutil#
#=======================================================================||
now = dt.datetime.today()#
start = 'Start @ '+str(now)#
tdy = now.remove end
#=======================================================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
o = obs.focus().messages().outs# 										||
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class act:#																||
	'Complete Actions derived from all areas'
	version = '0.0.0.0.0.0'#											||=>Set version
	def __init__(self, given=None):
		if given == None:
			dolist = here+'/'+given
		else:
			dolist = given
		self.doid = calcgen.thing().uuid
		self.action = 'Waiting On'
		self.do = 'Disposition eMail'
	def work(self):
		return self
	def schedule(self, timeframe='day'):
		planrng = '10days'
		timetmp = config.load(timeframe).code(timeframe).text
		cal = calendar.box(today).to(planrng)
		for day in cal.days:
			newday = calendar.plan(today).time(timetmp)
		return self
	def getDOs(self, queue=None):
		if queue == None:
			queue = 'prime'
class new:
	def __init__(self):
		self.name = name
		self.taskid = genid()
		self.tasktype = 'eMail' #need a way to analyze the object and determine the type
		self.concern = 'SAM' #need to look at all stored concerns and determine
		if 'X' in message.Categories:
			self.action = 'Action'
			self.do = ''
		elif 'NX' in message.Categories:
			self.action = 'Need Action'
			if 'Notes' in message.Categories:
				self.do = 'Transcribe'
			if 'ToRead' in message.Categories:
				pass
			if 'ToReview' in message.Categories:
				pass
		elif 'WO' in message.Categories:
			self.action = 'Waiting On'
		else:
			self.action = 'Action'
			self.do = 'Disposition eMail'
class collect:
	def  __init__(self, profile):
		self.profile = profile
		self.action_model = profile['ActionModel']
	def email(self):
		self.emails = self.profile['Emails']
		for email in emails:
			pass
		if self.task_model == 'GTD':#Getting Things Done
			self.tags = pheonix.organisms.models.actmd.GTD().tags
		elif self.task_model == 'BJ':#Bullet Journal
			pass
		elif self.task_model == 'PT':#Pomedoro Technique
			pass
		elif self.task_model == 'PP':#Productivity Panda
			pass
def genid():
	pass
#	lexi.qdev.get.now(db, schema, table, columns, records)
#	lexi.qdev.store.now(db, schema, table, columns, records)
# need to return the new task id
class collect:
	def  __init__(self, profile):
		self.profile = profile
		self.action_model = profile['ActionModel']
	def email(self):
		self.emails = self.profile['Emails']
		for email in emails:
			pass
		if self.task_model == 'GTD':#Getting Things Done
			self.tags = lexi.pheonix.organisms.models.actmd.GTD().tags
		elif self.task_model == 'BJ':#Bullet Journal
			pass
		elif self.task_model == 'PT':#Pomedoro Technique
			pass
		elif self.task_model == 'PP':#Productivity Panda
			pass
src_dir = mp+'/OPS/Manage_TODOs/_info'
src = src_dir+'/TODOs.ctd'
dst_dir = mp+'/IMA/JDB/TODOs/History'
dst = dst_dir+'/'+tdy+'_TODOs.ctd'
shutil.copy2(src, dst)
def GetSchedule():
	#Retrieve calendar items for the next 24 hours after the given date time
	#Get schedule from JDB GMail
Schedule = GetSchedule(now)
cherrytree = ''
x_con = 'Put Action tasks below: Need action Tools and Context Requirements:'
x_con += '(OD->OutsideDaylight, ID->InsideDaylight, I->Inside, BH->BusinessHours)\n'
x_con += 30*('@')+'\n\n'
for TODO in TODOs.x:
	x_con += TODO+'\n'
x_con += 30*('@')+'\n\n'
nx_con = 'Put Need Action tasks below: Need action Tools and Context Requirements:'
nx_con += '(OD->OutsideDaylight, ID->InsideDaylight, I->Inside, BH->BusinessHours)\n'
nx_con += 30*('@')+'\n\n'
for TODO in TODOs.nx
	nx_con +=
'node-.0.0':['X: Action', x_con, x_tag]
,'node0.1.0': ['News', news_con, news_tag]
,'node-.2.1': ['NX: Need Action', nx_con, nx_tag]
,'node-.3.2': ['WO: Waiting On'
,'node-.4.3': ['Procure'
,'node-.5.4': ['0_Tools',
,'node5.6.1': ['hour-plan', hour_plan_con, hour_plan_tag]
,'node5.7.2': ['min-plan', min_plan_con, min_plan_tag]
def hour_loop():
	start = 0
	txt += pad+start
	cnt = 0
	while time < 2200:
		cnt += 1
		txt += pad+(start+100*cnt)
TODO = todo.nx.new()
newTODO = TODO.Expand
actions = json.load()
for TODO.x in TODOs:
	for action in actions:
		if x == action:
			get.process(rte)
		else:
			s3t.new_action()#
def clean(area):
	for t45k, w0rk in t45k5.items():#														||asign the task based on the file extension and work to directories for move
		s = w0rk[0]#																		||
		d = w0rk[1]#																		||
		s_f1l35 = os.listdir(s)#															||list all files at the source directory
		for s_f1l3 in s_f1l35:#																||iterate over files listed from the source directory
			s_94th = s+'/'+s_f1l3#															||construct the full source path for each file
			d_94th = d+'/'+s_f1l3#															||construct the full destination path for each file
			if re.search(t45k,s_94th):#														||check each source path for the current task extension
				if not os.path.exists(d):#													||
					os.makedirs(d)#															||
				shutil.move(s_94th,d_94th)#
	if area == 'Downloads':
		pass
	elif area == 'Security':
		pass
class cooler():
	def __init__(self, pid, service):
		while True:
	#vectors reprsent the paths through the door that the bouncer must monitor
			for vector in vectors:
				self.service = service
				self.pid = pid
				#take a process id argument
				#check on that pid periodically and if it fails
				#restart the service
class bouncer():
	def __init__():
		self.name = vector['name']
		self.start = lexi.panda.service_starter(vector['service'])
		self.supervisor = lexi.panda.service_super(self.start)
		self.vector = vector
		self.door = lexi.wolf.loc.entryway(vector)#.speakeasy - to access encrypted areas
		self.bouncer = lexi.wolf.bouncer()
class loc():
	def __init__(self):
		pass
	def entryway(self, vector):
		com = lexi.panda.com.channelifier(vector['message'])
		com.width = ''
		door.height = ''
		door.que = ''
		door.maxrate = ''
		door.minrate = ''
		door.avgrate = ''
		self.door = door
class profile:
	def __init__(self):
		profile = json#need to get json data object
class track:
	def __init__(self):
		pass
	def filetype(self):
		pass
	def meta(self):
		pass
	def content(self):
		pass#open file and turn content into a cherrytree document
class catalog:
	def __init__(self, pattern):
		pass
	def f1l3s(self, path):
		fs = lexi.panda.store.fs.get()
		for path, d1rs, f1l3s in fs:
			for f1l3 in f1l3s:
				if pattern in f1l3:
					lexi.panda.comm.log.heavy().ctql()
class sec:
	def __init__(self):
		pass
	def cam(self):
		fpad = '_'#
		bpad = ''#
		vac.datesort(ark,fpad,bpad).suck()
	def key(self):
		pass
lexi.panda.store.fsql.Trash().tree()
#Clean Laptop Music
samlt = False
if samlt == True:
	path = '/home/solubrew/DataStack/Dropbox/Archive/data/CIM/SyncThing/SAM_DT/Music'
	lexi.wolf.lone.maint.Trash(path).scortch()
#Clean Primary Cell Phone Music
mainpt = False
if mainpt == True:
	path = '/home/solubrew/Mobile/Music'
	lexi.wolf.lone.maint.Trash(path).scortch()
#Clean Primary Cell Phone Images
class Trim:
	def __init__(self):
		pass
	def tree(self):#build this to trim various automatically created cherrytree
		pass#also trim a fs tree or any other type of tree based file and/or directory structure
	def f1l3(self):#
		pass
class Trash:
	def __init__(self,path):
		self.name = ''
		self.path = path
	def scortch(self):
		f1l3s = os.listdir(path)
		for f1l3 in f1l3s:
			os.remove(self.path+'/'+f1l3)
	def ghost(self):
		lexi.panda.store.fsql.remove.prune(fs)
	def death(self):
		pass
class ark:
	def __init__(self, path='/home/solubrew'):
		self.path = path
	def filelist(self, exts):
		for ext in exts:
			lexi.wolf.pack.catalog(self.path).f1l3s(ext)
	def calendar(self):
		pass
#how to populate information onto agenda?  write it on the background and then assign that background to the first page???
src_dir = mp+'/OPS/Manage_TODOs/_info'
src = src_dir+'/TODOs.ctd'
dst_dir = mp+'/IMA/JDB/TODOs/History'
dst = dst_dir+'/'+tdy+'_TODOs.ctd'
shutil.copy2(src, dst)
def GetSchedule():
#Retrieve calendar items for the next 24 hours after the given date time
#Get schedule from JDB GMail
#
Schedule = GetSchedule(now)
cherrytree = ''
x_con = 'Put Action tasks below: Need action Tools and Context Requirements:'
x_con += '(OD->OutsideDaylight, ID->InsideDaylight, I->Inside, BH->BusinessHours)\n'
x_con += 30*('@')+'\n\n'
for TODO in TODOs.x:
 x_con += TODO+'\n'
x_con += 30*('@')+'\n\n'
nx_con = 'Put Need Action tasks below: Need action Tools and Context Requirements:'
nx_con += '(OD->OutsideDaylight, ID->InsideDaylight, I->Inside, BH->BusinessHours)\n'
nx_con += 30*('@')+'\n\n'
for TODO in TODOs.nx
 nx_con +=
'node-.0.0':['X: Action', x_con, x_tag]
,'node0.1.0': ['News', news_con, news_tag]
,'node-.2.1': ['NX: Need Action', nx_con, nx_tag]
,'node-.3.2': ['WO: Waiting On'
,'node-.4.3': ['Procure'
,'node-.5.4': ['0_Tools',
,'node5.6.1': ['hour-plan', hour_plan_con, hour_plan_tag]
,'node5.7.2': ['min-plan', min_plan_con, min_plan_tag]
with open(src,'r') as note:
note.closed
def hour_loop():
 start = 0
 txt += pad+start
 cnt = 0
while time < 2200:
  cnt += 1
  txt += pad+(start+100*cnt)
#need to get exchange feed to trigger this script to run when a document is added or changed
TODO = todo.nx.new()
newTODO = TODO.Expand
actions = json.load()
for TODO.x in TODOs:
for action in actions:
  if x == action:
   get.process(rte)
  else:
   s3t.new_action()#
'''
write out urls to a todo sheet for investigation
search the url for known research topics and distribute accordyingly??
set a todo to follow up with said research topics
every design model
github - kick over to sourcables
python - add to SoftMD/RnD
create an Investigate Workflow
'''
import os, datetime as dt
import lexi
tdy = dt.datetime.today()
here = os.path.join(os.path.dirname(__file__),'')
class test:
	def __init__(self):
		print('lexi.panda.capture')
def launch_quotes():
	tickers = lexi.pheonix.cells.product.data.stocks.getTickers()
	lexi.pheonix.cells.product.data.stocks.getQuotes(tickers)
#launch downloads cleanup
#launch conflict vaccum
#launch history vaccum
#launch security vaccum....retool to be a running positioning
#launch mobile note organization
#retrieve yesterdays notes and distribute accordingly
#distribute todays notes
	#schedule
	#sam notes
	#market notes
	#
#use schedule to define various file distributions
	#travel entertainment
	#travel itenary documents
	#
#move and convert snotes
#archive .snb in a retrieveable way
#disposition based on naming convention?
class sod:
	def __init__(self):
		self.profile = lexi.wolf.lone.profile(user)
	def notes_review(self):
		loci = self.profile.locations
		lexi.panda.comm.note.notes_review().snote(loci['snote'])
		lexi.panda.comm.note.notes_review().chnote(loci['chnote'])
	def email_review(self):
		#grab static snapshot from the email pump
		pass
	def schedule_review(self):
		pass
	def notes_create(self):
		pass
	def xs_upd8(self):
		pass
	def nxs_upd8(self):
		pass
class eod:
	def __init__(self, profile):
		self.profile = profile
		self.dbs = profile['db']
	def notes_review(self):
		pass
	def schedule_review(self):
		pass
	def notes_create(self):
		pass
	def xs_upd8(self):
		pass
	def nxs_upd8(self):
		pass
	def grab(self):
		db = dbs['Stocks']
		lexi.pheonix.molecules.grabber.grab('Stocks', self.db)
	def vacuum(self, path, ark):
#		path = '/home/solubrew'#																			|| mps - machine path source
#		ark = '/home/solubrew/DataStore/DataPile'#																|| mpe - machine path exception
#-----------------Functions---------------------------------------------------------------------||
		vac = lexi.panda.vacuum.vacuum(path)
		#vac.conflict(ark).suck()
		hist = '/home/solubrew/DataStack/Dropbox/Archive/data/IMA/zz_hist'
		vac.history(hist).suck()
class new:
	def __init__(self):
		self.name = name
		self.taskid = genid()
		self.tasktype = 'eMail' #need a way to analyze the object and determine the type
		self.concern = 'SAM' #need to look at all stored concerns and determine
		if 'X' in message.Categories:
			self.action = 'Action'
			self.do = ''
		elif 'NX' in message.Categories:
			self.action = 'Need Action'
			if 'Notes' in message.Categories:
				self.do = 'Transcribe'
			if 'ToRead' in message.Categories:
				pass
			if 'ToReview' in message.Categories:
				pass
		elif 'WO' in message.Categories:
			self.action = 'Waiting On'
		else:
			self.action = 'Action'
			self.do = 'Disposition eMail'
class collect:
	def  __init__(self, profile):
		self.profile = profile
		self.action_model = profile['ActionModel']
	def email(self):
		self.emails = self.profile['Emails']
		for email in emails:
			pass
		if self.task_model == 'GTD':#Getting Things Done
			self.tags = lexi.pheonix.organisms.models.actmd.GTD().tags
		elif self.task_model == 'BJ':#Bullet Journal
			pass
		elif self.task_model == 'PT':#Pomedoro Technique
			pass
		elif self.task_model == 'PP':#Productivity Panda
			pass
start = 'Start @ '+str(now)#
src_dir = mp+'/OPS/Manage_TODOs/_info'
src = src_dir+'/TODOs.ctd'
dst_dir = mp+'/IMA/JDB/TODOs/History'
dst = dst_dir+'/'+tdy+'_TODOs.ctd'
x_con = 'Put Action tasks below: Need action Tools and Context Requirements:'
x_con += '(OD->OutsideDaylight, ID->InsideDaylight, I->Inside, BH->BusinessHours)\n'
x_con += 30*('@')+'\n\n'
for TODO in TODOs.x:
	x_con += TODO+'\n'
x_con += 30*('@')+'\n\n'
nx_con = 'Put Need Action tasks below: Need action Tools and Context Requirements:'
nx_con += '(OD->OutsideDaylight, ID->InsideDaylight, I->Inside, BH->BusinessHours)\n'
nx_con += 30*('@')+'\n\n'
'node-.0.0':['X: Action', x_con, x_tag]
,'node0.1.0': ['News', news_con, news_tag]
,'node-.2.1': ['NX: Need Action', nx_con, nx_tag]
,'node-.3.2': ['WO: Waiting On'
,'node-.4.3': ['Procure'
,'node-.5.4': ['0_Tools',
,'node5.6.1': ['hour-plan', hour_plan_con, hour_plan_tag]
,'node5.7.2': ['min-plan', min_plan_con, min_plan_tag]
sessions = {
	'MainDT': ''
	,'SamDT': ''
	,'SamLT': ''
}
bookmarks = {
	'MainDT': ''
	,'SamDT': ''
	,'SamLT': ''
	,'MainPT': ''
	,'MainHT': ''
}


				
