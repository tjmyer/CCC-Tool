
version = "B1.02.0"
# B1.00.0 - working interface and basic R command without any check or logging
# B1.00.1 - added Lookup command and check for no record found on R cmd lookoup
# B1.00.2 - added logging  - next up return code
# B1.01.0 - reordered code
# B1.01.1 - added cpumodel refinement and Mlist.csv lookup (still need to add grep of CPU speed for mutiple entries
# B1.01.2 - added logic to sort on cpucore count and memory type
# B1.02.0 - bug fixes to core count, and PC lookup.  PC Lookup required redesign of logic - simpler now.

import commands
import sys
import re
from datetime import datetime

#       0        1         2         3         4         5         6         7         8
#       12345678901234567890123456789012345678901234567890123456789012345678901234567890
# Command Line
Aline1="                {0:1s}  {1:40s}"
# Log Line
#print Lline.format(tsinfo,fate,CPU,SPEED,passmark,ddrtype,memory,modelname,snnumber)
Lline="{0:12s},{1:9s},{2:15s},{3:4.2f},{4:5s},{5:4s},{6:4.1f},{7:30s},{8:8s}\n"
# Label Line
RlineRecycle="RECYCLE RECYCLE RECYCLE RECYCLE RECYCLE RECYCLE RECYCLE RECYCLE RECYCLE RECYCLE"
RlineRefurbish="REFURBISH REFURBISH REFURBISH REFURBISH REFURBISH REFURBISH REFURBISH REFURBISH"
RlineT="__________________________________________________"
Rline1="|                                                |"
Rline2="| CPU: {0:29s} SPEED: {1:4.2f} |"
Rline3="| MEMORY: {0:4.1f}    TYPE: {1:4s}                     |"   
RlineB="|________________________________________________|"

#       0        1         2         3         4         5         6         7         8
#       12345678901234567890123456789012345678901234567890123456789012345678901234567890
Sline1="CCC Sorter Version: {0:7s}                              Plist Version: {1:>8s}"
Sline2="Model: {0:35s}      Serial Number: {1:>17s}"
Sline3="CPU Type: {0:45s}          CPU Speed: {1:4.2f}"
Sline4="Memory: {0:4.1f}	                     				      Type: {1:>4s}"


	

debugflag = "N"
command = "R"

if len(sys.argv) > 1 :
	command = "H"
	DMICMD = "/usr/sbin/dmidecode --from-dump " + sys.argv[1]
	print 'Using file',sys.argv[1],'for processing DMIDECODE commands'
	print DMICMD
	print ""
else:
	command = "R"
	DMICMD = "sudo dmidecode"
	
	
actionDebug = "Debug"
actionQuit = "Quit"
actionSystem = "System Info"
actionRecycle = "Refurbish or Recycle Determination"
actionHelp = "Help"
actionNew = "New command in progress"
actionFile = "File for DMIDECODE input"
actionLookup = "Lookup Processor"




def DMIDECODE(value,cmdline):
	result = commands.getoutput(DMICMD + cmdline)
	DebugPrint(value,result)
	return(result)

def DebugPrint(vname,value):
	if debugflag == "Y":
		print vname,"=", value
	return

def SystemInfo():
    DebugPrint ("System Info",1)
    

def FileAction():
	DebugPrint ("File Action Initiated",1)
	global DMICMD
	# filelist = commands.getoutput('ls -1dp *|grep -v ".py"|grep -v ".csv"|grep -v ".log"|grep -v "/"').split("\n")
	filelist = commands.getoutput('find * |grep "/"').split("\n")
	for i in range(0,len(filelist)):
		print i,filelist[i]
	filenum = int(raw_input("File to Number Use: "))
	DMICMD="/usr/sbin/dmidecode --from-dump " + filelist[filenum]
	
def HelpAction():
	print "Select from commands below:"
	print ""
	print Aline1.format(actionDebug[:1],actionDebug)
	print Aline1.format(actionQuit[:1],actionQuit)
	print Aline1.format(actionLookup[:1],actionLookup)
	print Aline1.format(actionRecycle[:1],actionRecycle)
	print Aline1.format(actionSystem[:1],actionSystem)
	print ""
	return
	
def DebugAction():
	global debugflag
	if debugflag == "N":
		debugflag = "Y"
	else:
		debugflag = "N"
	print "debugflag = ",debugflag
	return        

def SystemAction():
	DebugPrint ("System Action initiated",1)
		
#	meminfo = DMIDECODE("meminfo"," -t 17")
	# meminfo2 = list(commands.getoutput("sudo dmidecode -t 17").replace('\t',"").strip().splitlines())
	return

def LookupAction():
	DebugPrint ("Lookup Action initiated",1)
	lookupvalue = raw_input("Value to Lookup: ")
	print " "
	print "Results: ",commands.getoutput("grep '"+ lookupvalue +"' Plist.csv").strip()
	print " "
	return

def NewAction():
	DebugPrint("New Action initiated","Y")
	return
	
def RecycleAction():
    DebugPrint("Recycle Action initiated",1)
    snnumber   = DMIDECODE("snnumber"," -s system-serial-number|grep -v 'Invalid entry length'")
    DMIDUMP=DMIDECODE("DMIDUMP"," --dump-bin "+ snnumber)
    modelname  = DMIDECODE("modelname"," -s system-product-name|grep -v 'Invalid entry length'").strip()
    cpuversion   = DMIDECODE("cpuversion"," -t processor|grep 'Version:'").replace("Version:","").replace(":","").replace("CPU ","").strip()
    cpuspeed     = DMIDECODE("cpuspeed"," -s processor-frequency|grep MHz").replace("MHz","")
    SPEED = round(float(cpuspeed)/1000,2)
    try:
		corecount     = int(DMIDECODE("cpucount"," -t 4 |grep -i 'Core Count:'").replace("Core Count:","").strip())
    except ValueError:
		corecount = 1
    ddrtype        = DMIDECODE("ddrtype"," -t 17 |grep -m 1 'Type: D'").replace("Type: ","").strip()
    memsize = commands.getoutput("grep 'MemTotal' /proc/meminfo").replace("MemTotal:","").replace("kB","").strip()
    MEMORY = round(float(memsize)/1000000,1)

    dimlist=[""]
    sizelist=[""]
    dimdata = DMIDECODE("input"," -t 17").split("\n")
    for line in dimdata:
        x=line.find("Locator:")
        y=line.find("Size:")
        if y == 1:
            sizelist.append(line.replace("Size:","").strip())
        if x == 1:
            dimlist.append(line.replace("Locator:","").strip()+":")

	#print("\033[H\033[J")
    print Sline1.format(version,"04/15/17")
    print ""
    print Sline2.format(modelname,snnumber)
    print Sline3.format(cpuversion,SPEED)
    print Sline4.format(MEMORY,ddrtype)
    for i in range(len(dimlist)):
		if sizelist[i].find("MB") != -1:
			size = str(round(float(sizelist[i].replace("MB","").strip())/1000,1))+" GB"
		else:
			size = sizelist[i]
		print dimlist[i],size

    tsinfo = datetime.now()
    DebugPrint("tsinfo",tsinfo)	

# Parse cpuversion
# Remove (R), (TM), (tm), Processor, Intel, AMD and duplicate spaces
    cpulookup = re.sub(' +'," ",cpuversion.replace("(R)","").replace("(TM)","").replace("(tm)","").replace("Processor","").replace("Intel","").replace("AMD",""))
    cpulookupX = cpuversion.replace("(R)","").replace("(TM)","").replace("(tm)","").replace("Processor","").replace("Intel","").replace("AMD","")
    lookupcount = int(commands.getoutput("grep -c '"+ cpulookup +"' Plist.csv"))
    DebugPrint("cpulookup",cpulookup)
    DebugPrint("cpulookupX",cpulookupX)
    if lookupcount == 0:
        cpulookupA = cpulookup.replace("Pentium","").replace("Dual ", "").replace("Dual-Core", "").strip()
        lookupcount = int(commands.getoutput("grep -c '"+ cpulookupA +"' Plist.csv"))
        DebugPrint("cpulookupA", cpulookupA)
        if lookupcount <> 0:
            cpulookup = cpulookupA
        else:
            cpulookupB = cpulookupA.replace("APU with Radeon HD Graphics", "").strip()
            lookupcount = int(commands.getoutput("grep -c '"+ cpulookupB+"' Plist.csv"))
            DebugPrint("cpulookupB", cpulookupB)
            if lookupcount <> 0:
                cpulookup = cpulookupB
            else:
                if cpulookup == "Not Specified":
                    modelcount = int(commands.getoutput("grep -c '"+ modelname +"' Mlist.csv"))
                    print "modelcount",modelcount
                    if modelcount <> 0:
                       x, y, cpulookup = commands.getoutput("grep -m 1 '"+ modelname +"' Mlist.csv").split(",")
                       lookupcount = modelcount
                       
    if lookupcount == 0:
        lookupaction = "UNKNOWN"
        CPU="UNKNOWN"
        passmark = ""
    else:
        x,y,passmark,CPU,lookupaction =  commands.getoutput("grep -m 1 '"+ cpulookup +"' Plist.csv").strip().split(",")
        DebugPrint("passmark",passmark)
        DebugPrint("CPU",CPU)
        DebugPrint("lookupaction",lookupaction)

# Determine if 4 core vs 2 core, if DDR2 vs DDR3  
    if corecount >= 3:
        action = lookupaction       # Keep CPU if it's fast enought no matter what the memory type
    elif corecount == 2:
        if ddrtype == "DDR2":       # Only 2 core - and DDR2 don't want it
            action = "Recycle"
        else:
            action = lookupaction     # Only 2 core - keep fast ones
    else:
        if ddrtype == "DDR2":        # core count no known, but DDR2 so don't keep
            action = "Recycle"
        else:
            action = lookupaction

    print ""
    print "PassMark:", passmark
    print "CPU Cores: ", corecount
    print ""
    
    DebugPrint("action", action)
    if action == "UNKNOWN":
		print " "
		print "WARNING: CPU TYPE NOT FOUND"
		print "   CPU version: ",cpuversion
		print "   CPU lookup : ",cpulookup
		print ""
		CPU=cpulookup
		passmark = ""	
    else:
    	if action == "Recycle":
			print RlineRecycle.format()
        else:
			print RlineRefurbish.format()
			print ""
			print RlineT.format()
			print Rline1.format()
			print Rline2.format(CPU,SPEED)
			print Rline1.format()
			print Rline3.format(MEMORY,ddrtype)
			print Rline1.format()
			print RlineB.format()
			print ""
			print ""
    with open("lookup.log","a") as logfile:
		logfile.write(Lline.format(str(tsinfo),action,CPU,SPEED,passmark,ddrtype,MEMORY,modelname,snnumber))
    logfile.closed
    DebugPrint("Log Line",Lline.format(str(tsinfo),action   ,CPU,SPEED,passmark,ddrtype,MEMORY,modelname,snnumber))		
    return
	
# Main()

while not ((command == "Q") or (command == "X")) :
	if command == actionDebug[:1]:
		DebugAction()
	elif command == actionNew[:1]:
		NewAction()
	elif command == actionLookup[:1]:
		LookupAction()
	elif command == actionRecycle[:1]:
		RecycleAction()
	elif command == actionSystem[:1]:
		SystemAction()
	elif command == actionFile[:1]:
		FileAction()
	else :
		HelpAction()
	command = raw_input("Enter Command > ")[:1].upper()
	print ""

if command == "Q" :
	print "Program Shutdown"
	sys.exit(5)
else :
	print "Program Exit"
	sys.exit(0)
