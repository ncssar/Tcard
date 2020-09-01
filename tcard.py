from PyQt5 import QtGui, QtCore, QtWidgets  # Import the PyQt5 modules we'll need
from PyQt5.QtGui import QFont
import sys  # We need sys so that we can pass argv to QApplication

##import table  # This file holds our MainWindow and all table related things
import tcard_ui      ## table display routine file
import csv
from pathlib import Path
import winsound
import re
import json
from operator import rshift
from collections import deque   ## pronounced deck
import requests

global DEBUG

DEBUG = 0
fntBold = QFont()
fntNorm = QFont()
fntBold.setBold(True)
fntField = QFont()
fntField.setPointSize(40)
fntField.setBold(True)

# it also keeps events etc that we defined in Qt Designer
import os  # For listing directory methods
import time
import io
import glob
import traceback
import threading
from datetime import date, datetime
from random import *
from operator import itemgetter
from PIL import ImageGrab, Image, ImageWin
import win32api
import win32ui
import win32print
from ctypes import windll
## pip install Pillow
## pip install pypiwin32   -> need to restart after 
import logging
logging.basicConfig(level=logging.INFO)

sys.tracebacklimit = 1000
API_KEY = os.environ.get("SIGN_API_KEY")
payload = {}
headers = {
  'Authorization': 'Bearer '+API_KEY
}
### Network Server host pointer
host="http://caver456.pythonanywhere.com"   ## set value here and in chk4data
columns=["ID","Name","Agency","Resource","TimeIn","TimeOut","Total","InEpoch","OutEpoch","TotalSec","CellNum","Status","Synced"]

event_url = host+"/api/v1/events"

### interval timing function In a separate thread
def setInterval(interval):
    def decorator(function):
        def wrapper(*args, **kwargs):
            stopped = threading.Event()

            def loop(): # executed in another thread
                while not stopped.wait(interval): # until stopped
                    function(*args, **kwargs)

            t = threading.Thread(target=loop)
            t.daemon = True # stop if the program exits
            t.start()
            return stopped
        return wrapper
    return decorator
     
### handler for intercepting exceptions
def excepthook(excType, excValue, tracebackobj):
    """
    Global function to catch unhandled exceptions.
    
    @param excType exception type
    @param excValue exception value
    @param tracebackobj traceback object
    """
    separator = '-' * 8
    logFile = "simple.log"
    notice = "\n"
    breakz = "\n"
    versionInfo="    0.0.1\n"
    timeString = time.strftime("%Y-%m-%d, %H:%M:%S")
    tbinfofile = io.StringIO()
    traceback.print_tb(tracebackobj, None, tbinfofile)
    tbinfofile.seek(0)
    tbinfo = tbinfofile.read()
    errmsg = '%s: %s' % (str(excType), str(excValue))
    sections = [separator, timeString, breakz, separator, errmsg, breakz, separator, tbinfo]
    msg = ''.join(sections)
    try:
        f = open(logFile, "w")
        f.write(msg)
        f.write(versionInfo)
        f.close()
    except IOError:
        pass
    print("\nMessage: %s" % str(notice)+str(msg)+str(versionInfo))

### replacement of system exception handler
sys.excepthook = excepthook   
           

class TableApp(QtWidgets.QMainWindow, QtWidgets.QTableWidget, tcard_ui.Ui_MainWindow, tcard_ui.tabinfo):  #####
    def __init__(self):
        # super is used here in that it allows us to
        # access variables, methods etc in the tcard_ui.py file
        super(self.__class__, self).__init__()
        xx=tcard_ui.Ui_MainWindow()  ## also see yy below
                                    ## works here because Hmain and Wmain are class variables?
        self.setupUi(self)          # This is defined in tcard_ui.py file automatically
        if (DEBUG == 1): print("main self: %s" % self)
        self.mm = self
        self.xx2 = xx           ## appears xx is only used here
        self.xx2.READIN = 0     ## set to determine if we have read MEMBERS yet
        self.prev_file = 'xxx'
        self.incident = " Test1 "
        self.idate = " "
        self.flag_noconn = 0   # flag to only alert no remote conn once in a row
        # It sets up layout and widgets that are defined
 
        self.pushButton.clicked.connect(self._addSrchr)  # When the ADD button is pressed
        self.pushButton_2.clicked.connect(self._rmSrchr)  # When the REMOVE button is pressed
        self.pushButton_undo.clicked.connect(self._undo)  # When the UNDO button is pressed
        self.pushButton_readMem.clicked.connect(self._readMemb)  # When the READ button is pressed
        self.pushButton_teams.clicked.connect(self.listTeams) # When list teams pushed
        self.pushButton_prntScrn.clicked.connect(self.prntScrn) # When prnt scrn is pushed
        self.pushButton_prnt104.clicked.connect(self.prnt104) # When prnt 104 is pushed
        self.num9.clicked.connect(lambda: self.numbers(9)) # put numbers in SAR ID field
        self.num8.clicked.connect(lambda: self.numbers(8)) # put numbers in SAR ID field
        self.num7.clicked.connect(lambda: self.numbers(7)) # put numbers in SAR ID field
        self.num6.clicked.connect(lambda: self.numbers(6)) # put numbers in SAR ID field
        self.num5.clicked.connect(lambda: self.numbers(5)) # put numbers in SAR ID field
        self.num4.clicked.connect(lambda: self.numbers(4)) # put numbers in SAR ID field
        self.num3.clicked.connect(lambda: self.numbers(3)) # put numbers in SAR ID field
        self.num2.clicked.connect(lambda: self.numbers(2)) # put numbers in SAR ID field
        self.num1.clicked.connect(lambda: self.numbers(1)) # put numbers in SAR ID field
        self.num0.clicked.connect(lambda: self.numbers(0)) # put numbers in SAR ID field
        self.numB.clicked.connect(lambda: self.numbers(10)) # put numbers in SAR ID field
        self.numD.clicked.connect(lambda: self.numbers(11)) # put numbers in SAR ID field
        self.numE.clicked.connect(lambda: self.numbers(12)) # put numbers in SAR ID field
        self.numN.clicked.connect(lambda: self.numbers(13)) # put numbers in SAR ID field
        self.numR.clicked.connect(lambda: self.numbers(14)) # put numbers in SAR ID field
        self.numS.clicked.connect(lambda: self.numbers(15)) # put numbers in SAR ID field
        self.numT.clicked.connect(lambda: self.numbers(16)) # put numbers in SAR ID field
        self.numALP.clicked.connect(lambda: self.numbers(17)) # put numbers in SAR ID field       
        self.modex = 0  ## set for select cell  if = 1, then drag and drop
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.tableWidget.cellDoubleClicked.connect(self.cell_was_Dclicked)
        self.tableWidget2.cellClicked.connect(self.dialog_was_clicked)      ## RMB for Team
        self.tableWidget5.cellClicked.connect(self.dialog_was_clicked4)      # RMB for Searcher
        ##  the following is not used
        ##self.tableWidget6.cellClicked.connect(self.dialog_was_clicked5)      # Event ID selection
        self.tableWidget3.cellClicked.connect(self.dialog_was_clicked2)      # RMB for Group creation
        self.tableWidget4.cellClicked.connect(self.dialog_was_clicked3)      # RMB for Find   
        self.selected = 0  ## preset to nothing selected   NOT USED?
        self.setAcceptDrops(True)               ## do not pickup drag/drop if assoc with tableWidget
        self.tableWidget.setDragEnabled(True)   ## needs to refer to tableWidget

        zz = tcard_ui.tabinfo()

        self.ww = tcard_ui.chk4data()
        self.ww.pntrx = zz         # pointer for RMTchange and eventID for use in chk4data
        '''
        ww.setDaemon(True)
        ww.start()   # start check for sql data change in new thread
        print("Start chk4data")
        '''
### call to timing function
        @setInterval(20)  ## decorator to call timing thread (seconds)
        def datetime_update(xxx):
          today = date.today()
          tod = today.strftime('%b %d, %Y')
          time  = datetime.now().time()
          xxx.dateTime.setText(str(tod)+" @ "+str(time)[0:5])  ## updates the date/time stamp on mainWindow
          ##print("Call to func")
        ##self.num = 1
        self.stop = datetime_update(self)  ## start timer
        ###self.num = 0
        #####self.stop.set()        ## will stop timer
        ###
        ###@setInterval(30)         ## 30 seconds to recheck members file update  CHECK??
        ###def chk_new_srchr(xxx):  ## checks for update of searchers new/remove
        ###    self.num = self.num+1
        ###    self.mm.infox.setText("30 sec timer count: "+str(self.num))
        ####
        #####self.stop2 = setInterval(chk_new_srchr(self))   # start timer2
        #

        ###  The following does not appear to have an affect
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.tableWidget.setSizePolicy( sizePolicy )


#
#  list TEAMS : [Name, xloc, yloc, #srchrs, type, location, timeout]
#
#  list SRCHR : [Name, agency, idnumb, xloc, yloc, xteam, yteam, leader (char1/0), medical (char1/0), Blink, Cell#, Resources, MEMBERSptr]
#
#  list MEMBERS:[Name, IDval, Agncy, leader, medical, TimeIN, TimeOUT, Cell#, Resources, CumTime]  (use TimeIn != "-1" ? as checked-in)
#                                         Want to add total time field for multiple time segments
#
# preset values  for each type
#       TEAMS : sheriff -> [Sheriff Coord, 0,0,0,IC,IC,0.0]
#               ops     -> [OPS, 0,8,0,IC, IC, 0.0]
#               unas    -> [UnAssigned, Nunas_col,0,UNAS, IC, 0,0]
#     SEARCHERS: SRCHR  -> [Namex1, NC, #1, 6, 1, ->UNAS(x,y) (team), 0, 0, 0, 0, 0, 0]
#                          [Namexz, NC, #2, 6, z, ->UNAS(x,y) (team), 0, 0, 0, 0, 0, 0]

######
     
## the following is writing to tabinfo.info
        i=0   ## entry #
        j=0    ## cnt of members
        m = 0  ## ID's
        savei = 0
        savej = 0
        clr_order = "RGBYMC "  ## team #
        self.zz2 = zz
        ##print("TOP: %s:%s"%(zz,self.zz2))
        zz.TEAM_NUM = 0
        ## place headers for Search MGMT in column 0

        ##  Name, xloc, yloc, #srchrs, Type, Location, Time Deployed
        zz.TEAMS.append(["Sheriff Coord", 0, 1, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Search Mngr", 0, 5, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Operations", 0, 10, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Planning", 0, 15, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Logistics", 0, 20, 0, "IC", "IC", 0.0])
        zz.TEAMS.append(["Comms", 0, 25, 0, "IC", "IC", 0.0])
        xunas = 6 ## location of Unassigned header
        yunas = 1
        team_unas = 6   ## after the are defined
        zz.TEAMS.append(["UnAssigned", xunas, yunas, 0, "UNAS", "IC", 0.0])
        zz.TEAMS.append(["END"])
        if (DEBUG == 1): print(zz.TEAMS[team_unas])

        iw = 0     ## initialization
        zz.TEAMS[team_unas][3] = iw  ## set number of searchers in unassigned    
        zz.SRCHR.append(["END"])   
        zz.tabload(self,0)         ## load display table
        if (DEBUG == 1): print("At init\n")
        ####  end of __init__


    def _addSrchr(self): ## Button ADD SEARCHER
        team_unas = 6                    ####   This is the number of the entry for the Unassigned Team
                                         ##         This may change as default or over time
        yy = self.mm  ##tcard_ui.Ui_MainWindow()  
        zz = self.zz2
        yy.saveLastIDentry = ""        
        ##print("TOP: %s"%zz.SRCHR)
        if (DEBUG == 1): print("At mode %i\n" % self.modex)
        self.modex = 1 - self.modex    ## change state
        xmodel(self.modex)   # call routine outside of class
        ## read the sarID field
        sarINFOval = yy.sarID.text()
        if (len(sarINFOval) == 0): return
        sarINFOsplit = sarINFOval.split()   ## SAR ID field can be "ID" or "ID AGENCY"
        sarIDval = sarINFOsplit[0].upper()
        sarAGENCY = "NC"                      ## default AGENCY
        if (len(sarINFOsplit) > 1):         ## then agency arg was entered
            sarAGENCY = sarINFOsplit[1].upper()
        if (DEBUG == 1): print("ADD: %s"% zz)
        memPtr = -1
        for xx in range(0,len(zz.MEMBERS)):
          if (zz.MEMBERS[xx][1] == sarIDval and zz.MEMBERS[xx][2] == sarAGENCY):
            memPtr = xx
            break
        if (memPtr == -1):                  ## ID not found
            winsound.Beep(2500, 1200)       ## BEEP, 2500Hz for 1 second, needs to be empty
            return
        elif (zz.MEMBERS[memPtr][5] != -1):    ## member already checked-in, ignore
            winsound.Beep(2500, 300)           ## BEEP, short 2500Hz, needs to be empty
            winsound.Beep(2500, 300)           ## double
            yy.sarID.setText("")
            return
        if (DEBUG == 1): print("PTR  %s"%memPtr)
        ## find vacancy in UNAS_USED
        ##  MEMBERS csv file: name, id, agency, leader, medical (add local fields: checked-in flag and ptr-to-srchr)
        ##print("UNAS list %s"%zz.UNAS_USED)
        for ixx in range(2,len(zz.UNAS_USED)):
            if ((ixx % yy.Nrows) == 0): continue   ## skip all rows == 0
            if (zz.UNAS_USED[ixx] == 0):           ## found available location
                zz.UNAS_USED[ixx] = 1
                ##print("ENTRY %i"%ixx)
                break
        if (DEBUG == 1): print("ptr %i"% ixx)
        colu = int(ixx/yy.Nrows)
        rowu = ixx - colu * yy.Nrows
        colu = colu + yy.Nunas_col
        TimeIN = time.time()    ## time since epoch
        tx = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        ##print("%f:%s"%(TimeIN,tx))
        if (DEBUG == 1): print("TimeIN %i"% TimeIN)  ## If the srchr comes back how to accum time? In members
        zz.SRCHR.insert(-1,[zz.MEMBERS[memPtr][0],zz.MEMBERS[memPtr][2],zz.MEMBERS[memPtr][1],  \
                        colu, rowu, yy.Nunas_col, 1, zz.MEMBERS[memPtr][3], zz.MEMBERS[memPtr][4], 5, \
                        zz.MEMBERS[memPtr][7], zz.MEMBERS[memPtr][8],memPtr]) # set blink to 5 sec # ADD memPtr to fields for easy backtrack
                                    ## Team is Unas at (Nunas_col,1) place before "END"
        zz.MEMBERS[memPtr][6] = -1                      ## time-out initialize to -1
        zz.MEMBERS[memPtr][5] = TimeIN                  ##  set as time-in
###
###  Need to construct correct entry
###       ALSO, check that SAR has not already been loaded
###             AND, when removing check that it was there        
###
##   SRCHR :        Name, agency, IdNumb, xloc, yloc, TeamX, TeamY, Leader(bit), Med(bit), Blink vs TimeIN, TimeOUT    ???
## put these \/ in some initialization place
##   incase searchers are added after movement has occurred, need to skip locations already used        

        zz.TEAMS[team_unas][3] = zz.TEAMS[team_unas][3] + 1  ## set number of searchers in unassigned
        yy.saveLastIDentry = yy.sarID.text()
        yy.sarID.setText("")  ## clear sarID field
        if (DEBUG == 1): print("PTR2 %s"%yy)
        zz.masterBlink = 10      ## set time for blinker to run until restarted 10 * 0.5 = 5sec
        zz.time_chk()            ## start blinker clock
        ##print("SRCHR chk2: %s"%zz.SRCHR)  
        zz.tabload(yy,0)         ## load display table


    def _rmSrchr(self): ## button REMOVE SEARCHER
        zz = self.zz2
        yy = self.mm
        #
        ## Can send a bit back to sign-in that the member is associated with a Team (vs Unassigned)
        ##   to indicate that the member cannot be removed.  To create this bit check the SRCHR
        ##   team location [5] and [6] to see if = Nunas_col, 1 (Unassigned)
        #

        memPtr = -1
        sarIDval = yy.sarID.text()
        if (sarIDval == ""):   ## blank entry means to remove previous ADD searcher (probably incorrect member chosen)
          sarIDval = yy.saveLastIDentry       ####  NEED to get agency, too  PARSE ID and agency from entry

        sarINFOsplit = sarIDval.split()       ## SAR ID field can be "ID" or "ID AGENCY"
        sarIDval = sarINFOsplit[0].upper()
        sarAGENCY = "NC"                      ## default AGENCY
        if (len(sarINFOsplit) > 1):           ## then agency arg was entered
          sarAGENCY = sarINFOsplit[1].upper()
          
        for xx in range(0,len(zz.MEMBERS)):
          if (zz.MEMBERS[xx][1] == sarIDval and zz.MEMBERS[xx][2] == sarAGENCY):
            memPtr = xx
            break
        if (memPtr == -1):
            winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, member not found
            return
        if (DEBUG == 1): print("PTR  %s"%memPtr)        
        fnd = -1
        for ptr in range(0, len(zz.SRCHR)-1):  ## do not test the lst element (END)
          ## match ID and agency  
          if (zz.SRCHR[ptr][2] == sarIDval and zz.SRCHR[ptr][1] == sarAGENCY):
            fnd = 1
            if (DEBUG == 1): print("ID, Cnty %s %s"%(zz.SRCHR[ptr][2],zz.SRCHR[ptr][1]))
            break
        if (fnd == -1 or (zz.SRCHR[ptr][5] != yy.Nunas_col and zz.SRCHR[ptr][6] != 1 )): ## TEAM of SRCHR must be UNASSIGNED
            winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, searcher not found
            return          
        TimeOUT = time.time()                         ## add to MEMBERS record
        zz.MEMBERS[memPtr][6] = TimeOUT               ##  set as checked-out
        zz.MEMBERS[memPtr][9] = zz.MEMBERS[memPtr][9] + zz.MEMBERS[memPtr][6] - zz.MEMBERS[memPtr][5]  ## cum time
        zz.MEMBERS[memPtr][5] = -1                    ## reset for next checkin
        rowy = zz.SRCHR[ptr][4]
        colx = zz.SRCHR[ptr][3]
        npt = rowy + (colx - yy.Nunas_col)*yy.Nrows
        zz.UNAS_USED[npt] = 0
        del zz.SRCHR[ptr]                     ## we are deleting the record and marking MEMBERS entry with TimeOUT
### Will only remove if in Unassigned.  THEN, also put the space as available again  
        yy.sarID.setText("")
        zz.tabload(yy,0)                      ## update table


    def _undo(self): ## Button UNDO - put status/display back one change, saving MEMBERS, too
        zz = self.zz2
        yy = self.mm
        if (DEBUG == 1): print("At undo %i \n" % self.modex)
        ## call undo_table (single deep)

        #print("POP1: %s"%zz.saveTeam)
        zz.saveTeam.pop()
        try:
          zz.TEAMS = zz.saveTeam.pop()      
        except:
          print("End of queue")
          winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty          
          return
        zz.saveSrchr.pop()
        zz.SRCHR = zz.saveSrchr.pop()
        zz.saveUnUsed.pop()
        zz.UNAS_USED = zz.saveUnUsed.pop()
        zz.saveMembers.pop()                ## these are double pop's because of intervening append
        zz.MEMBERS = zz.saveMembers.pop()
        zz.tabload(yy,0)
        

        
    def _readMemb(self): ## Button READ MEMBERS from CVS files
        ###  nominally the ncssar members.csv and OTHERS.csv files are read to get member info.
        ####### FOR the case when the INFOX box starts with JSON, instead this is a recovery and
        #######   the latest JSON files are read and populate TEAMS, SRCHR, UNAS_USED and MEMBERS
        def useLEEp(elem):  # function for sort of Event IDs by Last Event Epoch
           return elem[0]

        ww = self.ww
        
        caps = ["EMT", "PM"]  ##  capabilities for Medical type - probably temporary?
        yy = self.mm
        zz = self.zz2
        if (DEBUG == 1): print("At readmemb %i\n" % self.modex)
        self.modex = 1 - self.modex    ## change state  test
        xmodel(self.modex)             # call routine outside of class test
        test_info = yy.infox.text()
        if (test_info[0:4].upper() != "JSON" and test_info[0:3].upper() != "REM" ): # 4th char "O" for CSV or "2" for SQL
            ## if INFOX has "JSON" means recovery; if REMOTE means get info from sign-in program output
          if (zz.READIN == 0):  ## otherwise skip MEMBERS read-in, but do OTHERS read-in
             zz.MEMBERS = []          ## reset list
             zz.READIN = 1      ## set as having been read
                   
             my_file = Path("MEMBERS2.csv")       #############  NCSSAR member database
             if my_file.is_file():
               with open(my_file,'rt') as csvIN:
                 csvPtr = csv.reader(csvIN, dialect='excel')
                 regShrf = r"[0-9][A-Z].*"        ## reg ex to find sheriff IDs
                 for row in csvPtr:
                   make = ["0", "0", "NC", "0", "0", -1, -1, " ", " ", 0]  ## MEMBERS: need to re-initalize make here for some reason
                   if (row[0].isdigit()):        ## has to be all digits (searcher)
                     make[1] = row[0]   # SAR ID
                     make[0] = row[1]   # name
                     make[7] = row[3]   # cell number
                     make[8] = row[5]   # resources
                     for cx in caps:
                       regcap = r"[ ,]" + cx + r"[ ,]"
                       fnd = re.search(regcap, row[5])
                       if (fnd != None):     ## found a match (sets MEDICAL bit)
                         make[4] = "1"   
                     if (row[6] == "1"):       ## type 1 searcher; used for now to choose LEADER (temporary)
                       make[3] = "1"        
                   elif (re.search(regShrf, row[0]) != None):    ## numb/letter... found sheriff coord
                     make[1] = row[0]
                     make[0] = row[1]
                     make[7] = row[3]   # cell number
                     make[8] = row[5]   # resources
                   else:
                     continue                   ## valid entry not located - go to next line
      #
      ## For remote sign-in do we want to check if member has already been loaded?
      ## For pickup from sign-in do we want to assign time-in and then time-out to MEMBERS db?
      ##     Or when using sign-in program, we do not use MEMBERS db??
      ## From sign-in need: Name, ID#, Agency, leader, medical, time-in, time-out, capabilities? (Carda, OHV, Nordic...)
      ##      if done, any need for Members db? could save info for searcher, while eliminating from SRCHR db when they leave
      #              
                   zz.MEMBERS.append(make)        ## load MEMBERS if valid entry
                   zz.AssignCheck.append([0, 0])
               if (DEBUG == 1): print("\n\n")
               if (DEBUG == 1): print("READ: %s:%s"%(zz,self.zz2))
             else:
               winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty
               return
                 
             zz.SRCHR.clear()             ##  reset for now only first time thru
             zz.SRCHR.append(["END"])     ## preset the first time thru
            
          my_file = Path("OTHERS.csv")

##### Could check for existing ID and agency and replace upon readin

          ###  format of OTHERS.csv is "Member,ID,agency,Leader,Medical,(add CheckedIn)(maybe add time-out?)" 
          if my_file.is_file():
            if (DEBUG == 1): print("In other")  
            with open('OTHERS.csv','rt') as csvIN2:
              csvPtr = csv.reader(csvIN2, dialect='excel')
              for row in csvPtr:
                ## name, ID, Agency
                row = [row[0],row[1],row[2],row[3],row[4],-1, -1, " ", " ", 0]      ## will map to srchr
                ifnd = 0  
                for ix in range(len(zz.MEMBERS)):          
                  if (row[1] == zz.MEMBERS[ix][1] and row[2] == zz.MEMBERS[ix][2]): ## match: ID,agency
                    del zz.MEMBERS[ix]         ##    update entry
                    zz.MEMBERS.insert(ix,row)
                    ifnd = 1                   ## mark event
                    break                      ## done, so skip the rest
                if (ifnd == 0):                ##    add
                  zz.MEMBERS.append(row)       ## possibly change # and order of cells
                  zz.AssignCheck.append([0, 0])
                  if (DEBUG == 1): print("new row: %s" % row)  
          ### ignore otherwise
          if (DEBUG == 1): print("READ: %s"%zz.SRCHR)
          
        elif (test_info[0:4].upper() == "JSON"): ## read json files to load MEMBERS, TEAMS, SRCHR, UNAS_USED for RECOVERY
            if (DEBUG == 1): print("JSON found")
            mt1 = 0
            for m in range(0,5):    # find most recent saved state file
              mtime = os.path.getmtime("DATA\saveAll"+zz.saveNames[m]+".json")  ## file modified time
              if (mtime > mt1):
                  mt1 = mtime
                  mpnt = m
            setName = zz.saveNames[mpnt]
               ##   Newest save time.  If corrupted, then delete
               ##   the set and use the other one
            ##print("Set: %s"%setName)
            zz.READIN = 1   ## set as having read members in
            try:
              with open("DATA\saveAll" + setName + ".json", 'r') as infile:  ## opens, reads, closes
                [zz.TEAMS, zz.SRCHR, zz.MEMBERS, zz.UNAS_USED, zz.TEAM_NUM, \
                    zz.RemoteSignInMode, zz.eventID, zz.AssignCheck] = json.load(infile)   
              print("Doing recovery reload...RMT SIGNIN=%i"%zz.RemoteSignInMode)
              zz.tabload(yy,0)
            except:
              print("Bad JSON save file, try another version of the file")
              winsound.Beep(2500, 1200)       ## BEEP, 2500Hz for 1 second, needs to be empty
            if (zz.RemoteSignInMode >= 1):   # we were in remote mode
                self.priorRead = []          # need to restore previous entries (OR check if they are already
                                             #  entered in MEMBERS
                ww.setDaemon(True)
                ww.start()                 ## starts thread chk4data
                zz.srchr_chk(yy)           ## start checking for remote entry updates, again (json recovery)
        else:   # MUST be REMOTE  will check every so many seconds and see if file time-modified is updated
                #  So need timer to call routine to check if interface file modify time has changed.
            zz.READIN = 1  # started reading in via remote
            self.priorRead = []
            print("AT remote: %s %s %s"%(self,yy,zz))
            if (test_info[3] == "2"):
                ####
                ##   CHECK if can access cloud db  - if not, set test_info message and return
                ##          if Okay print events table
                ####
                codex = " "
                try:
                  response = requests.request("GET", event_url, headers=headers, data = payload)
                except:
                  stat = 408
                  codex = " - T/O"
                else:                 
                  #r=requests.get(url=self.host+"/api/v1/events")  ## to get events table
                  stat=response.status_code # gives status to check if got valid return
                if (stat != 200):
                    self.mm.infox.setText('Error: No server connection, try again'+codex)
                    return
##    HOW DID I GET PAST here with no internet connection???????
                if (test_info[4] == '-'):
                  zz.eventID = "/"+test_info[5:]  # integer as a string
                else:    # search for eventID
 ## Pickup Event Name, Date and ID list here ...
 ##     Ask which to choose                   
                  j=response.json()      # r.json() returns a list of dictionaries
                  ##print("Check connection status: %s, value: \n%s"%(stat,j))
                  ## find entry with most recent activity
                  LEE = []
                  entry = []
                  for d in j:
                    entry.append(d['LastEditEpoch'])  ## use last edit epoch as an indication of the current activity LEE.append(entry1)
                    entry.append(d['LocalEventID'])
                    entry.append(d['EventName'])
                    entry.append(d['EventStartDate'])
                    print('%s %s, %s'%(entry[1],entry[2],entry[3]))
                    LEE.append(entry)     ## old method to find most recent eventID activity
                    entry = []
                    ## Ask using format: dialog_was_clicked
                    
                  
                  # sort entries decending using LEEpoch
                  LEE.sort(key=useLEEp,reverse=True)         # descending time
                  
                  if (1==1):   # create indent
                    #   only keep the top 4
                    
                    cx = 100
                    rx = 100   # upper left corner of window
                    self.tableWidget6.move(cx, rx)  
                    ## Ename, Esdate, Eid
                    for i in range(0,4):
                        for j in range(1,4):
                           itemv = str(LEE[i][j])
                           item = QtWidgets.QTableWidgetItem(itemv)
                           self.tableWidget6.setItem(i+1,j-1,item)   ## r,c,val  0-based
                        ## id:4 digits, Name:20 chars, StartDate: 12 chars
                    ## using tablewidget6
                    self.tableWidget6.show()
### need code to find selected row, hence eventID                    
                  val = 0
                  for indx in range(len(LEE)):  ## this old loop scans for most recent change Epoch
                    xval = float(LEE[indx][1])    ## LEE was a dictionary
                    if (xval > val):
                      val = xval
                  ## set eventID to local value
                  zz.eventID = "/"+str(j[indx-1]['LocalEventID'])  ##  dictionary entries are zero based
                  
                print("EventID %s"% zz.eventID)
                zz.RemoteSignInMode = 2  # SQL
                ww.setDaemon(True)
                ww.start()               ## starts thread chk4data
                print("Start sql check")
            else:    
                zz.RemoteSignInMode = 1  # CSV
            zz.srchr_chk(yy)             ## start checking for remote entry updates (original)

            
    def rmtInProcess(self):    
            ########### PUT the following in a routine called by timer
            ###   Start timer above
            ##  Enable check remote sign-in timer above; In timer routine check time modified and if so, do...
 
        ##*SARID, "NAME(LAST,FIRST)", AGENCY, RESOURCES, TIME-IN(HUMAN), TIME-OUT, TIME-DELTA, TIME-IN(EPOCH FLOAT),
        ##         TIME-OUT, TIME-DELTA, CELL#, "STATUS(SignedIn, SignedOut, Unassigned, Committed)"
        
        ##     Status exchange: SignIn from Sign-in program, acknowledge by Unassigned from Tcard
        ##                      which enables SignOut, being Committed blocks Signout
        ##     When Tcard sees Sign-In checks for a MEMBERS entry from a previous participation, if found update
        ##          sign-in and sign-out times. Delta will accumulate. Also, create a SRCHR entry
        ##          Then update the remote file status to Uncommitted and write file.  Also change priorRead db status, too     
        ##     When a member tells Tcard they are leaving, Tcard allows this when Uncommitted.
        ##          After signout removes the SRCHR entry, updates the MEMBERS entry to
        ##          set the time-out and delta times.  Committed blocks signout

        ####
        ##  Sequence of operations:
        ##     chk4data (separate thread) gets activated each 15sec and sets RMTchange flag if there is
        ##                 a data change
        ##     srchr_chk calls rmtInProcess each 15 sec.  Upon entry rmtInProcess checks the
        ##                 RMTchange flag.  If 0 it returns, otherwise executes
        ####
            char1_0 = ["0","1"]  ## use to convert number 0 and 1 to char "0" and "1" vs false, true
            yy = self.mm
            zz = self.zz2
            print("RMTchange %i"%zz.RMTchange)
            team_unas = 6                    ####   This is the number of the entry for the Unassigned Team
                                             ##         This may change as default or over time

            if (DEBUG == 1): print("At Remote sign-in")
            server = "x:\\Download\\"    ## on Android device
            ##server_loc = "c:\\Tcard\\signin_files\\"
            server_loc = "c:\\Users\\Steve\\Documents\\python\\signin_files\\"
            server = server_loc  ## set for local disk program debug
            lenPrior = len(self.priorRead)
            rows = []
            update = 0     # only reading remote file
            deltaTime = 10 # number of seconds old is time stamp - must be rogue

###            
###  call to SQL SERVER
###
            test_info = yy.infox.text()
            if (test_info[3] == "2"):       ## Do not want to call sync, nor do other processing, unless:
                                              #    AssignCheck delta  or RMTchange
              print("Top of SQL data check")                                
              SYNCcall = 0     # preset flag  - local set=1 when call made to sync (get of cloud db)                           
              ## AT some point, update LOCAL SQL sqlite3 database (here?)
                
## Determine if there have been searcher STATUS CHANGEs between Committed and Uncommitted that need to get
              # sent to server
              if (len(zz.SRCHR) > 1):
                for iz in range(0,len(zz.SRCHR)-1):  ## scan all searchers don't include 'END'
                  memPtr = zz.SRCHR[iz][12]
                  istate = 1
                  if (zz.SRCHR[iz][5] == yy.Nunas_col and zz.SRCHR[iz][6] == 1):  # current area is Unassigned
                      istate = 0
                  if (zz.AssignCheck[memPtr][1] == 2):   ## just added
                      zz.AssignCheck[memPtr][1] = 0
                      zz.AssignCheck[memPtr][0] = -1     # set as changed to Uncommitted
                      if (SYNCcall == 0):
                          print("At sync call 1")
                          csvPtr = self.sync()  # csvPtr order uses 'self.columns'
                          SYNCcall = 1
                  else:                                            ## recheck
                      zz.AssignCheck[memPtr][0] = istate - zz.AssignCheck[memPtr][1]   # set change value
                      if (zz.AssignCheck[memPtr][0] != 0 and SYNCcall == 0):
                          print("At sync call 2")
                          csvPtr = self.sync()  # csvPtr order uses 'self.columns'
                          SYNCcall = 1
                      zz.AssignCheck[memPtr][1] = istate  # update prev state delta-> -1 to Unassigned; +1 to Assigned; 0 no change
                  print("AssignCheck: ->%s for %s"%(zz.AssignCheck[memPtr][0], zz.SRCHR[iz][0]))
                  if (zz.AssignCheck[memPtr][0] != 0): # searcher moved to Uncommitted or Committed
                      # find searcher in csvPtr (match ID, Agency, timeIn epoch from MEMBERS
                      if (DEBUG == 1): print("found %s:%s:%f"%(zz.MEMBERS[memPtr][1],zz.MEMBERS[memPtr][2],zz.MEMBERS[memPtr][5]))
                      ifnd = 0
                      for cx in csvPtr:     # match ID, Agency, TimeInEpoch
                          if (DEBUG == 1): print("Look: %s:%s:%f"%(cx[0],cx[2],cx[7]))
                          if (cx[0] == zz.MEMBERS[memPtr][1] and cx[2][0:2] == zz.MEMBERS[memPtr][2] and cx[7] == zz.MEMBERS[memPtr][5]):
                              ifnd = 1
                              break
                      ##  do we want to put in an error check if not found?      
                      if (ifnd == 1):
                          if (zz.AssignCheck[memPtr][0] == -1):  # set changed status: -1 => to Uncommitted; 1 => to Committed
                              cx[11] = 'Uncommitted'
                          else:
                              cx[11] = 'Committed'
                          self.sendAction(cx)   ## comm to sql server
              rem = []   #  don't use rem - remove searcher function (mgmt does not want that operation) for now in this mode

            else:    ## test_info = 1 USING CSV FILE TRANSFER 
## first scan members for searchers removed from Tcards
      ## add code to check MEMBERS db for new Time-out (previous T/O # are negative)
      ## If any found, change record status to Uncommitted? for each
      ##  negate Time-out value in MEMBERS db
              if (DEBUG == 1): print('b4 look for rm members')
              ifnd = 0         # indicates found at least one sign-out
              rem = []
              for ix in range(len(zz.MEMBERS)):
                if (float(zz.MEMBERS[ix][6]) > 0):      # timeout set, so removed from Tcard
                    rem.append(ix)               # create list of members to remove
                    ifnd = ifnd + 1
                    if (DEBUG == 1): print("RM %i"%ix)
            
              ##print('b4 lock')
    ### create file LOCK
              while (1):                    
                    curT = time.time()               # current time
                    while (1):
                        files = glob.glob(server_loc + 'rmt_lock_*')
                        if (len(files) == 0): break  # no lock files found
                        for fi in files:
                            strt = fi.find('#')+1
                            fi_time = int(float(fi[strt:len(fi)]))
                            if ((curT - fi_time) > deltaTime):         ## file around too long
                                #print("remove %f"%deltaTime)
                                os.remove(fi)
                    strCurT = str(curT)
                    rand = int(strCurT[-1])       # use to get different delays
                    time.sleep(rshift(rand,7))    # delay by rand/128 
                    cname = os.environ['COMPUTERNAME']
                    fx = open(server_loc + 'rmt_lock_' + cname + '#' + strCurT, 'w+')  ## create lock
                    fx.close()
                    files = glob.glob(server_loc + 'rmt_lock_*')
                    if (len(files) > 1):          # someelse created a lock too
                        os.remove(server_loc + 'rmt_lock_' + cname + '#' + strCurT)
                    else: break                   # only our lock; continue on    
                 #  loop back ; end file lock
              if (DEBUG == 1): print('aftr lock; List of removes %s'%rem)
  
## code to find most recent sign in csv file; do we need to repeat?  Is the file name changing?
              files = glob.glob(server + 'sign-in_*')  # filename: sign-in_<search>_<date>_HHMM.csv
              if (len(files) == 0):
                print("No connection to external sign-in database")
                if (self.flag_noconn == 0):
                  winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second
                  winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second
                  winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second
                  winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second                  
                  self.flag_noconn = 1
                return()
              self.flag_noconn = 0    
              timex = 0
              ifi = 0
              ifipnt = 0
              for fi in files:
                fix = fi[len(server):] # extract portion after sign-in
                file_parts = fix.split("_")
                # print("FILE: %s"%fi)
                year = int(file_parts[5])
                mon  = (file_parts[3].find("Jan_Feb_Mar_Apr_May_Jun_Jul_Aug_Sep_Oct_Nov_Dec")+4)/4
                day  = int(file_parts[4])
                hhmm = int(file_parts[6][0:-4])  ## remove '.csv'
                timei = ((year*12+mon)*31+day)*2400+hhmm
                # print("time: %i"%timei)
                if (timei > timex):
                  timex = timei
                  ifipnt = ifi
                ifi = ifi + 1        
              new_file = files[ifipnt]
              file_parts = new_file.split("_")
              self.incident = file_parts[1]
              self.idate = file_parts[3]+"-"+file_parts[4]+"-"+file_parts[5]
##  instead of looking at file name look at modified date
              mtime2 = os.path.getmtime(new_file)       ## file modified time
              # print("Times %s : %s"%(zz.lastTime, mtime2))
              if (mtime2 == zz.lastTime): 
                if (DEBUG == 1): print("Leave remote, no new file")
                return()                             ## no new file
              zz.lastTime = mtime2                      # update time
              self.prev_file = new_file                ## set latest file as prev file for next pass
## end code to find most recent file
        
              #X with open(server + 'REMOTE_SIGN_IN.csv','rt') as csvIN2:
              with open(self.prev_file,'rt') as csvIN2:
                csvPtr = csv.reader(csvIN2, dialect='excel', skipinitialspace=True)
              #
### DECODE each input line from SQL or CSV            
###########
            if (True):   ## Indent fixer
              print("Top of combo check")  
              if (test_info[3] == "2"):    # sql db usage
                  if (zz.RMTchange == 0): return     ## leave, no changes
                  elif (SYNCcall == 0):             # csvPtr did not get updated, need to do it now
                      print("At sync call 3")
                      csvPtr = self.sync()  # csvPtr order uses 'self.columns'
                      SYNCcall = 1
                  zz.RMTchange = 0          # reset to force check for changes again, later   
            ## this code gets executed for either CSV or SQL input
              irow = 0  
              if (DEBUG == 1): print('open remote signin file')
              for row in csvPtr:
                  rows.append(row)   ## create rows list by combining each row
                  irow = irow + 1    ### always read entire file comparing lines
                  ##print('rowlong %s'%row)
                  if (DEBUG and len(row) > 1): print("RMT row%i: %s, %s: lenP %i"% (irow,row[0],row[1],lenPrior))
                  if (row[0].startswith("*") or row[0].startswith("#") or row[0].startswith("ID")):
                      continue             ## skip comment lines
                  if (irow <= lenPrior):   #Ax # for existing lines, first compare to prior
                      if (DEBUG == 1): print("At compare")
                      if (1 == 0):  #Ax  get rid of check since one direction (self.priorRead[irow-1] != row):
                          if (DEBUG == 1): print("At difference check\n   %s\n   %s"%(self.priorRead[irow-1],row))    ## check for differences if name, sarid -> give error
                          if (row[0] != self.priorRead[0] or row[2] != self.priorRead[2]):
                              print("Error in remote file at %s"% row)
                              winsound.Beep(2500, 300)           ## BEEP, short 2500Hz
                              winsound.Beep(1000, 1200)          ## double
                              winsound.Beep(2500, 300)
                              break


######check what should be the preset value for timeIn and Out as 0 or -1 from SignIn program
                            
                          ## check for change: timeout times, delta time and status s/b SignOut
                          ##   if other changes issue warning
                          # find MEMBERS entry
                      else:  #Ax   part of indent fixer    
                          memPtr = -1
                          for ix in range(0,len(zz.MEMBERS)):  ## look thru all entries to see if already member
                              ##Ax print('ix=%i:%s:%s:%s'%(ix,row[0],row[2],zz.MEMBERS[ix][2]))
                              ##Ax Note, Only using first two char of agency, below
                              if (row[0] == zz.MEMBERS[ix][1] and row[2][0:2] == zz.MEMBERS[ix][2]): ## match: ID, agency
                                  memPtr = ix
                                  print('MeM ptr %i:%s'%(memPtr,row))
                                  break
                          if (memPtr == -1 and len(zz.MEMBERS) > 0 and row[11] != "SignedOut"):  #Ax # if signed-out, still in MEMBERS
                              print("Record not found in MEMBERS: %s"% row)
                              winsound.Beep(2500, 300)
                              return                      ## record not found
                          elif (memPtr in rem):           # did we find a member to be removed?
                              rows[irow-1][11] = "Uncommitted"   
                              zz.MEMBERS[memPtr][6] = -zz.MEMBERS[memPtr][6]     # negate as flag that sign-out has processed
                              ##print("Update MEM for RM %i, irow %i"%(memPtr, irow))
                          if (row[11] == "SignedOut"):      ## completed signOut
                              pass                        # should already have updated the following:
                              #zz.MEMBERS[memPtr][6] = row[8]                           # timeout
                              #zz.MEMBERS[memPtr][9] = zz.MEMBERS[memPtr][9] + row[9]   # delta time cum
                          elif (row[11] == "SignedIn"):    ## re-signIn    
                            if (False):           ##Ax DISABLE FOR NOW DUE to NON-SHARED input 
                              zz.MEMBERS[memPtr][5] = row[7]                           # timein
                              zz.MEMBERS[memPtr][6] = -1                               # timeout
                              #### create SRCHR entry
                              ## find vacancy in UNAS_USED
                              for ixx in range(2,len(zz.UNAS_USED)):
                                  if ((ixx % yy.Nrows) == 0): continue   ## skip all rows == 0
                                  if (zz.UNAS_USED[ixx] == 0):           ## found available location
                                      zz.UNAS_USED[ixx] = 1
                                      break
                              colu = int(ixx/yy.Nrows)
                              rowu = ixx - colu * yy.Nrows
                              colu = colu + yy.Nunas_col
                              zz.SRCHR.insert(-1,[zz.MEMBERS[memPtr][0],zz.MEMBERS[memPtr][2],zz.MEMBERS[memPtr][1],  \
                                 colu, rowu, yy.Nunas_col, 1, zz.MEMBERS[memPtr][3], zz.MEMBERS[memPtr][4], 5, \
                                 zz.MEMBERS[memPtr][7], zz.MEMBERS[memPtr][8],memPtr]) # set blink to 5 sec
                              zz.TEAMS[team_unas][3] = zz.TEAMS[team_unas][3] + 1  ## set number of searchers in unassigned
                              rows[irow-1][11] = "Uncommitted"  
                              zz.masterBlink = 10      ## set time for blinker to run until restarted 10 * 0.5 = 5sec
                          elif (row[11] == "Uncommitted" or row[11] == "Committed"):
                                               ## Already Signed-In and on Tcard
                              pass    # just continue on
                          else:
                              print("Unexpected changes in record: %s"% row)
                              winsound.Beep(2500, 300)
                  else:
                      #B
                      #B   check if already in MEMBERS, issue warning only
                      fnd = 0
                      for ix in range(0,len(zz.MEMBERS)):  ## look thru all entries to see if already member
                          if (row[0] == zz.MEMBERS[ix][1] and row[2][0:2] == zz.MEMBERS[ix][2]): ## match: ID, agency
                              if (zz.MEMBERS[ix][6] != 0):  ## record exists (checking TimeOut), but was signed-out
                                  fnd = 2
                              else:    
                                  print('Warning: Member already admitted %s: %s: %s'%(row[0], row[1], row[2]))
                                  fnd = 1
                              break
                      if (fnd == 1): continue  ## skip     
                      #B
                      if (DEBUG == 1): print("New entry %s"%row[3])
                      ## should be for new sign_in only, so only time-in set and status s/b set as SignIn
                      ##print('stat :%s:'%row[11])

########### have test code:  \/  commented PUT below

                      if (row[11][0:8] == "SignedIn" or 1 == 1):
                          ## check resources row[3] for LD and MED and set logic 0 or 1
                          lead = char1_0[row[3].find("LD") >= 0]
                          med = char1_0[row[3].find("PM") >= 0 or row[3].find("EMT") >= 0]  ## Del says not to include RN
                          ##print("Lead & Med %s , %s"%(str(lead),str(med)))
                          ##Ax Note, only use first 2 char of Agency
                          if (fnd == 2):
                              zz.MEMBERS[ix][6] = row[8]  ## index ix from above - previously existing
                              zz.MEMBERS[ix][5] = row[7]
                          else:    
                              rownu = [row[1], row[0], row[2][0:2], str(lead), str(med), row[7], row[8], row[10],row[3], row[9]] # watch for numeric vs string
                              zz.MEMBERS.append(rownu)
                              zz.AssignCheck.append([0, 2])  # set state flag to note ADDed to Uncommitted
                              ix = len(zz.MEMBERS)-1         # set ix as pointer

                          #### create SRCHR entry
                          ## find vacancy in UNAS_USED
                          for ixx in range(2,len(zz.UNAS_USED)):
                              if ((ixx % yy.Nrows) == 0): continue   ## skip all rows == 0
                              if (zz.UNAS_USED[ixx] == 0):           ## found available location
                                  zz.UNAS_USED[ixx] = 1
                                  break         
                          colu = int(ixx/yy.Nrows)
                          rowu = ixx - colu * yy.Nrows
                          colu = colu + yy.Nunas_col
                          ## take only the first 2 char of Agency  #Ax
                          zz.SRCHR.insert(-1,[row[1], row[2][0:2], row[0], colu, rowu, yy.Nunas_col, 1, str(lead), \
                                          str(med), 5, row[10], row[3],ix])       # set blink to 5 sec
                          zz.masterBlink = 10      ## set time for blinker to run until restarted 10 * 0.5 = 5sec      
                          zz.TEAMS[team_unas][3] = zz.TEAMS[team_unas][3] + 1  ## set number of searchers in unassigned
                          rows[irow-1][11] = "Uncommitted"   
                      else:
                          print("Unexpected Status: %s %s, possibly at initial database connection"%(row[0:3],row[11]))
                          #C winsound.Beep(2500, 300)
              #
                          
            if (DEBUG == 1): print('prior to tmp open')
#$#
            if (test_info[3] != "2"): 
              with open(server + 'remote_tmp.csv', 'w+', newline='') as csvOUT:      ##  create a tmp updated interface file
                csvPtr = csv.writer(csvOUT, dialect='excel', skipinitialspace=True)            
                csvPtr.writerows(rows)
                
              if (DEBUG == 1): print('opened and wrote tmp file')
              #Ax os.remove(server + 'REMOTE_SIGN_IN.csv')     ## remove pre-existing file
              #Ax os.rename(server + 'remote_tmp.csv', server + 'REMOTE_SIGN_IN.csv')  ## put tmp file into normal file
              #Ax2 os.remove(self.prev_file)                             ## remove pre-existing file
              #Ax2 os.rename(server + 'remote_tmp.csv', self.prev_file)  ## put tmp file into normal file
              os.remove(server_loc + 'rmt_lock_' + cname + '#' + strCurT)    ## remove lock file
#$#
            if (DEBUG == 1): print('changed files')
            yy.saveLastIDentry = yy.sarID.text()
            yy.sarID.setText("")  ## clear sarID field
            if (DEBUG == 1): print("PTR2 %s"%yy)
            #Dzz.masterBlink = 10      ## set time for blinker to run until restarted 10 * 0.5 = 5sec
            zz.time_chk()              ## start blinker clock
            ##print("SRCHR chk: %s"%zz.SRCHR)
            zz.tabload(yy,0)
            
            ## At end save current input to priorRead
            ## print("Rows: %s"% rows)
            self.priorRead = rows
            ##print("PriorRead: %s"% self.priorRead)


    def numbers(self,n):  ## take the number buttons and fill SAR ID field
        strg1 = ["D", "E", "N", "P", "S", "T"]
        strg2 = [["H", " ", "R", "G", "M", "A", "U", "Y", "B", "L"], \
                 ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]]
        yy = self.mm
        if (DEBUG == 1): print("Button %i : %i\n"%(n, yy.keyBrd))
        ## if "B" num=10 delete a character
        if (n == 17):
          yy.keyBrd = 1 - yy.keyBrd   ## toggle
          yy.setKeys(yy.keyBrd)
          return
        strg = yy.sarID.text()
        if (n == 10):  ## backspace
          yy.sarID.setText(strg[0:-1])
        elif (n > 10):  
          yy.sarID.setText(strg+strg1[n-11])
        else:  # n < 10
          yy.sarID.setText(strg+strg2[yy.keyBrd][n]) 

    def prntScrn(self):
      user32 = windll.user32
      user32.SetProcessDPIAware()
      im = ImageGrab.grab(bbox=None)
      im.save('screenshot.png')
      self.prnt('screen')
      
    def prnt104(self):
      self.prnt('p104')

      

    def prnt(self,type):  ## type = screen or ??
      yy = self.mm
      zz = self.zz2
        
#
# Constants for GetDeviceCaps
#
#
# HORZRES / VERTRES = printable area
#
      HORZRES = 8
      VERTRES = 10
#
# LOGPIXELS = dots per inch
#
      LOGPIXELSX = 88
      LOGPIXELSY = 90
#
# PHYSICALWIDTH/HEIGHT = total area
#
      PHYSICALWIDTH = 110
      PHYSICALHEIGHT = 111
#
# PHYSICALOFFSETX/Y = left / top margin
#
      PHYSICALOFFSETX = 112
      PHYSICALOFFSETY = 113

      printer_name = win32print.GetDefaultPrinter ()

#
# You can only write a Device-independent bitmap
#  directly to a Windows device context; therefore
#  we need (for ease) to use the Python Imaging
#  Library to manipulate the image.
#
# Create a device context from a named printer
#  and assess the printable size of the paper.
#
      hDC = win32ui.CreateDC ()
      printer_name = win32print.GetDefaultPrinter()  # added
      hDC.CreatePrinterDC (printer_name)  ## 600 dpi
      printable_area = hDC.GetDeviceCaps (HORZRES), hDC.GetDeviceCaps (VERTRES)
      printer_size = hDC.GetDeviceCaps (PHYSICALWIDTH), hDC.GetDeviceCaps (PHYSICALHEIGHT)
      printer_margins = hDC.GetDeviceCaps (PHYSICALOFFSETX), hDC.GetDeviceCaps (PHYSICALOFFSETY)
      if (DEBUG): print("PA: %s   PS: %s  PM: %s"%(printable_area,printer_size,printer_margins))
#
# Start the print job, and draw the bitmap to
#  the printer device at the scaled size.
#
      hDC.StartDoc ("print_output")
  
      if (type == 'screen'):
        hDC.StartPage () 
        file_name = "screenshot.png"
#
# Open the image, rotate it if it's wider than
#  it is high, and work out how much to multiply
#  each pixel by to get it as big as possible on
#  the page without distorting.
#
        bmp = Image.open (file_name)
##bmp = bmp.rotate (90)  
        ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
        if (DEBUG): print("RAT: %i:%i,%i:%i"%(printable_area[0],bmp.size[1],printable_area[1],bmp.size[0]))
        scale = min (ratios)
        dib = ImageWin.Dib (bmp)
        scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
        if (DEBUG): print("Scale: %i:%i"%(scaled_width, scaled_height))
        x1 = int ((printer_size[0] - scaled_width) / 2) 
        y1 = int ((printer_size[1] - scaled_height) / 2)
        x2 = x1 + scaled_width -80  # fudge factor
        y2 = y1 + scaled_height
        if (DEBUG): print("rectup: %i,%i,%i,%i"%(x1,y1,x2,y2))
        dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))
        hDC.EndPage()
      else:   ##  104 output
        xt1 = yy.t1.text()
        xt2 = yy.t2.text()
        if (xt1 == ""):  # set defaults
            xt1 = "0"
            xt2 = "1000"
        fontdata = {'name':'Consolas', 'height':100}
        font = win32ui.CreateFont(fontdata)
        hDC.SelectObject(font)
        self.prnt_104form(hDC,xt1,xt2)  # t1, te first and last team number; last is blank for 1 team
                                       # team starts with "T" and are usually integers; if 1 team can be alphanumeric name
      hDC.EndDoc ()
      hDC.DeleteDC ()
      print("print complete")

    def prnt_104form(self,hDC,t1,te): #t1 is first team, te is end team to print
###
        if (DEBUG == 1): print("In prnt104 Teams")
        yy = self.mm
        zz = self.zz2
        
        Tsort = sorted(zz.TEAMS[0:-1],key=itemgetter(0))  ## ignore "end"        
        Ssort = sorted(zz.SRCHR[0:-1],key=itemgetter(3,4))
        if (DEBUG == 1): print("T:%s"%Tsort)
        tsStrt = 0
        ssStrt = 0
        ## write header
        while 1:
         for ts in range(tsStrt,len(Tsort)):  ## possibly use while
           ifnd = 0
           # Look for leading T (only) for new Team number format
           #   Not printing out 'teams' that are not in the field
           if (Tsort[ts][0][0:1] == "T" and Tsort[ts][1] < yy.Nunas_col):
              if (len(te) == 0):
                  if (t1!= Tsort[ts][0][1:]): continue
              else:
                  it1 = int(t1)  # maybe check to be sure these are numbers
                  ite = int(te)
                  if (int(Tsort[ts][0][1:]) < it1 or int(Tsort[ts][0][1:]) > ite): continue  # skip
              hDC.StartPage ()     
              # (Tsort[ts][0], Tsort[ts][4], Tsort[ts][5])) # team name, type, location
              for yax in (0, 3200):
                hDC.TextOut(500,500+yax,"TEAM ASSIGNMENT     Incident:             Operational Period and Team Number")
                hDC.TextOut(1000,600+yax,"  %-20.20s %-12.12s      %-5.5s "%(self.incident,self.idate,Tsort[ts][0]))
                hDC.TextOut(500,700+yax,"Resource Type:   "+Tsort[ts][4]+"       OES Type        Assignment")
                hDC.TextOut(500,800+yax,"                           1  2  3  4                 "+Tsort[ts][5])
                hDC.MoveTo(500,900+yax)
                hDC.LineTo(4500,900+yax)  # draw line         

              scnt = Tsort[ts][3]  ## numb of srchr's in team
              sloc = Tsort[ts][1]*yy.Nrows + Tsort[ts][2] + 1   ## addr of first srchr in team
              tsStrt = ts + 1
              ifnd = 1
              break
         ccnt = 0
         ssStrt = 0  ## have to restart search for srchr due to possible ordering
         if (ifnd == 1):
           ix = 0  
           for ss in range(ssStrt,len(Ssort)):
             cloc = Ssort[ss][3]*yy.Nrows + Ssort[ss][4]  
             if (cloc == sloc):
               lead = ""
               med = ""
               if (DEBUG == 1): print(Ssort[ss][7])
               if (Ssort[ss][7]=="1"):
                 lead = "LEAD"
               if (Ssort[ss][8]=="1"):
                 med = "MED"
 # (Ssort[ss][0], Ssort[ss][1], lead , med, Ssort[ss][10])) # name, agency, lead, med, cell#
               for yax in (0, 3200):   
                 hDC.TextOut(500,950+ix+yax,"   %-20.20s   %-4.4s   %-5.5s %-5.5s   %-13.13s"%(Ssort[ss][0],Ssort[ss][1],lead,med,Ssort[ss][10]))                             
               ix = ix + 100
               ccnt = ccnt + 1
               sloc = sloc + 1
               ssStrt = ss + 1
               if (ccnt == scnt):
                 break      ## got all of team
           ipnt = 1000 + ix
           for yax in (0, 3200):
             hDC.MoveTo(500,ipnt+yax)
             hDC.LineTo(4500,ipnt+yax)  # draw line
             hDC.TextOut(500,ipnt+100+yax,"Briefer:                             Briefing Time:      ")
           hDC.EndPage ()
 
         else:
           if (DEBUG == 1): print("End")
           break           ##  output all teams

    def listTeams(self):
        if (DEBUG == 1): print("In List Teams")
        fts = open("teams.txt","wt+")  ## possibly delete file first (above)
        yy = self.mm
        zz = self.zz2

        Tsort = sorted(zz.TEAMS[0:-1],key=itemgetter(0))  ## ignore "end"        
        Ssort = sorted(zz.SRCHR[0:-1],key=itemgetter(3,4))
        if (DEBUG == 1): print("T:%s"%Tsort)
        tsStrt = 0
        ssStrt = 0
        ## write header
        fts.write("%s   %s\n" % ("Search", yy.dateTime.text()))
        while 1:
         for ts in range(tsStrt,len(Tsort)):  ## possibly use while
          ifnd = 0
          # Look for leading T (only) for new Team number format
          #   Not printing out 'teams' that are not in the field
          if (Tsort[ts][0][0:1] == "T" and Tsort[ts][1] < yy.Nunas_col):
            fts.write("\n%-10.10s %-10.10s %-10.10s\n" % (Tsort[ts][0], Tsort[ts][4], Tsort[ts][5])) # team name, type, location
            scnt = Tsort[ts][3]  ## numb of srchr's in team
            sloc = Tsort[ts][1]*yy.Nrows + Tsort[ts][2] + 1   ## addr of first srchr in team
            tsStrt = ts + 1
            ifnd = 1
            break
         ccnt = 0
         ssStrt = 0  ## have to restart search for srchr due to possible ordering
         if (ifnd == 1):
          for ss in range(ssStrt,len(Ssort)):
           cloc = Ssort[ss][3]*yy.Nrows + Ssort[ss][4]  
           if (cloc == sloc):
             lead = ""
             med = ""
             if (DEBUG == 1): print(Ssort[ss][7])
             if (Ssort[ss][7]=="1"):
               lead = "LEAD"
             if (Ssort[ss][8]=="1"):
               med = "MED"
             fts.write("%-20.20s %-4.4s %-4.4s %-3.3s %-12.12s\n" % (Ssort[ss][0], Ssort[ss][1], lead , med, Ssort[ss][10]))
                                         # name, agency, lead, med, cell# 
             ccnt = ccnt + 1
             sloc = sloc + 1
             ssStrt = ss + 1
             if (ccnt == scnt):
               break      ## got all of team
         else:
          if (DEBUG == 1): print("End")
          break           ##  output all teams
        fts.close()

    def cell_was_clicked(self, row, column):
        ##
        if self.selected :
            self.selected = 0  # reset after 1 more click
            return
        if (QtWidgets.qApp.mouseButtons() & QtCore.Qt.LeftButton):
            if (DEBUG == 1): print("LMB")
        self.selected = 1
        if (DEBUG == 1): print("Row %d and Column %d was clicked" % (row+1, column+1))
        item = self.tableWidget.item(row, column)  
        if (DEBUG == 1):
          if (item != None): print("Item is #%s#\n" % item.text())
          else: print("*** Item was None ***")
        self.ID = item.text()
        self.lrow = row  ## previous row/column
        self.lcolumn = column
        self.repaint()
        if (DEBUG == 1): print(".....repaint click.....")        
        
    def cell_was_Dclicked(self, row, column):
        ## Does a double click always also create a single click?
        ## appears default item change is by double click; can this be turned-off? yes
        if (DEBUG == 1): print("Row %d and Column %d was Dclicked" % (row+1, column+1))
        text = self.ID

        ##  currentRow or currentColumn  itemAt gives item, not contents
        ##      using .text() will give the contents

    def dialog_was_clicked(self, row, column): ## tableWidget2  RMB for Team (settable)
        ##
        if self.selected :         ## PROBABLY not used??
            self.selected = 0  # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget2.item(2,1)   ## just to set a value    
        if (DEBUG == 1): print("DIALOG HIDE: Row %d and Column %d was clicked" % (row+1, column+1))
        if (column == 0 or row == 3): item = self.tableWidget2.item(row, column) 
        if (DEBUG == 1):
          if (item != None): print("Item is %s\n" % item.text())
          else: print("*** Item was None ***")
        if (row == 3):
          self.tableWidget2.hide()
          if (column == 0):  ## Ok
            ## change values in TEAMS (& re-display)  (otherwise leave them alone)
              if (DEBUG == 1): print("FOUND: %s %s"% (self.tableWidget.fnd_team,self.tableWidget2.item(0,1).text()))
              self.zz2.TEAMS[self.tableWidget.fnd_team][0] = self.tableWidget2.item(0,1).text()
              self.zz2.TEAMS[self.tableWidget.fnd_team][4] = self.tableWidget2.item(1,1).text()
              self.zz2.TEAMS[self.tableWidget.fnd_team][5] = self.tableWidget2.item(2,1).text()                    
              self.zz2.tabload(self.mm,0)

    def dialog_was_clicked4(self, row, column): ## tableWidget3  RMB for Searcher Detail (view only, except remove)
        ##
        yy = self.mm
        zz = self.zz2
        
        if self.selected :         ## PROBABLY not used??
            self.selected = 0      # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget5.item(4, 1)   ## info at Remove?
        if (item.text().upper() == "Y"):      ## Yes remove
            if (row == 5 and column == 0):
               ptr = self.tableWidget.fnd_srchr
               if (self.zz2.SRCHR[ptr][5] != yy.Nunas_col and zz.SRCHR[ptr][6] != 1 ): ## TEAM of SRCHR must be UNASSIGNED
                  winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, searcher not found
                  return          
               TimeOUT = time.time()          ## add to MEMBERS record
               memPtr = -1
               for xx in range(0,len(zz.MEMBERS)):           ## find the MEMBERS record
                   if (zz.MEMBERS[xx][1] == zz.SRCHR[ptr][2] and zz.MEMBERS[xx][2] == zz.SRCHR[ptr][1]): # match Id, Agency
                       memPtr = xx
                       break               
               zz.MEMBERS[memPtr][6] = TimeOUT         ##  set as checked-out (AT some point want to add total time field
               zz.MEMBERS[memPtr][9] = float(zz.MEMBERS[memPtr][9]) + zz.MEMBERS[memPtr][6] - float(zz.MEMBERS[memPtr][5])  ## cum time
               zz.MEMBERS[memPtr][5] = -1              ## reset for next checkin               
               rowy = zz.SRCHR[ptr][4]
               colx = zz.SRCHR[ptr][3]
               npt = rowy + (colx - yy.Nunas_col)*yy.Nrows
               zz.UNAS_USED[npt] = 0
               del zz.SRCHR[ptr]                       ## we are deleting the record and marking MEMBERS entry with TimeOUT
        if (DEBUG == 1): print("DIALOG HIDE: Row %d and Column %d was clicked" % (row+1, column+1))
        if (row == 5):
          self.tableWidget5.hide()
        zz.tabload(yy,0)
        ##   really no need to update the table unless remove is happening                   


    def dialog_was_clicked2(self, row, column): ## tableWidget3  RMB last column groups
        ##
        if (DEBUG == 1): print("Dialog3 GROUPS row: %i, column: %i"%(row, column))
        item = self.tableWidget3.item(row,column).text()
        if (row == 4): return    # set choice value
        if (row == 5):           ## This is OK.  Need to set group name for choice first 
            item = self.tableWidget3.item(4,0).text()
            if (item == "<create>"):      ## not set so skip
                self.tableWidget3.hide()
                return    
            self.tableWidget3.setItem(4,0,QtWidgets.QTableWidgetItem("<create>"))  # reset to default 
        self.tableWidget3.hide()
        self.zz2.TEAMS.insert(self.zz2.TEAMS.index(["END"]),[item, \
                    self.tableWidget.ccm, self.tableWidget.rrm, 0, item, "--", 0.0]) # insert prior to END                    
        self.zz2.tabload(self.mm,0)

    def dialog_was_clicked3(self, row, column): ## tableWidget4  RMB out-of-bounds FIND
        ##
        if self.selected :         ## PROBABLY not used??
            self.selected = 0      # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget4.item(2,1)   ## just to set a value    
        if (DEBUG == 1): print("DIALOG4 OUT-OF-Bounds Row %d and Column %d was clicked" % (row+1, column+1))
        if (column == 0 or row == 5): item = self.tableWidget4.item(row, column)  
        if (DEBUG == 1):
          if (item != None): print("Item is %s\n" % item.text())
          else: print("*** Item was None ***")
        if (row == 5):
          self.tableWidget4.hide()
          if (column == 0):  ## Ok
            ## change values in TEAMS (& re-display)  (otherwise leave them alone)
              self.zz2.findSrchrId = self.tableWidget4.item(1,1).text()
              self.zz2.findAgncy = self.tableWidget4.item(3,1).text()
              if (DEBUG == 1): print("Looking for SrchrId %s and Agency %s"%(self.zz2.findSrchrId,self.zz2.findAgncy))  #Ax
              self.zz2.findName = self.tableWidget4.item(2,1).text()
              self.zz2.findResource = self.tableWidget4.item(4,1).text()
              if (self.zz2.findResource == " " or len(self.zz2.findResource) == 0):
                  self.zz2.findResource = "xxx"     # set to value that will not match
              if (self.zz2.findName == " " or len(self.zz2.findName) == 0):
                  self.zz2.findName = "xxx"         # set to value that will not match
  ### ?  Add info for resource type             
              if (self.zz2.findAgncy == " "): self.zz2.findAgncy = "NC"   ## the default
          else:              ## cancel
              self.zz2.findSrchrId = "0"
              self.zz2.findAgncy = " "
              self.zz2.findName = "xxx"
              self.zz2.findResource = "xxx"  # set to not match 'blank'
          self.zz2.tabload(self.mm,0)        ## for Ok or Cancel update the maintable
          ##  the above sets up the information for changing the background

##### Functions for accessing databasse files from the server
# this function name may change - right now it is intended to grab the entire table
    #  from the server using http api
#        self.host="http://caver456.pythonanywhere.com"
#        self.columns=["ID","Name","Agency","Resource","TimeIn","TimeOut","Total","InEpoch","OutEpoch","TotalSec","CellNum","Status"]
 
    def sync(self):   ## GET entire SQL database from net server
        logging.info("sync called")
        ### print("In sync %s"%self.host+"/api/v1/events"+self.zz2.eventID)
        codex = " "
        try:
            response = requests.request("GET", event_url+self.zz2.eventID, headers=headers, data = payload)
        except:
            stat = 408
            codex = " - T/O"
        else:                 
        ## r=requests.get(url=self.host+"/api/v1/events"+self.zz2.eventID)
        #logging.info("response json:"+str(r.json()))
        # the response json entries are unordered; need to put them in the right
        #  order to store in the internal list of lists
            stat=response.status_code # gives status to check if got valid return
        if (stat != 200):
            self.mm.infox.setText('Error: No Server connected, try again'+codex)
            return
        j=response.json() # r.json() returns a list of dictionaries
          
        signInList=[]
        for d in j:
            ##logging.info("  entry dict:"+str(d))
            entry=[d[k] for k in columns]
            logging.info("  entry list:"+str(entry))
            signInList.append(entry)
        logging.info("Received json:"+str(j))            
        return(signInList)    

##Also some of the overhead functions if they are useful to you - I haven't done a commit lately:

##    def q(self,query):
###         Logger.info("** EXECUTING QUERY: "+str(query))
##        self.cur.execute(query)

    def sendAction(self,entry):    ## PUT a single record out to the SQL net server
        logging.info("sendAction called")
        d=dict(zip(columns,entry))
        j=json.dumps(d)
#$        logging.info("dict:"+str(d))
#$        logging.info("json:"+str(j))
#$#         requests.post(url="http://127.0.0.1:5000/api/v1/events/current/add",json=j)
#$        codex = " "
#$        try:
#$            response = requests.request("PUT", event_url+self.zz2.eventID, headers=headers, data = payload, json = j)
#$        except:
#$            stat = 408
#$            codex = " - T/O"
#$        else:                 
#$          #q=requests.put(url=self.host+"/api/v1/events"+self.zz2.eventID,json=j)
#$          print("Received %s"%response)

#### end of TableApp class



def xmodel(mdx) :
    ## routine outside of class TableApp
    
    if (DEBUG == 1): print("In xmodel %i\n" % mdx)  ##TableApp.modex
    return

def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    if (DEBUG == 1): print("B4 form define\n")
    form = TableApp()  # We set the form to be our ExampleApp (table)
    if (DEBUG == 1): print("B4 form show\n")
    form.show()  # Show the form
    if (DEBUG == 1): print("Call app\n")
    app.exec_()  # and execute the app
    


if __name__ == '__main__':  # if we're running file directly and not importing it
    main()  # run the main function
