


import commands
import re

debugflag = "N"

def DebugPrint(vname,value):
	if debugflag == "Y":
		print vname,"=", value
	return

def DMIDECODE(value,cmdline):
	result = commands.getoutput(DMICMD + cmdline)
	DebugPrint(value,result)
	return(result)

def CHECKITX(index,cpuversion,logfile):
	lookupcount = int(commands.getoutput("grep -c '"+ cpuversion +"' Plist.csv"))
	if lookupcount == 1:
		LOGIT(index,cpuversion,logfile)
	return(lookupcount)

def CHECKIT(cpuversion):
	lookupcount = int(commands.getoutput("grep -c '"+ cpuversion +"' Plist.csv"))
	LOGIT(lookupcount,cpuversion,"check.log")
	if lookupcount == 1:
		x,y,passmark,CPU,action =  commands.getoutput("grep -m 1 '"+ cpuversion +"' Plist.csv").strip().split(",")
		return(lookupcount,passmark,CPU,action)
	else:
		return(lookupcount,"0","Not Found","Unknown")

def MODELLOOKUP(modelname):
	modelcount = int(commands.getoutput("grep -c '"+ modelname +"' Mlist.csv"))
	print "modelcount",modelcount
	if modelcount <> 0:
		x, y, cpulookup = commands.getoutput("grep -m 1 '"+ modelname +"' Mlist.csv").split(",")
		lookupcount = modelcount
	else:
		cpulookup = modelname
	return (cpulookup)

	
def LOGIT(index,value,filename):
	with open(filename,"a") as logfile:
		logfile.write(str(index)+" "+value+"\n")
	logfile.closed
	
filelist = commands.getoutput('find * |grep "/"').split("\n")
for i in range(0,len(filelist)):
	# print "Test ",i,filelist[i]
	DMICMD="/usr/sbin/dmidecode --from-dump " + filelist[i]
	
	modelname  = DMIDECODE("modelname"," -s system-product-name|grep -v 'Invalid entry length'").strip()
	cpuversion = DMIDECODE("cpuversion"," -t processor|grep 'Version:'").replace("Version:","").replace(":","").replace("CPU ","").strip()
	LOGIT(i,cpuversion,"lookup-0.log")
	
	if cpuversion == "Not Specified":
		cpuversion = MODELLOOKUP(modelname)
		
	cpuversionP1 = re.sub(' +'," ",cpuversion.replace("(R)","").replace("(TM)","").replace("(tm)","").replace("Processor","").replace("Intel","").replace("AMD",""))
	lookupcount,passmark,CPU,action = CHECKIT(cpuversionP1)
	if lookupcount <> 1:
		cpuversionP2 = cpuversionP1.replace("APU with Radeon HD Graphics", "").strip()
		lookupcount,passmark,CPU,action = CHECKIT(cpuversionP2)
		if lookupcount <> 1:
			cpuversionP3 = cpuversionP2.replace("i5 ","i5-").replace("i3 ","i3-").replace("i7 ","i7-").replace("Pentium Dual-Core","").replace("Pentium Dual","").strip()
			lookupcount,passmark,CPU,action = CHECKIT(cpuversionP3)
			if lookupcount <> 1:
				if lookupcount == 0:
					print i," ",filelist[i]
					LOGIT(i,cpuversionP3,"lookup-NONE.log")
				else:
					LOGIT(i,cpuversionP3,"lookup-REFINE.log")
			