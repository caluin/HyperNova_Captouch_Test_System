import ConsoleGUI
from PyQt5 import QtWidgets, QtCore


class ConsoleLogic(ConsoleGUI.Ui_Console):
    def __init__(self, ConsoleQDialog, parent=None):
        ConsoleGUI.Ui_Console.__init__(self)
        # set up GUI
        self.setupUi(ConsoleQDialog)

    def setup_functions(self):
        # connect functions
        self.process = QtCore.QProcess()
        self.process.readyReadStandardOutput.connect(self.stdout_ready)
        self.process.readyReadStandardError.connect(self.stderr_ready)
        # kick off the CapTouchTestSystemGUI
        self.process.start('python', ['CapTouchTestSystem.py'])

    def append(self, text):
         self.ConsoleOutput.append(text)
         #cursor = self.textBrowser.textCursor()
         #cursor.movePosition(cursor.End)
         #cursor.insertText(text)
        # self.output.ensureCursorVisible()

    def stdout_ready(self):
        text = str(self.process.readAllStandardOutput())
        print(text.strip())
        self.append(text)

    def stderr_ready(self):
        text = str(self.process.readAllStandardError())
        print(text.strip())
        self.append(text)


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    # create the console and initialized it
    ConsoleQDialog = QtWidgets.QDialog()
    ConsoleLogicInstance = ConsoleLogic(ConsoleQDialog, ConsoleGUI.Ui_Console)
    ConsoleLogicInstance.setup_functions()
    ConsoleQDialog.show()

    sys.exit(app.exec_())
