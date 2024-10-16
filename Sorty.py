from Sortdata import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
import pandas as pd
import time 
import Resources.resources_Rc
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import  QUrl
from PyQt5.QtWidgets import QMessageBox , QApplication
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem

import sys

class SortWorker(QThread):
    finished = pyqtSignal(pd.DataFrame, float)
    error = pyqtSignal(str)

    def __init__(self, data, column, algorithm):
        super().__init__()
        self.data = data
        self.column = column
        self.algorithm = algorithm

    def run(self):
        try:
            start_time = time.time()
            datacopy = self.data.copy()
            datacopy = ApplySorting(datacopy, self.column, self.algorithm)
            end_time = time.time()
            elapsed_time = end_time - start_time
            self.finished.emit(datacopy, elapsed_time)
        except Exception as e:
            self.error.emit(str(e))


class MultiColumnSortWorker(QThread):
    finished = pyqtSignal(pd.DataFrame, float)

    def __init__(self, file_path, sort_column, then_column, algorithm):
        super(MultiColumnSortWorker, self).__init__()
        self.file_path = file_path
        self.sort_column = sort_column
        self.then_column = then_column
        self.algorithm = algorithm

    def run(self):
        try:
            df = pd.read_csv(self.file_path)
            start_time = time.time()

            grouped_data = self.group_by_column(df, self.sort_column)

            sorted_groups = []

            for group_name, current_data in grouped_data.items():
                sorted_data = ApplySorting(current_data, self.then_column, self.algorithm)
                sorted_groups.append(sorted_data)

            final_data = pd.concat(sorted_groups, ignore_index=False)
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            self.finished.emit(final_data, elapsed_time)
        except Exception as e:
            print(f"An error occurred during sorting: {str(e)}")

    def group_by_column(self, df, column):
        grouped_data = {name: group.copy() for name, group in df.groupby(column)}
        return grouped_data






class SearchThread(QThread):
    sorted_data_signal = pyqtSignal(pd.DataFrame,str)
    sorted_data_signal2 = pyqtSignal(pd.DataFrame,pd.DataFrame,str,str,str)

    def __init__(self, file_path, startcolumn,startText,start_indexFunction,startBool,lastColumn=None,LastText=None,lastIndexFunction=None,lastBool=None,baseCon=None):
        super().__init__()
        self.file_path = file_path
        self.startColumn = startcolumn
        self.start_indexFunction = start_indexFunction
        self.startText = startText
        
        self.LastText = LastText
        self.LastColumn = lastColumn
        self.LastFunction = lastIndexFunction
        self.StartBool = startBool
        self.LastBool = lastBool
        
        self.BaseCon = baseCon
    def run(self):
        try:
            if(self.LastFunction is not None):
                df = pd.read_csv(self.file_path)
                sorted_df = self.start_indexFunction(df, self.startColumn, self.startText)
                sorted_df2 = self.LastFunction(df,self.LastColumn,self.LastText)
                self.sorted_data_signal2.emit(sorted_df,sorted_df2,self.StartBool,self.LastBool,self.BaseCon)
            else:
                df = pd.read_csv(self.file_path)
                sorted_df = self.start_indexFunction(df, self.startColumn, self.startText)
                self.sorted_data_signal.emit(sorted_df,self.StartBool)
            
        except Exception as e:
            print(f"Error reading CSV: {e}")
            self.sorted_data_signal.emit(pd.DataFrame(),"")  # Emit an empty DataFrame on error
            

class Ui_SecondWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1207, 817)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(250, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setMinimumSize(QtCore.QSize(250, 0))
        self.frame_3.setStyleSheet("background-color: rgb(17, 168, 182);\n"
                "border: 3px solid black;\n"
                "")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.mainPicture = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.mainPicture.sizePolicy().hasHeightForWidth())
        self.mainPicture.setSizePolicy(sizePolicy)
        self.mainPicture.setStyleSheet("border:2px solid black;\n"
                "border-radius:10px;\n"
                "QPushButton{\n"
                "border-radius:20px;\n"
                "background-color:white;\n"
                "}\n"
                "\n"
                "QPushButton:hover {\n"
                "    background-color: green;\n"
                "    color:white;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    background-color:red;\n"
                "    color:green;\n"
                "}")
        self.mainPicture.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Icons/admin-panel.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mainPicture.setIcon(icon)
        self.mainPicture.setIconSize(QtCore.QSize(100, 100))
        self.mainPicture.setCheckable(False)
        self.mainPicture.setObjectName("mainPicture")
        self.verticalLayout.addWidget(self.mainPicture)
        spacerItem = QtWidgets.QSpacerItem(20, 120, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrapButton = QtWidgets.QPushButton(self.frame_3)


        self.scrapButton.clicked.connect(self.OnClickscrap)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.scrapButton.sizePolicy().hasHeightForWidth())
        self.scrapButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.scrapButton.setFont(font)
        self.scrapButton.setStyleSheet("\n"
                "QPushButton{\n"
                "border:2px solid black;\n"
                "border-radius:15px;\n"
                "}\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(0, 255, 255);\n"
                "    color:black;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    \n"
                "    background-color: rgb(224, 176, 255);\n"
                "    color:black;\n"
                "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Icons/whiteIcons/trello.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.scrapButton.setIcon(icon1)
        self.scrapButton.setIconSize(QtCore.QSize(40, 40))
        self.scrapButton.setObjectName("scrapButton")
        self.verticalLayout.addWidget(self.scrapButton)
        
        
        self.scrapButton.clicked.connect(lambda: self.open_scrap_window(MainWindow))
        
        spacerItem1 = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.sortButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.sortButton.sizePolicy().hasHeightForWidth())
        self.sortButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.sortButton.setFont(font)
        self.sortButton.setStyleSheet("\n"
                "QPushButton{\n"
                "border:2px solid black;\n"
                "border-radius:15px;\n"
                "}\n"
                "\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(0, 255, 255);\n"
                "    color:black;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    \n"
                "    background-color: rgb(224, 176, 255);\n"
                "    color:black;\n"
                "}")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Icons/whiteIcons/sliders.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sortButton.setIcon(icon2)
        self.sortButton.setIconSize(QtCore.QSize(40, 40))
        self.sortButton.setObjectName("sortButton")
        self.verticalLayout.addWidget(self.sortButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 150, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.exitButton = QtWidgets.QPushButton(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.exitButton.sizePolicy().hasHeightForWidth())
        self.exitButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.exitButton.setFont(font)
        self.exitButton.setStyleSheet("\n"
                "QPushButton{\n"
                "border:2px solid black;\n"
                "border-radius:15px;\n"
                "}\n"
                "\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(0, 255, 255);\n"
                "    color:black;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    \n"
                "    background-color: rgb(224, 176, 255);\n"
                "    color:black;\n"
                "}")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Icons/whiteIcons/x-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exitButton.setIcon(icon3)
        self.exitButton.setIconSize(QtCore.QSize(40, 40))
        self.exitButton.setObjectName("exitButton")
        self.verticalLayout.addWidget(self.exitButton)
        
        self.exitButton.clicked.connect(self.exit)
        
        self.horizontalLayout_3.addWidget(self.frame_3)
        self.horizontalLayout_2.addWidget(self.frame)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setSizeIncrement(QtCore.QSize(850, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.sidebarFrame = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebarFrame.sizePolicy().hasHeightForWidth())
        self.sidebarFrame.setSizePolicy(sizePolicy)
        self.sidebarFrame.setMinimumSize(QtCore.QSize(800, 0))
        self.sidebarFrame.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.sidebarFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sidebarFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sidebarFrame.setLineWidth(1)
        self.sidebarFrame.setObjectName("sidebarFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.sidebarFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.sidebarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.frame_4.setFont(font)
        self.frame_4.setStyleSheet("background-color: rgb(0, 135, 203);\n"
                "background-color: rgb(17, 168, 182);")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_4)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.SortLabel = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.SortLabel.setFont(font)
        self.SortLabel.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.SortLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.SortLabel.setLineWidth(5)
        self.SortLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SortLabel.setObjectName("SortLabel")
        self.verticalLayout_3.addWidget(self.SortLabel)
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.sidebarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.frame_6 = QtWidgets.QFrame(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setStyleSheet("background-color: rgb(17, 168, 182);\n"
                "border:1px solid black;")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame_8 = QtWidgets.QFrame(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setStyleSheet("border:none;")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.sortingButton = QtWidgets.QPushButton(self.frame_8)
        self.sortingButton.setGeometry(QtCore.QRect(10, 220, 161, 41))
        
        
        
        
        self.sortingButton.clicked.connect(self.OnClicksorting)
        
        
        
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.sortingButton.sizePolicy().hasHeightForWidth())
        self.sortingButton.setSizePolicy(sizePolicy)

        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sortingButton.setFont(font)
        self.sortingButton.setStyleSheet("\n"
                "QPushButton{\n"
                "background-color: rgb(255, 255, 255);\n"
                "border:2px solid black;\n"
                "border-radius:15px;\n"
                "}\n"
                "\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(0, 255, 255);\n"
                "    color:black;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    \n"
                "    background-color: rgb(224, 176, 255);\n"
                "    color:black;\n"
                "}")
        self.sortingButton.setIcon(icon2)
        self.sortingButton.setIconSize(QtCore.QSize(25, 25))
        self.sortingButton.setCheckable(False)
        self.sortingButton.setChecked(False)
        self.sortingButton.setObjectName("sortingButton")
        self.thenbycomboBox = QtWidgets.QComboBox(self.frame_8)
        self.thenbycomboBox.setGeometry(QtCore.QRect(180, 170, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.thenbycomboBox.setFont(font)
        self.thenbycomboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "color:rgb(0, 0, 0);\n"
                "border:1px solid black;")
        self.thenbycomboBox.setIconSize(QtCore.QSize(16, 16))
        self.thenbycomboBox.setDuplicatesEnabled(False)
        self.thenbycomboBox.setObjectName("thenbycomboBox")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenbycomboBox.addItem("")
        self.thenByLabel = QtWidgets.QLabel(self.frame_8)
        self.thenByLabel.setGeometry(QtCore.QRect(10, 170, 131, 31))

        # self.sortingButton.clicked.connect(self.onMultiSortButtonClicked)

        self.thenByLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;\n"
                "border:1px solid black;")
        self.thenByLabel.setObjectName("thenByLabel")
        self.sortByLabel = QtWidgets.QLabel(self.frame_8)
        self.sortByLabel.setGeometry(QtCore.QRect(10, 120, 131, 31))
        self.sortByLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;\n"
                "border:1px solid black;")
        self.sortByLabel.setObjectName("sortByLabel")
        self.sortbycomboBox = QtWidgets.QComboBox(self.frame_8)
        self.sortbycomboBox.setGeometry(QtCore.QRect(180, 120, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.sortbycomboBox.setFont(font)
        self.sortbycomboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "color:rgb(0, 0, 0);\n"
                "border:1px solid black;")
        self.sortbycomboBox.setEditable(False)
        self.sortbycomboBox.setObjectName("sortbycomboBox")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.sortbycomboBox.addItem("")
        self.algorithmcomboBox = QtWidgets.QComboBox(self.frame_8)
        self.algorithmcomboBox.setGeometry(QtCore.QRect(180, 70, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.algorithmcomboBox.setFont(font)
        self.algorithmcomboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "color:rgb(0, 0, 0);\n"
                "border:1px solid black;")
        self.algorithmcomboBox.setObjectName("algorithmcomboBox")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmcomboBox.addItem("")
        self.algorithmLabel = QtWidgets.QLabel(self.frame_8)
        self.algorithmLabel.setGeometry(QtCore.QRect(10, 70, 131, 31))
        self.algorithmLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;\n"
                "border:1px solid black;")
        self.algorithmLabel.setObjectName("algorithmLabel")
        self.sortTimeLabel = QtWidgets.QLabel(self.frame_8)
        self.sortTimeLabel.setGeometry(QtCore.QRect(10, 20, 131, 31))
        self.sortTimeLabel.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;\n"
                "border:1px solid black;")
        self.sortTimeLabel.setObjectName("sortTimeLabel")
        self.sortingtimeShow = QtWidgets.QLabel(self.frame_8)
        self.sortingtimeShow.setGeometry(QtCore.QRect(180, 20, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.sortingtimeShow.setFont(font)
        self.sortingtimeShow.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border:1px solid black;\n"
                "color:rgb(0, 0, 0);")
        self.sortingtimeShow.setObjectName("sortingtimeShow")
        self.sortingButton_2 = QtWidgets.QPushButton(self.frame_8)
        self.sortingButton_2.setGeometry(QtCore.QRect(180, 220, 141, 41))
        
        
        
        
        
        self.sortingButton_2.clicked.connect(self.OnClicksortingBtn)





        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.sortingButton_2.sizePolicy().hasHeightForWidth())
        self.sortingButton_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sortingButton_2.setFont(font)
        self.sortingButton_2.setStyleSheet("\n"
                "QPushButton{\n"
                "background-color: rgb(255, 255, 255);\n"
                "border:2px solid black;\n"
                "border-radius:15px;\n"
                "}\n"
                "\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(0, 255, 255);\n"
                "    color:black;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    \n"
                "    background-color: rgb(224, 176, 255);\n"
                "    color:black;\n"
                "}")
        self.sortingButton_2.setIconSize(QtCore.QSize(25, 25))
        self.sortingButton_2.setCheckable(False)
        self.sortingButton_2.setChecked(False)
        self.sortingButton_2.setObjectName("sortingButton_2")
        self.sortingButton_3 = QtWidgets.QPushButton(self.frame_8)
        self.sortingButton_3.setGeometry(QtCore.QRect(330, 220, 141, 41))


        self.sortingButton_3.clicked.connect(self.OnClicksortingBtn2)


        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.sortingButton_3.sizePolicy().hasHeightForWidth())
        self.sortingButton_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.sortingButton_3.setFont(font)
        self.sortingButton_3.setStyleSheet("\n"
                "QPushButton{\n"
                "background-color: rgb(255, 255, 255);\n"
                "border:2px solid black;\n"
                "border-radius:15px;\n"
                "}\n"
                "\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(0, 255, 255);\n"
                "    color:black;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    \n"
                "    background-color: rgb(224, 176, 255);\n"
                "    color:black;\n"
                "}")
        self.sortingButton_3.setIconSize(QtCore.QSize(25, 25))
        self.sortingButton_3.setCheckable(False)
        self.sortingButton_3.setChecked(False)
        self.sortingButton_3.setObjectName("sortingButton_3")
        self.horizontalLayout_8.addWidget(self.frame_8)
        self.frame_10 = QtWidgets.QFrame(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.frame_10.sizePolicy().hasHeightForWidth())
        self.frame_10.setSizePolicy(sizePolicy)
        self.frame_10.setMinimumSize(QtCore.QSize(470, 0))
        self.frame_10.setStyleSheet("border:none;")
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.searchButton = QtWidgets.QPushButton(self.frame_10)
        self.searchButton.setGeometry(QtCore.QRect(160, 230, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.searchButton.setFont(font)
        self.searchButton.setStyleSheet("\n"
                "QPushButton{\n"
                "background-color: rgb(255, 255, 255);\n"
                "border:2px solid black;\n"
                "border-radius:15px;\n"
                "}\n"
                "\n"
                "QPushButton:hover {\n"
                "    background-color: rgb(0, 255, 255);\n"
                "    color:black;\n"
                "}\n"
                "QPushButton:pressed{\n"
                "    \n"
                "    background-color: rgb(224, 176, 255);\n"
                "    color:black;\n"
                "}")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/whiteIcons/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.searchButton.setIcon(icon4)
        self.searchButton.setIconSize(QtCore.QSize(30, 30))
        self.searchButton.setObjectName("searchButton")
        
        #Search button
        self.searchButton.clicked.connect(self.SearchTableClick)
        #
        
        
        self.Column2Sort = QtWidgets.QComboBox(self.frame_10)
        self.Column2Sort.setGeometry(QtCore.QRect(250, 190, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.Column2Sort.setFont(font)
        self.Column2Sort.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "color:rgb(0, 0, 0);border:1px solid black;")
        self.Column2Sort.setObjectName("Column2Sort")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.Column2Sort.addItem("")
        self.column2Label = QtWidgets.QLabel(self.frame_10)
        self.column2Label.setGeometry(QtCore.QRect(90, 190, 141, 31))
        self.column2Label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;border:1px solid black;")
        self.column2Label.setObjectName("column2Label")
        self.column1Label = QtWidgets.QLabel(self.frame_10)
        self.column1Label.setGeometry(QtCore.QRect(90, 150, 141, 31))
        self.column1Label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;border:1px solid black;")
        self.column1Label.setObjectName("column1Label")
        self.Column1Sort = QtWidgets.QComboBox(self.frame_10)
        self.Column1Sort.setGeometry(QtCore.QRect(250, 150, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.Column1Sort.setFont(font)
        self.Column1Sort.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "color:rgb(0, 0, 0);border:1px solid black;")
        self.Column1Sort.setObjectName("Column1Sort")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Column1Sort.addItem("")
        self.Search2Line = QtWidgets.QLineEdit(self.frame_10)
        self.Search2Line.setGeometry(QtCore.QRect(250, 100, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Search2Line.setFont(font)
        self.Search2Line.setStyleSheet("background-color: rgb(255, 255, 255);border:1px solid black;")
        self.Search2Line.setObjectName("Search2Line")
        self.Search2Label = QtWidgets.QLabel(self.frame_10)
        self.Search2Label.setGeometry(QtCore.QRect(90, 100, 141, 31))
        self.Search2Label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;border:1px solid black;")
        self.Search2Label.setObjectName("Search2Label")
        self.AND_OR = QtWidgets.QComboBox(self.frame_10)
        self.AND_OR.setGeometry(QtCore.QRect(190, 50, 111, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.AND_OR.setFont(font)
        self.AND_OR.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;border:1px solid black;")
        self.AND_OR.setObjectName("AND_OR")
        self.AND_OR.addItem("")
        self.AND_OR.addItem("")
        self.AND_OR.addItem("")
        self.AND_OR.addItem("")
        self.AND_OR.setItemText(3, "")
        self.Search1Line = QtWidgets.QLineEdit(self.frame_10)
        self.Search1Line.setGeometry(QtCore.QRect(250, 10, 181, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Search1Line.setFont(font)
        self.Search1Line.setStyleSheet("background-color: rgb(255, 255, 255);border:1px solid black;")
        self.Search1Line.setObjectName("Search1Line")
        self.Search1Label = QtWidgets.QLabel(self.frame_10)
        self.Search1Label.setGeometry(QtCore.QRect(90, 10, 141, 31))
        self.Search1Label.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;border:1px solid black;")
        self.Search1Label.setObjectName("Search1Label")
        self.Column1comboBox = QtWidgets.QComboBox(self.frame_10)
        self.Column1comboBox.setGeometry(QtCore.QRect(10, 10, 69, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Column1comboBox.setFont(font)
        self.Column1comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;border:1px solid black;")
        self.Column1comboBox.setObjectName("Column1comboBox")
        self.Column1comboBox.addItem("")
        self.Column1comboBox.addItem("")
        self.Column1comboBox.addItem("")
        self.Column1comboBox.setItemText(2, "")
        self.Column2comboBox = QtWidgets.QComboBox(self.frame_10)
        self.Column2comboBox.setGeometry(QtCore.QRect(10, 100, 69, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.Column2comboBox.setFont(font)
        self.Column2comboBox.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                "border-radius:1px;border:1px solid black;")
        self.Column2comboBox.setObjectName("Column2comboBox")
        self.Column2comboBox.addItem("")
        self.Column2comboBox.addItem("")
        self.Column2comboBox.addItem("")
        self.Column2comboBox.setItemText(2, "")
        self.horizontalLayout_8.addWidget(self.frame_10)
        self.frame_10.raise_()
        self.frame_8.raise_()
        self.verticalLayout_4.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(7)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 11))
        self.frame_7.setStyleSheet("")
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_7)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_9 = QtWidgets.QFrame(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setStyleSheet("background-color: rgb(17, 168, 182);\n"
                "border: 1px solid black;")
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(290, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.frame_11 = QtWidgets.QFrame(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.dataLabel = QtWidgets.QLabel(self.frame_11)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.dataLabel.setFont(font)
        self.dataLabel.setStyleSheet("border: none")
        self.dataLabel.setObjectName("dataLabel")
        self.horizontalLayout_5.addWidget(self.dataLabel)
        self.horizontalLayout_4.addWidget(self.frame_11)
        spacerItem4 = QtWidgets.QSpacerItem(240, 15, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem4)
        self.verticalLayout_6.addWidget(self.frame_9)
        self.dataGridFrame = QtWidgets.QFrame(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(60)
        sizePolicy.setHeightForWidth(self.dataGridFrame.sizePolicy().hasHeightForWidth())
        self.dataGridFrame.setSizePolicy(sizePolicy)
        self.dataGridFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dataGridFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dataGridFrame.setObjectName("dataGridFrame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.dataGridFrame)
        self.horizontalLayout_6.setContentsMargins(0, 5, 0, 2)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tableDataCollector = QtWidgets.QTableWidget(self.dataGridFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.tableDataCollector.sizePolicy().hasHeightForWidth())
        self.tableDataCollector.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.tableDataCollector.setFont(font)
        self.tableDataCollector.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tableDataCollector.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableDataCollector.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.tableDataCollector.setObjectName("tableDataCollector")
        self.tableDataCollector.setColumnCount(9)
        self.tableDataCollector.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        item.setFont(font)
        self.tableDataCollector.setHorizontalHeaderItem(8, item)
        self.tableDataCollector.horizontalHeader().setDefaultSectionSize(100)
        self.tableDataCollector.horizontalHeader().setMinimumSectionSize(130)
        self.tableDataCollector.horizontalHeader().setSortIndicatorShown(True)
        self.tableDataCollector.horizontalHeader().setStretchLastSection(True)
        self.tableDataCollector.verticalHeader().setVisible(False)
        self.tableDataCollector.verticalHeader().setDefaultSectionSize(30)
        self.tableDataCollector.verticalHeader().setSortIndicatorShown(False)
        self.horizontalLayout_6.addWidget(self.tableDataCollector)
        self.verticalLayout_6.addWidget(self.dataGridFrame)
        self.verticalLayout_4.addWidget(self.frame_7)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout_7.addWidget(self.sidebarFrame)
        self.horizontalLayout_2.addWidget(self.frame_2)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.thenbycomboBox.setCurrentIndex(0)
        self.sortbycomboBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Create an instance of DataLoader
        self.data_loader = DataLoader(self.tableDataCollector)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.scrapButton.setText(_translate("MainWindow", "Scrap"))
        self.sortButton.setText(_translate("MainWindow", "Sort"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.SortLabel.setText(_translate("MainWindow", "<html><head/><body><p><img src=\":/Icons/whiteIcons/sliders.svg\"/><span style=\" font-size:36pt;\"> Sorting</span></p></body></html>"))
        self.sortingButton.setText(_translate("MainWindow", "Sort"))
        self.thenbycomboBox.setItemText(0, _translate("MainWindow", "None"))
        self.thenbycomboBox.setItemText(1, _translate("MainWindow", "Title"))
        self.thenbycomboBox.setItemText(2, _translate("MainWindow", "Model"))
        self.thenbycomboBox.setItemText(3, _translate("MainWindow", "Price"))
        self.thenbycomboBox.setItemText(4, _translate("MainWindow", "Mileage"))
        self.thenbycomboBox.setItemText(5, _translate("MainWindow", "Fuel Type"))
        self.thenbycomboBox.setItemText(6, _translate("MainWindow", "Engine"))
        self.thenbycomboBox.setItemText(7, _translate("MainWindow", "Transmission"))
        self.thenbycomboBox.setItemText(8, _translate("MainWindow", "City"))
        self.thenByLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/codepen.svg\"/><span style=\" font-size:16pt;\"> Then By:</span></p></body></html>"))
        self.sortByLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/chrome.svg\"/><span style=\" font-size:16pt;\"> Sort By:</span></p></body></html>"))
        self.sortbycomboBox.setItemText(0, _translate("MainWindow", "None"))
        self.sortbycomboBox.setItemText(1, _translate("MainWindow", "Title"))
        self.sortbycomboBox.setItemText(2, _translate("MainWindow", "Model"))
        self.sortbycomboBox.setItemText(3, _translate("MainWindow", "Price"))
        self.sortbycomboBox.setItemText(4, _translate("MainWindow", "Mileage"))
        self.sortbycomboBox.setItemText(5, _translate("MainWindow", "Fuel Type"))
        self.sortbycomboBox.setItemText(6, _translate("MainWindow", "Engine"))
        self.sortbycomboBox.setItemText(7, _translate("MainWindow", "Transmission"))
        self.sortbycomboBox.setItemText(8, _translate("MainWindow", "City"))
        self.algorithmcomboBox.setItemText(0, _translate("MainWindow", "None"))
        self.algorithmcomboBox.setItemText(1, _translate("MainWindow", "Bubble Sort"))
        self.algorithmcomboBox.setItemText(2, _translate("MainWindow", "Selection Sort"))
        self.algorithmcomboBox.setItemText(3, _translate("MainWindow", "Insertion Sort"))
        self.algorithmcomboBox.setItemText(4, _translate("MainWindow", "Merge Sort"))
        self.algorithmcomboBox.setItemText(5, _translate("MainWindow", "Hybrid Merge Sort"))
        self.algorithmcomboBox.setItemText(6, _translate("MainWindow", "Quick Sort"))
        self.algorithmcomboBox.setItemText(7, _translate("MainWindow", "Shell Sort"))
        self.algorithmcomboBox.setItemText(8, _translate("MainWindow", "Heap Sort"))
        self.algorithmcomboBox.setItemText(9, _translate("MainWindow", "Counting Sort"))
        self.algorithmcomboBox.setItemText(10, _translate("MainWindow", "Radix Sort"))
        self.algorithmcomboBox.setItemText(11, _translate("MainWindow", "Bucket Sort"))
        self.algorithmcomboBox.setItemText(12, _translate("MainWindow", "Pigeonhole Sort"))
        self.algorithmLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/bar-chart-2.svg\"/><span style=\" font-size:16pt;\"> Algorithm</span></p></body></html>"))
        self.sortTimeLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/target.svg\"/><span style=\" font-size:16pt;\">Sort Time</span></p></body></html>"))
        self.sortingtimeShow.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><br/></p></body></html>"))
        self.sortingButton_2.setText(_translate("MainWindow", "Load Data"))
        self.sortingButton_3.setText(_translate("MainWindow", "Clear Data"))
        self.searchButton.setText(_translate("MainWindow", "Search"))
        self.Column2Sort.setItemText(0, _translate("MainWindow", "None"))
        self.Column2Sort.setItemText(1, _translate("MainWindow", "Index"))
        self.Column2Sort.setItemText(2, _translate("MainWindow", "Title"))
        self.Column2Sort.setItemText(3, _translate("MainWindow", "Model"))
        self.Column2Sort.setItemText(4, _translate("MainWindow", "Price"))
        self.Column2Sort.setItemText(5, _translate("MainWindow", "Mileage"))
        self.Column2Sort.setItemText(6, _translate("MainWindow", "Fuel Type"))
        self.Column2Sort.setItemText(7, _translate("MainWindow", "Engine"))
        self.Column2Sort.setItemText(8, _translate("MainWindow", "Transmission"))
        self.Column2Sort.setItemText(9, _translate("MainWindow", "City"))
        self.column2Label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Column 2</span></p></body></html>"))
        self.column1Label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Column 1</span></p></body></html>"))
        self.Column1Sort.setItemText(0, _translate("MainWindow", "None"))
        self.Column1Sort.setItemText(1, _translate("MainWindow", "Index"))
        self.Column1Sort.setItemText(2, _translate("MainWindow", "Title"))
        self.Column1Sort.setItemText(3, _translate("MainWindow", "Model"))
        self.Column1Sort.setItemText(4, _translate("MainWindow", "Price"))
        self.Column1Sort.setItemText(5, _translate("MainWindow", "Mileage"))
        self.Column1Sort.setItemText(6, _translate("MainWindow", "Fuel Type"))
        self.Column1Sort.setItemText(7, _translate("MainWindow", "Engine"))
        self.Column1Sort.setItemText(8, _translate("MainWindow", "Transmission"))
        self.Column1Sort.setItemText(9, _translate("MainWindow", "City"))
        self.Search2Line.setPlaceholderText(_translate("MainWindow", "Ends with"))
        self.Search2Label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Search</span></p></body></html>"))
        self.AND_OR.setItemText(0, _translate("MainWindow", "None"))
        self.AND_OR.setItemText(1, _translate("MainWindow", "AND &&"))
        self.AND_OR.setItemText(2, _translate("MainWindow", "OR | |"))
        self.Search1Line.setPlaceholderText(_translate("MainWindow", "Start with"))
        self.Search1Label.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:16pt;\">Search</span></p></body></html>"))
        self.Column1comboBox.setItemText(0, _translate("MainWindow", "NONE X"))
        self.Column1comboBox.setItemText(1, _translate("MainWindow", "NOT !"))
        self.Column2comboBox.setItemText(0, _translate("MainWindow", "NONE X"))
        self.Column2comboBox.setItemText(1, _translate("MainWindow", "NOT !"))
        self.dataLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/bar-chart.svg\"/><span style=\" font-size:18pt;\">Sorted Data</span></p></body></html>"))
        item = self.tableDataCollector.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Index"))
        item = self.tableDataCollector.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Title"))
        item = self.tableDataCollector.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Model"))
        item = self.tableDataCollector.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Price"))
        item = self.tableDataCollector.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Mileage"))
        item = self.tableDataCollector.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Fuel Type"))
        item = self.tableDataCollector.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Engine"))
        item = self.tableDataCollector.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Transmission"))
        item = self.tableDataCollector.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "City"))
    
    
    def OnClickscrap(self):
        QDesktopServices.openUrl(QUrl.fromLocalFile('MiniProject.py'))
    
    def OnClicksortingBtn(self):
        self.data_loader.load_data()

    def OnClicksortingBtn2(self):
        self.tableDataCollector.clearContents()
        self.tableDataCollector.setRowCount(0)

    def OnClicksorting(self):
        
        algorithm = self.algorithmcomboBox.currentText()
        sort_column = self.sortbycomboBox.currentText()
        then_column = self.thenbycomboBox.currentText()
        data = pd.read_csv('data.csv')

        if (algorithm == "None"):
            QMessageBox.warning(None, "Warning", "Select an algorithm")
            return
        if(sort_column == "None" or (then_column != "None" and sort_column=="None")):
            QMessageBox.warning(None, "Warning", "Select firstColumn")
            return
        if (then_column != "None" and sort_column != "None"):
            self.worker = MultiColumnSortWorker('data.csv', sort_column, then_column, algorithm)
            self.worker.finished.connect(self.on_sort_finished)
            self.worker.start()
        else:
            self.worker = SortWorker(data, sort_column, algorithm)
            self.worker.finished.connect(self.on_sort_finished)
            self.worker.error.connect(self.on_sort_error)
            self.worker.start()

        self.sortingButton.setEnabled(False)
        self.sortingButton_2.setEnabled(False)
        self.sortingButton_3.setEnabled(False)
        self.searchButton.setEnabled(False)
        self.scrapButton.setEnabled(False)
        self.sortButton.setEnabled(False)
        self.exitButton.setEnabled(False)

    def on_sort_finished(self, sorted_data, elapsed_time):
        self.sortingtimeShow.setText(f"{elapsed_time:.7f} ms")
        self.tableDataCollector.clearContents()
        self.tableDataCollector.setRowCount(0)

        for index, row in sorted_data.iterrows():
            row_position = self.tableDataCollector.rowCount()
            self.tableDataCollector.insertRow(row_position)
            for column, item in enumerate(row):
                self.tableDataCollector.setItem(row_position, column, QTableWidgetItem(str(item)))

        
        self.sortingButton.setEnabled(True)
        self.sortingButton_2.setEnabled(True)
        self.sortingButton_3.setEnabled(True)
        self.searchButton.setEnabled(True)
        self.scrapButton.setEnabled(True)
        self.sortButton.setEnabled(True)
        self.exitButton.setEnabled(True)
        
    def on_sort_error(self, error_message):
        QMessageBox.critical(None, "Error", error_message)


    #Searching Based on the Condition
    
        
    def filterRowsByStart(self,df, column_name, filter_string):
        filtered_df = df[df[column_name].astype(str).str.startswith(filter_string)]
        return filtered_df

    def filterRowsByEnd(self, df, column_name, filter_string):
        filtered_df = df[df[column_name].astype(str).str.endswith(filter_string)]
        return filtered_df

    def SearchTableClick(self):
        file_path = 'data.csv'
        first_column_name = self.Column1Sort.currentText()
        StartString = self.Search1Line.text()
        second_Column_Name =self.Column2Sort.currentText()
        endString = self.Search2Line.text()
        condition = self.AND_OR.currentText()
        col1Condition = self.Column1comboBox.currentText()
        col2Condition = self.Column2comboBox.currentText()
        
        if(not StartString and first_column_name == "None" and not(endString) and second_Column_Name=="None"):
            self.show_Message("Select any column and condition") 
            return
        
        if(StartString and first_column_name != "None"):
            if(endString or second_Column_Name != "None"):
                if(endString and second_Column_Name != "None"):
                    validItems = ["None","AND &&","OR | |"]
                    if(condition != "None" and condition in validItems):
                        #all conditions are satisfied for multiplle search
                        self.worker = SearchThread(file_path, first_column_name,StartString,self.filterRowsByStart,col1Condition,second_Column_Name,endString,self.filterRowsByEnd,col2Condition,condition)
                        self.worker.sorted_data_signal2.connect(self.update_table2)
                        self.worker.start()
                        
                    else:
                        self.show_Message("Select The Condition")   
                else:
                    self.show_Message("Select both second Column and end text")
                    
            else:          
                self.worker = SearchThread(file_path, first_column_name,StartString,self.filterRowsByStart,col1Condition)
                self.worker.sorted_data_signal.connect(self.update_table)
                self.worker.start()
        elif(StartString or first_column_name != "None"):
            self.show_Message("Selcet Both,First Column and Start text")
            
        
        elif(endString and second_Column_Name != "None"):
            if(StartString and first_column_name != "None"):
                if(not(StartString and first_column_name != "None")):
                    self.show_Message("Select both First Column and end text")
            else:
                self.worker = SearchThread(file_path,second_Column_Name,endString,self.filterRowsByEnd,col2Condition)
                self.worker.sorted_data_signal.connect(self.update_table)
                self.worker.sorted_data_signal2.connect(self.update_table2)
                self.worker.start()
        elif(endString or second_Column_Name != "None"):
            self.show_Message("Selcet Both Second Column and end text")
            
        
    def update_table(self,df,con):
        condition = (con=="NOT !")
        AllData = pd.read_csv("data.csv")
        if(condition):
            diff_data = pd.concat([AllData, df]).drop_duplicates(keep=False)
        else:
            diff_data = df
        self.tableDataCollector.setRowCount(0)

        self.tableDataCollector.setColumnCount(len(diff_data.columns))
        
        self.tableDataCollector.setHorizontalHeaderLabels(diff_data.columns.tolist())
        
        for row_index, row_data in diff_data.iterrows():
            row_position = self.tableDataCollector.rowCount()
            self.tableDataCollector.insertRow(row_position)
            for column_index, value in enumerate(row_data):
                self.tableDataCollector.setItem(row_position, column_index, QTableWidgetItem(str(value)))
    
    def update_table2(self,df1,df2,con1,con2,BaseCon):
        condition1 = (con1 == "NOT !")
        condition2 = (con2 == "NOT !")
        AllData = pd.read_csv("data.csv")

        if condition1:
            diff_data1 = pd.concat([AllData, df1]).drop_duplicates(keep=False)
        else:
            diff_data1 = df1

        if condition2:
            diff_data2 = pd.concat([AllData, df2]).drop_duplicates(keep=False)
        else:
            diff_data2 = df2

        if BaseCon == "AND &&":
            merged_Data = pd.merge(diff_data1, diff_data2, how='inner')
        else:
            df1 = df1.set_index('Index', inplace=False)
            df2 = df2.set_index('Index', inplace=False)
    
        merged_Data = diff_data1.combine_first(diff_data2).reset_index(drop=True)
        self.tableDataCollector.setRowCount(0)

        self.tableDataCollector.setColumnCount(len(merged_Data.columns))
        
        self.tableDataCollector.setHorizontalHeaderLabels(merged_Data.columns.tolist())
        
        for row_index, row_data in merged_Data.iterrows():
            row_position = self.tableDataCollector.rowCount()
            self.tableDataCollector.insertRow(row_position)
            for column_index, value in enumerate(row_data):
                self.tableDataCollector.setItem(row_position, column_index, QTableWidgetItem(str(value)))
        
            
        
    def show_Message(self,message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText(message)
        msg_box.setWindowTitle("Invalid input")
        msg_box.setStandardButtons(QMessageBox.Ok) 
        msg_box.exec_()

    def open_scrap_window(self, MainWindow):
        
        
        from Scrap import Ui_MainWindow
        
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()  # Initialize the second window
        self.ui.setupUi(self.window)  # Setup the UI of the second window
        self.window.show()  # Show the second window
        
        MainWindow.close() 
    
    def exit(self):
        QApplication.quit()


class DataLoader:
            def __init__(self, tableDataCollector):
                self.tableDataCollector = tableDataCollector
                
            def load_data(self):
                try:
                    data = pd.read_csv('data.csv')

                    self.tableDataCollector.setColumnCount(len(data.columns))
                    self.tableDataCollector.setHorizontalHeaderLabels([
                        "Index", "Title", "Model", "Price", 
                        "Mileage", "Fuel Type", "Engine", "Transmission", "City"
                    ])
                    self.tableDataCollector.clearContents()
                    self.tableDataCollector.setRowCount(0)

                    for index, row in data.iterrows():
                        row_position = self.tableDataCollector.rowCount()
                        self.tableDataCollector.insertRow(row_position) 
                        for column, item in enumerate(row):
                            self.tableDataCollector.setItem(row_position, column, QTableWidgetItem(str(item)))

                except FileNotFoundError as e:
                    QMessageBox.critical(None, "Error", f"Failed to load data: {e}")
                except Exception as e:
                    QMessageBox.critical(None, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_SecondWindow()
    ui.setupUi(MainWindow)
    tableDataCollector = ui.tableDataCollector 

    data_loader = DataLoader(tableDataCollector)

    data_loader.load_data()
    MainWindow.show()
    sys.exit(app.exec_())
    