import sys
from datetime import datetime

from PyQt5.QtCore import QDate, Qt
from PyQt5 import QtCore
from pandas.core.common import flatten

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QFileDialog, QCalendarWidget, QFormLayout, QGroupBox, QGridLayout, QComboBox, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtWidgets import QMessageBox, QHeaderView
from PyQt5.QtWidgets import *
from matplotlib.ticker import MaxNLocator
import traceback
from pprint import pprint
from Preliminary_Report_Helper_Functions import cap_analysis

# class ApplicationWindow(QtWidgets.QMainWindow):
class interface_report(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.button_choose_file = QPushButton('Choose file')
        self.button_choose_file.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.button_choose_file)
        self.cb = QComboBox()
        self.cb.addItem('Slider instant')
        self.cb.addItem('Slider base')
        self.cb.addItem('CaptureBtn instant')
        self.cb.addItem('CaptureBtn base')
        self.cb.addItem('FaceProx instant')
        self.cb.addItem('FaceProx base')
        self.cb.addItem('useful')
        self.cb.addItem('diff')
        layout.addWidget(self.cb)
        self.setLayout(layout)
        self.setWindowTitle("interface report")

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        # fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*_xy1.csv);;Data Files (*.csv)", options=options)
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Data Files (*.csv)", options=options)
        if fileName:
            print(fileName)
        try:
            column_name = str(self.cb.currentText())
            if 'Full_Scan_Measurement' in fileName.split('/')[-1]:
                # if fileName.split('/')[-1].startswith('full_scale_hover'):
                my_analysis = cap_analysis(fileName,column_name,'full_scan_hover')
                my_analysis.plot_full_scale()
                my_analysis.plot_hover()
                # my_analysis.show_plot()
            elif 'Linearity_Jitter' in fileName.split('/')[-1]:
                my_analysis = cap_analysis(fileName,column_name,'linearity_jitter')
                my_analysis.plot_linearity()
                result=my_analysis.find_jitter()
                print('jitter')
                pprint(result)
                # my_analysis.show_plot()
            elif 'Noise_Measurement' in fileName.split('/')[-1]:
                my_analysis = cap_analysis(fileName,column_name,'noise')
                result=my_analysis.find_noise()
                print('noise')
                pprint(result)
            elif 'Arbitrary_X_Hover' in fileName.split('/')[-1]:
            # elif fileName.split('/')[-1].startswith('arbitrary_x_hover'):
                my_analysis = cap_analysis(fileName,column_name,'arbitrary_x_hover')
                print('arbitrary x hover')
                my_analysis.plot_arbitrary_x_hover()
                # my_analysis.show_plot()
            else:
                my_analysis = cap_analysis(fileName,column_name,'semtech_debug')
                my_analysis.plot_full_scale()
                my_analysis.plot_hover()
                my_analysis.show_plot()

                my_analysis.plot_linearity()
                result=my_analysis.find_noise()
                result=my_analysis.find_jitter()
            my_analysis.show_plot()
        except:
            print(traceback.print_exc())

if __name__ == "__main__":
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    # app = ApplicationWindow()
    app = interface_report()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()