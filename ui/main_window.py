# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Mon Aug 11 17:28:27 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_BlurringDialogBase(object):
    def setupUi(self, BlurringDialogBase):
        BlurringDialogBase.setObjectName(_fromUtf8("BlurringDialogBase"))
        BlurringDialogBase.resize(1001, 723)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(BlurringDialogBase)
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.listWidget = QtGui.QListWidget(BlurringDialogBase)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)
        self.listWidget.setMinimumSize(QtCore.QSize(100, 200))
        self.listWidget.setMaximumSize(QtCore.QSize(153, 16777215))
        self.listWidget.setStyleSheet(_fromUtf8("QListWidget{\n"
"    background-color: rgb(69, 69, 69, 220);\n"
"    outline: 0;\n"
"}\n"
"QListWidget::item {\n"
"    color: white;\n"
"    padding: 3px;\n"
"}\n"
"QListWidget::item::selected {\n"
"    color: black;\n"
"    background-color:palette(Window);\n"
"    padding-right: 0px;\n"
"}"))
        self.listWidget.setFrameShape(QtGui.QFrame.Box)
        self.listWidget.setLineWidth(0)
        self.listWidget.setIconSize(QtCore.QSize(32, 32))
        self.listWidget.setUniformItemSizes(True)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        item = QtGui.QListWidgetItem()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Blurring/resources/blur.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Blurring/resources/sigma.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon1)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Blurring/resources/about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon2)
        self.listWidget.addItem(item)
        item = QtGui.QListWidgetItem()
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Blurring/resources/info.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        item.setIcon(icon3)
        self.listWidget.addItem(item)
        self.horizontalLayout_2.addWidget(self.listWidget)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.messageBar = QgsMessageBar(BlurringDialogBase)
        self.messageBar.setObjectName(_fromUtf8("messageBar"))
        self.verticalLayout_5.addWidget(self.messageBar)
        self.stackedWidget = QtGui.QStackedWidget(BlurringDialogBase)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.blur = BlurWidget()
        self.blur.setObjectName(_fromUtf8("blur"))
        self.verticalLayout = QtGui.QVBoxLayout(self.blur)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.stackedWidget.addWidget(self.blur)
        self.statistics = StatsWidget()
        self.statistics.setObjectName(_fromUtf8("statistics"))
        self.stackedWidget.addWidget(self.statistics)
        self.help = QtGui.QWidget()
        self.help.setObjectName(_fromUtf8("help"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.help)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.webview = QtWebKit.QWebView(self.help)
        self.webview.setObjectName(_fromUtf8("webview"))
        self.verticalLayout_2.addWidget(self.webview)
        self.stackedWidget.addWidget(self.help)
        self.about = QtGui.QWidget()
        self.about.setObjectName(_fromUtf8("about"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.about)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.groupBox = QtGui.QGroupBox(self.about)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout_7.addWidget(self.label_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Blurring/resources/umr.jpeg")))
        self.label_6.setScaledContents(False)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.verticalLayout_6.addWidget(self.label_9)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.verticalLayout_6.addWidget(self.label_8)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_7.addLayout(self.horizontalLayout)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.about)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_8.addWidget(self.label)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_8.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_8.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_8.addWidget(self.label_4)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_4 = QtGui.QGroupBox(self.about)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_19 = QtGui.QLabel(self.groupBox_4)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_4.addWidget(self.label_19, 0, 0, 1, 1)
        self.label_20 = QtGui.QLabel(self.groupBox_4)
        self.label_20.setOpenExternalLinks(True)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_4.addWidget(self.label_20, 0, 1, 1, 1)
        self.verticalLayout_9.addLayout(self.gridLayout_4)
        self.verticalLayout_4.addWidget(self.groupBox_4)
        self.groupBox_3 = QtGui.QGroupBox(self.about)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_10 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_15 = QtGui.QLabel(self.groupBox_3)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_4.addWidget(self.label_15)
        self.label_16 = QtGui.QLabel(self.groupBox_3)
        self.label_16.setAlignment(QtCore.Qt.AlignCenter)
        self.label_16.setOpenExternalLinks(True)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_4.addWidget(self.label_16)
        self.verticalLayout_10.addLayout(self.horizontalLayout_4)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        self.stackedWidget.addWidget(self.about)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.retranslateUi(BlurringDialogBase)
        self.listWidget.setCurrentRow(-1)
        self.stackedWidget.setCurrentIndex(3)
        QtCore.QObject.connect(self.listWidget, QtCore.SIGNAL(_fromUtf8("currentRowChanged(int)")), self.stackedWidget.setCurrentIndex)
        QtCore.QMetaObject.connectSlotsByName(BlurringDialogBase)

    def retranslateUi(self, BlurringDialogBase):
        BlurringDialogBase.setWindowTitle(_translate("BlurringDialogBase", "Blurring", None))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("BlurringDialogBase", "Blur", None))
        item = self.listWidget.item(1)
        item.setText(_translate("BlurringDialogBase", "Statistics", None))
        item = self.listWidget.item(2)
        item.setText(_translate("BlurringDialogBase", "Help", None))
        item = self.listWidget.item(3)
        item.setText(_translate("BlurringDialogBase", "About", None))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("BlurringDialogBase", "Supervision", None))
        self.label_5.setText(_translate("BlurringDialogBase", "This project was supervised by UMR Espace-Dev (IRD, UAG, UM2, UR)", None))
        self.label_9.setText(_translate("BlurringDialogBase", "Thérèse Libourel", None))
        self.label_8.setText(_translate("BlurringDialogBase", "Vincent Herbreteau", None))
        self.label_7.setText(_translate("BlurringDialogBase", "Christophe Révillion", None))
        self.groupBox_2.setTitle(_translate("BlurringDialogBase", "Realization", None))
        self.label.setText(_translate("BlurringDialogBase", "Mamadou Sane", None))
        self.label_2.setText(_translate("BlurringDialogBase", "Modou Ndiaye", None))
        self.label_3.setText(_translate("BlurringDialogBase", "Thomas Gauer", None))
        self.label_4.setText(_translate("BlurringDialogBase", "Etienne Trimaille", None))
        self.groupBox_4.setTitle(_translate("BlurringDialogBase", "Sources", None))
        self.label_19.setText(_translate("BlurringDialogBase", "Github\'s repository", None))
        self.label_20.setText(_translate("BlurringDialogBase", "<a href=\"https://github.com/Gustry/Blurring\" style=\"text-decoration:none;\">https://github.com/Gustry/Blurring</a>", None))
        self.groupBox_3.setTitle(_translate("BlurringDialogBase", "Licence", None))
        self.label_15.setText(_translate("BlurringDialogBase", "<html><head/><body><p><a href=\"http://www.gnu.org/licenses/gpl-2.0.html\"><span style=\" text-decoration: none; color:#0057ae;\">Licence GPL Version 2</span></a></p></body></html>", None))
        self.label_16.setText(_translate("BlurringDialogBase", "<html><head/><body><p><a href=\"https://www.gnu.org/licenses/gpl-2.0.html\"><img src=\":/plugins/Blurring/resources/gnu.png\"/></a></p></body></html>", None))

from PyQt4 import QtWebKit
from stats_dialog import StatsWidget
from qgis.gui import QgsMessageBar
from blur_dialog import BlurWidget
from Blurring import resources_rc
