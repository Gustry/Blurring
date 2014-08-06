# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created: Wed Aug  6 14:24:14 2014
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
        BlurringDialogBase.resize(547, 536)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(BlurringDialogBase)
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
        self.label = QtGui.QLabel(self.help)
        self.label.setGeometry(QtCore.QRect(70, 20, 56, 15))
        self.label.setObjectName(_fromUtf8("label"))
        self.stackedWidget.addWidget(self.help)
        self.about = QtGui.QWidget()
        self.about.setObjectName(_fromUtf8("about"))
        self.label_2 = QtGui.QLabel(self.about)
        self.label_2.setGeometry(QtCore.QRect(100, 60, 56, 15))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.stackedWidget.addWidget(self.about)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)

        self.retranslateUi(BlurringDialogBase)
        self.listWidget.setCurrentRow(-1)
        self.stackedWidget.setCurrentIndex(1)
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
        self.label.setText(_translate("BlurringDialogBase", "Help soon", None))
        self.label_2.setText(_translate("BlurringDialogBase", "About soon", None))

from stats_dialog import StatsWidget
from qgis.gui import QgsMessageBar
from blur_dialog import BlurWidget
from Blurring import resources_rc
