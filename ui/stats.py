# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stats.ui'
#
# Created: Mon Aug 11 18:07:56 2014
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(818, 728)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.pushButton_refreshLayers = QtGui.QPushButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/Blurring/resources/refresh.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_refreshLayers.setIcon(icon)
        self.pushButton_refreshLayers.setObjectName(_fromUtf8("pushButton_refreshLayers"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.pushButton_refreshLayers)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.comboBox_blurredLayer = QtGui.QComboBox(Form)
        self.comboBox_blurredLayer.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox_blurredLayer.setObjectName(_fromUtf8("comboBox_blurredLayer"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBox_blurredLayer)
        self.comboBox_statsLayer = QtGui.QComboBox(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_statsLayer.sizePolicy().hasHeightForWidth())
        self.comboBox_statsLayer.setSizePolicy(sizePolicy)
        self.comboBox_statsLayer.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContentsOnFirstShow)
        self.comboBox_statsLayer.setObjectName(_fromUtf8("comboBox_statsLayer"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.comboBox_statsLayer)
        self.verticalLayout.addLayout(self.formLayout)
        self.label_progressStats = QtGui.QLabel(Form)
        self.label_progressStats.setObjectName(_fromUtf8("label_progressStats"))
        self.verticalLayout.addWidget(self.label_progressStats)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.progressBar_stats = QtGui.QProgressBar(Form)
        self.progressBar_stats.setProperty("value", 0)
        self.progressBar_stats.setObjectName(_fromUtf8("progressBar_stats"))
        self.horizontalLayout_2.addWidget(self.progressBar_stats)
        self.buttonBox_stats = QtGui.QDialogButtonBox(Form)
        self.buttonBox_stats.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_stats.setCenterButtons(False)
        self.buttonBox_stats.setObjectName(_fromUtf8("buttonBox_stats"))
        self.horizontalLayout_2.addWidget(self.buttonBox_stats)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButton_saveTable = QtGui.QPushButton(Form)
        self.pushButton_saveTable.setObjectName(_fromUtf8("pushButton_saveTable"))
        self.horizontalLayout_3.addWidget(self.pushButton_saveTable)
        self.pushButton_saveYValues = QtGui.QPushButton(Form)
        self.pushButton_saveYValues.setObjectName(_fromUtf8("pushButton_saveYValues"))
        self.horizontalLayout_3.addWidget(self.pushButton_saveYValues)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tableWidget = QtGui.QTableWidget(Form)
        self.tableWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.tableWidget)
        self.layout_plot = QtGui.QVBoxLayout()
        self.layout_plot.setObjectName(_fromUtf8("layout_plot"))
        self.horizontalLayout.addLayout(self.layout_plot)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.pushButton_refreshLayers.setText(_translate("Form", "Refresh layers", None))
        self.label.setText(_translate("Form", "Blurred layer", None))
        self.label_2.setText(_translate("Form", "Stats layer", None))
        self.label_progressStats.setText(_translate("Form", "progress", None))
        self.pushButton_saveTable.setText(_translate("Form", "Save table", None))
        self.pushButton_saveYValues.setText(_translate("Form", "Save Y values", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Parameter", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Value", None))

from Blurring import resources_rc
