# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_blurring.ui'
#
# Created: Wed Mar 12 16:05:38 2014
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
        Blurring.resize(310, 194)
        self.verticalLayoutWidget = QtGui.QWidget(Blurring)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 301, 179))
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
        self.comboBox_blurredLayer.setObjectName(_fromUtf8("comboBox_blurredLayer"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBox_blurredLayer)
        self.label_2 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.spinBox_radius = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.spinBox_radius.setMinimum(50)
        self.spinBox_radius.setMaximum(999999999)
        self.spinBox_radius.setSingleStep(50)
        self.spinBox_radius.setProperty("value", 1000)
        self.spinBox_radius.setObjectName(_fromUtf8("spinBox_radius"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBox_radius)
        self.verticalLayout.addLayout(self.formLayout)
        self.pushButton_calculation = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButton_calculation.setObjectName(_fromUtf8("pushButton_calculation"))
        self.verticalLayout.addWidget(self.pushButton_calculation)
        self.progressBar_progression = QtGui.QProgressBar(self.verticalLayoutWidget)
        self.progressBar_progression.setProperty("value", 0)
        self.progressBar_progression.setObjectName(_fromUtf8("progressBar_progression"))
        self.verticalLayout.addWidget(self.progressBar_progression)
        self.label_3 = QtGui.QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.checkBox_premierBuffer = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_premierBuffer.setObjectName(_fromUtf8("checkBox_premierBuffer"))
        self.verticalLayout.addWidget(self.checkBox_premierBuffer)
        self.checkBox_pointAlea = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.checkBox_pointAlea.setObjectName(_fromUtf8("checkBox_pointAlea"))
        self.verticalLayout.addWidget(self.checkBox_pointAlea)

        self.retranslateUi(Blurring)
        QtCore.QMetaObject.connectSlotsByName(Blurring)

    def retranslateUi(self, Blurring):
        Blurring.setWindowTitle(_translate("Blurring", "Blurring", None))
        self.label.setText(_translate("Blurring", "Couche à flouter", None))
        self.label_2.setText(_translate("Blurring", "Rayon (m)", None))
        self.pushButton_calculation.setText(_translate("Blurring", "Calculer", None))
        self.label_3.setText(_translate("Blurring", "Ci-dessous, temporaire, uniquement pour le debug :", None))
        self.checkBox_premierBuffer.setText(_translate("Blurring", "Afficher le premier buffer", None))
        self.checkBox_pointAlea.setText(_translate("Blurring", "Afficher les points aléatoires", None))

