# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_blurring.ui'
#
# Created: Thu Apr 17 14:08:22 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_Blurring(object):
    def setupUi(self, Blurring):
        Blurring.setObjectName(_fromUtf8("Blurring"))
        Blurring.resize(338, 239)
        Blurring.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.verticalLayoutWidget = QtGui.QWidget(Blurring)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 336, 221))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox_blurredLayer = QtGui.QComboBox(self.verticalLayoutWidget)
        self.comboBox_blurredLayer.setStatusTip(_fromUtf8(""))
        self.comboBox_blurredLayer.setWhatsThis(_fromUtf8(""))
        self.comboBox_blurredLayer.setAccessibleName(_fromUtf8(""))
        self.comboBox_blurredLayer.setAccessibleDescription(_fromUtf8(""))
        self.comboBox_blurredLayer.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_blurredLayer.setMinimumContentsLength(11)
        self.comboBox_blurredLayer.setObjectName(_fromUtf8("comboBox_blurredLayer"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_blurredLayer)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinBox_radius = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_radius.setMinimum(1)
        self.spinBox_radius.setMaximum(999999999)
        self.spinBox_radius.setSingleStep(50)
        self.spinBox_radius.setProperty("value", 1000)
        self.spinBox_radius.setObjectName(_fromUtf8("spinBox_radius"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox_radius)
        self.checkBox_selectedFeatures = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_selectedFeatures.setText(_fromUtf8(""))
        self.checkBox_selectedFeatures.setObjectName(_fromUtf8("checkBox_selectedFeatures"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.checkBox_selectedFeatures)
        self.label_4 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.checkBox_addToMap = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_addToMap.setText(_fromUtf8(""))
        self.checkBox_addToMap.setChecked(True)
        self.checkBox_addToMap.setObjectName(_fromUtf8("checkBox_addToMap"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.checkBox_addToMap)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lineEdit_outputFile = QtGui.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_outputFile.setObjectName(_fromUtf8("lineEdit_outputFile"))
        self.horizontalLayout.addWidget(self.lineEdit_outputFile)
        self.pushButton_browseFolder = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_browseFolder.setObjectName(_fromUtf8("pushButton_browseFolder"))
        self.horizontalLayout.addWidget(self.pushButton_browseFolder)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButton_help = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_help.setObjectName(_fromUtf8("pushButton_help"))
        self.horizontalLayout_2.addWidget(self.pushButton_help)
        spacerItem = QtGui.QSpacerItem(22, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButton_ok = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_ok.setObjectName(_fromUtf8("pushButton_ok"))
        self.horizontalLayout_2.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_cancel.setObjectName(_fromUtf8("pushButton_cancel"))
        self.horizontalLayout_2.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.progressBar_progression = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progressBar_progression.setProperty("value", 0)
        self.progressBar_progression.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_progression.setObjectName(_fromUtf8("progressBar_progression"))
        self.verticalLayout.addWidget(self.progressBar_progression)

        self.retranslateUi(Blurring)
        QtCore.QMetaObject.connectSlotsByName(Blurring)

    def retranslateUi(self, Blurring):
        Blurring.setWindowTitle(_translate("Blurring", "Blurring", None))
        self.label.setToolTip(_translate("Blurring", "<html><head/><body><p>Layer which will be blurred</p></body></html>", None))
        self.label.setText(_translate("Blurring", "Layer", None))
        self.comboBox_blurredLayer.setToolTip(_translate("Blurring", "Layer which will be blurred", None))
        self.label_2.setToolTip(_translate("Blurring", "Maximum radius", None))
        self.label_2.setText(_translate("Blurring", "Radius (m)", None))
        self.spinBox_radius.setToolTip(_translate("Blurring", "Maximum radius", None))
        self.label_4.setText(_translate("Blurring", "Use only selected features", None))
        self.label_3.setText(_translate("Blurring", "Add result to canvas", None))
        self.pushButton_browseFolder.setText(_translate("Blurring", "Browse", None))
        self.pushButton_help.setText(_translate("Blurring", "Help", None))
        self.pushButton_ok.setText(_translate("Blurring", "OK", None))
        self.pushButton_cancel.setText(_translate("Blurring", "Cancel", None))

