# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwin.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
from PyQt5 import QtCore, QtGui, QtWidgets
import images
import PyQt5.QtWidgets 
import PyQt5.QtGui 
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import pyqtgraph.exporters
import sys
import numpy as np
import pandas as pd
import mne
import soundfile as sf
from spectrogram import Ui_OtherWindow
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

from reportlab.platypus import Table
from reportlab.platypus import Image
from reportlab.platypus import TableStyle
from reportlab.lib import colors

import matplotlib.pyplot as plt

#signal class
class Signal(PlotWidget):

    def __init__ (self,file_path,data):
        self.file_path=file_path
        self.data=data
        #initial plot range
        self.x_range=[0,2000]
        
    #pg configurations
    pg.setConfigOptions(background='w')
    #anti aliasing to improve the appearance of a small image that's being scaled up
    pg.setConfigOptions(antialias=True)

    # #for plotting after reading signal
    # def plot_signal(self):
    #     self.win=pg.GraphicsWindow()
    #     self.win.setFocus()   
    #     self.win.resize(750, 356)
    #     self.waveform = self.win.addPlot(row=1, col=1)
    #     x= np.arange(0,  len(self.data) , 1)
    #     self.waveform.showGrid( x = True, y = True)
    #     self.waveform.enableAutoRange( x = False, y = True)
    #     p = self.waveform.plot(pen='b', width=0.1)
    #     p.setData(x, self.data)
    #     #self.waveform.setYRange(min(self.data)-1.5, max(self.data)+1.5, padding=0)
    #     self.waveform.setXRange(self.x_range[0], self.x_range[1],padding=0.005)
    #     #to send signal when clicked
    #     self.waveform.scene().sigMouseClicked.connect(lambda : ui.detect_click(self.file_path))
    #     self.win.closeEvent=self.closeEvent
    
    #     #self.waveform.scene().sigItemRemoved.connect(lambda : ui.signal_closed(self.file_path))
    #     # pg.SignalProxy( self.waveform.scene().sigMouseClicked, rateLimit=60, slot=self.emit_path)  
    
        
    #for plotting after reading signal
    # plotting using graphics layout widget instead of graphics window
    def plot_signal(self):
        self.sa = pg.QtGui.QScrollArea()
        self.sa.setFocus()   
        self.w = pg.GraphicsLayoutWidget()
        self.w.resize(850, 556)
        self.sa.setWidget(self.w)
        
        self.waveform = self.w.addPlot(row=1, col=1)
        x= np.arange(0,  len(self.data) , 1)
        self.waveform.showGrid( x = True, y = True)
        self.waveform.enableAutoRange( x = False, y = True)
        p = self.waveform.plot(pen='b', width=0.1)
        p.setData(x, self.data)
        #self.waveform.setYRange(min(self.data)-1.5, max(self.data)+1.5, padding=0)
        self.waveform.setXRange(self.x_range[0], self.x_range[1],padding=0.005)
        #to send signal when clicked
        self.waveform.scene().sigMouseClicked.connect(lambda : ui.detect_click(self.file_path))
        self.sa.show()
        self.sa.closeEvent=self.closeEvent


    def closeEvent(self, event):
        ui.signal_closed(self.file_path)

class Pin():
    def __init__ (self): 
        self.title = ''
        self.SignalPath= [] 
        self.GramPath= [] 
        self.pinElementTable=None

    def getPins(self,path):
        name = path.split("/")[-1]
        self.title = name 
        self.SignalPath = [name+".png"]
        self.GramPath = [name+"s"+".png"]
    
    

class Ui_MainWindow(object):

    signals={} #have signal path and the created signal object
    pins={} # have signal path and creted pin object
    played=0 #playing flag 
    pause=0 #pause flag

    def open_window(self):
        self.spectro_draw()
        self.window=QtWidgets.QMainWindow()
        self.ui= Ui_OtherWindow()
        self.ui.setupUi(self.window)
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowIcon(QtGui.QIcon("images/appicon.png")) 
        MainWindow.resize(1860, 696)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 697, 668))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.frame.setMinimumSize(QtCore.QSize(0, 650))
        self.frame.setStyleSheet("background-color: rgb(170, 170, 170);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2.addWidget(self.frame)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 734, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuASCII_CSV_files = QtWidgets.QMenu(self.menuFile)
        self.menuASCII_CSV_files.setObjectName("menuASCII_CSV_files")
        self.menuData_acquisition = QtWidgets.QMenu(self.menubar)
        self.menuData_acquisition.setObjectName("menuData_acquisition")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuPlay_navigate = QtWidgets.QMenu(self.menubar)
        self.menuPlay_navigate.setObjectName("menuPlay_navigate")
        self.menu3D_tools = QtWidgets.QMenu(self.menubar)
        self.menu3D_tools.setObjectName("menu3D_tools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpen_signal = QtWidgets.QAction(MainWindow)
        self.actionOpen_signal.setEnabled(True)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon1.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_signal.setIcon(icon)
        self.actionOpen_signal.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionOpen_signal.setObjectName("actionOpen_signal")
        self.actionRaw_binary_files = QtWidgets.QAction(MainWindow)
        self.actionRaw_binary_files.setObjectName("actionRaw_binary_files")
        self.actionOpen_data_log_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_data_log_file.setObjectName("actionOpen_data_log_file")
        self.actionSignal_from_clipboard_data_ASCII_CSV = QtWidgets.QAction(MainWindow)
        self.actionSignal_from_clipboard_data_ASCII_CSV.setObjectName("actionSignal_from_clipboard_data_ASCII_CSV")
        self.actionRecent_signals = QtWidgets.QAction(MainWindow)
        self.actionRecent_signals.setObjectName("actionRecent_signals")
        self.actionRecent_workspaces = QtWidgets.QAction(MainWindow)
        self.actionRecent_workspaces.setObjectName("actionRecent_workspaces")
        self.actionReplace_signal_with = QtWidgets.QAction(MainWindow)
        self.actionReplace_signal_with.setObjectName("actionReplace_signal_with")
        self.actionSave_signal_as = QtWidgets.QAction(MainWindow)
        self.actionSave_signal_as.setObjectName("actionSave_signal_as")
        self.actionSave_visible_signal_part_as = QtWidgets.QAction(MainWindow)
        self.actionSave_visible_signal_part_as.setObjectName("actionSave_visible_signal_part_as")
        self.Export_pdf = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/pdf.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Export_pdf.setIcon(icon1)
        self.Export_pdf.setObjectName("Export_pdf")
        self.actionSave_Workspace = QtWidgets.QAction(MainWindow)
        self.actionSave_Workspace.setObjectName("actionSave_Workspace")
        self.actionLoad_Workspace = QtWidgets.QAction(MainWindow)
        self.actionLoad_Workspace.setObjectName("actionLoad_Workspace")
        self.actionSave_window_as_bitmap = QtWidgets.QAction(MainWindow)
        self.actionSave_window_as_bitmap.setObjectName("actionSave_window_as_bitmap")
        self.actionSave_window_as_custom_tool = QtWidgets.QAction(MainWindow)
        self.actionSave_window_as_custom_tool.setObjectName("actionSave_window_as_custom_tool")
        self.actionUse_custom_tool = QtWidgets.QAction(MainWindow)
        self.actionUse_custom_tool.setObjectName("actionUse_custom_tool")
        self.actionApplication_settings = QtWidgets.QAction(MainWindow)
        self.actionApplication_settings.setObjectName("actionApplication_settings")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionImport_signal_from_CSV_decimal_dot = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/icon2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionImport_signal_from_CSV_decimal_dot.setIcon(icon2)
        self.actionImport_signal_from_CSV_decimal_dot.setObjectName("actionImport_signal_from_CSV_decimal_dot")
        self.actionImport_signal_from_CSV_decimal_comma = QtWidgets.QAction(MainWindow)
        self.actionImport_signal_from_CSV_decimal_comma.setObjectName("actionImport_signal_from_CSV_decimal_comma")
        self.action_Signal_beginning = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/signalbegin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_Signal_beginning.setIcon(icon3)
        self.action_Signal_beginning.setObjectName("action_Signal_beginning")
        self.actionSignal_End = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/signalend.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSignal_End.setIcon(icon4)
        self.actionSignal_End.setObjectName("actionSignal_End")
        self.actionGo_to_sample = QtWidgets.QAction(MainWindow)
        self.actionGo_to_sample.setObjectName("actionGo_to_sample")
        self.actionPlay_signal_no_sound = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/play.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPlay_signal_no_sound.setIcon(icon5)
        self.actionPlay_signal_no_sound.setObjectName("actionPlay_signal_no_sound")
        self.actionPlay_as_fast_as_possible = QtWidgets.QAction(MainWindow)
        self.actionPlay_as_fast_as_possible.setObjectName("actionPlay_as_fast_as_possible")
        self.actionPlay_signal_with_sound = QtWidgets.QAction(MainWindow)
        self.actionPlay_signal_with_sound.setObjectName("actionPlay_signal_with_sound")
        self.actionPlay_visible_segment_only_with_sound = QtWidgets.QAction(MainWindow)
        self.actionPlay_visible_segment_only_with_sound.setObjectName("actionPlay_visible_segment_only_with_sound")
        self.actionStop_playing = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionStop_playing.setIcon(icon6)
        self.actionStop_playing.setObjectName("actionStop_playing")
        self.actionStep_change = QtWidgets.QAction(MainWindow)
        self.actionStep_change.setObjectName("actionStep_change")
        self.actionRepeat_forever_play_in_loop = QtWidgets.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/loop.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRepeat_forever_play_in_loop.setIcon(icon7)
        self.actionRepeat_forever_play_in_loop.setObjectName("actionRepeat_forever_play_in_loop")
        self.actionAdjust_volume_automatically = QtWidgets.QAction(MainWindow)
        self.actionAdjust_volume_automatically.setObjectName("actionAdjust_volume_automatically")
        self.actionPlay_automatically_if_signal_changes = QtWidgets.QAction(MainWindow)
        self.actionPlay_automatically_if_signal_changes.setObjectName("actionPlay_automatically_if_signal_changes")
        self.actionTime_FFT = QtWidgets.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/timeffticon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTime_FFT.setIcon(icon8)
        self.actionTime_FFT.setObjectName("actionTime_FFT")
        self.actionSpectrogram = QtWidgets.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("images/specicon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSpectrogram.setIcon(icon9)
        self.actionSpectrogram.setObjectName("actionSpectrogram")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")
        self.actionCut = QtWidgets.QAction(MainWindow)
        self.actionCut.setObjectName("actionCut")
        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")
        self.actionZoom_In = QtWidgets.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("images/zoomin.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_In.setIcon(icon10)
        self.actionZoom_In.setObjectName("actionZoom_In")
        self.actionZoom_out = QtWidgets.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("images/zoomout.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_out.setIcon(icon11)
        self.actionZoom_out.setObjectName("actionZoom_out")
        self.actionZoom_to_X_sample_values = QtWidgets.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("images/zoomto.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionZoom_to_X_sample_values.setIcon(icon12)
        self.actionZoom_to_X_sample_values.setObjectName("actionZoom_to_X_sample_values")
        self.menuASCII_CSV_files.addAction(self.actionImport_signal_from_CSV_decimal_dot)
        self.menuASCII_CSV_files.addAction(self.actionImport_signal_from_CSV_decimal_comma)
        self.menuFile.addAction(self.actionOpen_signal)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.menuASCII_CSV_files.menuAction())
        self.menuFile.addAction(self.actionRaw_binary_files)
        self.menuFile.addAction(self.actionOpen_data_log_file)
        self.menuFile.addAction(self.actionSignal_from_clipboard_data_ASCII_CSV)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionRecent_signals)
        self.menuFile.addAction(self.actionRecent_workspaces)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionReplace_signal_with)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_signal_as)
        self.menuFile.addAction(self.actionSave_visible_signal_part_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.Export_pdf)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_Workspace)
        self.menuFile.addAction(self.actionLoad_Workspace)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_window_as_bitmap)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_window_as_custom_tool)
        self.menuFile.addAction(self.actionUse_custom_tool)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionApplication_settings)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionCut)
        self.menuEdit.addAction(self.actionPaste)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionZoom_In)
        self.menuEdit.addAction(self.actionZoom_out)
        self.menuEdit.addAction(self.actionZoom_to_X_sample_values)
        self.menuPlay_navigate.addAction(self.action_Signal_beginning)
        self.menuPlay_navigate.addAction(self.actionSignal_End)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionGo_to_sample)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionPlay_signal_no_sound)
        self.menuPlay_navigate.addAction(self.actionPlay_as_fast_as_possible)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionPlay_signal_with_sound)
        self.menuPlay_navigate.addAction(self.actionPlay_visible_segment_only_with_sound)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionStop_playing)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionStep_change)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionRepeat_forever_play_in_loop)
        self.menuPlay_navigate.addAction(self.actionAdjust_volume_automatically)
        self.menuPlay_navigate.addSeparator()
        self.menuPlay_navigate.addAction(self.actionPlay_automatically_if_signal_changes)
        self.menu3D_tools.addAction(self.actionTime_FFT)
        self.menu3D_tools.addAction(self.actionSpectrogram)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuData_acquisition.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuPlay_navigate.menuAction())
        self.menubar.addAction(self.menu3D_tools.menuAction())
        self.toolBar.addAction(self.actionOpen_signal)
        self.toolBar.addAction(self.actionImport_signal_from_CSV_decimal_dot)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.Export_pdf)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionZoom_In)
        self.toolBar.addAction(self.actionZoom_out)
        self.toolBar.addAction(self.actionZoom_to_X_sample_values)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_Signal_beginning)
        self.toolBar.addAction(self.actionPlay_signal_no_sound)
        self.toolBar.addAction(self.actionSignal_End)
        self.toolBar.addAction(self.actionStop_playing)
        self.toolBar.addAction(self.actionPlay_as_fast_as_possible)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRepeat_forever_play_in_loop)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionTime_FFT)
        self.toolBar.addAction(self.actionSpectrogram)



        #Actions 
        self.actionOpen_signal.triggered.connect(self.open_sig)
        self.actionImport_signal_from_CSV_decimal_comma.triggered.connect(self.open_csv)
        #self.actionImport_signal_from_CSV_decimal_dot.triggered.connect(self.open_scv)
        self.actionZoom_In.triggered.connect(self.zoom_in)
        self.actionZoom_out.triggered.connect(self.zoom_out)
        self.actionPlay_signal_no_sound.triggered.connect(lambda: self.play_signal(3))
        self.actionStop_playing.triggered.connect(self.pause_signal)
        self.action_Signal_beginning.triggered.connect(self.signal_beginning)
        self.actionSignal_End.triggered.connect(self.signal_end)
        self.actionPlay_as_fast_as_possible.triggered.connect(self.play_fast)
        self.Export_pdf.triggered.connect(self.E_pdf)
        self.actionSpectrogram.triggered.connect(self.open_window)

        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SIGVIEW"))
        self.menuFile.setStatusTip(_translate("MainWindow", "Creates a new document"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuASCII_CSV_files.setStatusTip(_translate("MainWindow", "Import new ASCII signal (dot as decimal separator)"))
        self.menuASCII_CSV_files.setTitle(_translate("MainWindow", "ASCII / CSV files"))
        self.menuData_acquisition.setTitle(_translate("MainWindow", "Data acquisition"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuPlay_navigate.setTitle(_translate("MainWindow", "Play && navigate"))
        self.menu3D_tools.setTitle(_translate("MainWindow", "3D tools"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpen_signal.setText(_translate("MainWindow", "Open signal..."))
        self.actionOpen_signal.setStatusTip(_translate("MainWindow", "Opens new signal"))
        self.actionOpen_signal.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionRaw_binary_files.setText(_translate("MainWindow", "Raw binary files"))
        self.actionOpen_data_log_file.setText(_translate("MainWindow", "Open data log file..."))
        self.actionSignal_from_clipboard_data_ASCII_CSV.setText(_translate("MainWindow", "Signal from clipboard data... (ASCII / CSV)"))
        self.actionSignal_from_clipboard_data_ASCII_CSV.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionRecent_signals.setText(_translate("MainWindow", "Recent signals"))
        self.actionRecent_workspaces.setText(_translate("MainWindow", "Recent workspaces"))
        self.actionReplace_signal_with.setText(_translate("MainWindow", "Replace signal with..."))
        self.actionSave_signal_as.setText(_translate("MainWindow", "Save signal as..."))
        self.actionSave_visible_signal_part_as.setText(_translate("MainWindow", "Save visible signal part as..."))
        self.Export_pdf.setText(_translate("MainWindow", "Export report as pdf"))
        self.Export_pdf.setStatusTip(_translate("MainWindow", "Export report for the selected signals as pdf"))
        self.Export_pdf.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.actionSave_Workspace.setText(_translate("MainWindow", "Save Workspace..."))
        self.actionLoad_Workspace.setText(_translate("MainWindow", "Load Workspace..."))
        self.actionSave_window_as_bitmap.setText(_translate("MainWindow", "Save window as bitmap..."))
        self.actionSave_window_as_custom_tool.setText(_translate("MainWindow", "Save window as custom tool"))
        self.actionUse_custom_tool.setText(_translate("MainWindow", "Use custom tool"))
        self.actionApplication_settings.setText(_translate("MainWindow", "Application settings..."))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Alt+F4"))
        self.actionImport_signal_from_CSV_decimal_dot.setText(_translate("MainWindow", "Import signal from CSV (decimal dot)..."))
        self.actionImport_signal_from_CSV_decimal_dot.setStatusTip(_translate("MainWindow", "Import new ASCII  signal (dot as decimal separator)"))
        self.actionImport_signal_from_CSV_decimal_comma.setText(_translate("MainWindow", "Import signal from CSV (decimal comma)..."))
        self.actionImport_signal_from_CSV_decimal_comma.setStatusTip(_translate("MainWindow", "Import new ASCII signal (comma as decimal separator)"))
        self.action_Signal_beginning.setText(_translate("MainWindow", "<< Signal beginning"))
        self.action_Signal_beginning.setShortcut(_translate("MainWindow", "Home"))
        self.actionSignal_End.setText(_translate("MainWindow", "Signal End >>"))
        self.actionSignal_End.setShortcut(_translate("MainWindow", "End"))
        self.actionGo_to_sample.setText(_translate("MainWindow", "Go to sample..."))
        self.actionPlay_signal_no_sound.setText(_translate("MainWindow", "Play signal (no sound)"))
        self.actionPlay_signal_no_sound.setShortcut(_translate("MainWindow", "F5"))
        self.actionPlay_as_fast_as_possible.setText(_translate("MainWindow", "Play as fast as possible"))
        self.actionPlay_signal_with_sound.setText(_translate("MainWindow", "Play signal (with sound)"))
        self.actionPlay_visible_segment_only_with_sound.setText(_translate("MainWindow", "Play visible segment only (with sound)"))
        self.actionPlay_signal_with_sound.setShortcut(_translate("MainWindow", "F6"))
        self.actionStop_playing.setText(_translate("MainWindow", "Stop playing"))
        self.actionStop_playing.setStatusTip(_translate("MainWindow", "Stops acquisition"))
        self.actionStop_playing.setShortcut(_translate("MainWindow", "F7"))
        self.actionStep_change.setText(_translate("MainWindow", "Step change..."))
        self.actionStep_change.setStatusTip(_translate("MainWindow", "Change step for moving trough signals"))
        self.actionStep_change.setShortcut(_translate("MainWindow", "Alt+Up, Alt+Down"))
        self.actionRepeat_forever_play_in_loop.setText(_translate("MainWindow", "Repeat forever (play in loop)"))
        self.actionRepeat_forever_play_in_loop.setStatusTip(_translate("MainWindow", "Start playing signal from the beginning each time its end has been reached"))
        self.actionAdjust_volume_automatically.setText(_translate("MainWindow", "Adjust volume automatically"))
        self.actionPlay_automatically_if_signal_changes.setText(_translate("MainWindow", "Play automatically if signal changes"))
        self.actionPlay_automatically_if_signal_changes.setStatusTip(_translate("MainWindow", "Play signal on sound card on every change"))
        self.actionTime_FFT.setText(_translate("MainWindow", "Time FFT..."))
        self.actionTime_FFT.setShortcut(_translate("MainWindow", "Ctrl+T"))
        self.actionSpectrogram.setText(_translate("MainWindow", "Spectrogram..."))
        self.actionSpectrogram.setShortcut(_translate("MainWindow", "Ctrl+G"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionCut.setText(_translate("MainWindow", "Cut"))
        self.actionCut.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))
        self.actionZoom_In.setText(_translate("MainWindow", "Zoom In"))
        self.actionZoom_In.setStatusTip(_translate("MainWindow", "Zoom selected part"))
        self.actionZoom_out.setText(_translate("MainWindow", "Zoom out"))
        self.actionZoom_out.setStatusTip(_translate("MainWindow", "Show previous zoom"))
        self.actionZoom_to_X_sample_values.setText(_translate("MainWindow", "Zoom to X sample/values..."))
        self.actionZoom_to_X_sample_values.setStatusTip(_translate("MainWindow", "Zoom to X samples/values"))
        self.actionZoom_to_X_sample_values.setShortcut(_translate("MainWindow", "Ctrl+2"))

    
    #open for signals .wav , .edf
    def open_sig(self):
        if len(self.signals) < 3:
            print("open_sig")
            path = PyQt5.QtWidgets.QFileDialog.getOpenFileName(None, 'Open', None, "EDF(*.edf);;WAV (*.wav)")[0]

            #load .wav data
            if path:
                if path.endswith('.wav'):
                    data, samplerate = sf.read(path)
                    #create signa object and plot
                    self.create_signal(path,data)
                
                elif path.endswith('.edf'):
                    data = mne.io.read_raw_edf(path)
                    data = data.get_data()
                    #create signa object and plot
                    self.create_signal(path,100000*data[0])

                    
    #open for signals .csv
    def open_csv(self):
        if len(self.signals) < 3:
            print("open_csv")
            path = PyQt5.QtWidgets.QFileDialog.getOpenFileName(None, 'Open', None, "CSV (*.csv)")[0]
            if path:
                df=pd.read_csv(path,usecols=[0,1])
                data=np.array(df.iloc[:,1])
                #create signa object and plot
                self.create_signal(path,data)
                
                
    #create Signal object and plot signal
    def create_signal(self,path,data):
        self.signals[path]=Signal(path,data)
        self.signals[path].plot_signal()
        #to send signal when clicked
        # self.signals[path].waveform.scene().sigMouseClicked.connect(self.detect_click)
 
    #emit path of the last clicked on signal  
    def detect_click(self,file_path):
        self.selected_signal=file_path
        #self.signal.emit(file_path)
        #print(file_path)

    # Zoom 
    def zoom_in(self):
        center_x=(self.signals[self.selected_signal].waveform.getAxis("bottom").range[0]+self.signals[self.selected_signal].waveform.getAxis("bottom").range[1])/2
        center_y=0
        self.signals[self.selected_signal].waveform.getViewBox().scaleBy(y=0.9 ,x=0.9,center=(center_x,center_y))
        # self.signals[self.selected_signal].waveform.getViewBox().scaleBy(x=0.1)

    def zoom_out(self,file_path):
        center_x=(self.signals[self.selected_signal].waveform.getAxis("bottom").range[0]+self.signals[self.selected_signal].waveform.getAxis("bottom").range[1])/2
        center_y=0
        self.signals[self.selected_signal].waveform.getViewBox().scaleBy(y=(1/0.9), x=(1/0.9),center=(center_x,center_y))
        # self.signals[self.selected_signal].waveform.getViewBox().scaleBy(x=(1/0.1))

    ##play function and play as fast as possible
    def play_signal(self,step):
        self.pause=0
        self.played=1
        #save signal path 
        sig_path=self.selected_signal
        sig_length = len(self.signals[self.selected_signal].data)
        #print(sig_length)
        starting_x=self.signals[self.selected_signal].waveform.getAxis("bottom").range
        x_end=starting_x[1]
        #check if signal reached the end
        if starting_x [1] < sig_length:
            i=1
            #play signal 
            while x_end < sig_length:
                #break if another signal is selected
                if sig_path != self.selected_signal:
                    break
                #break if pause is pressed
                if self.pause == 1:
                    break
                self.signals[self.selected_signal].waveform.setXRange(starting_x [0] + step*i , starting_x[1] + step*i)
                QtWidgets.QApplication.processEvents()
                #x_end= x_end + step
                x_end = self.signals[self.selected_signal].waveform.getAxis("bottom").range[1]
                i+=1
            #print(x_end)
            #print(i)

    def play_fast(self):
        self.pause_signal()
        self.play_signal(40)
    
    #pause function
    def pause_signal(self):
            self.pause=1
            self.played=0
        

    #to signal beginning
    def signal_beginning(self):
        self.pause_signal()
        #get original xrange
        x_range=self.signals[self.selected_signal].x_range
        self.signals[self.selected_signal].waveform.setXRange(x_range[0] , x_range[1], padding=0.005)
    

    #to signal end
    def signal_end(self):
        self.pause_signal()
        #set xrange to be  
        x_end=len(self.signals[self.selected_signal].data)
        self.signals[self.selected_signal].waveform.setXRange(x_end-2000 , x_end, padding=0.005)
   

    #delete closed signal
    def signal_closed(self,file_path):
        #print(len(self.signals))
        del self.signals[file_path]
        #print(len(self.signals))
    
        #save signal plots
    def save(self):
        for sig in self.signals:
            #signal im save
            plot_data=self.signals[sig].waveform
            QtGui.QApplication.processEvents()
            exporter = pg.exporters.ImageExporter(plot_data)
            exporter.parameters()['width'] = 500
            name=sig.split("/")[-1]
            exporter.export(name+".png")
            fig = plt.figure()
            plt.subplot(212)
            data=self.signals[sig].data
            plt.specgram(data, Fs=1000)
            plt.xlabel('Time(sec)')
            plt.ylabel('Frequency(Hz)')
            fig.savefig(name+"s"+".png")
            plt.close(fig)
 
        

    def genPinTable(self):
        pinElemTable = None
        pinElemWidth = 500
        pinElemHeight = 1000

        # (1) Building Table Structure
        titles=[]
        for pin in self.pins:
            #titles.append(self.pins[pin].title)
            mini_titleTable=Table([
                self.pins[pin].title
            ], pinElemWidth)
            titles.append(mini_titleTable)
        
        # titleTable=Table([
        #        titles
        #     ], pinElemWidth)

        S_pictures=[]
        G_pictures=[]
        
        for pin in self.pins:
            S_picture=Image(self.pins[pin].SignalPath[0])
            S_picture.drawWidth=200
            S_picture.drawHeight = 100
            S_pictures.append(S_picture)
        
            G_picture = Image(self.pins[pin].GramPath[0])
            G_picture.drawWidth = 200
            G_picture.drawHeight = 100
            G_pictures.append(G_picture)

        print(S_pictures) 
        mini_tables = []
        for i in range(3): 
            titleTable=Table([
                [titles[i]]
            ], pinElemWidth)
            
            picSignal=Table([
                [S_pictures[i]]
                ], 250, 125)

            picGram = Table([ 
                [G_pictures[i]]
                ], 250, 125)
        
            PicTable = Table([
                [picSignal, picGram]
            ], [250,250])

            pinElemTable = Table([
                [titleTable],
                [PicTable]
            ],pinElemWidth)

            # (2) Adding Style
        
        
            titleTableStyle = TableStyle([
                ('ALIGN',(0,0),(-1,-1),'CENTER'),
                ('FONTSIZE', (0,0), (-1,-1), 14),
                ('FONTNAME', (0,0), (-1,-1),'Helvetica-Oblique'), 
                ('TOPPADDING',(0,0),(-1,-1), 0),
                ('BOTTOMPADDING',(0,0),(-1,-1), 0), 
            ])
            titleTable.setStyle(titleTableStyle)

            picTableStyle = TableStyle([
                ('LEFTPADDING',(0,0),(-1,-1), 15),

                ('TOPPADDING',(0,0),(-1,-1), 0),
            ])
            picSignal.setStyle(picTableStyle)
            picGram.setStyle(picTableStyle)
            
            pinElemTableStyle = TableStyle([
                ('BOX',(0,0),(-1,-1),3,colors.pink),
                ('TOPPADDING',(0,0),(-1,-1), 0),
                ('BOTTOMPADDING',(0,0),(-1,-1), 0),
            ])
            pinElemTable.setStyle(pinElemTableStyle)

            mini_tables.append(pinElemTable)

        # (2) Adding Style
        
        # to get all available fonts
        '''
        from reportlab.pdfgen import canvas
        for font in canvas.Canvas('abc').getAvailableFonts(): 
            print(font)
        '''                
        # titleTableStyle = TableStyle([
        #     ('ALIGN',(0,0),(-1,-1),'CENTER'),
        #     ('FONTSIZE', (0,0), (-1,-1), 14),
        #     ('FONTNAME', (0,0), (-1,-1), 
        #         'Helvetica-Oblique'
        #         ), 

        #     ('TOPPADDING',(0,0),(-1,-1), 0),
        #     ('BOTTOMPADDING',(0,0),(-1,-1), 0), 
        # ])
        # titleTable.setStyle(titleTableStyle)

        # picTableStyle = TableStyle([
        #     ('LEFTPADDING',(0,0),(-1,-1), 15),

        #     ('TOPPADDING',(0,0),(-1,-1), 0),
        # ])
        # picSignal.setStyle(picTableStyle)
        # picGram.setStyle(picTableStyle)
        
        # pinElemTableStyle = TableStyle([
        #     ('BOX',(0,0),(-1,-1),3,colors.pink),
        #     ('TOPPADDING',(0,0),(-1,-1), 0),
        #     ('BOTTOMPADDING',(0,0),(-1,-1), 0),
        # ])
        # pinElemTable.setStyle(pinElemTableStyle)

        #return pinElemTable
        return mini_tables
        

    def E_pdf(self):
        self.save()
        for i  in self.signals:
            self.pins[i]=Pin()
            self.pins[i].getPins(i)
    
        self.fileName = 'pdfTable.pdf'
        self.pdf = SimpleDocTemplate(self.fileName,pagesize=letter)

        self.elems = []
        ta=self.genPinTable()
        for i in range(3):
            self.elems.append(ta[i])

        self.pdf.build(self.elems)
        print("Report is done")

    def spectro_draw(self):
        plt.subplot(212)
        plt.specgram(self.signals[self.selected_signal].data, Fs=1000)
        plt.xlabel('Time(sec)')
        plt.ylabel('Frequency(Hz)')
        plt.show()
        

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
