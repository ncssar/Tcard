# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'table.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from random import *
import winsound
import time
from collections import deque  ## provides for faster copy operations than a normal list
import copy                    ## using deepcopy for copying complex lists
import csv
import json
from datetime import date, datetime
import threading

global DEBUG


DEBUG = 0
fntNorm = QFont("Times", 14)
fntSmall = QFont("Times", 10)
fntSmall2 = QFont("Consolas", 9)    # should be mono-space
fntBold = QFont("Times", 12, QtGui.QFont.Bold)
fntField = QFont("Times", 16, QtGui.QFont.Bold)

class AsyncCopy(threading.Thread): 

	def __init__(self, infile, out): 

		# calling superclass init 
		threading.Thread.__init__(self) 
		self.infile = infile 
		self.out = out 

	def run(self): 

          f = open(self.infile, "r") 
          temp = json.load(f)
          f.close()
          f = open(self.out, "w")
          json.dump(temp,f)
          f.close()
          if (DEBUG == 1): print("Finished background file copy")
								


#
class PaintTable(QtWidgets.QTableWidget):
    def __init__(self, parent):
        QtWidgets.QTableWidget.__init__(self, parent)
        self.center = QtCore.QPoint(-10,-10)
        if (DEBUG == 1): print("PAINT INIT %s %s\n" % (self, parent))
        self.a = 25
        self.inxt = 0
        self.inxd = 0
        self.pntrtab = 0
        self.coordxp = [x for x in range(100)]
        self.coordyp = [y for y in range(100)]
        self.coordxd = [z for z in range(200)]
        self.coordyd = [w for w in range(200)]
        self.type = [u for u in range(200)]
        
    def mousePressEvent(self, e):  ## redefined event (for RMB push)
        if (DEBUG == 1): print("SELF: %s" % self.pntrtab)
        ##QtWidgets.QPushButton
        if e.button() == QtCore.Qt.LeftButton:
            if (DEBUG == 1): print ('LMB')  ## processed later in dialog clicked routine
        if e.button() == QtCore.Qt.RightButton:
          if (DEBUG == 1): print('Pressed RMB')
          positionm = e.pos()
          if (DEBUG == 1): print("Mouse Position %s pntr %s" % (positionm,self))
          if (positionm.x() > 0 and positionm.x() < self.pntrtab.Wtable) :
            indexm = self.pntrtab.tableWidget.indexAt(positionm)
            self.rrm = indexm.row()
            self.ccm = indexm.column()
            if (self.ccm >= 0 and self.rrm > 0):    ## on grided table
              self.fnd_team = tabinfo.fndloc(self, self.pntrtab.save_pntr.TEAMS, 2, 1, self.rrm, self.ccm) 
              if (DEBUG == 1): print("row %i column %i fnd %i" % (self.rrm, self.ccm, self.fnd_team))
              if (self.fnd_team != -1):   ## pointing to a TEAM
                if (DEBUG == 1): print("Team name: %s, type: %s, location: %s"%(self.pntrtab.save_pntr.TEAMS[self.fnd_team][0], \
                        self.pntrtab.save_pntr.TEAMS[self.fnd_team][4],self.pntrtab.save_pntr.TEAMS[self.fnd_team][5]))
                rx = (self.rrm+1)*50
                if (self.rrm > self.pntrtab.Nrows-4):
                  rx = (self.rrm-3)*50
                self.pntrtab.tableWidget2.move((self.ccm+1)*275, rx)
                iz = (0, 4, 5)  ## name, type, location
                for i in range(0,3):
                  iz0 = iz[i]  
                  item = QtWidgets.QTableWidgetItem(self.pntrtab.save_pntr.TEAMS[self.fnd_team][iz0])
                  self.pntrtab.tableWidget2.setItem(i,1,item)
                ## using tablewidget2
                self.pntrtab.tableWidget2.show()
              elif (self.pntrtab.tableWidget.item(self.rrm,self.ccm).text() != " "):  ## SEARCHER ENTRY
                ## should be a searcher entry
                self.fnd_srchr = tabinfo.fndloc(self, self.pntrtab.save_pntr.SRCHR, 4, 3, self.rrm, self.ccm)
                rx = (self.rrm+1)*50
                if (self.rrm > self.pntrtab.Nrows-4):
                  rx = (self.rrm-3)*50
                self.pntrtab.tableWidget5.move((self.ccm+1)*275, rx)
                iz = (0, 2, 10, 11)  ## name, ID, cell#, resources
                for i in range(0,5):
                  if (i != 4):      
                      iz0 = iz[i]  
                      item = QtWidgets.QTableWidgetItem(self.pntrtab.save_pntr.SRCHR[self.fnd_srchr][iz0])
                  else:
                      item = QtWidgets.QTableWidgetItem(" ")
                  self.pntrtab.tableWidget5.setItem(i,1,item)           
                ## using tablewidget5
                self.pntrtab.tableWidget5.show()  
              elif (self.pntrtab.tableWidget.item(self.rrm,self.ccm).text() == " " and self.ccm == self.pntrtab.Nsets-1):
                                             ## presently only last column, and blank
                ## create a group <from list> (check to see if already exists)
                if (DEBUG == 1): print("Found GROUP location")
                cx = (self.ccm+1)*275
                rx = (self.rrm+1)*50
                if (self.ccm > self.pntrtab.Nsets-3):
                  cx = (self.ccm-2)*275+100
                if (self.rrm > self.pntrtab.Nrows-4):
                  rx = (self.rrm-3)*50
                ## using tablewidget3  
                self.pntrtab.tableWidget3.move(cx, rx)
                self.pntrtab.tableWidget3.show()
            else:      ## out-of-bounds ccm or rrm == -1
              ## out-of-bounds RMB -> use for special table to do FIND or other function
                    ##     Find searcher ID#, Agency Name, then change color or found names
              self.pntrtab.tableWidget4.move(1000,1000)  # near center
              self.pntrtab.tableWidget4.show() 
        ## below, need QtWidgets.QTableWidget to set proper type for event     
        super(QtWidgets.QTableWidget,self).mousePressEvent(e)  ## allow rest of 'click' event to process


    def paintEvent(self, event):
        painter = QtGui.QPainter(self.viewport())
        sizex = self.viewport().width()
        sizey = self.viewport().height()
        #See: http://stackoverflow.com/questions/12226930/overriding-qpaintevents-in-pyqt
        #print("Viewport %s # %i / %i ## %i"% (self, sizex, sizey, self.inxd))
        painter.setPen(QtGui.QPen(QtCore.Qt.blue, 20))
        qfont = QFont('Times', 24, QFont.Bold)
        painter.setFont(qfont)
        painter.drawText(500,-15,1200,100,QtCore.Qt.AlignLeft, "A s s i g n e d")
        painter.drawText(2100,-15,1200,100,QtCore.Qt.AlignLeft, "U n A s s i g n e d")
        line = QtCore.QLineF(1620, 0, 1620, 1600.0)  ## divider btwn assigned / unassigned
        painter.drawLine(line)

        painter.setPen(QtGui.QPen(QtCore.Qt.red, 5))
        
        for ib in range(self.inxt):
          painter.drawRoundedRect(self.coordxp[ib]+1,self.coordyp[ib]+3,268,44,20,20)
        painter.setPen(QtCore.Qt.blue)
        for ib in range(self.inxd):
          if (self.type[ib] == 1):  ## output MEDICAL blue dot
            painter.setBrush(QtCore.Qt.blue)
            center = QtCore.QPoint(self.coordxd[ib]+250,self.coordyd[ib]+25)
          elif (self.type[ib] == 2):  ## output LEADER red dot
            painter.setBrush(QtCore.Qt.red)
            center = QtCore.QPoint(self.coordxd[ib]+225,self.coordyd[ib]+25)              
          painter.drawEllipse(center,10,10)
        QtWidgets.QTableWidget.paintEvent(self,event)  ## necessary to write stuff other than graphics



class Ui_MainWindow(object):     #QtWidgets.QTableWidget
    Hmain = 1900  # in pixels
    Wmain = 3000  # in pixels
    Nrows = 30   
    Nsets = 11
    Nunas_col = int(Nsets/2)+1   ## presently 6
    sarID = 1                    
    DISPLAY_LOCK = 0
    TabYoff=0
    save_pntr=0
    keyBrd = 1                   ## 1 is numeric, 0 is alpha
    saveLastIDentry = ""
    clr_order = "RGBYMC "
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        Nchars = 20
        Hcell = 50
        Ncols = self.Nsets       
        Wcell = int(self.Wmain/self.Nsets)
        self.Wtable = self.Nsets*(Wcell)      ## width of table in pixels
        if (DEBUG == 1): print("MainWindow self %s" % self)
        Tpoint = int(Wcell/Nchars/3)
        MainWindow.resize(self.Wmain, self.Hmain)
        if (DEBUG == 1): print("Self, Win2: %s:%i" % (self,MainWindow.width()))
        
        ##MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)   ## removes Frame from main window, but ...

        self.centralwidget = QtWidgets.QWidget(self)  #@#MainWindow) ## self or MainWindow works here
        self.centralwidget.setObjectName("centralwidget")
        #@#
        MainWindow.setCentralWidget(self.centralwidget)
        #
        self.tableWidget = PaintTable(self.centralwidget)
        if (DEBUG == 1): print("TABWIG is %s" % self.tableWidget)
        self.tableWidget.setGeometry(QtCore.QRect(0, self.TabYoff, self.Wmain, self.Hmain))

        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.tableWidget.setRowCount(self.Nrows)
        self.tableWidget.setColumnCount(Ncols)
        self.tableWidget.setObjectName("tableWidget")

        # do not allow cell editing on the window
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        for i in range(0,Ncols):
          self.tableWidget.setColumnWidth(i, Wcell)
        for i in range(0,self.Nrows):
          self.tableWidget.setRowHeight(i, Hcell)
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget.horizontalHeader().hide()
        self.tableWidget.verticalHeader().hide()
        ##  activated by RMB for Team header
        self.tableWidget2 = PaintTable(self.centralwidget)  ## secondary small table above primary table
        self.tableWidget2.setGeometry(QtCore.QRect(400, 520, 400, 250))
        self.tableWidget2.setRowCount(4)
        self.tableWidget2.setColumnCount(2)
        self.tableWidget2.setObjectName("tableWidget2")
        items = ("Name", "Type", "Location", "        Ok", "      Cancel")
        for i in range(0,5):
          item = QtWidgets.QTableWidgetItem(items[i])
          item.setFlags(Qt.ItemIsEnabled)      # protected
          if (i < 4): self.tableWidget2.setItem(i,0,item)
          else:       self.tableWidget2.setItem(3,1,item)
        self.tableWidget2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget2.horizontalHeader().hide()
        self.tableWidget2.verticalHeader().hide()        
        self.tableWidget2.hide()
        ##  activated by RMB for Searcher entry detail
        self.tableWidget5 = PaintTable(self.centralwidget)  ## secondary small table above primary table
        self.tableWidget5.setGeometry(QtCore.QRect(400, 520, 400, 400))
        self.tableWidget5.setRowCount(6)
        self.tableWidget5.setColumnCount(2)
        self.tableWidget5.setRowHeight(3,100)  ## more room for resources
        self.tableWidget5.setObjectName("tableWidget5")
        items = ("Name", "ID", "Cell#", "Resources", "Remove? (y, N)", "        Ok", "      Cancel")
        for i in range(0,7):
          item = QtWidgets.QTableWidgetItem(items[i])
          item.setFlags(Qt.ItemIsEnabled)      # protected
          if (i < 6): self.tableWidget5.setItem(i,0,item)
          else:       self.tableWidget5.setItem(5,1,item)
        self.tableWidget5.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget5.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget5.horizontalHeader().hide()
        self.tableWidget5.verticalHeader().hide()        
        self.tableWidget5.hide()
        #  from RMB in Groups column
        self.tableWidget3 = PaintTable(self.centralwidget)  ## secondary small table above primary table
        self.tableWidget3.setGeometry(QtCore.QRect(400, 520, 200, 350))
        self.tableWidget3.setRowCount(6)
        self.tableWidget3.setColumnCount(1)
        self.tableWidget3.setObjectName("tableWidget3")
        itemxs = ("K9", "Nordic", "SnowMobile", "Unavail","<create>","     Ok")
        for i in range(0,6):
          item = QtWidgets.QTableWidgetItem(itemxs[i])
          if (i != 4): item.setFlags(Qt.ItemIsEnabled)    # protected; <create> not protected
          self.tableWidget3.setItem(i,0,item)
        self.tableWidget3.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget3.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget3.horizontalHeader().hide()
        self.tableWidget3.verticalHeader().hide()        
        self.tableWidget3.hide()
        ##  activated by RMB for out-of-bounds FIND
        self.tableWidget4 = PaintTable(self.centralwidget)  ## secondary small table above primary table
        self.tableWidget4.setGeometry(QtCore.QRect(400, 520, 400, 360))
        self.tableWidget4.setRowCount(6)
        self.tableWidget4.setColumnCount(2)
        self.tableWidget4.setObjectName("tableWidget4")
        items = ("           Find", "SearcherID", "SearcherName", "Agency", "Resource Type", "        Ok", "      Cancel")
        for i in range(0,7):
          item = QtWidgets.QTableWidgetItem(items[i])
          item.setFlags(Qt.ItemIsEnabled)     # protected
          if (i < 6):
            self.tableWidget4.setItem(i,0,item)
            if (i < 5): self.tableWidget4.setItem(i,1,QtWidgets.QTableWidgetItem(" "))
          else:       self.tableWidget4.setItem(5,1,item)
        self.tableWidget4.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget4.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tableWidget4.horizontalHeader().hide()
        self.tableWidget4.verticalHeader().hide()        
        self.tableWidget4.hide()        
        #
        #
        item = QtWidgets.QTableWidgetItem()   ##  How to set all cells to a default font
        font = QtGui.QFont()
        font.setPointSize(Tpoint)
        self.tableWidget.setFont(font)  
        item.setFont(font)
        self.tableWidget.setItem(0, 0, item)
        ##

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.tableWidget.pntrtab = self
        self.pushButton.setGeometry(QtCore.QRect(450, 1700, 150, 46))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(650, 1700, 150, 46))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_undo = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_undo.setGeometry(QtCore.QRect(50, 1700, 150, 46))
        self.pushButton_undo.setObjectName("pushButton_undo")
        self.pushButton_readMem = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_readMem.setGeometry(QtCore.QRect(250, 1700, 150, 46))
        self.pushButton_readMem.setObjectName("pushButton_readMem")
        self.pushButton_teams = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_teams.setGeometry(QtCore.QRect(1220, 1700, 150, 46))
        self.pushButton_teams.setObjectName("pushButton_teams")
        
        self.num7 = QtWidgets.QPushButton(self.centralwidget)
        self.num7.setGeometry(QtCore.QRect(950, 1650, 40, 46))
        self.num7.setObjectName("num7")
        self.num8 = QtWidgets.QPushButton(self.centralwidget)
        self.num8.setGeometry(QtCore.QRect(1000, 1650, 40, 46))
        self.num8.setObjectName("num8")
        self.num9 = QtWidgets.QPushButton(self.centralwidget)
        self.num9.setGeometry(QtCore.QRect(1050, 1650, 40, 46))
        self.num9.setObjectName("num9")
        self.num4 = QtWidgets.QPushButton(self.centralwidget)
        self.num4.setGeometry(QtCore.QRect(950, 1700, 40, 46))
        self.num4.setObjectName("num4")
        self.num5 = QtWidgets.QPushButton(self.centralwidget)
        self.num5.setGeometry(QtCore.QRect(1000, 1700, 40, 46))
        self.num5.setObjectName("num5")
        self.num6 = QtWidgets.QPushButton(self.centralwidget)
        self.num6.setGeometry(QtCore.QRect(1050, 1700, 40, 46))
        self.num6.setObjectName("num6")
        self.num1 = QtWidgets.QPushButton(self.centralwidget)
        self.num1.setGeometry(QtCore.QRect(950, 1750, 40, 46))
        self.num1.setObjectName("num1")
        self.num2 = QtWidgets.QPushButton(self.centralwidget)
        self.num2.setGeometry(QtCore.QRect(1000, 1750, 40, 46))
        self.num2.setObjectName("num2")
        self.num3 = QtWidgets.QPushButton(self.centralwidget)
        self.num3.setGeometry(QtCore.QRect(1050, 1750, 40, 46))
        self.num3.setObjectName("num3")
        self.num0 = QtWidgets.QPushButton(self.centralwidget)
        self.num0.setGeometry(QtCore.QRect(950, 1800, 40, 46))
        self.num0.setObjectName("num0")
        self.numR = QtWidgets.QPushButton(self.centralwidget)
        self.numR.setGeometry(QtCore.QRect(1000, 1800, 40, 46))
        self.numR.setObjectName("numR")
        self.numS = QtWidgets.QPushButton(self.centralwidget)
        self.numS.setGeometry(QtCore.QRect(1050, 1800, 40, 46))
        self.numS.setObjectName("numS")
        self.numD = QtWidgets.QPushButton(self.centralwidget)
        self.numD.setGeometry(QtCore.QRect(1100, 1650, 40, 46))
        self.numD.setObjectName("numD")
        self.numE = QtWidgets.QPushButton(self.centralwidget)
        self.numE.setGeometry(QtCore.QRect(1100, 1700, 40, 46))
        self.numE.setObjectName("numE")
        self.numN = QtWidgets.QPushButton(self.centralwidget)
        self.numN.setGeometry(QtCore.QRect(1100, 1750, 40, 46))
        self.numN.setObjectName("numN")
        self.numT = QtWidgets.QPushButton(self.centralwidget)
        self.numT.setGeometry(QtCore.QRect(1100, 1800, 40, 46))
        self.numT.setObjectName("numT")
        self.numB = QtWidgets.QPushButton(self.centralwidget)
        self.numB.setGeometry(QtCore.QRect(1150, 1650, 40, 46))
        self.numB.setObjectName("numB")        
        self.numALP = QtWidgets.QPushButton(self.centralwidget)
        self.numALP.setGeometry(QtCore.QRect(1150, 1700, 40, 46))
        self.numALP.setObjectName("numAlp")        
        
        ### date/time and information windows at bottom
        if (DEBUG == 1): print("AT BOTTOM  %s\n" % self)
        self.dateTime = QtWidgets.QLineEdit(self.centralwidget)
        self.dateTime.move(1420, 1700)
        self.dateTime.resize(500,46)
        self.dateTime.setFont(fntField)
        self.dateTime.setText("Date and Time")
        self.infox = QtWidgets.QLineEdit(self.centralwidget)
        self.infox.move(1950, 1700)
        self.infox.resize(1000,46)
        self.infox.setFont(fntField)
        self.infox.setText("Information; like Radio band(s) being used")
        self.sarID = QtWidgets.QLineEdit(self.centralwidget)
        self.sarID.move(840, 1700)
        self.sarID.resize(100,40)
        self.sarID.setFont(fntSmall)
        self.sarID.setText("")
        self.sarIDlab = QtWidgets.QLabel(self.centralwidget)
        self.sarIDlab.move(840, 1650)
        self.sarIDlab.resize(100,40)
        self.sarIDlab.setFont(fntSmall)
        self.sarIDlab.setText("SAR ID")
        
        #
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1096, 38))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    

                
    def setKeys(self, n):  ## keys for searcher ID entry
        _translate = QtCore.QCoreApplication.translate
        if (n == 1):  # numbers
          self.num7.setText(_translate("MainWindow", "7"))
          self.num8.setText(_translate("MainWindow", "8"))
          self.num9.setText(_translate("MainWindow", "9"))
          self.num4.setText(_translate("MainWindow", "4"))
          self.num5.setText(_translate("MainWindow", "5"))
          self.num6.setText(_translate("MainWindow", "6"))
          self.num1.setText(_translate("MainWindow", "1"))
          self.num2.setText(_translate("MainWindow", "2"))
          self.num3.setText(_translate("MainWindow", "3"))
          self.num0.setText("0")
          self.numD.setText("D")
          self.numE.setText("E")
          self.numN.setText("N")
          self.numR.setText("P")
          self.numS.setText("S")
          self.numT.setText("T")
          self.numALP.setText(_translate("MainWindow", u"\u03B1"))
          self.numALP.setFont(fntField)
        else:  ## letters
          self.num7.setText(_translate("MainWindow", "Y"))
          self.num8.setText(_translate("MainWindow", "B"))
          self.num9.setText(_translate("MainWindow", "L"))
          self.num4.setText(_translate("MainWindow", "M"))
          self.num5.setText(_translate("MainWindow", "A"))
          self.num6.setText(_translate("MainWindow", "U"))
          self.num1.setText(_translate("MainWindow", "_"))
          self.num2.setText(_translate("MainWindow", "R"))
          self.num3.setText(_translate("MainWindow", "G"))
          self.num0.setText("H")
          self.numALP.setText(_translate("MainWindow", "#"))
          self.numALP.setFont(fntField)
        self.numB.setText(_translate("MainWindow", u"\u21A9")) # backspace - circle arrow
        self.numB.setFont(fntField)
        return

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "       Searcher Assignments for XYZ Search"))
        ## MainWindow.setFont(fntField) # operates on all fields on sheet

        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton.setText(_translate("MainWindow", "ADD"))
        self.pushButton_2.setText(_translate("MainWindow", "REMOVE"))
        self.pushButton_undo.setText(_translate("MainWindow", "UNDO"))
        self.pushButton_readMem.setText(_translate("MainWindow", "READ MEMBs"))
        self.pushButton_teams.setText(_translate("MainWindow", "LIST TEAMS"))
        self.setKeys(self.keyBrd)

      
    def dragMoveEvent(self, e):  
        e.accept(QtCore.QRect(0,0,3000,1800))  ##QRect for moves
        # do not print("in move") from here; will get many

##  locations appear to be related to the upper left corner of the Main Window, not the table

    def dragEnterEvent(self, e):  ## redefined event
      ##
      self.DISPLAY_LOCK = 1  ## using?
##  TRYING to adjust position of table widget
##### test area        
##   
      was = e.pos()
      #$#print("At top enter %s" % self)
      if (was.x() > 0 and was.x() < self.Wtable) :        
        e.accept()
        wxy = QtCore.QPoint()    ## wxy does not appear to be used
        wxy.setX(was.x())
        wxy.setY(was.y()-self.TabYoff)

        index = self.tableWidget.indexAt(was)
        #$#print ("position-> %s" % e.pos())
        self.rr = index.row()
        self.cc = index.column()

        ## need to convert to text, as value@pointer disappears while dragging
      else :
        e.ignore()
        

    def dropEvent(self, e):  ## redefined event
        #$#print ('drop %s' % self.itemt[0])
        position2 = e.pos()
        if (position2.x() > 0 and position2.x() < self.Wtable) :
         index2 = self.tableWidget.indexAt(position2)
         self.rr2 = index2.row()
         self.cc2 = index2.column()
         if (self.rr2 > 0):
          e.accept()
          ##vxy = QtCore.QPoint()    ## does not appear to be used?
          ##vxy.setX(position2.x())   ## e.pos().x().toInt())
          ##vxy.setY(position2.y()-self.TabYoff)        
          #self.button.move(position)
          e.setDropAction(QtCore.Qt.CopyAction)  ## can affect the value at the orig loc
          if (DEBUG == 1): print("AT x placement error......")
          ## do not set color here
        else :
          e.ignore()
          #$#print("Ignored drag/drop")
          return
        ## save info in case of undo
        if (DEBUG == 1): print("IN DROP %s:%s"%(self,self.save_pntr))
        zz =  self.save_pntr 
        ##  rr, cc are the FROM (enter) indices and rr2, cc2 are the TO (drop) indices of a move event
        tabinfo.tabmove2(self, zz, self.rr, self.cc, self.rr2, self.cc2)


class tabinfo(object):  ## table operations: tabload and tabmove
    def __init__(self):
        zz = Ui_MainWindow
        self.Ndata=1000
        self.Nteams=100
        self.Nsrchr=300
        self.NinfoTeam=7
        self.NinfoSrchr=9
        self.Ninfo = 4
        self.chk_file = ""
        ##### SAVE FILE 
        self.SAVE_FILE_PATH = "DATA\saveSEARCH"   ## changing save to JSON
        savelen = 5
        self.saveSet = 0
        self.saveNames = ["A", "B", "C", "D", "E"]
        self.READIN = 0
        self.findSrchrId = "0"    ## initialize find function
        self.findAgncy = " "
        self.findName = "xxx"
        self.findResource = "xxx" # default, don't want a match to 'blank'
        self.RemoteSignInMode = 0
        self.RemoteLastRow = 0
        self.pulsey = 0
        self.pntrtab2 = 0

        self.TEAMS = []  ## teams DB 
        self.saveTeam = deque([],savelen)
        self.SRCHR = []  ## srchr DB 
        self.saveSrchr = deque([],savelen)
        self.MEMBERS = []   ##  All NC SAR and OTHERS members 
        self.saveMembers = deque([],savelen)
        self.UNAS_USED = [0 for x in range(zz.Nrows*(Ui_MainWindow.Nsets-zz.Nunas_col))]  ## =1 if occupied; ptr = (col-Nunas_col)*Nrows + row
        self.saveUnUsed = deque([],savelen)

        ##self.SRCHR = [[0 for x in range(self.NinfoSrchr)] for y in range(self.Nsrchr)]
        ## name is team name (Sheriff, OPS, Team#, Unasssigned) or person name/agency
        ## type = 0 empty; = 1 header; = 2 searcher
        ## if name is team, info is cnt (including team entry); if person, info is searcher ID
        ## OLD: pntr is entry to display array = column# * rowMax + row#
        ## name at end of each list is "END"

        ##self.time_chk()    ## start blinker timer - put this in addSrchr
        self.masterBlink = 0

    def time_chk(self):  ## possibly only run/restart when new user add by _addSrchr  
        try:
          yy = self.pntrtab2 
          if (yy == 0): return
          self.pulsey = 1 - self.pulsey
          tabinfo.tabload(self,yy, 1)
        finally:
          if (self.masterBlink > 0):                     ## only starts timer when needed
            self.masterBlink = self.masterBlink - 1  
            QtCore.QTimer.singleShot(500, self.time_chk)


    def tabload(self,xxx,fromWhat):  ## loads the screen table 
        ## initial load of display table from linear list (database)
        ## load columns, 1) have a blank between teams, 2) move to new column if a Team does not fit;
        ##                   does not apply to Unassigned
        ## in tablex2.Ui_MainWindow: Nrows and Nsets give the number of rows and column sets

        zz = Ui_MainWindow
        #print("fromWhat %i"%fromWhat)
        ## fromWhat Will allow no state saves when called for blinking
        ###  possibly do not need to call tabload for blinking? Just update color for affected

        ##
        indk = [QtCore.Qt.red,QtCore.Qt.green,QtCore.Qt.blue,QtCore.Qt.yellow,QtCore.Qt.magenta,QtCore.Qt.cyan,QtCore.Qt.white]
        if (DEBUG == 1): print("In tabload0 :%s: %s %s" % (Ui_MainWindow.save_pntr, self, xxx))
        if (Ui_MainWindow.save_pntr == 0):
            Ui_MainWindow.save_pntr = self
            if (DEBUG == 1): print("setting save_pntr")
        mam = str(self)                 ## pickup self value to see if we need to interchange self and xxx
        if (mam.find("TableApp") > 0):  ## self has ptr that needs to be in xxx
            xxx = self
            self = Ui_MainWindow.save_pntr
            if (DEBUG == 1): print("interchanging xxx")
        if (DEBUG == 1): print("xxx IS %s, self is %s" % (xxx,self))
        if (self.pntrtab2 == 0):  self.pntrtab2 = xxx   ## pntr to TableApp for use with blinker
        #### load titles
        if (DEBUG == 1): print("TABLEWIDGET %s"%xxx.tableWidget)
        xxx.tableWidget.inxt = 0  ## counter for team coord's
        xxx.tableWidget.inxd = 0  ## counter for searcher coord's for leader/medical dots

        if (fromWhat == 0):   ## do not store state if from blinker 
          #self.saveTeam.append(list(self.TEAMS))            ## save for possible UNDO operation
          #print("Previous Team: %s"%self.saveTeam)
          self.saveTeam.append(copy.deepcopy(self.TEAMS))   # Using this instead
          #print("Current Team: %s"%self.TEAMS)
          self.saveSrchr.append(copy.deepcopy(self.SRCHR))  #  Need deepcopy for more complex structures
          self.saveUnUsed.append(list(self.UNAS_USED))      #  depth of save's is set by savelen in tabinfo
          self.saveMembers.append(copy.deepcopy(self.MEMBERS))
          #print("SRin: %s"%self.SRCHR)
          #print("SRsave1: %s"%self.saveSrchr)

        ##
## CLEAR entire table first        
        self.ncol = 0
        self.nplace = 0
        for ix in range(self.ncol, zz.Nsets):    
          for iy in range(self.nplace, zz.Nrows):        ##  cleanup
            xxx.tableWidget.setItem(iy, ix, QtWidgets.QTableWidgetItem(" "))       ## blanks - to b4 unassigned
        
        self.lin = 0
        if (DEBUG == 1): print("In tabload1 %s %s %s" % (Ui_MainWindow.save_pntr, self, xxx))
## FIRST run thru TEAMS
        if (DEBUG == 1): print("TeamZ: %s"% self.TEAMS[self.lin])
        text = self.TEAMS[self.lin][0]
        ttype = self.TEAMS[self.lin][4]
        tloc = self.TEAMS[self.lin][5]
## text consists of 30 char for name and 3 char for color positions
##   color is in char 30, 31, 32 and can be R,G,B,Y,M,C
##        
        tflag = 0  ## which area OverHead, Assigned teams, UnAssigned Teams
        ##if (hasattr(self, 'info_save')): print("tabload: %i %s\nBB %s" % (self.lin, self.info[0:50],self.info_save[0:40]))

#### START TEAMS LOOP:
        while (text != "END"):
          if (text != "END" and DEBUG == 1): print("not end %s" % text)  
   ## do we want to skip if not enough rows or find one that will fit?
   ##  Change sections to put entries into (Overhead, Teams-Assigned, UnAssigned:tflag0,1,2))

          rowy = self.TEAMS[self.lin][2]    ## rows         
          colx = self.TEAMS[self.lin][1]
          fnt = fntBold                 ## for team headers
          color = QtCore.Qt.magenta
          ##  add stuff to painter list - rounded rectangles
          if (colx != Ui_MainWindow.Nunas_col and rowy != 0): ## Don't place UnAssigned header
              xxx.tableWidget.coordxp[xxx.tableWidget.inxt] = xxx.tableWidget.columnViewportPosition(colx)
              xxx.tableWidget.coordyp[xxx.tableWidget.inxt] = xxx.tableWidget.rowViewportPosition(rowy)
              xxx.tableWidget.inxt = xxx.tableWidget.inxt + 1
              if (colx > 0):
                xxx.tableWidget.setItem(rowy, colx, QtWidgets.QTableWidgetItem(text[0:15]+" "+ttype[0:3]+" "+tloc[0:3]))
              else:
                xxx.tableWidget.setItem(rowy, colx, QtWidgets.QTableWidgetItem(text[0:21]))  
              xxx.tableWidget.item(rowy, colx).setFont(fnt)
              xxx.tableWidget.item(rowy, colx).setForeground(color)
              if (colx >= Ui_MainWindow.Nunas_col and colx < zz.Nsets-1):    ## set used locations in unassigned
                  npt = rowy + (colx - Ui_MainWindow.Nunas_col)*Ui_MainWindow.Nrows
                  if (DEBUG == 1): print("ZZ %i"%npt)
                  self.UNAS_USED[npt] = 1       ## set position
          self.lin = self.lin + 1
          text  = self.TEAMS[self.lin][0]    ## next slot name to use
          if (text != "END"):
            ttype = self.TEAMS[self.lin][4]
            tloc  = self.TEAMS[self.lin][5]
        #### end of TEAMS while
              
#### START SRCHR LOOP:
        self.lin = 0      
        text = self.SRCHR[self.lin][0]
        fnt = fntSmall2
        color = QtCore.Qt.blue
        colorB = QtCore.Qt.yellow
        colorX = QtCore.Qt.magenta
        while (text != "END"):
            rowy = self.SRCHR[self.lin][4] % zz.Nrows          
            colx = self.SRCHR[self.lin][3]         
            if (self.SRCHR[self.lin][8] == "1"):   ## MEDICAL
              xxx.tableWidget.coordxd[xxx.tableWidget.inxd] = xxx.tableWidget.columnViewportPosition(colx)
              xxx.tableWidget.coordyd[xxx.tableWidget.inxd] = xxx.tableWidget.rowViewportPosition(rowy)
              xxx.tableWidget.type[xxx.tableWidget.inxd] = 1
              xxx.tableWidget.inxd = xxx.tableWidget.inxd + 1
            if (self.SRCHR[self.lin][7] == "1"):   ## LEADER   #### need to differentiate between these with diff COLOR
              xxx.tableWidget.coordxd[xxx.tableWidget.inxd] = xxx.tableWidget.columnViewportPosition(colx)
              xxx.tableWidget.coordyd[xxx.tableWidget.inxd] = xxx.tableWidget.rowViewportPosition(rowy)
              xxx.tableWidget.type[xxx.tableWidget.inxd] = 2
              xxx.tableWidget.inxd = xxx.tableWidget.inxd + 1              

            xxx.tableWidget.setItem(rowy, colx, QtWidgets.QTableWidgetItem(f"{text[:13]:<13}"+" "+self.SRCHR[self.lin][1]))
            xxx.tableWidget.item(rowy, colx).setFont(fnt)
 #####  Blinking          
            if (self.SRCHR[self.lin][9] != 0 and self.pulsey == 1):  ## Blinker for new searcher add            
                xxx.tableWidget.item(rowy, colx).setForeground(colorX)
                self.SRCHR[self.lin][9] = self.SRCHR[self.lin][9] - 1
            else:
                xxx.tableWidget.item(rowy, colx).setForeground(color)
 #####  Find - change background    FIND
            if  (self.SRCHR[self.lin][0].upper().find(self.findName.upper()) != -1):  
                 xxx.tableWidget.item(rowy, colx).setBackground(colorB)   
            if  (self.SRCHR[self.lin][11].upper().find(self.findResource.upper()) != -1):  
                 xxx.tableWidget.item(rowy, colx).setBackground(colorB)   
            if ((self.SRCHR[self.lin][2] == self.findSrchrId or self.findSrchrId == " " or len(self.findSrchrId) == 0) \
                and self.SRCHR[self.lin][1] == self.findAgncy and self.findResource != "xxx" and self.findName != "xxx"):   
                xxx.tableWidget.item(rowy, colx).setBackground(colorB)      ## change background when using find             
            if (colx >= Ui_MainWindow.Nunas_col and colx < zz.Nsets-1):     ## set used for locations in UNASsigned
                npt = rowy + (colx - Ui_MainWindow.Nunas_col)*Ui_MainWindow.Nrows
                self.UNAS_USED[npt] = 1         ## set position
            self.lin = self.lin + 1
            text = self.SRCHR[self.lin][0]    ## next slot name to use
        #### end of SRCHR while
        

#### JSON write of data alternating to A and B filesets (in case one gets corrupted while writing)
    ##   possibly will keep a save (with time stamp) every so-many minutes for history?

####    Don't do this every tick of Blinking ...
        if (fromWhat == 0 and self.READIN == 1):    ## don't do when = 1, is blinker AND until READMEMB is active 
          self.saveSet = self.saveSet + 1
          if (self.saveSet == 5): self.saveSet = 0
          setName = self.saveNames[self.saveSet]
          if (DEBUG == 1): print("SAVE files %i"%self.saveSet)
          with open("DATA\saveAll"+setName+".json", 'w') as outfile:  ## opens, saves, closes
            json.dump([self.TEAMS, self.SRCHR, self.MEMBERS, self.UNAS_USED, self.TEAM_NUM, self.RemoteSignInMode, \
                                self.RemoteLastRow], outfile) ## save TEAMS, SRCHR, MEMBERS and TEAM_NUM, Remote info
          ## have another thread started to copy the last file written to another machine
##
#####      May want to add a periodic Keep set, say every 10min or so          
##  
          bg = AsyncCopy("DATA\saveAll"+setName+".json","DATA2\saveAll"+setName+".json")
          bg.start()
          ##bg.join()   ## would cause the main thread to wait              

   
    def fndloc(self, xlist, posr, posc, r, c):
        ## routine to find the location of a team or srchr in its database
        #  xlist is either TEAMS or SRCHR DB
        #  posr and posc are position in the list for the given 'xlist' type of the row and col info
        #  r and c are the row and col that are being matched
        #  fnd returned is the pointer into the 'xlist' database
        fnd = -1
        #print("FNDLOC %i %i %i %i %i" % (len(xlist),r,c,posr,posc))

        for t in range(0, xlist.index(["END"])):    ## stop prior to END
          #print(" %i,%i"%(xlist[t][posr],xlist[t][posc]))
          if (r == xlist[t][posr] and c == xlist[t][posc]):
            fnd = t
            break
        return fnd   ## returns -1 if not found
    

    def fnd_srchrs(self, team_ptr, t_row, t_col):
        ## routine to find the location of all srchrs in a team
        #  team_ptr is the location of the given team in TEAMS
        #  t_row and t_col are the location of the team header (either pointed-to or found by search)
        #  srch_list is the output list of searchers for this team
        #######  This routine assumes all searchers in a team are in one column
        ix = 0
        numSrchr = self.TEAMS[team_ptr][3]
        srch_list = [0 for x in range(0, numSrchr)]
        ##xxx = self.SRCHR.index(["END"])+1
        ##print("END PLACE %i" % xxx)

        for s in range(0, self.SRCHR.index(["END"])):  #### STOP at "END"? try: self.SRCHR.index("END")+1
                                                          ##   OR self.SRCHR[0].index("END")+1
          if (t_row == self.SRCHR[s][6] and t_col == self.SRCHR[s][5]):
            srch_list[self.SRCHR[s][4] - t_row - 1] = s  ## ordered (by row under team header) list of searchers in team
            ix = ix + 1
        if (DEBUG == 1): print("TM_PTR: %i"%team_ptr)    
        if (ix != self.TEAMS[team_ptr][3]):
          ## error message, so always print      
          print("Incorrect number of members for %s, %i != %i" % (self.TEAMS[team_ptr][0],ix,self.TEAMS[team_ptr][3]))
          return [-1]
        return srch_list  

##
##
    def tabmove2(self, zz, rowf, colf, rowt, colt):  ## moves/combines teams, searchers; then calls tabload
        ww = Ui_MainWindow   
 
        ## info from drop_event
        ## rowf, rowt, colf, colt are the locations pointed-to on screen table
        ## convert screen coord to table row and col
        fnd_from_t = tabinfo.fndloc(self, zz.TEAMS, 2, 1, rowf, colf)
        fnd_to_t   = tabinfo.fndloc(self, zz.TEAMS, 2, 1, rowt, colt)
        fnd_from_s = tabinfo.fndloc(self, zz.SRCHR, 4, 3, rowf, colf)
        fnd_to_s   = tabinfo.fndloc(self, zz.SRCHR, 4, 3, rowt, colt)
        if (DEBUG == 1): print("in move2 %i %i %i %i" %(fnd_from_t,fnd_to_t,fnd_from_s,fnd_to_s))
        if (DEBUG == 1): print(" rowf %i, colf %i; rowt %i, colt %i" % (rowf, colf, rowt, colt))

## find type (team or searcher) of FROM pointer and get all searchers
#     calc_from_t is the calculated pointer to the team entry of the searcher
        if (fnd_from_t != -1):
            if (DEBUG == 1): print("FROM TEAM HEAD")  ## find all team searchers
            srch_from = tabinfo.fnd_srchrs(zz, fnd_from_t, rowf, colf)  ## returns list of from-searchers
            if (srch_from == -1): return
        elif (fnd_from_s != -1):
            if (DEBUG == 1): print("FROM SRCHR HEAD")
            # find the team header, same col (unless unas), start at rowf and go up
            if (colf < ww.Nunas_col or colf == ww.Nsets-1):  ## not unas (normal team area OR Groups (last column))
              for rx in range(rowf-1, 0, -1):  # look for team header
                  calc_from_t = tabinfo.fndloc(self, zz.TEAMS, 2, 1, rx, colf)  ## do we need to save rx?
                  if (calc_from_t != -1): break   # found
###
### need to have colt, rowt of the team, not the srchr
              if (DEBUG == 1): print("B4 srch_from")    
              srch_from = tabinfo.fnd_srchrs(zz, calc_from_t, rx, colf)  ## returns list of from searchers
              if (srch_from == -1): return             
              if (rx == 0 or calc_from_t == -1):
                if (DEBUG == 1): print("Error, team-from header not found!")
            else:  ## in unassigned
              calc_from_t = tabinfo.fndloc(self, zz.TEAMS, 2, 1, 1, ww.Nunas_col)    ## unassigned header (do not get srch_from) 
        elif (colf >= ww.Nunas_col):   ## in unas
            calc_from_t = tabinfo.fndloc(self, zz.TEAMS, 2, 1, 1, ww.Nunas_col)  ## unassigned team header          
        else:   ## both not found, error when FROM TEAM, so, ignore  possibly set a return flag?
            return
## find type of TO pointer and get all searchers
#     calc_to_t is the calculated pointer to the team entry of the searcher
        lastRow = 0         ## set to default if not calculated below
        if (fnd_to_t != -1):
            if (DEBUG == 1): print("At fnd_to_t Ok")
            srch_to = tabinfo.fnd_srchrs(zz, fnd_to_t, rowt, colt)  ## srch_to <- pntr to SRCHR entry
            if (srch_to == -1): return
            lastRow = zz.TEAMS[fnd_to_t][2] + zz.TEAMS[fnd_to_t][3] # row of team header + numb of members
        elif (fnd_to_s != -1):
            if (DEBUG == 1): print("At fnd_to_s Ok")
            # find the team header, same col, start at rowt and go up
            for rx in range(rowt-1, 0, -1):
                calc_to_t = tabinfo.fndloc(self, zz.TEAMS, 2, 1, rx, colt)  ## do we need to save rx?
                if (calc_to_t != -1): break   # found
            srch_to = tabinfo.fnd_srchrs(zz, calc_to_t, rx, colt)  ## srch_to <- pntr to SRCHR entry
            if (srch_to == -1): return            
            lastRow = zz.TEAMS[calc_to_t][2] + zz.TEAMS[calc_to_t][3] # row of team header + numb of members
            if (DEBUG == 1): print("AT findit")
            if (rx == 0 or calc_to_t == -1):
                if (DEBUG == 1): print("Error, team-to header not found!")
        elif (colt >= ww.Nunas_col and colt < ww.Nsets-1 and colt !=0 ):      ## both not found, if from is srchr create new team unless col >=Unas_col then just ADD all to unassigned
            calc_to_t = tabinfo.fndloc(self, zz.TEAMS, 2, 1, 1, ww.Nunas_col)   ## create team below in move searcher logic
                              ##  move team if colt < 6 & colt > 0 (can't move team from/to col 0 (Overhead) or unas_col,row1 (unas))
        else:
            pass              ## both not found - move to empty

##@# check for space (for unassigned area use UNAS_USED  ENOUGH ROOM
        
        ### check for available space to move team/srchr to
        if (fnd_from_t != -1):     # from is pointing to team; note team ptr is calc_from_t for srchr movement
          nAdd = zz.TEAMS[fnd_from_t][3] + 1           # team: number of members + 1
        else:
          nAdd = 2                                     # srchr: 1 member + possible team header
          if (DEBUG == 1): print("SINGLE")
        rowx = max(rowt, lastRow)                      # rowx is rowt for unassigned and empty; lastrow for main team area
        if (DEBUG == 1): print("ROWX, ROWT, lastrow: %i, %i, %i"%(rowx,rowt,lastRow))
        if (rowx > (self.Nrows - nAdd) or rowt == -1): # check for enough room (Okay for >=6 when not creating team)
           winsound.Beep(2500, 1200)     ## BEEP, 2500Hz for 1 second, needs to be empty                    
           if (DEBUG == 1): print("BEEP1")
           return
        else:                            ## 2nd check for enough space  FIND next unassigned entry
          if (colt >= ww.Nunas_col and colt < ww.Nsets-1):          ## unassigned area
            ifnd = 0                                                #  preset to larger than number of rows
            istrt = (colt - self.Nunas_col) * self.Nrows + rowt + 1 #  start at loc+1 of this entry
            for ixx in range(istrt,len(zz.UNAS_USED)):              #  search for next used entry in this column
              if (zz.UNAS_USED[ixx] == 1):                         
                break
              ifnd = ifnd + 1            # increment cause available loc (note 1st check will do limit
                                         #    to just this column)
            if (ifnd < nAdd):            ## not enough room BEEP (this case only needs room for 1 searcher)
              winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty                    
              if (DEBUG == 1): print("BEEP2a")
              return            
          else:   ## normal team area  (and last column-Groups) use lastrow to find excess area needed
#
###    DO NOT ALLOW last column move to unless to existing item, Group or srchr
#
            ipnt = -1
            ifnd = 100                                    #  preset to larger than number of rows
            if (DEBUG == 1): print("Checking room")
            for ixx in range(0,zz.TEAMS.index(["END"])):  ## search thru all teams for team header in same column after insert loc
              rowchk = zz.TEAMS[ixx][2]                   #  rowchk is row of team to be checked
              #print("ROWCHK: %i, %i, %i"%(rowchk,colt,ifnd))
              if (zz.TEAMS[ixx][1] == colt and rowchk > rowx and rowchk < ifnd):  ## have to check for rowchk closest to rowt
                 ipnt = ixx              ## ipnt >= 0 implies at least 1 has been found; this is team ptr of next team entry
                 ifnd = rowchk           ## move max check down closer to rowt
            if (ifnd < rowx + nAdd):     ## not enough room BEEP
              winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty                    
              if (DEBUG == 1): print("BEEP2b %i %i %i"%(ifnd,lastRow,nAdd))
              return

              
        if (DEBUG == 1): print("xt %i, %i" % (fnd_from_t,fnd_to_t))
## MOVE TEAM logic
        if (fnd_from_t != -1):     # from is pointing to team
          if (colf == 0 or (colf == ww.Nunas_col and rowf == 1)): return   # don't move team in col 0 or Unassigned header 
          else:          
            if (fnd_to_t != -1 and fnd_to_t != fnd_from_t):   # to is pointing to team; not same location
                ## add members to new team, inc count of srchrs, remove from-team (unless to is unassigned)
                if (DEBUG == 1): print("Combining teams")
                for tf in range(0, zz.TEAMS[fnd_from_t][3]):
                  zz.SRCHR[srch_from[tf]][4] = rowt+tf+1       ## put from_searchers in to-team
                  zz.SRCHR[srch_from[tf]][3] = colt            ## column may change
                  zz.SRCHR[srch_from[tf]][5] = colt
                  zz.SRCHR[srch_from[tf]][6] = rowt               
                for tt in range(0, zz.TEAMS[fnd_to_t][3]):
                  zz.SRCHR[srch_to[tt]][4] = rowt+tf+1+tt+1    ## put after the above  
                zz.TEAMS[fnd_to_t][3] = zz.TEAMS[fnd_to_t][3] + zz.TEAMS[fnd_from_t][3] # inc # srchrs
                del zz.TEAMS[fnd_from_t]                       ## del from team
            elif (fnd_to_s != -1): # to is pointing to srchr
                if (colt >= ww.Nunas_col and colt < ww.Nsets-1):    # unassigned area
                    winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty
                    return
                else:              # add all srchs to new team, remove from_team
                  if (DEBUG == 1): print("Combining teams2")
                  for tf in range(0, zz.TEAMS[fnd_from_t][3]):
                    zz.SRCHR[srch_from[tf]][4] = rowt+tf         ## put from_searchers in to-team
                    zz.SRCHR[srch_from[tf]][3] = colt            ## column may change                    
                    zz.SRCHR[srch_from[tf]][5] = zz.TEAMS[calc_to_t][1]
                    zz.SRCHR[srch_from[tf]][6] = zz.TEAMS[calc_to_t][2]
                  m = 0  
                  for tt in range(0, zz.TEAMS[calc_to_t][3]): # move existing searches, below add point, down 
                    if (rowt == zz.SRCHR[srch_to[tt]][4] or m > 0): ## move searchers down by 1
                      m = m+1
                      zz.SRCHR[srch_to[tt]][4] = rowt+tf+m     ## put after the above  
                  zz.TEAMS[calc_to_t][3] = zz.TEAMS[calc_to_t][3] + zz.TEAMS[fnd_from_t][3] # inc # srchrs
                  del zz.TEAMS[fnd_from_t]                       ## del from team         
            else:  ## empty   
                if (colt >= ww.Nunas_col and colt < ww.Nsets-1):    # unassigned area
                    zz.TEAMS[fnd_from_t][2] = rowt  # new team location
                    zz.TEAMS[fnd_from_t][1] = colt
                    iz = (colt - ww.Nunas_col) * self.Nrows + rowt   ## team entry
                    zz.UNAS_USED[iz] = 1                                      
                    for tt in range(0, zz.TEAMS[fnd_from_t][3]): ## keep team intact in UNASSIGNED 
                        zz.SRCHR[srch_from[tt]][4] = rowt+tt+1
                        zz.SRCHR[srch_from[tt]][3] = colt                        
                        zz.SRCHR[srch_from[tt]][5] = colt 
                        zz.SRCHR[srch_from[tt]][6] = rowt
                        iz = iz + 1                              ## incr for each member entry
                        zz.UNAS_USED[iz] = 1                                      
                    zz.TEAMS[calc_to_t][3] = zz.TEAMS[calc_to_t][3] + zz.TEAMS[fnd_from_t][3] ## add searcher cnt to unassigned    
                    if (DEBUG == 1): print("IN UNAS")
                elif ((colt > 0 and colt < ww.Nsets-1) or (colf == ww.Nsets-1 and colt == ww.Nsets-1)):   # move only if in team area
                                ## can only move existing Group up/down in last column 
                    zz.TEAMS[fnd_from_t][2] = rowt  # new team location
                    zz.TEAMS[fnd_from_t][1] = colt
                    for tt in range(0, zz.TEAMS[fnd_from_t][3]): # move team to new location
                        zz.SRCHR[srch_from[tt]][4] = rowt+tt+1
                        zz.SRCHR[srch_from[tt]][3] = colt                        
                        zz.SRCHR[srch_from[tt]][5] = colt
                        zz.SRCHR[srch_from[tt]][6] = rowt                           
                else:
                    winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty
                    if (DEBUG == 1): print("BEEP2c")
                    return         ## BEEP as not allowed
  
## MOVE SRCHR logic
        elif (fnd_from_s != -1):   # from is pointing to srchr
            setDeleteTeam = 0      # flag to delete a FROM team after other updates
            if (fnd_to_t != -1):   # to is pointing to team
                ## add member to top of new team, inc count of srchrs, remove from team if last member or
                if (colt >= ww.Nunas_col and colt < ww.Nsets-1):    # unassigned area
                    winsound.Beep(2500, 1200)            ## BEEP, 2500Hz for 1 second, needs to be empty                    
                    if (DEBUG == 1): print("BEEP4")# needs to be empty location
                    return        
                else:       ## moving to norm team area, including col 0 (Overhead)    
                    if (colf < ww.Nunas_col):   ## not for from-srchr if in unas area  
                      m = 0                   
                      for ixx in range(0,zz.TEAMS[calc_from_t][3]):
                        if (rowf < zz.SRCHR[srch_from[ixx]][4] or m == 1):     ## move from-searchers up by 1                      
                          if (DEBUG == 1): print("AT0d: %i,%i,%i"%(rowt,ixx,srch_from[ixx]))    
                          ## move searchers up by 1
                          m = 1
                          zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1  ## move up a row
## start  - alternative: COULD not allow taking one member of a team while in unas
                    elif (colf >= ww.Nunas_col and (zz.SRCHR[fnd_from_s][5] != ww.Nunas_col or \
                          zz.SRCHR[fnd_from_s][6] != 1)):   ## must be in unas and part of a team, but not Unassigned Team
                      ## find TEAMS entry
                      if (DEBUG == 1): print("COLF: %i"%colf)  
                      ## calc_from_t2 is an alternative team pntr for the Unassigned area  
                      calc_from_t2 = tabinfo.fndloc(self,zz.TEAMS,2,1,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
                      srch_from = tabinfo.fnd_srchrs(zz,calc_from_t2,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
     ### doing fnd_srchrs here would have issue cause SRCHR already had its row,col changed                 
                      m = 0
                      for ixx in range(0,zz.TEAMS[calc_from_t2][3]):
                        if (rowf < zz.SRCHR[srch_from[ixx]][4] or m == 1):     ## move from-searchers up by 1                      
                          if (DEBUG == 1): print("AT0b: %i,%i,%i"%(rowt,ixx,srch_from[ixx]))    
                          ## move searchers up by 1
                          m = 1
                          zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1  ## move up a row
                      iz = (zz.SRCHR[srch_from[ixx]][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][4]
                      zz.UNAS_USED[iz] = 0                     ## set bottom-most entry to unused
                      if (colf < ww.Nsets-1): ## Do not reduce cnt if in Groups; done below as normal team, not unassigned team
                        if (zz.TEAMS[calc_from_t2][3] == 1):   # cnt was 1, but removed, so get rid of team entry in Unassigned
                          setDeleteTeam = 1                    
                        else:
                          zz.TEAMS[calc_from_t2][3] = zz.TEAMS[calc_from_t2][3]-1          # reduce FROM cnt by 1 
                      if (colf == ww.Nsets-1):    # from Groups column
                        typex = zz.TEAMS[calc_from_t][4]
                        zz.TEAMS[fnd_to_t][4] = typex        ## change TO team type (from Group)
                      if (DEBUG == 1): print("t2: %i %s"%(calc_from_t2,zz.TEAMS[calc_from_t2]))
                    else:  ## from is individual entry (not part of a team)
                      if (DEBUG == 1): print("Unassigned individual entry to a team")                   
                    ## use srch_to to find order of searchers
                    ## now do changes to the TO team entries
                    if (DEBUG == 1): print("XC: %i  %s"%  (fnd_to_t,zz.TEAMS[fnd_to_t]))                    
                    for ixx in range(0,zz.TEAMS[fnd_to_t][3]):       ## move to-searchers down by 1
                      #print("AT0e: %i,%i,%i"%(rowt,ixx,srch_to[ixx]))
                      #print("            %s"%zz.TEAMS[8])
                      ## move searchers down by 1
                      zz.SRCHR[srch_to[ixx]][4] = zz.SRCHR[srch_to[ixx]][4]+1
                    zz.TEAMS[fnd_to_t][3] = zz.TEAMS[fnd_to_t][3]+1  ## add 1 to team
                    if (zz.TEAMS[calc_from_t][3] == 1 and colf > 0 and colf < ww.Nunas_col): # only if in TEAM area
                      del zz.TEAMS[calc_from_t]   # if last member to remove, disband from-team
                    else:
                        zz.TEAMS[calc_from_t][3] = zz.TEAMS[calc_from_t][3]-1  # reduce from cnt by 1
                        iz = (zz.SRCHR[fnd_from_s][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[fnd_from_s][4]
                        zz.UNAS_USED[iz] = 0
                    zz.SRCHR[fnd_from_s][4] = rowt+1  # add srchr to new team after team header, remove from from_team
                    zz.SRCHR[fnd_from_s][3] = colt
                    zz.SRCHR[fnd_from_s][5] = colt    # point to team entry
                    zz.SRCHR[fnd_from_s][6] = rowt
                    if (setDeleteTeam == 1):
                      del zz.TEAMS[calc_from_t2]             # if last member to remove, disband from-team
                      iz = (zz.SRCHR[srch_from[ixx]][5] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][6]
                      zz.UNAS_USED[iz] = 0                                             
            elif (fnd_to_s != -1): # to is pointing to srchr
                if (colt >= ww.Nunas_col and colt < ww.Nsets-1):    # unassigned area
                    winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, needs to be empty                    
                    if (DEBUG == 1): print("BEEP3")     # needs to be empty location
                    return        
                else:  ## to is in team area
                    if (calc_from_t == calc_to_t):   # make correction for same team srchr movement
                        print("same team srchr move")
                        rowt = rowt - 1     # don't move down by 1
                    #
                    # if moving a leader to a srchr of a team promote to first position if that position
                    #   is not already held by a leader
                    if (zz.SRCHR[fnd_from_s][7] == "1"):      # this is a leader
                        if (zz.SRCHR[srch_to[0]][7] != "1"):  # first srchr is not already a leader
                            rowt = zz.SRCHR[srch_to[0]][6]    # change to-row to the row of team header
                    if (colf < ww.Nunas_col):   ## not for moving from-srchr if in unas
                      m = 0
                      for ixx in range(0,zz.TEAMS[calc_from_t][3]):
                        if (rowf < zz.SRCHR[srch_from[ixx]][4] or m == 1):        ## move from-searchers up by 1
                          m = 1  
                          if (DEBUG == 1): print("AT0a: %i,%i,%i"%(rowf,ixx,srch_from[ixx]))    
                          zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1  ## move up a row                          
## start  - alternative: COULD not allow taking one member of a team while in unas
                      ## the two addresses below are for the team (Unassigned) (not the srchr...) So, this is the area to get a srchr from a team
                      ##                that is currently in the Unassigned area                         
                    elif (colf >= ww.Nunas_col and (zz.SRCHR[fnd_from_s][5] != ww.Nunas_col or \
                          zz.SRCHR[fnd_from_s][6] != 1)):  ## must be in unas and part of a team (but not Unassigned team)
                      ## find TEAMS entry
                      calc_from_t2 = tabinfo.fndloc(self,zz.TEAMS,2,1,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
                      srch_from = tabinfo.fnd_srchrs(zz,calc_from_t2,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
     ### doing fnd_srchrs here could have issue cause SRCHR already had row,col changed                 
                      m = 0
                      for ixx in range(0,zz.TEAMS[calc_from_t2][3]):
                        if (rowf < zz.SRCHR[srch_from[ixx]][4] or m == 1):     ## move from-searchers up by 1   (WHY DO THIS for UNassigned?)                   
                          if (DEBUG == 1): print("AT0b: %i,%i,%i"%(rowt,ixx,srch_from[ixx]))    
                          ## move searchers up by 1
                          m = 1
                          zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1  ## move up a row
                      iz = (zz.SRCHR[srch_from[ixx]][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][4]
                      zz.UNAS_USED[iz] = 0                   ## set bottom-most entry to unused                          
                      if (colf < ww.Nsets-1):  ## Do not reduce cnt if in Groupsdone below; as normal team, not unassigned team
                        if (zz.TEAMS[calc_from_t2][3] == 1):   # CHECK for team in Unassigned area  
                          setDeleteTeam = 1                                           
                        else:
                          zz.TEAMS[calc_from_t2][3] = zz.TEAMS[calc_from_t2][3]-1          # reduce FROM cnt by 1
                      elif (colf == ww.Nsets-1):    # from Groups column
                        typex = zz.TEAMS[calc_from_t][4]
                        zz.TEAMS[calc_to_t][4] = typex        ## change TO team type (from Group)                      
                    else:  ## moving an individual (not part of team) searcher from unassigned
                      if (DEBUG == 1): print("Unassigned individual entry to searcher")
                      iz = (zz.SRCHR[fnd_from_s][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[fnd_from_s][4]
                      zz.UNAS_USED[iz] = 0                   ## set entry to unused
                    ## use srch_to to find insert position
                    m = 0
                    if (DEBUG == 1): print("CALC FROM-TO %i %i"% (calc_from_t, calc_to_t))
                    if (DEBUG == 1): print("XXXX %s: %s"%(zz.TEAMS[calc_to_t],zz.TEAMS[calc_from_t]))     
                    for ixx in range(0,zz.TEAMS[calc_to_t][3]):
                      if (DEBUG == 1): print("ATx: %i,%i,%i:%i"%(rowt,ixx,srch_to[ixx],zz.SRCHR[srch_to[ixx]][4]))
     ###  could find which index in srch_to == rowt b4 above loop
                      ## add 1 to rowt to move the 'next' existing srchr down by 1                     
                      if (rowt+1 == zz.SRCHR[srch_to[ixx]][4] or m == 1): ## move to-searchers down by 1
                        m = 1
                        zz.SRCHR[srch_to[ixx]][4] = zz.SRCHR[srch_to[ixx]][4]+1  ## move down a row (only 1 mover)
                    zz.TEAMS[calc_to_t][3] = zz.TEAMS[calc_to_t][3]+1  ## add 1 to team
                    if (zz.TEAMS[calc_from_t][3] == 1 and colf > 0 and colf < ww.Nunas_col): # only if in TEAM area
                        setDeleteTeam = 2
                        # if last member to remove, disband the from-team
                    else:
                        zz.TEAMS[calc_from_t][3] = zz.TEAMS[calc_from_t][3]-1  # reduce from cnt by 1
                    ## below, add 1 to place the new srchr below the existing srchr    
                    zz.SRCHR[fnd_from_s][4] = rowt+1  # add srchr to new team (or within orig team) after srchr, remove from from_team
                    zz.SRCHR[fnd_from_s][3] = colt    # Note, searcher is added below the position pointed to                         
                    zz.SRCHR[fnd_from_s][5] = zz.TEAMS[calc_to_t][1]    ## col - point to team entry
                    zz.SRCHR[fnd_from_s][6] = zz.TEAMS[calc_to_t][2]
                    if (setDeleteTeam == 1):
                      del zz.TEAMS[calc_from_t2]           # if last member to remove, disband from-team
                      iz = (zz.SRCHR[srch_from[ixx]][5] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][6]
                      zz.UNAS_USED[iz] = 0
                    elif (setDeleteTeam == 2):
                      del zz.TEAMS[calc_from_t]  
            else:  ## TO is pointing to empty
                if (DEBUG == 1): print("AT EMPTY........")
                if (colt >= ww.Nunas_col and colt < ww.Nsets-1):        # to unassigned area
                    ##
                    ##   use UNAS_USED[ixx] to see if there is enough room for proposed placement
                    ##      colu = int(ixx/self.Nrows)
                    ##      rowu = ixx - colu * self.Nrows
                    ##      colu = colu + self.Nunas_col   
                    ##
                    ####  will NEED to collapse from-team searchers                
                    if (colf < ww.Nunas_col):        ## collapse from-team if in team area
                      if (DEBUG == 1): print("AT first branch")  
                      for ixx in range(0,zz.TEAMS[calc_from_t][3]):
                        if (rowf < zz.SRCHR[srch_from[ixx]][4]):         ## move from-searchers up by 1                          
                          zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1   ## move up a row                                       
                      if (zz.TEAMS[calc_from_t][3] == 1 and colf > 0 and colf < ww.Nunas_col): # only if in TEAM area
                        del zz.TEAMS[calc_from_t]   # if last member to remove, disband from-team
                      else:
                        zz.TEAMS[calc_from_t][3] = zz.TEAMS[calc_from_t][3]-1  # reduce from cnt by 1
                    elif (colf >= ww.Nunas_col and (zz.SRCHR[fnd_from_s][5] != ww.Nunas_col or \
                            zz.SRCHR[fnd_from_s][6] != 1)):  ## must be in unas and part of a real team (not the Unassigned team)
                        ## find TEAMS entry
                        if (DEBUG == 1): print("IN move from unas team to searcher in unassigned")
                        calc_from_t2 = tabinfo.fndloc(self,zz.TEAMS,2,1,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
                        srch_from = tabinfo.fnd_srchrs(zz,calc_from_t2,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
     ### doing fnd_srchrs here would have issue cause SRCHR already had row,col changed                 
                        m = 0
                        for ixx in range(0,zz.TEAMS[calc_from_t2][3]):
                          if (rowf < zz.SRCHR[srch_from[ixx]][4] or m == 1):     ## move from-searchers up by 1                      
                            if (DEBUG == 1): print("AT0f: %i,%i,%i"%(rowt,ixx,srch_from[ixx]))    
                            ## move searchers up by 1
                            m = 1
                            zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1  ## move up a row
                        iz = (zz.SRCHR[srch_from[ixx]][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][4]
                        zz.UNAS_USED[iz] = 0                   ## set bottom-most entry to unused                                                    
                        if (zz.TEAMS[calc_from_t2][3] == 1 and colf != ww.Nsets-1): ## Do not remove GROUPS headers
                          del zz.TEAMS[calc_from_t2]   # if last member to remove, disband from-team
                          iz = (zz.SRCHR[srch_from[ixx]][5] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][6]
                          zz.UNAS_USED[iz] = 0                                                                     
                        else:
                          zz.TEAMS[calc_from_t2][3] = zz.TEAMS[calc_from_t2][3]-1          # reduce from cnt by 1
                    else:
                        if (DEBUG == 1): print("AT third branch")
                        iz = (zz.SRCHR[fnd_from_s][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[fnd_from_s][4]
                        zz.UNAS_USED[iz] = 0                   ## set bottom-most entry to unused             
                        zz.TEAMS[calc_from_t][3] = zz.TEAMS[calc_from_t][3]-1    ## moved searcher (from unas)   
                    zz.SRCHR[fnd_from_s][4] = rowt  # add srchr to unas team, remove from from_team; do after above so as to not affect above search
                    zz.SRCHR[fnd_from_s][3] = colt
                    zz.SRCHR[fnd_from_s][5] = zz.TEAMS[calc_to_t][1]   ## col - point to TO team entry
                    zz.SRCHR[fnd_from_s][6] = zz.TEAMS[calc_to_t][2]
                    zz.TEAMS[calc_to_t][3] = zz.TEAMS[calc_to_t][3]+1  ## add 1 to TO team (Unassigned in this case)
                    iz = (colt - ww.Nunas_col) * self.Nrows + rowt
                    zz.UNAS_USED[iz] = 1                                                                 
                else:      ## TO normal team area (includes last column for GROUPS)
######
##   CHECKING FOR ENOUGH ROOM OR pointing off the table   from srchr, to empty/assigned, therefore 1 memb move
######          (will have to look for team-wise, too)    
####  do we search for next team to find available room?

                    if (DEBUG == 1): print("AT going to NORM TEAM area .....")
                    if (colt == 0):       ## do not create in col 0
                         winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, do not create a team in col 0                    
                         if (DEBUG == 1): print("BEEP6")
                         return
                    elif (colt < ww.Nsets-1):   ## do not create a team in last column                     
                    ## CREATE team        ((( if from an existing team, need to collapse the from-team )))
                      if (DEBUG == 1): print("zz %i %i %i" % (zz.TEAM_NUM,colt,rowt))
                      zz.TEAM_NUM = zz.TEAM_NUM + 1
                      typex = "GND"   # default
                      if (colf == ww.Nsets-1):
                        typex = zz.TEAMS[calc_from_t][4]   # came from Groups, so use type                          
                      zz.TEAMS.insert(zz.TEAMS.index(["END"]),["TEAM "+str(zz.TEAM_NUM), colt, rowt, 1, typex, "IC", 0.0]) # insert prior to END
                      ##print("ALL TEAMS: %s"%zz.TEAMS)
                      if (colf < ww.Nunas_col):        ## collapse from-team if in team area
                        for ixx in range(0,zz.TEAMS[calc_from_t][3]):
                          if (rowf < zz.SRCHR[srch_from[ixx]][4]):         ## move from-searchers up by 1                          
                            zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1   ## move up a row                                       
                        if (zz.TEAMS[calc_from_t][3] == 1 and colf > 0 and colf < ww.Nunas_col):     # only if in TEAM area
                          del zz.TEAMS[calc_from_t]   # if last member to remove, disband from-team
                        else:
                          zz.TEAMS[calc_from_t][3] = zz.TEAMS[calc_from_t][3]-1  ## moved searcher (from another team)
## start  - alternative: COULD not allow taking one member of a team while in unas
                      elif (colf >= ww.Nunas_col and (zz.SRCHR[fnd_from_s][5] != ww.Nunas_col or \
                            zz.SRCHR[fnd_from_s][6] != 1)):  ## must be in unas and part of a real team (not the Unassigned team)
                        ## find TEAMS entry 
                        calc_from_t2 = tabinfo.fndloc(self,zz.TEAMS,2,1,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
                        srch_from = tabinfo.fnd_srchrs(zz,calc_from_t2,zz.SRCHR[fnd_from_s][6],zz.SRCHR[fnd_from_s][5])
     ### doing fnd_srchrs here would have issue cause SRCHR already had row,col changed                 
                        m = 0
                        for ixx in range(0,zz.TEAMS[calc_from_t2][3]):
                          if (rowf < zz.SRCHR[srch_from[ixx]][4] or m == 1):     ## move from-searchers up by 1                      
                            if (DEBUG == 1): print("AT0c: %i,%i,%i"%(rowt,ixx,srch_from[ixx]))    
                            ## move searchers up by 1
                            m = 1
                            zz.SRCHR[srch_from[ixx]][4] = zz.SRCHR[srch_from[ixx]][4]-1  ## move up a row
                        iz = (zz.SRCHR[srch_from[ixx]][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][4]
                        zz.UNAS_USED[iz] = 0                   ## set bottom-most entry to unused                                                    
                        if (zz.TEAMS[calc_from_t2][3] == 1 and colf != ww.Nsets-1): ## Do not remove GROUPS headers
                          del zz.TEAMS[calc_from_t2]   # if last member to remove, disband from-team
                          iz = (zz.SRCHR[srch_from[ixx]][5] - ww.Nunas_col) * self.Nrows + zz.SRCHR[srch_from[ixx]][6]
                          zz.UNAS_USED[iz] = 0                                                                     
                        else:
                          zz.TEAMS[calc_from_t2][3] = zz.TEAMS[calc_from_t2][3]-1          # reduce from cnt by 1
                      else:
                        zz.TEAMS[calc_from_t][3] = zz.TEAMS[calc_from_t][3]-1    ## moved searcher (from unas)
                        iz = (zz.SRCHR[fnd_from_s][3] - ww.Nunas_col) * self.Nrows + zz.SRCHR[fnd_from_s][4]
                        zz.UNAS_USED[iz] = 0                   ## set entry to unused                                                                                               
                    else:  ## must be at last column
                      winsound.Beep(2500, 1200)  ## BEEP, 2500Hz for 1 second, do not create a team in last column this way                    
                      if (DEBUG == 1): print("BEEP6c")
                      return
                    zz.SRCHR[fnd_from_s][3] = colt       ## move searcher after Team header (do after above, so as to not affect above search
                    zz.SRCHR[fnd_from_s][5] = colt
                    zz.SRCHR[fnd_from_s][6] = rowt               ## can this be in unassigned area??? do not think so
                    zz.SRCHR[fnd_from_s][4] = rowt + 1
##  Need to add check that room exists in column or to next team in the column, if not do a BEEP

        #print("WOW: %s"%zz.saveTeam)  
        if (DEBUG == 1): print("end tabmove2 %s" % zz)
        tabinfo.tabload(self,zz,0)       ## overload display table
        if (DEBUG == 1): print("Pre update2")
        self.update()                    ## is this a function of printEvent?
        ##QtGui.QGuiApplication.processEvents() #update gui for pyqt
        if (DEBUG == 1): print("Post update2")
               

        

