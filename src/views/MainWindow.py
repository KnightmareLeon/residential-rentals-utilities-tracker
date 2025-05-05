from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from src.views.pages.UnitsPage import UnitsPage
from src.views.pages.UtilitiesPage import UtilitiesPage
from src.views.pages.BillsPage import BillsPage
from src.views.pages.HomePage import HomePage
from src.utils.sampleDataGenerator import generateUnitData, generateUtilityData, generateBillData

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("assets/logos/logoIcon.png"))
        
        self.searchbarTextByPage = {
            "Home": "",
            "Units": "",
            "Utilities": "",
            "Bills": "",
        }

        self.setupUi(self)
        self.setupPages()

        self.currentSidebarButton = self.homeButton
        self.stackedWidget.setCurrentWidget(self.homePage)

        self.searchInputLineEdit.returnPressed.connect(self.handleSearch)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1102, 737)
        MainWindow.setStyleSheet("""
            QMainWindow {
                font-family: "Urbanist";
                background-color: #080808;
            }

            QFrame {
                border: none;
            }

            /* Sidebar */
            #sidebarFrame QPushButton {
                font-family: "Urbanist";
                color: white;
                font-size: 18px;
                border: none;
                padding: 15px 30px;
                border-radius: 15px;
                text-align: left;
            }
            #sidebarFrame QPushButton::hover {
                background-color: #15161a;
            }

            #homeButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                        stop:0.4 #3A0CA3, stop:1 #F72585);
                color: white;
            }

            /* Header */
            QFrame#searchBarFrame {
                background-color: #15161a;
                border-radius: 12px;
                margin: 5px;
                padding: 12px;
            }

            QLabel#searchIconLabel {
                min-width: 35px;
                min-height: 25px;
                margin-left: 8px;
                margin-right: 6px;
            }

            QLineEdit#searchInputLineEdit {
                border: none;
                background: transparent;
                color: white;
                font-size: 18px;
                font-family: "Urbanist";
            }

            QLineEdit#searchInputLineEdit::placeholder {
                color: #A0A0A0;
            }

            QLabel#windowLabel {
                font-size: 40px;
                font-weight: 700;
                font-family: "Urbanist";
                color: white;
            }

            QLabel#userNameLabel {
                font-family: "Urbanist";
                font-size: 20px;
                color: white;
                margin: 15px;
            }
            QScrollBar:vertical {
                background: #2e2e2e;
                width: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #888;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
            QScrollBar:horizontal { 
                background: #2e2e2e;
                height: 12px;
                margin: 0px 0px 0px 0px;
                border-radius: 6px;
            }
            QScrollBar::handle:horizontal {
                background: #888;
                min-width: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                background: none;
                width: 0px;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            """)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sidebarFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.sidebarFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.sidebarFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sidebarFrame.setObjectName("sidebarFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.sidebarFrame)
        self.verticalLayout.setContentsMargins(-1, 0, -1, 0)
        self.verticalLayout.setSpacing(30)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sidebarLogoFrame = QtWidgets.QFrame(parent=self.sidebarFrame)
        self.sidebarLogoFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.sidebarLogoFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sidebarLogoFrame.setObjectName("sidebarLogoFrame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.sidebarLogoFrame)
        self.horizontalLayout_6.setContentsMargins(0, 25, 0, 0)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.logoLabel = QtWidgets.QLabel(parent=self.sidebarLogoFrame)
        self.logoLabel.setMaximumSize(QtCore.QSize(182, 39))
        self.logoLabel.setText("")
        self.logoLabel.setPixmap(QtGui.QPixmap("src/ui\\../../assets/logos/Logo.png"))
        self.logoLabel.setScaledContents(True)
        self.logoLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logoLabel.setObjectName("logoLabel")
        self.horizontalLayout_6.addWidget(self.logoLabel)
        self.verticalLayout.addWidget(self.sidebarLogoFrame)

        self.sidebarButtonsFrame = QtWidgets.QFrame(parent=self.sidebarFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sidebarButtonsFrame.sizePolicy().hasHeightForWidth())
        self.sidebarButtonsFrame.setSizePolicy(sizePolicy)
        self.sidebarButtonsFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.sidebarButtonsFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.sidebarButtonsFrame.setObjectName("sidebarButtonsFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.sidebarButtonsFrame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        self.homeButton = QtWidgets.QPushButton(parent=self.sidebarButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.homeButton.sizePolicy().hasHeightForWidth())
        self.homeButton.setSizePolicy(sizePolicy)
        self.homeButton.setMinimumSize(QtCore.QSize(200, 0))
        self.homeButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.homeButton.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("src/ui\\../../assets/icons/home.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.homeButton.setIcon(icon)
        self.homeButton.setIconSize(QSize(24, 24))  
        self.homeButton.setObjectName("homeButton")
        self.verticalLayout_3.addWidget(self.homeButton, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.unitsButton = QtWidgets.QPushButton(parent=self.sidebarButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.unitsButton.sizePolicy().hasHeightForWidth())
        self.unitsButton.setSizePolicy(sizePolicy)
        self.unitsButton.setMinimumSize(QtCore.QSize(200, 0))
        self.unitsButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("src/ui\\../../assets/icons/units.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.unitsButton.setIcon(icon1)
        self.unitsButton.setIconSize(QSize(24, 24))  
        self.unitsButton.setObjectName("unitsButton")
        self.verticalLayout_3.addWidget(self.unitsButton, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.utilitiesButton = QtWidgets.QPushButton(parent=self.sidebarButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.utilitiesButton.sizePolicy().hasHeightForWidth())
        self.utilitiesButton.setSizePolicy(sizePolicy)
        self.utilitiesButton.setMinimumSize(QtCore.QSize(200, 0))
        self.utilitiesButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("src/ui\\../../assets/icons/utilities.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.utilitiesButton.setIcon(icon2)
        self.utilitiesButton.setIconSize(QSize(24, 24))
        self.utilitiesButton.setObjectName("utilitiesButton")
        self.verticalLayout_3.addWidget(self.utilitiesButton, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.billsButton = QtWidgets.QPushButton(parent=self.sidebarButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.billsButton.sizePolicy().hasHeightForWidth())
        self.billsButton.setSizePolicy(sizePolicy)
        self.billsButton.setMinimumSize(QtCore.QSize(200, 0))
        self.billsButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("src/ui\\../../assets/icons/bills.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.billsButton.setIcon(icon3)
        self.billsButton.setIconSize(QSize(24, 24))
        self.billsButton.setObjectName("billsButton")
        self.verticalLayout_3.addWidget(self.billsButton, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.recordsButton = QtWidgets.QPushButton(parent=self.sidebarButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recordsButton.sizePolicy().hasHeightForWidth())
        self.recordsButton.setSizePolicy(sizePolicy)
        self.recordsButton.setMinimumSize(QtCore.QSize(200, 0))
        self.recordsButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("src/ui\\../../assets/icons/records.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.recordsButton.setIcon(icon4)
        self.recordsButton.setIconSize(QSize(24, 24))
        self.recordsButton.setObjectName("recordsButton")
        # TODO:
        self.recordsButton.setVisible(False)
        self.verticalLayout_3.addWidget(self.recordsButton, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.profileButton = QtWidgets.QPushButton(parent=self.sidebarButtonsFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.profileButton.sizePolicy().hasHeightForWidth())
        self.profileButton.setSizePolicy(sizePolicy)
        self.profileButton.setMinimumSize(QtCore.QSize(200, 0))
        self.profileButton.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("src/ui\\../../assets/icons/profiles.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.profileButton.setIcon(icon5)
        self.profileButton.setIconSize(QSize(24, 24))
        self.profileButton.setObjectName("profileButton")
        # TODO:
        self.profileButton.setVisible(False)
        self.verticalLayout_3.addWidget(self.profileButton, 0, QtCore.Qt.AlignmentFlag.AlignLeft)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 1)
        self.verticalLayout_3.setStretch(2, 1)
        self.verticalLayout_3.setStretch(3, 1)
        self.verticalLayout_3.setStretch(4, 1)
        self.verticalLayout_3.setStretch(5, 1)
        self.verticalLayout.addWidget(self.sidebarButtonsFrame, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        spacerItem = QtWidgets.QSpacerItem(20, 315, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(2, 8)

        self.horizontalLayout.addWidget(self.sidebarFrame)
        self.centerFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.centerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.centerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.centerFrame.setObjectName("centerFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centerFrame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headerFrame = QtWidgets.QFrame(parent=self.centerFrame)
        self.headerFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.headerFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.headerFrame.setObjectName("headerFrame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.headerFrame)
        self.horizontalLayout_2.setContentsMargins(0, 25, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.headerCenterFrame = QtWidgets.QFrame(parent=self.headerFrame)
        self.headerCenterFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.headerCenterFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.headerCenterFrame.setObjectName("headerCenterFrame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.headerCenterFrame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.windowLabelFrame = QtWidgets.QFrame(parent=self.headerCenterFrame)
        self.windowLabelFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.windowLabelFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.windowLabelFrame.setObjectName("windowLabelFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.windowLabelFrame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.windowLabel = QtWidgets.QLabel(parent=self.windowLabelFrame)
        font = QtGui.QFont()
        font.setFamily("Urbanist")
        font.setBold(True)
        self.windowLabel.setFont(font)
        self.windowLabel.setObjectName("windowLabel")
        self.horizontalLayout_4.addWidget(self.windowLabel)
        self.horizontalLayout_3.addWidget(self.windowLabelFrame)
        self.searchBarFrame = QtWidgets.QFrame(parent=self.headerCenterFrame)
        self.searchBarFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.searchBarFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.searchBarFrame.setObjectName("searchBarFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.searchBarFrame)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.searchIconButton = QtWidgets.QPushButton(parent=self.searchBarFrame)
        self.searchIconButton.setText("")
        self.searchIconButton.setIcon(QtGui.QIcon("src/ui\\../../assets/icons/searchIcon.png"))
        self.searchIconButton.setObjectName("searchIconButton")
        self.searchIconButton.setFixedSize(25, 25)
        self.searchIconButton.setStyleSheet("border: none; background: transparent;")
        self.horizontalLayout_5.addWidget(self.searchIconButton)

        self.searchInputLineEdit = QtWidgets.QLineEdit(parent=self.searchBarFrame)
        self.searchInputLineEdit.setMaximumSize(QtCore.QSize(16777215, 75))
        self.searchInputLineEdit.setText("")
        self.searchInputLineEdit.setReadOnly(False)
        self.searchInputLineEdit.setObjectName("searchInputLineEdit")
        self.horizontalLayout_5.addWidget(self.searchInputLineEdit)

        self.searchBarFrame.setVisible(False)

        self.horizontalLayout_3.addWidget(self.searchBarFrame, 0, QtCore.Qt.AlignmentFlag.AlignVCenter)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 5)
        self.horizontalLayout_2.addWidget(self.headerCenterFrame)
        self.headerProfileFrame = QtWidgets.QFrame(parent=self.headerFrame)
        self.headerProfileFrame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.headerProfileFrame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.headerProfileFrame.setObjectName("headerProfileFrame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.headerProfileFrame)
        self.horizontalLayout_7.setContentsMargins(-1, -1, 50, -1)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        spacerItem1 = QtWidgets.QSpacerItem(4, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem1)
        self.userNameLabel = QtWidgets.QLabel(parent=self.headerProfileFrame)
        self.userNameLabel.setObjectName("userNameLabel")
        self.horizontalLayout_7.addWidget(self.userNameLabel)
        self.userProfileLabel = QtWidgets.QLabel(parent=self.headerProfileFrame)
        self.userProfileLabel.setMaximumSize(QtCore.QSize(50, 50))
        self.userProfileLabel.setText("")
        self.userProfileLabel.setPixmap(QtGui.QPixmap("src/ui\\../../assets/icons/account.png"))
        self.userProfileLabel.setScaledContents(True)
        self.userProfileLabel.setObjectName("userProfileLabel")
        self.horizontalLayout_7.addWidget(self.userProfileLabel)
        self.horizontalLayout_7.setStretch(0, 2)
        self.horizontalLayout_7.setStretch(1, 1)
        self.horizontalLayout_7.setStretch(2, 1)
        self.horizontalLayout_2.addWidget(self.headerProfileFrame)
        self.horizontalLayout_2.setStretch(0, 3)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addWidget(self.headerFrame)

        self.stackedWidget = QtWidgets.QStackedWidget(parent=self.centerFrame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout_2.addWidget(self.stackedWidget)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 8)
        self.horizontalLayout.addWidget(self.centerFrame)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.homeButton.setText(_translate("MainWindow", "    Home"))
        self.unitsButton.setText(_translate("MainWindow", "    Units"))
        self.utilitiesButton.setText(_translate("MainWindow", "    Utilities"))
        self.billsButton.setText(_translate("MainWindow", "    Bills"))
        self.recordsButton.setText(_translate("MainWindow", "    Records"))
        self.profileButton.setText(_translate("MainWindow", "    Profile"))
        self.windowLabel.setText(_translate("MainWindow", "Welcome back"))
        self.userNameLabel.setText(_translate("MainWindow", "Leonard"))

    def setupPages(self):
        self.unitsPage = UnitsPage(mainWindow=self)
        self.utilitiesPage = UtilitiesPage(mainWindow=self)
        self.billsPage = BillsPage(mainWindow=self)
        self.homePage = HomePage(mainWindow=self)

        self.stackedWidget.addWidget(self.homePage)
        self.stackedWidget.addWidget(self.unitsPage)
        self.stackedWidget.addWidget(self.utilitiesPage)
        self.stackedWidget.addWidget(self.billsPage)

        self.unitsPage.table.updateTable()
        self.utilitiesPage.table.updateTable()
        self.billsPage.table.updateTable()

        self.homeButton.clicked.connect(lambda: self.updatePage(self.homePage, self.homeButton, "Welcome back"))
        self.unitsButton.clicked.connect(lambda: self.updatePage(self.unitsPage, self.unitsButton, "Units"))
        self.utilitiesButton.clicked.connect(lambda: self.updatePage(self.utilitiesPage, self.utilitiesButton, "Utilities"))
        self.billsButton.clicked.connect(lambda: self.updatePage(self.billsPage, self.billsButton, "Bills"))

        self.updatePage(self.homePage, self.homeButton, "Welcome back")

    def updatePage(self, pageWidget, button, title):
        self.searchbarTextByPage[self.windowLabel.text()] = self.searchInputLineEdit.text()

        self.stackedWidget.setCurrentWidget(pageWidget)

        restoredText = self.searchbarTextByPage.get(title, "")
        self.searchInputLineEdit.setText(restoredText)
        self.searchInputLineEdit.setPlaceholderText(f"Search {title.lower()}...")

        if hasattr(self, 'currentSidebarButton') and self.currentSidebarButton:
            self.currentSidebarButton.setStyleSheet("""
                    QPushButton {
                        background: none;
                        color: white;
                    }
                    QPushButton:hover {
                        background-color: #15161a;
                    }
                    """)
    
        button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0.4 #3A0CA3, stop:1 #F72585);
                    color: white;
                    font-weight: bold;
                }
                """)

        self.searchBarFrame.setVisible(button != self.homeButton)

        self.currentSidebarButton = button
        self.windowLabel.setText(title)

    def handleSearch(self):
        currentPage = self.stackedWidget.currentWidget()
        if currentPage == self.unitsPage:
            self.unitsPage.resetPage()
        elif currentPage == self.utilitiesPage:
            self.utilitiesPage.resetPage()
        elif currentPage == self.billsPage:
            self.billsPage.resetPage()
