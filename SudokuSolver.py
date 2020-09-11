# Follow us on twitter @PY4ALL
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic, QtGui, QtCore
from time import sleep
from threading import Thread
from pathlib import Path

sys.setrecursionlimit(5000)

uifile = 'SudokuSolverUI.ui'
form, base = uic.loadUiType(uifile)


class MainPage(base, form):
    def __init__(self):
        super(base, self).__init__()
        self.setupUi(self)

        self.setWindowTitle("Sudoku Solver")

        self.pushButton_load.clicked.connect(self.thread_fill)
        self.pushButton_clear.clicked.connect(self.thread_clear)
        self.pushButton_solve.clicked.connect(self.thread_solve)

        self.setFocus()


    def fill(self,A):
        Palette= QtGui.QPalette()
        for i in range(9):
            for j in range(9):
                if A[i][j] != '0':
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setText(A[i][j])
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))
                    Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setPalette(Palette)
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setReadOnly(True)
                else:
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setText('')
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setFont(QtGui.QFont("Times",weight=QtGui.QFont.Normal))
                    Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.blue)
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setPalette(Palette)
                    getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setReadOnly(False)
                sleep(0.01)
                
    def clear(self):
        Palette= QtGui.QPalette()
        for i in range(9):
            for j in range(9):
                getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setText('')
                getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setFont(QtGui.QFont("Times",weight=QtGui.QFont.Normal))
                Palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
                getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setPalette(Palette)
                getattr(self, "lineEdit_"+str(i)+"_"+str(j)).setReadOnly(False)
                sleep(0.01)
        
    def solve(self):
        for r in range(9):
            for c in range(9):
                if getattr(self, "lineEdit_"+str(r)+"_"+str(c)).text() == '':
                    for d in range(1,10):
                        if self.is_valid(r, c, d):
                            getattr(self, "lineEdit_"+str(r)+"_"+str(c)).setText(str(d))
                            sleep(0.03)
                            if self.solve():
                                return True
                            getattr(self, "lineEdit_"+str(r)+"_"+str(c)).setText('')
                    return False
        return True

    def is_valid(self, r, c, d):
        for row in range(9):
            if getattr(self, "lineEdit_"+str(row)+"_"+str(c)).text() == str(d):
                return False
        for col in range(9):
            if getattr(self, "lineEdit_"+str(r)+"_"+str(col)).text() == str(d):
                return False
        for row in range((r//3)*3, (r//3+1)*3):
            for col in range((c//3)*3, (c//3+1)*3):
                if getattr(self, "lineEdit_"+str(row)+"_"+str(col)).text() == str(d):
                    return False
        return True
    
    def thread_fill(self):
        self.setFocus()
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Text Files (*.txt)", options=options)
        A = []
        SudokuFile = False
        if fileName:
            SudokuFile = True
            with open(fileName, 'r') as reader:
                lines = reader.readlines()
            if len(lines)==9:
                for line in lines:
                    if len(line.rstrip()) == 9:
                        tmp = []
                        for digit in line.rstrip():
                            tmp.append(digit)
                        A.append(tmp)
                    else:
                        SudokuFile = False
                        return
            else:
                SudokuFile = False

        if SudokuFile:
            thread = Thread(target=self.fill, args=(A,))
            thread.start()
        else:
            print('Sudoku file must be of size 9x9')

    def thread_clear(self):
        self.setFocus()
        thread = Thread(target=self.clear)
        thread.start()

    def thread_solve(self):
        self.setFocus()
        thread = Thread(target=self.solve)
        thread.start()  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainPage()
    ex.show()
    sys.exit(app.exec_())
