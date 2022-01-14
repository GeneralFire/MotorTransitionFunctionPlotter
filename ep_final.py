from PyQt5 import QtCore, QtGui, QtWidgets
#from ep_gui import Ui_dialog
import sys
import numpy as np
from scipy import signal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

from ctypes import windll # An included library with Python install.
def Mbox(title, text, style):
    return windll.user32.MessageBoxW(0, text, title, style)

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog(object):
    def setupUi(self, dialog):
        dialog.setObjectName("dialog")
        dialog.resize(450, 221)
        dialog.setWindowTitle("")
        self.formLayout = QtWidgets.QFormLayout(dialog)
        self.formLayout.setObjectName("formLayout")
        self.splitter_9 = QtWidgets.QSplitter(dialog)
        self.splitter_9.setOrientation(QtCore.Qt.Vertical)
        self.splitter_9.setObjectName("splitter_9")
        self.splitter_7 = QtWidgets.QSplitter(self.splitter_9)
        self.splitter_7.setOrientation(QtCore.Qt.Vertical)
        self.splitter_7.setObjectName("splitter_7")
        self.splitter = QtWidgets.QSplitter(self.splitter_7)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setObjectName("label")
        self.Amatrix = QtWidgets.QLineEdit(self.splitter)
        self.Amatrix.setObjectName("Amatrix")
        self.splitter_2 = QtWidgets.QSplitter(self.splitter_7)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.label_4 = QtWidgets.QLabel(self.splitter_2)
        self.label_4.setObjectName("label_4")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.splitter_2)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.splitter_8 = QtWidgets.QSplitter(self.splitter_9)
        self.splitter_8.setOrientation(QtCore.Qt.Vertical)
        self.splitter_8.setObjectName("splitter_8")
        self.splitter_3 = QtWidgets.QSplitter(self.splitter_8)
        self.splitter_3.setOrientation(QtCore.Qt.Vertical)
        self.splitter_3.setObjectName("splitter_3")
        self.label_2 = QtWidgets.QLabel(self.splitter_3)
        self.label_2.setObjectName("label_2")
        self.Bmatrix = QtWidgets.QLineEdit(self.splitter_3)
        self.Bmatrix.setObjectName("Bmatrix")
        self.splitter_5 = QtWidgets.QSplitter(self.splitter_8)
        self.splitter_5.setOrientation(QtCore.Qt.Vertical)
        self.splitter_5.setObjectName("splitter_5")
        self.label_3 = QtWidgets.QLabel(self.splitter_5)
        self.label_3.setObjectName("label_3")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.splitter_5)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.splitter_9)
        self.splitter_10 = QtWidgets.QSplitter(dialog)
        self.splitter_10.setOrientation(QtCore.Qt.Vertical)
        self.splitter_10.setObjectName("splitter_10")
        self.splitter_4 = QtWidgets.QSplitter(self.splitter_10)
        self.splitter_4.setOrientation(QtCore.Qt.Vertical)
        self.splitter_4.setObjectName("splitter_4")
        self.label_5 = QtWidgets.QLabel(self.splitter_4)
        self.label_5.setMaximumSize(QtCore.QSize(200, 20))
        self.label_5.setObjectName("label_5")
        self.LEVoltage = QtWidgets.QLineEdit(self.splitter_4)
        self.LEVoltage.setMaximumSize(QtCore.QSize(200, 20))
        self.LEVoltage.setObjectName("LEVoltage")
        self.splitter_6 = QtWidgets.QSplitter(self.splitter_10)
        self.splitter_6.setOrientation(QtCore.Qt.Vertical)
        self.splitter_6.setObjectName("splitter_6")
        self.label_6 = QtWidgets.QLabel(self.splitter_6)
        self.label_6.setMaximumSize(QtCore.QSize(200, 20))
        self.label_6.setObjectName("label_6")
        self.LETime = QtWidgets.QLineEdit(self.splitter_6)
        self.LETime.setMaximumSize(QtCore.QSize(200, 20))
        self.LETime.setObjectName("LETime")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.splitter_10)
        self.GetGraphButton = QtWidgets.QPushButton(dialog)
        self.GetGraphButton.setObjectName("GetGraphButton")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.GetGraphButton)

        self.retranslateUi(dialog)
        QtCore.QMetaObject.connectSlotsByName(dialog)

    def retranslateUi(self, dialog):
        _translate = QtCore.QCoreApplication.translate
        self.label.setText(_translate("dialog", "Матрица A в формате [a11, a12; a21, a22]"))
        self.label_4.setText(_translate("dialog", "Пример:"))
        self.lineEdit_2.setText(_translate("dialog", "1, 2; 3, 4"))
        self.label_2.setText(_translate("dialog", "Матрица B в формате [b1; b2]"))
        self.label_3.setText(_translate("dialog", "Пример:"))
        self.lineEdit_3.setText(_translate("dialog", "1; 2"))
        self.label_5.setText(_translate("dialog", "U, B"))
        self.label_6.setText(_translate("dialog", "Конечное время T, c"))
        self.GetGraphButton.setText(_translate("dialog", "График"))
        
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        
class GraphPlot(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(GraphPlot, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=8, height=6, dpi=100)
        self.setCentralWidget(self.canvas)
        
        ui.GetGraphButton.clicked.connect(self.RePlot)
    
    def RePlot(self):
        error = 0
        self.close()

        self.canvas.axes.cla()  # Clear the canvas.
        
        

        L = 0.202
        CdF = 1.68
        J = 0.487
        Tem = 0.158
        U = 115
        R = Tem*CdF**2/J

        ###
        try:
            #A = np.array([[-4.54*4, -8.32], [3.45*4, 0]])
            A = np.asarray(np.matrix(ui.Amatrix.text())*1.0);
            #B = np.array([[4.95], [0]])
            B = np.asarray(np.matrix(ui.Bmatrix.text())*1.0);
            GottenT = float(ui.LETime.text())
            U = float(ui.LEVoltage.text())
            print(GottenT)
        except (ValueError, SyntaxError):
            error = 1
            Mbox('Ошибка', 'Ошибка парсинга строки', 0)
        if error == 0:   
            C = np.array([[1, 0], [0, 1]])
            D = np.array([[0], [0]])
            ###
            try:
                sys = signal.StateSpace(A, B, C, D)
            except ValueError:
                error = 1
                Mbox('Ошибка', 'Ошибка парсинга строки', 0)
            if error == 0:
                T_array = np.arange(0, GottenT, 0.001)
                t, params = signal.step(sys, T = T_array)
                params = params * U
            ###

                self.canvas.axes.plot(t, params[:, 0], linewidth=2, linestyle='--', label = "i, А")
                self.canvas.axes.plot(t, params[:, 1], color='k', linewidth=2, linestyle='-', label = "$\omega$, рад/с")
                self.canvas.axes.set_xlabel('t, c');
                
                # Change major ticks to show every X.
                #self.sc.axes.xaxis.set_major_locator(MultipleLocator(0.1))
                #self.sc.axes.yaxis.set_major_locator(MultipleLocator(10))

                # Change minor ticks to show every X
                self.canvas.axes.xaxis.set_minor_locator(AutoMinorLocator(5))
                self.canvas.axes.yaxis.set_minor_locator(AutoMinorLocator(5))
                
                # Setting others
                self.canvas.axes.grid(which='major', axis='both', linestyle = '-', linewidth = 1)
                self.canvas.axes.grid(which='minor', axis='both', linestyle = ':', linewidth = 1)
                self.canvas.axes.grid(True, which='both')
                self.canvas.axes.legend();
                self.canvas.axes.set_xlim(0, GottenT)
                
                # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
                toolbar = NavigationToolbar(self.canvas, self)

                layout = QtWidgets.QVBoxLayout()
                layout.addWidget(toolbar)
                layout.addWidget(self.canvas)
                # Create a placeholder widget to hold our toolbar and canvas.
                widget = QtWidgets.QWidget()
                widget.setLayout(layout)
                self.setCentralWidget(widget)
                
                # Trigger the canvas to update and redraw.
                self.canvas.draw()
                self.show()
        
app = QtWidgets.QApplication(sys.argv)
dialog = QtWidgets.QDialog()
ui = Ui_dialog()
ui.setupUi(dialog)
dialog.show()
###
###
w = GraphPlot()
###
###
sys.exit(app.exec_())
    