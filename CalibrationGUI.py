# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CalibrationGUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Calibration(object):
    def setupUi(self, Calibration):
        Calibration.setObjectName("Calibration")
        Calibration.resize(800, 650)
        Calibration.setMaximumSize(QtCore.QSize(800, 700))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/CalibrationImages/resource/icon.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Calibration.setWindowIcon(icon)
        Calibration.setModal(True)
        self.Cancel = QtWidgets.QPushButton(Calibration)
        self.Cancel.setGeometry(QtCore.QRect(400, 560, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.Cancel.setFont(font)
        self.Cancel.setObjectName("Cancel")
        self.NextButton = QtWidgets.QPushButton(Calibration)
        self.NextButton.setGeometry(QtCore.QRect(570, 560, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.NextButton.setFont(font)
        self.NextButton.setObjectName("NextButton")
        self.groupBox = QtWidgets.QGroupBox(Calibration)
        self.groupBox.setGeometry(QtCore.QRect(50, 40, 701, 501))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.Photo = QtWidgets.QLabel(self.groupBox)
        self.Photo.setEnabled(True)
        self.Photo.setGeometry(QtCore.QRect(70, 50, 551, 281))
        self.Photo.setFrameShape(QtWidgets.QFrame.Box)
        self.Photo.setText("")
        self.Photo.setPixmap(QtGui.QPixmap(":/CalibrationImages/resource/photo1.jpg"))
        self.Photo.setScaledContents(False)
        self.Photo.setObjectName("Photo")
        self.Instruction_1 = QtWidgets.QTextBrowser(self.groupBox)
        self.Instruction_1.setEnabled(True)
        self.Instruction_1.setGeometry(QtCore.QRect(10, 340, 671, 141))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.Instruction_1.setFont(font)
        self.Instruction_1.setAcceptDrops(True)
        self.Instruction_1.setAutoFillBackground(False)
        self.Instruction_1.setFrameShape(QtWidgets.QFrame.VLine)
        self.Instruction_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Instruction_1.setLineWidth(1)
        self.Instruction_1.setObjectName("Instruction_1")
        self.Instruction_2 = QtWidgets.QTextBrowser(self.groupBox)
        self.Instruction_2.setEnabled(True)
        self.Instruction_2.setGeometry(QtCore.QRect(10, 340, 671, 141))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.Instruction_2.setFont(font)
        self.Instruction_2.setAcceptDrops(True)
        self.Instruction_2.setAutoFillBackground(False)
        self.Instruction_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.Instruction_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Instruction_2.setLineWidth(1)
        self.Instruction_2.setObjectName("Instruction_2")
        self.Instruction_3 = QtWidgets.QTextBrowser(self.groupBox)
        self.Instruction_3.setEnabled(True)
        self.Instruction_3.setGeometry(QtCore.QRect(240, 240, 241, 51))
        font = QtGui.QFont()
        font.setPointSize(15)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(False)
        self.Instruction_3.setFont(font)
        self.Instruction_3.setAcceptDrops(True)
        self.Instruction_3.setAutoFillBackground(False)
        self.Instruction_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.Instruction_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Instruction_3.setLineWidth(1)
        self.Instruction_3.setObjectName("Instruction_3")
        self.Instruction_3.raise_()
        self.Instruction_2.raise_()
        self.Photo.raise_()
        self.Instruction_1.raise_()
        self.groupBox.raise_()
        self.Cancel.raise_()
        self.NextButton.raise_()

        self.retranslateUi(Calibration)
        QtCore.QMetaObject.connectSlotsByName(Calibration)

    def retranslateUi(self, Calibration):
        _translate = QtCore.QCoreApplication.translate
        Calibration.setWindowTitle(_translate("Calibration", "Stella CapTouch Test System - Calibration Menu"))
        self.Cancel.setText(_translate("Calibration", "Cancel"))
        self.NextButton.setText(_translate("Calibration", "Next"))
        self.groupBox.setTitle(_translate("Calibration", "Calibration Instructions"))
        self.Instruction_1.setHtml(_translate("Calibration", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#000000;\">Step1: Mount the glass evenly to the test platform. The glass temple should be 90 degree angles with test probe. Move the probe to the hinge side of the glass. The probe should point to the glass vertically.(showing as the red dot in the photo)</span></p></body></html>"))
        self.Instruction_2.setHtml(_translate("Calibration", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#000000;\">Step2: Move the probe to the earpiece side of the glass. The probe should point to the glass vertically as well.(showing as the red dot in the photo)</span></p></body></html>"))
        self.Instruction_3.setHtml(_translate("Calibration", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:15pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; color:#000000;\">Calibration Complete.</span></p></body></html>"))
import CapTouch_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Calibration = QtWidgets.QDialog()
    ui = Ui_Calibration()
    ui.setupUi(Calibration)
    Calibration.show()
    sys.exit(app.exec_())
