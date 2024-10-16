import os
import pandas as pd
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox , QApplication
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import ScrapResources.resources_Rc
from concurrent.futures import ThreadPoolExecutor
import csv
import sys
class ScrapThread(QThread):
    finished = pyqtSignal()
    updateData = pyqtSignal(list)
    updateProgress = pyqtSignal(int)

    num = 0
    def __init__(self, base_link, templink,max_data, parent=None):
        super().__init__(parent)
        self.base_link = base_link
        self.templink = templink
        self.stop_event = threading.Event()
        self.is_paused = threading.Event()
        self.max_data = max_data
        self.is_paused.set()  # Start as not paused
        self.current_data_count = 0

    def run(self):
        global num
        chrome_options = Options() 
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage") 
        service = Service(executable_path="C:\Program Files\chromedriver-win64\chromedriver.exe")

        driver = webdriver.Chrome(service=service, options=chrome_options)
 
        num = 1
        while not self.stop_event.is_set() and self.current_data_count < self.max_data:
            self.scrap_data(driver, num)
            num += 1
            if not self.is_paused.is_set():
                self.is_paused.wait()

        driver.quit()
        self.finished.emit()

    def scrap_data(self, driver, n):
        global num
        link = self.base_link + self.templink
        driver.get(link)
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        divClass = f"well search-list clearfix ad-container page-{n}" if n != 1 else "well search-list clearfix ad-container"
        for a in soup.findAll("div", attrs={"class": divClass}):
            title = a.find("h3").get_text()
            price = a.find("div", attrs={"class": "price-details generic-dark-grey"}).get_text().strip()
            data = a.find("div", attrs={"class": "col-md-12 grid-date"})
            city = data.find("ul", attrs={"class": "list-unstyled search-vehicle-info fs13"}).find("li").get_text()
            listItems = data.find("ul", attrs={"class": "list-unstyled search-vehicle-info-2 fs13"}).find_all("li")

            model = listItems[0].get_text() if len(listItems) > 0 else ""
            distance = listItems[1].get_text() if len(listItems) > 1 else ""
            fuel_type = listItems[2].get_text() if len(listItems) > 2 else ""
            engine = listItems[3].get_text() if len(listItems) > 3 else ""
            transmission_type = listItems[4].get_text() if len(listItems) > 4 else ""

            # Emit signal to update data
            self.updateData.emit([self.current_data_count, title, model, price, distance, fuel_type, engine, transmission_type, city])
            self.current_data_count += 1  # Increment data count
            
            
            progress = int((self.current_data_count / self.max_data) * 100)
            self.updateProgress.emit(progress)
            
            if self.current_data_count >= self.max_data:  # Stop if limit reached
                self.stop_event.set()
                break

        # Check for next page
        listOfLinks = soup.find("ul", attrs={"class": "pagination search-pagi"})
        next_page = listOfLinks.find("li", attrs={"class": "next_page"})
        self.templink = next_page.find("a").get("href") if next_page else "used-cars/karachi/24857?page=1"
        if(not next_page):
            num = 0
    def pause(self):
        self.is_paused.clear()

    def resume(self):
        self.is_paused.set()

    def stop(self):
        self.stop_event.set()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1226, 828)
        MainWindow.setStyleSheet("QPushButton {\n"
                "background-color: lightgray;\n"
                "border-radius: 10px;\n"
                "padding: 10px;\n"
                "border: 2px solid #5c5c5c;\n"
                "}\n"
                "\n"
                "QPushButton:pressed {\n"
                "background-color: darkgray;\n"
                "padding-left: 12px;\n"
                "padding-top: 12px;\n"
                "border: 2px solid #3c3c3c;\n"
                "}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.bodyFrame = QtWidgets.QFrame(self.centralwidget)
        self.bodyFrame.setStyleSheet("")
        self.bodyFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bodyFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bodyFrame.setObjectName("bodyFrame")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.bodyFrame)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_3 = QtWidgets.QFrame(self.bodyFrame)
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
        
        self.sortButton.clicked.connect(lambda: self.open_sort_window(MainWindow))
        
        
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
        self.horizontalLayout.addWidget(self.frame_3)
        self.sidebarFrame = QtWidgets.QFrame(self.bodyFrame)
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
        self.ScrapLabel = QtWidgets.QLabel(self.frame_4)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(28)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.ScrapLabel.setFont(font)
        self.ScrapLabel.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.ScrapLabel.setFrameShape(QtWidgets.QFrame.Box)
        self.ScrapLabel.setLineWidth(5)
        self.ScrapLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ScrapLabel.setObjectName("ScrapLabel")
        self.verticalLayout_3.addWidget(self.ScrapLabel)
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
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.frame_6.sizePolicy().hasHeightForWidth())
        self.frame_6.setSizePolicy(sizePolicy)
        self.frame_6.setStyleSheet("background-color: rgb(17, 168, 182);\n"
                "border:3px solid black;")
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_6)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.stopButton = QtWidgets.QPushButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stopButton.sizePolicy().hasHeightForWidth())
        self.stopButton.setSizePolicy(sizePolicy)
        self.stopButton.setMinimumSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.stopButton.setFont(font)
        self.stopButton.setStyleSheet("\n"
                "QPushButton{\n"
                "border-radius:20px;\n"
                "background-color:white;\n"
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
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Icons/whiteIcons/stop-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon4)
        self.stopButton.setIconSize(QtCore.QSize(25, 25))
        self.stopButton.setObjectName("stopButton")

        
        #stop Button
        self.stopButton.clicked.connect(self.OnStopClicked)
        self.stopButton.setEnabled(False)
        #



        self.gridLayout_3.addWidget(self.stopButton, 2, 7, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(50, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 2, 1, 1, 3)
        self.startButton = QtWidgets.QPushButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startButton.sizePolicy().hasHeightForWidth())
        self.startButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.startButton.setFont(font)
        self.startButton.setStyleSheet("\n"
                "QPushButton{\n"
                "border-radius:20px;\n"
                "background-color:white;\n"
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Icons/whiteIcons/check-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.startButton.setIcon(icon5)
        self.startButton.setIconSize(QtCore.QSize(25, 25))
        self.startButton.setObjectName("startButton")
        self.gridLayout_3.addWidget(self.startButton, 2, 0, 1, 1)



        #start Button
        self.startButton.clicked.connect(self.OnStartClicked)
        #

        spacerItem4 = QtWidgets.QSpacerItem(20, 130, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 1, 0, 1, 1)
        self.resumeButton = QtWidgets.QPushButton(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.resumeButton.sizePolicy().hasHeightForWidth())
        self.resumeButton.setSizePolicy(sizePolicy)
        self.resumeButton.setMinimumSize(QtCore.QSize(0, 10))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.resumeButton.setFont(font)
        self.resumeButton.setStyleSheet("QPushButton{\n"
                "border-radius:20px;\n"
                "background-color:white;\n"
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Icons/whiteIcons/pause-circle.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.resumeButton.setIcon(icon6)
        self.resumeButton.setIconSize(QtCore.QSize(25, 25))
        self.resumeButton.setObjectName("resumeButton")
        self.gridLayout_3.addWidget(self.resumeButton, 2, 4, 1, 1)
        
        
        
        
        #Resume
        self.resumeButton.clicked.connect(self.OnPauseResumeClicked)
        self.stopButton.setEnabled(False)
        #
        
        
        

        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 0, 1, 1, 1)
        self.progressLabel = QtWidgets.QLabel(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.progressLabel.sizePolicy().hasHeightForWidth())
        self.progressLabel.setSizePolicy(sizePolicy)
        self.progressLabel.setStyleSheet("background-color: rgb(193, 193, 193);\n"
                "border-radius:15px;")
        self.progressLabel.setObjectName("progressLabel")
        self.gridLayout_3.addWidget(self.progressLabel, 0, 0, 1, 1)
        self.progressBar = QtWidgets.QProgressBar(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(5)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("#progressBar {\n"
                "\n"
                "\n"
                "background-color: rgb(255, 255, 255);\n"
                "border: 2px solid balck;\n"
                "color:orange;\n"
                "border-radius: 5px;\n"
                "text-align: center;\n"
                "}\n"
                "\n"
                "#progressBar::chunk {\n"
                "background-color: Grey; \n"
                "width: 15px;\n"
                "margin:2px; \n"
                "}")
        
        
        
        
        #progress bar
        self.progressBar.setProperty("value", 0)
        #        
        
        
        
        self.progressBar.setObjectName("progressBar")
        self.gridLayout_3.addWidget(self.progressBar, 0, 2, 1, 6)
        self.frame_8 = QtWidgets.QFrame(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_8.sizePolicy().hasHeightForWidth())
        self.frame_8.setSizePolicy(sizePolicy)
        self.frame_8.setStyleSheet("border:none;")
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_8)
        self.verticalLayout_5.setContentsMargins(0, 25, 0, 25)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.NoInput = QtWidgets.QLineEdit(self.frame_8)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.NoInput.sizePolicy().hasHeightForWidth())
        self.NoInput.setSizePolicy(sizePolicy)
        self.NoInput.setMinimumSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.NoInput.setFont(font)
        self.NoInput.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.NoInput.setObjectName("NoInput")
        self.verticalLayout_5.addWidget(self.NoInput, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.gridLayout_3.addWidget(self.frame_8, 1, 4, 1, 2)
        spacerItem6 = QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 2, 5, 1, 2)
        self.scrapingNumberLabel = QtWidgets.QLabel(self.frame_6)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.scrapingNumberLabel.setFont(font)
        self.scrapingNumberLabel.setStyleSheet("border:none;")
        self.scrapingNumberLabel.setObjectName("scrapingNumberLabel")
        self.gridLayout_3.addWidget(self.scrapingNumberLabel, 1, 2, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 130, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem7, 1, 7, 1, 1)
        self.verticalLayout_4.addWidget(self.frame_6)
        self.frame_7 = QtWidgets.QFrame(self.frame_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(6)
        sizePolicy.setHeightForWidth(self.frame_7.sizePolicy().hasHeightForWidth())
        self.frame_7.setSizePolicy(sizePolicy)
        self.frame_7.setMinimumSize(QtCore.QSize(0, 8))
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
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem8 = QtWidgets.QSpacerItem(290, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.frame_11 = QtWidgets.QFrame(self.frame_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_11.sizePolicy().hasHeightForWidth())
        self.frame_11.setSizePolicy(sizePolicy)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
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
        self.horizontalLayout_4.addWidget(self.dataLabel)
        self.horizontalLayout_3.addWidget(self.frame_11)
        spacerItem9 = QtWidgets.QSpacerItem(240, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.verticalLayout_6.addWidget(self.frame_9)
        self.dataGridFrame = QtWidgets.QFrame(self.frame_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(50)
        sizePolicy.setHeightForWidth(self.dataGridFrame.sizePolicy().hasHeightForWidth())
        self.dataGridFrame.setSizePolicy(sizePolicy)
        self.dataGridFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dataGridFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dataGridFrame.setObjectName("dataGridFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.dataGridFrame)
        self.horizontalLayout_2.setContentsMargins(0, 5, 0, 2)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")


        self.tableDataCollector = QtWidgets.QTableWidget(self.dataGridFrame)
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
        self.horizontalLayout_2.addWidget(self.tableDataCollector)
        self.verticalLayout_6.addWidget(self.dataGridFrame)
        self.verticalLayout_4.addWidget(self.frame_7)
        self.verticalLayout_2.addWidget(self.frame_5)
        self.horizontalLayout.addWidget(self.sidebarFrame)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.bodyFrame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.scrapButton.setText(_translate("MainWindow", "Scrap"))
        self.sortButton.setText(_translate("MainWindow", "Sort"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.ScrapLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/trello.svg\"/><span style=\" font-size:36pt; color:#090909;\"> Scraping</span></p></body></html>"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.resumeButton.setText(_translate("MainWindow", "Play/Pause"))
        self.progressLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/loader.svg\"/><span style=\" font-size:16pt;\">Progress</span></p></body></html>"))
        self.scrapingNumberLabel.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:16pt; font-weight:600;\">Scraping No.</span></p></body></html>"))
        self.dataLabel.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><img src=\":/Icons/whiteIcons/cloud-lightning.svg\"/><span style=\" font-size:18pt;\">Scraped Data</span></p></body></html>"))
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

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def insertDataToGrid(self, data):
        row_position = self.tableDataCollector.rowCount()
        self.tableDataCollector.insertRow(row_position)

    # Assuming the first item in the data is the index
        for column, value in enumerate(data):  
            self.tableDataCollector.setItem(row_position, column, QTableWidgetItem(str(value)))  # Convert value to string

    def appendDataToCsv(self, data):
        with open('data.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def clearCSV(self):
        headers = ['Index','Title', 'Model', 'Price', 'Mileage', 'Fuel Type', 'Engine', 'Transmission', 'City']  # Define your headers
        with open('data.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write only the headers

    def start_scraping(self, number):
        self.scrap_thread = ScrapThread("https://www.pakwheels.com/","used-cars/lahore/24858?page=1",number)
        self.scrap_thread.updateData.connect(self.insertDataToGrid)
        self.scrap_thread.updateData.connect(self.appendDataToCsv)
        self.scrap_thread.updateProgress.connect(self.update_progress)
        self.scrap_thread.finished.connect(self.on_thread_finished)
        self.scrap_thread.start()
    

    isPaused = False
    #Start Buttton Clicked
    def OnStartClicked(self):
        global isPaused
        totalNumbers = self.NoInput.text()
        if totalNumbers.isdigit():
            self.progressBar.setProperty("value", 0)
            self.tableDataCollector.clearContents()
            self.tableDataCollector.setRowCount(0)
            self.clearCSV()
            self.start_scraping(int(totalNumbers))
            self.startButton.setEnabled(False)
            self.sortButton.setEnabled(False)
            self.scrapButton.setEnabled(False)
            self.exitButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.resumeButton.setEnabled(True)
            self.resumeButton.setText("Pause")
            isPaused = False
        else:
            self.show_message("Enter a Scrapping Number")

    
    
    def OnPauseResumeClicked(self):
        global isPaused
        if hasattr(self, 'scrap_thread'):
            if not isPaused:
                self.scrap_thread.pause()
                self.resumeButton.setText("Resume")
                isPaused = True
                self.show_message("Scrapping Paused")
            else:
                self.scrap_thread.resume()
                self.resumeButton.setText("Pause")
                isPaused = False
                self.show_message("Scrapping Resumed")
    
    def OnStopClicked(self):
        if hasattr(self, 'scrap_thread'):
            self.scrap_thread.stop()

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("Message")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def on_thread_finished(self):
        self.show_message("Scraping finished")
        self.startButton.setEnabled(True)
        self.sortButton.setEnabled(True)
        self.scrapButton.setEnabled(True)
        self.exitButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.resumeButton.setEnabled(False)
        self.resumeButton.setText("Pause/Resume")
    def open_sort_window(self, MainWindow):
        from Sorty import Ui_SecondWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_SecondWindow()  # Initialize the second window
        self.ui.setupUi(self.window)  # Setup the UI of the second window
        self.window.show()  # Show the second window
        
        MainWindow.close() 
    
    def exit(self):
        QApplication.quit()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())