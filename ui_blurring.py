# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_blurring.ui'
#
# Created: Tue Mar 11 18:33:49 2014
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
        Blurring.resize(227, 151)
        self.formLayoutWidget = QtGui.QWidget(Blurring)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 201, 61))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.comboBox_blurredLayer = QtGui.QComboBox(self.formLayoutWidget)
        self.comboBox_blurredLayer.setObjectName(_fromUtf8("comboBox_blurredLayer"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_blurredLayer)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinBox_radius = QtGui.QSpinBox(self.formLayoutWidget)
        self.spinBox_radius.setMinimum(50)
        self.spinBox_radius.setMaximum(999999999)
        self.spinBox_radius.setSingleStep(50)
        self.spinBox_radius.setProperty("value", 1000)
        self.spinBox_radius.setObjectName(_fromUtf8("spinBox_radius"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox_radius)
        self.pushButton_calculation = QtGui.QPushButton(Blurring)
        self.pushButton_calculation.setGeometry(QtCore.QRect(60, 90, 93, 24))
        self.pushButton_calculation.setObjectName(_fromUtf8("pushButton_calculation"))
        self.progressBar_progression = QtGui.QProgressBar(Blurring)
        self.progressBar_progression.setGeometry(QtCore.QRect(10, 120, 201, 23))
        self.progressBar_progression.setProperty("value", 0)
        self.progressBar_progression.setObjectName(_fromUtf8("progressBar_progression"))

        self.retranslateUi(Blurring)
        QtCore.QMetaObject.connectSlotsByName(Blurring)

    def retranslateUi(self, Blurring):
        Blurring.setWindowTitle(_translate("Blurring", "Blurring", None))
        self.label.setText(_translate("Blurring", "Couche à flouter", None))
        self.label_2.setText(_translate("Blurring", "Rayon (m)", None))
        self.pushButton_calculation.setText(_translate("Blurring", "Calculer", None))

