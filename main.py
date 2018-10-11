    #!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, \
    QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def saveFileDialog(self, window_title):
        options = QFileDialog.Options()
        (fileName, _) = QFileDialog.getSaveFileName(self,
                window_title, '',
                'All Files (*);;Text Files (*.txt)', options=options)
        if fileName:
            print(fileName)
            return fileName

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        image_filename = self.openFileNameDialog('Choose Image Filename', '(*.jpg *.jpeg *.png)')
        if image_filename is None:
            self.show()
            return
        audio_filename = self.openFileNameDialog('Choose Audio Filename', '(*.mp3 *.wav)')
        if audio_filename is None:
            self.show()
            return
        save_file_destination = self.saveFileDialog('Name to save the file as')
        print(save_file_destination)
        if save_file_destination is None:
            self.show()
            return
        self.fffmpeg_run(image_filename, audio_filename, save_file_destination)
        self.show()

    def openFileNameDialog(self,window_title,file_type):
        options = QFileDialog.Options()

        (fileName, _) = QFileDialog.getOpenFileName(self,
                window_title, '',
                file_type, options=options)

        if fileName:
            return fileName

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        (files, _) = QFileDialog.getOpenFileNames(self,
                'QFileDialog.getOpenFileNames()', '',
                'All Files (*);;Python Files (*.py)', options=options)
        if files:
            print(files)

    def fffmpeg_run(self, image_filename, audio_filename, save_file_destination):
        completed = subprocess.run("./fffmpeg -loop 1 -i " + '"' + image_filename + '"' + " -i " + '"' + audio_filename + '"' + " -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest "+ '"' + save_file_destination + '"', shell=True)
        print('returncode:', completed.returncode)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
