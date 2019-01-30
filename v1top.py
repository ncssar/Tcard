from PyQt5 import QtGui, QtCore, QtWidgets  # Import the PyQt5 modules we'll need
from PyQt5.QtGui import QFont
import sys  # We need sys so that we can pass argv to QApplication

##import table  # This file holds our MainWindow and all table related things
import v1      ## table display routine file
import csv
from pathlib import Path
import winsound
import re
import json
from collections import deque   ## pronounced deck
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
import traceback
import threading
from datetime import date, datetime
from random import *
from operator import itemgetter

####### ADD undo button to put back previous move operation - how to catalog?
sys.tracebacklimit = 1000

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
           

class TableApp(QtWidgets.QMainWindow, QtWidgets.QTableWidget, v1.Ui_MainWindow, v1.tabinfo):  #####
    def __init__(self):
        # super is used here in that it allows us to
        # access variables, methods etc in the v1.py file
        super(self.__class__, self).__init__()
        xx=v1.Ui_MainWindow()  ## see yy below  Are these both separate instances?
                                    ## works here because Hmain and Wmain are class variables?
        self.setupUi(self)          # This is defined in v1.py file automatically
        if (DEBUG == 1): print("main self: %s" % self)
        self.mm = self
        self.xx2 = xx           ## appears xx is only used here
        self.xx2.READIN = 0     ## set to determine if we have read MEMBERS yet
        # It sets up layout and widgets that are defined

        self.pushButton.clicked.connect(self._addSrchr)  # When the ADD button is pressed
        self.pushButton_2.clicked.connect(self._rmSrchr)  # When the REMOVE button is pressed
        self.pushButton_undo.clicked.connect(self._undo)  # When the UNDO button is pressed
        self.pushButton_readMem.clicked.connect(self._readMemb)  # When the READ button is pressed
        self.pushButton_teams.clicked.connect(self.listTeams) # When list teams pushed
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
        self.tableWidget2.cellClicked.connect(self.dialog_was_clicked)
        self.tableWidget3.cellClicked.connect(self.dialog_was_clicked2)
        self.tableWidget4.cellClicked.connect(self.dialog_was_clicked3)        
        self.selected = 0  ## preset to nothing selected   NOT USED?
        self.setAcceptDrops(True)               ## do not pickup drag/drop if assoc with tableWidget
        self.tableWidget.setDragEnabled(True)   ## needs to refer to tablewWidget
        

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
        ##self.stop.set()    ## stop timer


        ###  The following does not appear to have an affect
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        self.tableWidget.setSizePolicy( sizePolicy )

######   TEMPORARY PRE-LOAD OF INFO TABLE THAT EMULATES A DATABASE   ######
#
#  list TEAMS : [Name, xloc, yloc, #srchrs, type, location, timeout]
#
#  list SRCHR : [Name, agency, idnumb, xloc, yloc, xteam, yteam, leader (bit), medical (bit), TimeIN, TimeOUT]
#
#  list MEMBERS:[Name, IDval, Cnty, leader, medical, checked-in]
# preset
#       TEAMS : sheriff -> [Sheriff Coord, 0,0,0,IC,IC,0.0]
#               ops     -> [OPS, 0,8,0,IC, IC, 0.0]
#               unas    -> [UnAssigned, Nunas_col,0,UNAS, IC, 0,0]
#     SEARCHERS: SRCHR  -> [Namex1, NC, #1, 6, 1, ->UNAS(x,y) (team), 0, 0]
#                          [Namexz, NC, #2, 6, z, ->UNAS(x,y) (team), 0, 0]

######
     
## the following is writing to tabinfo.info
        i=0   ## entry #
        j=0    ## cnt of members
        m = 0  ## ID's
        savei = 0
        savej = 0
        clr_order = "RGBYMC "  ## team #
        zz = v1.tabinfo()
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

############## GET rid of the following load  ????
        
        ##  Name, agency, IdNumb, xloc, yloc, TeamPtr, Med(bit), Leader(bit)
        col = 6  # starting
        row = 1
        iw = 0
        zz.TEAMS[team_unas][3] = iw  ## set number of searchers in unassigned    
        zz.SRCHR.append(["END"])   
        zz.tabload(self)         ## load display table                                                                   
        if (DEBUG == 1): print("At init\n")


    def _addSrchr(self): ## Button ADD SEARCHER
        ##zz = v1.tabinfo()
        team_unas = 6                    ####   This is the number of the entry for the Unassigned Team
                                         ##         This may change as default or over time
        yy = self.mm  ##v1.Ui_MainWindow()  
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
        elif (zz.MEMBERS[memPtr][5] == 1):  ## member already checked-in, ignore
            winsound.Beep(2500, 300)        ## BEEP, short 2500Hz, needs to be empty
            winsound.Beep(2500, 300)        ## double
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
        TimeIN = time.strftime("%Y-%m-%d, %H:%M:%S")
        if (DEBUG == 1): print("TimeIN %s"% TimeIN)  ## If the srchr comes back how to accum time?
        zz.SRCHR.insert(-1,[zz.MEMBERS[memPtr][0],zz.MEMBERS[memPtr][2],zz.MEMBERS[memPtr][1],  \
                        colu, rowu, yy.Nunas_col, 1, zz.MEMBERS[memPtr][3], zz.MEMBERS[memPtr][4], TimeIN, -1])  ## place before "END"
        if (DEBUG == 1): print("SRCHR ptr: %i\n" % len(zz.SRCHR))   ## ptr minus 2
        zz.MEMBERS[memPtr][6] = len(zz.SRCHR)-2    ## ptr into the SRCHR list
        zz.MEMBERS[memPtr][5] = 1                  ##  set as checked-in
###
###  Need to construct correct entry
###       ALSO, check that SAR has not already been loaded
###             AND, when removing check that it was there        
###
##   SRCHR:        Name, agency, IdNumb, xloc, yloc, TeamX, TeamY, Leader(bit, Med(bit), TimeIN, TimeOUT
## put these \/ in some initialization place
##   incase searchers are added after movement has occurred, need to skip locations already used        

        zz.TEAMS[team_unas][3] = zz.TEAMS[team_unas][3] +1  ## set number of searchers in unassigned
        yy.saveLastIDentry = yy.sarID.text()
        yy.sarID.setText("")  ## clear sarID field
        if (DEBUG == 1): print("PTR2 %s"%yy)
        zz.tabload(yy)         ## load display table


    def _rmSrchr(self): ## button REMOVE SEARCHER
        zz = self.zz2
        yy = self.mm  

        memPtr = -1
        sarIDval = yy.sarID.text()
        if (sarIDval == ""):   ## blank entry means to remove previous ADD searcher (probably incorrect member chosen)
#### FIX UP  add agency check
          sarIDval = yy.saveLastIDentry     ####  NEED to get agency, too  PARSE ID and agency from entry

        sarINFOsplit = sarIDval.split()   ## SAR ID field can be "ID" or "ID AGENCY"
        sarIDval = sarINFOsplit[0].upper()
        sarAGENCY = "NC"                      ## default AGENCY
        if (len(sarINFOsplit) > 1):         ## then agency arg was entered
          sarAGENCY = sarINFOsplit[1].upper()
          
        for xx in range(0,len(zz.MEMBERS)):
          if (zz.MEMBERS[xx][1] == sarIDval and zz.MEMBERS[xx][2] == sarAGENCY):
            memPtr = xx
            break
        if (memPtr == -1):
            winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, member not found
            return
        if (DEBUG == 1): print("PTR  %s"%memPtr)        
        zz.MEMBERS[memPtr][5] = 0       ##  set as checked-out
        fnd = -1
        for ptr in range(0, len(zz.SRCHR)-1):  ## do not test the lst element (END)
          ## match ID and agency  
          if (zz.SRCHR[ptr][2] == sarIDval and zz.SRCHR[ptr][1] == sarAGENCY):
            fnd = 1
            if (DEBUG == 1): print("ID, Cnty %s %s"%(zz.SRCHR[ptr][2],zz.SRCHR[ptr][1]))
            break
        if (fnd == -1 or (zz.SRCHR[ptr][5] != yy.Nunas_col and zz.SRCHR[ptr][6] != 1 )): ## team must be unassigned
            winsound.Beep(2500, 1200)   ## BEEP, 2500Hz for 1 second, searcher not found
            return          
        TimeOUT = time.strftime("%Y-%m-%d, %H:%M:%S") ## possibly add to SRCHR record
        zz.SRCHR[ptr][10] = TimeOUT #  does not help if we next delete the entry??
        rowy = zz.SRCHR[ptr][4]
        colx = zz.SRCHR[ptr][3]
        npt = rowy + (colx - yy.Nunas_col)*yy.Nrows
        zz.UNAS_USED[npt] = 0
        del zz.SRCHR[ptr]           ## are we deleting the record or marking it as GONE
### Only remove if in Unassigned.  THEN, also put the space as available again  
        yy.sarID.setText("")
        zz.tabload(yy)              ## update table


    def _undo(self): ## Button UNDO - put status/display back one change, saving MEMBERS, too
        zz = self.zz2
        if (DEBUG == 1): print("At undo %i \n" % self.modex)
        ## call undo_table (single deep)

        #print("POP1: %s"%zz.saveTeam)
        zz.saveTeam.pop()
        zz.TEAMS = zz.saveTeam.pop()      ## what if previous operation only affected a srchr?
        zz.saveSrchr.pop()
        zz.SRCHR = zz.saveSrchr.pop()
        zz.saveUnUsed.pop()
        zz.UNAS_USED = zz.saveUnUsed.pop()
        zz.saveMembers.pop()                ## these are double pop's because of intervening append
        zz.MEMBERS = zz.saveMembers.pop()

        v1.tabinfo.tabload(self, self.save_pntr)    ## call tabload to update screen
        

        
    def _readMemb(self): ## Button READ MEMBERS from CVS files
        ###  nominally the ncssar members.csv and OTHERS.csv files are read to get member info.
        ####### FOR the case when the INFOX box starts with JSON, instead this is a recovery and
        #######   the latest JSON files are read and populate TEAMS, SRCHR, UNAS_USED and MEMBERS
        
        caps = ["EMT", "PA", "RN"]  ##  capabilities for Medical type - probably temporary
        yy = self.mm
        zz = self.zz2
        if (DEBUG == 1): print("At readmemb %i\n" % self.modex)
        self.modex = 1 - self.modex    ## change state  test
        xmodel(self.modex)   # call routine outside of class test
        test_info = yy.infox.text()
        if (test_info[0:4].upper() != "JSON"):  ## if INFOX has "JSON" means recovery
          if (zz.READIN == 0):  ## otherwise skip MEMBERS readin ...
             zz.MEMBERS = []          ## reset list
             zz.READIN = 1      ## set as having been read
                   
             my_file = Path("MEMBERS2.csv")       #############  NCSSAR member database
             if my_file.is_file():
               with open('MEMBERS2.csv','rt') as csvIN:
                 csvPtr = csv.reader(csvIN, dialect='excel')
                 regShrf = r"[0-9][A-Z].*"        ## reg ex to find sheriff IDs
                 for row in csvPtr:
                   make = ["0", "0", "NC", "0", "0", "0", "0"]  ## need to re-initalize make here for some reason
                   if (row[0].isdigit()):        ## has to be all digits (searcher)
                     make[1] = row[0]
                     make[0] = row[1]
                     for cx in caps:
                       regcap = r"[ ,]" + cx + r"[ ,]"
                       fnd = re.search(regcap, row[5])
                       if (fnd != None):     ## found a match
                         make[4] = "1"   
                     if (row[6] == "1"):       ## type 1 searcher; used for now to choose LEADER temporary
                       make[3] = "1"        
                   elif (re.search(regShrf, row[0]) != None):    ## numb/letter... found sheriff coord
                     make[1] = row[0]
                     make[0] = row[1]
                   else:
                     continue                   ## valid entry not located - go to next line               
                   zz.MEMBERS.append(make)        ## load MEMBERS if valid entry
               
               if (DEBUG == 1): print("\n\n")
               if (DEBUG == 1): print("READ: %s:%s"%(zz,self.zz2))
             else:
               winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty
               return
                 
             zz.SRCHR.clear()             ##  reset for now only first time thru
             zz.SRCHR.append(["END"])     ## preset the first time thru
            
          my_file = Path("OTHERS.csv")

##### Could check for existing ID and agency and replace upon readin

          ###  format of others is "Member,ID,agency,Leader,Medical,CheckedIn" add cell for SRCHR pntr
          if my_file.is_file():
            if (DEBUG == 1): print("In other")  
            with open('OTHERS.csv','rt') as csvIN2:
              csvPtr = csv.reader(csvIN2, dialect='excel')
              for row in csvPtr:
                row = [row[0],row[1],row[2],row[3],row[4],row[5], "0"]  ## add position for SRCHR pointer
                ifnd = 0  
                for ix in range(len(zz.MEMBERS)):          
                  if (row[1] == zz.MEMBERS[ix][1] and row[2] == zz.MEMBERS[ix][2]): ## match: ID,agency
                    del zz.MEMBERS[ix]         ##    update entry
                    zz.MEMBERS.insert(ix,row)
                    ifnd = 1                   ## mark event
                    break                      ## done, so skip the rest
                if (ifnd == 0):                  ##    add
                  zz.MEMBERS.append(row)         ## possibly change # and order of cells
                  if (DEBUG == 1): print("new row: %s" % row)  
          ### ignore otherwise
          if (DEBUG == 1): print("READ: %s"%zz.SRCHR)
          
        else:       ## read json files to load MEMBERS, TEAMS, SRCHR, UNAS_USED for recovery
            if (DEBUG == 1): print("JSON found")
            mtimeA = os.path.getmtime("DATA\saveUnasA.json")
            mtimeB = os.path.getmtime("DATA\saveUnasB.json")
            if (mtimeA > mtimeB):
                setName = "A"   
            else:
                setName = "B"
               ##   Newest save time.  If corrupted, then delete
               ##   the set and use the other one
            print("Set: %s"%setName)             
            with open("DATA\saveAll"+setName+".json", 'r') as infile:  ## opens, reads, closes
                [zz.TEAMS, zz.SRCHR, zz.MEMBERS, zz.UNAS_USED, zz.TEAM_NUM] = json.load(infile)   
            print("Doing recovery reload...")    
            zz.tabload(yy)    


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
        

    def listTeams(self):
        if (DEBUG == 1): print("In List Teams")
        fts = open("teams.txt","wt+")  ## possibly delete file first (above)
        yy = self.mm
        zz = self.zz2

        Tsort = sorted(zz.TEAMS[0:-1],key=itemgetter(0))  ## ignore "end"        
        Ssort = sorted(zz.SRCHR[0:-1],key=itemgetter(3,4))
        tsStrt = 0
        ssStrt = 0
        while 1:
         for ts in range(tsStrt,len(Tsort)):  ## possibly use while
          ifnd = 0  
          if (Tsort[ts][0][0:4] == "TEAM" and Tsort[ts][1] < yy.Nunas_col):
            fts.write("\n%-10.10s %-10.10s\n" % (Tsort[ts][0], Tsort[ts][4]))
            scnt = Tsort[ts][3]  ## numb of srchr's in team
            sloc = Tsort[ts][1]*yy.Nrows + Tsort[ts][2] + 1   ## addr of first srchr in team
            tsStrt = ts + 1
            ifnd = 1
            break
         ccnt = 0
         ssStrt = 0  ## have to restart search for srchr due to possible ordering
         if (ifnd==1):
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
             fts.write("%-20.20s %-4.4s %-4.4s %-3.3s\n" % (Ssort[ss][0], Ssort[ss][1], lead , med))  
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
        item = self.tableWidget.item(row, column)  #  why not  itemAt(row, column)?
        if (DEBUG == 1):
          if (item != None): print("Item is #%s#\n" % item.text())
          else: print("*** Item was None ***")
        self.ID = item.text()
        self.lrow = row  ## previous row/column
        self.lcolumn = column
        self.repaint()
        if (DEBUG == 1): print(".....repaint click.....")        
        
    def cell_was_Dclicked(self, row, column):
        ## Does a 5double click always also create a single click?
        ## appears default item change is by double click; can this be turned-off? yes
        if (DEBUG == 1): print("Row %d and Column %d was Dclicked" % (row+1, column+1))
        text = self.ID

        ##  currentRow or currentColumn  itemAt gives item, not contents
        ##      using .text() will give the contents

    def dialog_was_clicked(self, row, column): ## tableWidget2  RMB for Team
        ##
        if self.selected :         ## PROBABLY not used??
            self.selected = 0  # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget2.item(2,1)   ## just to set a value    
        if (DEBUG == 1): print("DIALOG HIDE: Row %d and Column %d was clicked" % (row+1, column+1))
        if (column == 0 or row == 3): item = self.tableWidget2.item(row, column)  #  why not  itemAt(row, column)?
        if (DEBUG == 1):
          if (item != None): print("Item is %s\n" % item.text())
          else: print("*** Item was None ***")
        if (row == 3):
          self.tableWidget2.hide()
          if (column == 0):  ## Ok
            ## change values in TEAMS (& re-display?)  (otherwise leave them alone)
              if (DEBUG == 1): print("FOUND: %s %s"% (self.tableWidget.fnd_team,self.tableWidget2.item(0,1).text()))
              self.zz2.TEAMS[self.tableWidget.fnd_team][0] = self.tableWidget2.item(0,1).text()
              self.zz2.TEAMS[self.tableWidget.fnd_team][4] = self.tableWidget2.item(1,1).text()
              self.zz2.TEAMS[self.tableWidget.fnd_team][5] = self.tableWidget2.item(2,1).text()                    
              self.zz2.tabload(self.mm)

    def dialog_was_clicked2(self, row, column): ## tableWidget3  RMB last column groups
        ##
        if (DEBUG == 1): print("Dialog3 GROUPS row: %i, column: %i"%(row, column))
        self.tableWidget3.hide()
        self.zz2.TEAMS.insert(self.zz2.TEAMS.index(["END"]),[self.tableWidget3.item(row,column).text(), \
                    self.tableWidget.ccm, self.tableWidget.rrm, 0, self.tableWidget3.item(row,column).text(), "--", 0.0]) # insert prior to END                    
        self.zz2.tabload(self.mm)

    def dialog_was_clicked3(self, row, column): ## tableWidget4  RMB out-of-bounds
        ##
        if self.selected :         ## PROBABLY not used??
            self.selected = 0  # reset after 1 more click
            return
            self.selected = 1
        item = self.tableWidget4.item(2,1)   ## just to set a value    
        if (DEBUG == 1): print("DIALOG4 OUT-OF-Bounds Row %d and Column %d was clicked" % (row+1, column+1))
        if (column == 0 or row == 3): item = self.tableWidget4.item(row, column)  #  why not  itemAt(row, column)?
        if (DEBUG == 1):
          if (item != None): print("Item is %s\n" % item.text())
          else: print("*** Item was None ***")
        if (row == 3):
          self.tableWidget4.hide()
          if (column == 0):  ## Ok
            ## change values in TEAMS (& re-display?)  (otherwise leave them alone)
              if (DEBUG == 1): print("Looking for SrchrId %s and Agency %s"%(findSrchrId,findAgncy))
              self.zz2.findSrchrId = self.tableWidget4.item(1,1).text()
              self.zz2.findAgncy = self.tableWidget4.item(2,1).text()
              if (self.zz2.findAgncy == " "): self.zz2.findAgncy = "NC"   ## the default
          else:              ## cancel
              self.zz2.findSrchrId = "0"
              self.zz2.findAgncy = " "
          self.zz2.tabload(self.mm)    ## for Ok or Cancel update the maintable           

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
